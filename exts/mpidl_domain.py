# -*- coding: utf-8 -*-
"""
    mpidl_domain
    ~~~~~~~~~~~~

    The MPIDL language domain. This extension is based on C++ domain.

    :copyright: Copyright 2007-2011 by the Sphinx team, see AUTHORS.
    :copyright: Copyright 2013 Preferred Networks and Nippon Telegraph and Telephone Corporation.
    :license: BSD, see LICENSE for details.
"""

import re
from copy import deepcopy

from docutils import nodes

from sphinx import addnodes
from sphinx.roles import XRefRole
from sphinx.locale import l_, _
from sphinx.domains import Domain, ObjType
from sphinx.directives import ObjectDescription
from sphinx.util.nodes import make_refnode
from sphinx.util.compat import Directive
from sphinx.util.docfields import Field, GroupedField


_identifier_re = re.compile(r'(~?\b[a-zA-Z_][a-zA-Z0-9_]*)\b')
_whitespace_re = re.compile(r'\s+(?u)')
_string_re = re.compile(r"[LuU8]?('([^'\\]*(?:\\.[^'\\]*)*)'"
                        r'|"([^"\\]*(?:\\.[^"\\]*)*)")', re.S)
_template_arg_re = re.compile(r'(%s)|([^,>]+)' % _string_re.pattern, re.S)
_number_re = re.compile(r'[0-9]+')

_id_shortwords = {
    'char':         'c',
    'uchar':        'C',
    'int':          'i',
    'uint':         'U',
    'long':         'l',
    'ulong':        'L',
    'bool':         'b',
    'object':       'o',
    'string':       's',
    'list':         'l',
    'map':          'm',
}


class DefinitionError(Exception):

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.description


class DefExpr(object):

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        try:
            for key, value in self.__dict__.iteritems():
                if value != getattr(other, key):
                    return False
        except AttributeError:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    __hash__ = None

    def clone(self):
        """Clone a definition expression node."""
        return deepcopy(self)

    def get_id(self):
        """Return the id for the node."""
        return u''

    def get_name(self):
        """Return the name.

        Returns either `None` or a node with a name you might call
        :meth:`split_owner` on.
        """
        return None

    def split_owner(self):
        """Nodes returned by :meth:`get_name` can split off their
        owning parent.  This function returns the owner and the
        name as a tuple of two items.  If a node does not support
        it, it returns None as owner and self as name.
        """
        return None, self

    def prefix(self, prefix):
        """Prefix a name node (a node returned by :meth:`get_name`)."""
        raise NotImplementedError()

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        raise NotImplementedError()

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self)


class PrimaryDefExpr(DefExpr):

    def get_name(self):
        return self

    def prefix(self, prefix):
        if isinstance(prefix, PathDefExpr):
            prefix = prefix.clone()
            prefix.path.append(self)
            return prefix
        return PathDefExpr([prefix, self])


class NameDefExpr(PrimaryDefExpr):

    def __init__(self, name):
        self.name = name

    def get_id(self):
        name = _id_shortwords.get(self.name)
        if name is not None:
            return name
        return self.name.replace(u' ', u'-')

    def __unicode__(self):
        return unicode(self.name)


class PathDefExpr(PrimaryDefExpr):

    def __init__(self, parts):
        self.path = parts

    def get_id(self):
        rv = u'::'.join(x.get_id() for x in self.path)
        return _id_shortwords.get(rv, rv)

    def split_owner(self):
        if len(self.path) > 1:
            return PathDefExpr(self.path[:-1]), self.path[-1]
        return None, self

    def prefix(self, prefix):
        if isinstance(prefix, PathDefExpr):
            prefix = prefix.clone()
            prefix.path.extend(self.path)
            return prefix
        return PathDefExpr([prefix] + self.path)

    def __unicode__(self):
        return u'::'.join(map(unicode, self.path))


class TemplateDefExpr(PrimaryDefExpr):

    def __init__(self, typename, args):
        self.typename = typename
        self.args = args

    def split_owner(self):
        owner, typename = self.typename.split_owner()
        return owner, TemplateDefExpr(typename, self.args)

    def get_id(self):
        return u'%s:%s:' % (self.typename.get_id(),
                            u'.'.join(x.get_id() for x in self.args))

    def __unicode__(self):
        return u'%s<%s>' % (self.typename, u', '.join(map(unicode, self.args)))


class ArgumentDefExpr(DefExpr):

    def __init__(self, num, type, name, default=None):
        self.num = num
        self.name = name
        self.type = type
        self.default = default

    def get_name(self):
        return self.name.get_name()

    def get_id(self):
        buf = []
        buf.append(self.type and self.type.get_id() or 'X')
        return u''.join(buf)

    def __unicode__(self):
        buf = [(u'%s: %s %s' % (self.num, self.type or u'', self.name or u'')).strip()]
        if self.default is not None:
            buf.append('=%s' % self.default)
        return u''.join(buf)


class NamedDefExpr(DefExpr):

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name.get_name()


class TypeObjDefExpr(NamedDefExpr):

    def __init__(self, name):
        NamedDefExpr.__init__(self, name)

    def get_id(self):
        return self.name.get_id()

    def __unicode__(self):
        return unicode(self.name)


class MemberObjDefExpr(NamedDefExpr):

    def __init__(self, num, name, typename, value):
        NamedDefExpr.__init__(self, name)
        self.num = num
        self.typename = typename
        self.value = value

    def get_id(self):
        buf = [u'%s__%s' % (self.name.get_id(), self.typename.get_id())]
        return u''.join(buf)

    def __unicode__(self):
        buf = []
        buf.extend((unicode(self.typename), unicode(self.name)))
        buf = [u' '.join(buf)]
        if self.value is not None:
            buf.append(u' = %s' % self.value)
        return u''.join(buf)


class FuncDefExpr(NamedDefExpr):

    def __init__(self, name, rv, signature):
        NamedDefExpr.__init__(self, name)
        self.rv = rv
        self.signature = signature

    def get_id(self):
        return u'%s%s' % (
            self.name.get_id(),
            self.signature and u'__' +
                u'.'.join(x.get_id() for x in self.signature) or u''
        )

    def __unicode__(self):
        buf = []
        if self.rv is not None:
            buf.append(unicode(self.rv))
        buf.append(u'%s(%s)' % (self.name, u', '.join(
            map(unicode, self.signature))))
        return u' '.join(buf)


class ClassDefExpr(NamedDefExpr):

    def __init__(self, name, bases):
        NamedDefExpr.__init__(self, name)
        self.bases = bases

    def get_id(self):
        return self.name.get_id()

    def _tostring(self):
        buf.append(unicode(self.name))
        if self.bases:
            buf.append(u':')
            buf.append(u', '.join(base._tostring()
                                  for base in self.bases))
        return u' '.join(buf)

    def __unicode__(self):
        return self._tostring('public')

class DefinitionParser(object):

    def __init__(self, definition):
        self.definition = definition.strip()
        self.pos = 0
        self.end = len(self.definition)
        self.last_match = None
        self._previous_state = (0, None)

    def fail(self, msg):
        raise DefinitionError('Invalid definition: %s [error at %d]\n  %s' %
            (msg, self.pos, self.definition))

    def match(self, regex):
        match = regex.match(self.definition, self.pos)
        if match is not None:
            self._previous_state = (self.pos, self.last_match)
            self.pos = match.end()
            self.last_match = match
            return True
        return False

    def skip_string(self, string):
        strlen = len(string)
        if self.definition[self.pos:self.pos + strlen] == string:
            self.pos += strlen
            return True
        return False

    def check_string(self, string):
        strlen = len(string)
        return self.definition[self.pos:self.pos + strlen] == string

    def skip_word(self, word):
        return self.match(re.compile(r'\b%s\b' % re.escape(word)))

    def skip_ws(self):
        return self.match(_whitespace_re)

    def skip_word_and_ws(self, word):
        if self.skip_word(word):
            self.skip_ws()
            return True
        return False

    @property
    def eof(self):
        return self.pos >= self.end

    @property
    def current_char(self):
        try:
            return self.definition[self.pos]
        except IndexError:
            return 'EOF'

    @property
    def matched_text(self):
        if self.last_match is not None:
            return self.last_match.group()

    def _parse_name(self):
        return self._parse_name_or_template_arg()

    def _parse_name_or_template_arg(self):
        if not self.match(_identifier_re):
            self.fail('expected name')
        identifier = self.matched_text

        return NameDefExpr(identifier)

    def _parse_args(self, begin, end, type):
        args = []
        self.skip_ws()
        if not self.skip_string(begin):
            self.fail('missing open parenteses: "%s"' % begin)
        while 1:
            self.skip_ws()
            if self.eof:
                self.fail('missing closing parentheses: "%s"' % end)
            if self.skip_string(end):
                break
            if args:
                if not self.skip_string(','):
                    self.fail('"," or "%s" in template expected' % end)
                self.skip_ws()
            args.append(type(self))
        return args


    def _parse_type(self):
        typename = self._parse_name_or_template_arg()
        self.skip_ws()
        if not self.check_string('<'):
            return typename

        args = self._parse_args('<', '>', DefinitionParser._parse_type)
        return TemplateDefExpr(typename, args)

    def _parse_default_expr(self):
        self.skip_ws()
        if self.match(_string_re):
            return self.matched_text
        idx1 = self.definition.find(',', self.pos)
        idx2 = self.definition.find(')', self.pos)
        if idx1 < 0:
            idx = idx2
        elif idx2 < 0:
            idx = idx1
        else:
            idx = min(idx1, idx2)
        if idx < 0:
            self.fail('unexpected end in default expression')
        rv = self.definition[self.pos:idx]
        self.pos = idx
        return rv

    def _parse_arg(self):
        default = None
        num = self._parse_number()
        self.skip_ws()
        argtype = self._parse_type()
        self.skip_ws()
        argname = self._parse_name()
        self.skip_ws()
        if self.skip_string('='):
            default = self._parse_default_expr()

        return ArgumentDefExpr(num, argtype, argname, default)

    def _parse_signature(self):
        return self._parse_args('(', ')', DefinitionParser._parse_arg)

    def parse_type(self):
        return self._parse_type()

    def parse_type_object(self):
        name = self._parse_type()
        return TypeObjDefExpr(name)

    def _parse_number(self):
        self.skip_ws()
        if not self.match(_number_re):
            self.fail('number is expected')
        num = self.matched_text
        self.skip_ws()
        if not self.skip_string(':'):
            self.fail(': is expected')
        return num

    def parse_member_object(self):
        num = self._parse_number()
        self.skip_ws()
        typename = self._parse_type()
        self.skip_ws()
        name = self._parse_type()
        self.skip_ws()
        if self.skip_string('='):
            value = self.read_rest().strip()
        else:
            value = None
        return MemberObjDefExpr(num, name, typename, value)

    def parse_function(self):
        rv = self._parse_type()
        self.skip_ws()
        name = self._parse_name_or_template_arg()
        return FuncDefExpr(name, rv, self._parse_signature())

    def parse_class(self):
        name = self._parse_type()
        bases = []
        if self.skip_string(':'):
            self.skip_ws()
            while 1:
                base = self._parse_type()
                bases.append(ClassDefExpr(base, []))
                if self.skip_string(','):
                    self.skip_ws()
                else:
                    break
        return ClassDefExpr(name, bases)

    def read_rest(self):
        rv = self.definition[self.pos:]
        self.pos = self.end
        return rv

    def assert_end(self):
        self.skip_ws()
        if not self.eof:
            self.fail('expected end of definition, got %r' %
                      self.definition[self.pos:])


class MpidlObject(ObjectDescription):
    """Description of a MPIDL language object."""

    doc_field_types = [
        GroupedField('parameter', label=l_('Parameters'),
                     names=('param', 'parameter', 'arg', 'argument'),
                     can_collapse=False),
        GroupedField('exceptions', label=l_('Throws'), rolename='mpidl:message',
                     names=('throws', 'throw', 'exception'),
                     can_collapse=True),
        Field('returnvalue', label=l_('Returns'), has_arg=False,
              names=('returns', 'return')),
    ]

    def attach_name(self, node, name):
        owner, name = name.split_owner()
        varname = unicode(name)
        if owner is not None:
            owner = unicode(owner) + '::'
            node += addnodes.desc_addname(owner, owner)
        node += addnodes.desc_name(varname, varname)

    def attach_type(self, node, type):
        if isinstance(type, TemplateDefExpr):
            self.attach_type(node, type.typename)
            node += nodes.Text('<')
            first = True
            for arg in type.args:
                if not first:
                    node += nodes.Text(', ')
                first = False
                self.attach_type(node, arg)
            node += nodes.Text('>')
        else:
            text = unicode(type)
            pnode = addnodes.pending_xref(
                '', refdomain='mpidl', reftype='type',
                reftarget=text, modname=None, classname=None)
            pnode['mpidl:parent'] = self.env.temp_data.get('mpidl:parent')
            pnode += nodes.Text(text)
            node += pnode

    def add_target_and_index(self, sigobj, sig, signode):
        theid = sigobj.get_id()
        name = unicode(sigobj.name)
        if theid not in self.state.document.ids:
            signode['names'].append(theid)
            signode['ids'].append(theid)
            signode['first'] = (not self.names)
            self.state.document.note_explicit_target(signode)

            self.env.domaindata['mpidl']['objects'].setdefault(name,
                (self.env.docname, self.objtype, theid))

        indextext = self.get_index_text(name)
        if indextext:
            self.indexnode['entries'].append(('single', indextext, theid, '', None))

    def before_content(self):
        lastname = self.names and self.names[-1]
        if lastname and not self.env.temp_data.get('mpidl:parent'):
            assert isinstance(lastname, NamedDefExpr)
            self.env.temp_data['mpidl:parent'] = lastname.name
            self.parentname_set = True
        else:
            self.parentname_set = False

    def after_content(self):
        if self.parentname_set:
            self.env.temp_data['mpidl:parent'] = None

    def parse_definition(self, parser):
        raise NotImplementedError()

    def describe_signature(self, signode, arg):
        raise NotImplementedError()

    def handle_signature(self, sig, signode):
        parser = DefinitionParser(sig)
        try:
            rv = self.parse_definition(parser)
            parser.assert_end()
        except DefinitionError, e:
            self.state_machine.reporter.warning(e.description, line=self.lineno)
            raise ValueError
        self.describe_signature(signode, rv)

        parent = self.env.temp_data.get('mpidl:parent')
        if parent is not None:
            rv = rv.clone()
            rv.name = rv.name.prefix(parent)
        return rv


class MpidlMessageObject(MpidlObject):

    def get_index_text(self, name):
        return _('%s (MPIDL message)') % name

    def parse_definition(self, parser):
        return parser.parse_class()

    def describe_signature(self, signode, cls):
        signode += addnodes.desc_annotation('message ', 'message ')
        self.attach_name(signode, cls.name)
        if cls.bases:
            signode += nodes.Text(' : ')
            for base in cls.bases:
                signode += nodes.emphasis(unicode(base.name),
                                          unicode(base.name))
                signode += nodes.Text(', ')
            signode.pop()  # remove the trailing comma


class MpidlServiceObject(MpidlObject):

    def get_index_text(self, name):
        return _('%s (MPIDL service)') % name

    def parse_definition(self, parser):
        return parser.parse_class()

    def describe_signature(self, signode, cls):
        signode += addnodes.desc_annotation('service ', 'service ')
        self.attach_name(signode, cls.name)
        if cls.bases:
            signode += nodes.Text(' : ')
            for base in cls.bases:
                signode += nodes.emphasis(unicode(base.name),
                                          unicode(base.name))
                signode += nodes.Text(', ')
            signode.pop()  # remove the trailing comma


class MpidlTypeObject(MpidlObject):

    def get_index_text(self, name):
        if self.objtype == 'type':
            return _('%s (MPIDL type)') % name
        return ''

    def parse_definition(self, parser):
        return parser.parse_type_object()

    def describe_signature(self, signode, obj):
        signode += addnodes.desc_annotation('type ', 'type ')
        self.attach_name(signode, obj.name)


class MpidlMemberObject(MpidlObject):

    def get_index_text(self, name):
        if self.objtype == 'member':
            return _('%s (MPIDL member)') % name
        return ''

    def parse_definition(self, parser):
        return parser.parse_member_object()

    def describe_signature(self, signode, obj):
        signode += nodes.Text(obj.num + u': ')
        self.attach_type(signode, obj.typename)
        signode += nodes.Text(' ')
        self.attach_name(signode, obj.name)
        if obj.value is not None:
            signode += nodes.Text(u' = ' + obj.value)


class MpidlMethodObject(MpidlObject):

    def attach_function(self, node, func):
        owner, name = func.name.split_owner()
        if owner is not None:
            owner = unicode(owner) + '::'
            node += addnodes.desc_addname(owner, owner)

        funcname = unicode(name)
        node += addnodes.desc_name(funcname, funcname)

        paramlist = addnodes.desc_parameterlist()
        for arg in func.signature:
            param = addnodes.desc_parameter('', '', noemph=True)
            param += nodes.Text(arg.num)
            param += nodes.Text(u': ')
            self.attach_type(param, arg.type)
            param += nodes.Text(u' ')
            param += nodes.emphasis(unicode(arg.name), unicode(arg.name))
            if arg.default is not None:
                def_ = u'=' + unicode(arg.default)
                param += nodes.emphasis(def_, def_)
            paramlist += param

        node += paramlist

    def get_index_text(self, name):
        return _('%s (MPIDL method)') % name

    def parse_definition(self, parser):
        return parser.parse_function()

    def describe_signature(self, signode, func):
        # return value is None for things with a reverse return value
        # such as casting operator definitions or constructors
        # and destructors.
        if func.rv is not None:
            self.attach_type(signode, func.rv)
        signode += nodes.Text(u' ')
        self.attach_function(signode, func)


class MpidlXRefRole(XRefRole):

    def process_link(self, env, refnode, has_explicit_title, title, target):
        refnode['mpidl:parent'] = env.temp_data.get('mpidl:parent')
        if not has_explicit_title:
            target = target.lstrip('~') # only has a meaning for the title
            # if the first character is a tilde, don't display the module/class
            # parts of the contents
            if title[:1] == '~':
                title = title[1:]
                dcolon = title.rfind('::')
                if dcolon != -1:
                    title = title[dcolon + 2:]
        return title, target


class MpidlDomain(Domain):
    """Mpidl language domain."""
    name = 'mpidl'
    label = 'mpidl'
    object_types = {
        'message':  ObjType(l_('message'),  'type'),
        'service':  ObjType(l_('service'),  'serv'),
        'method':   ObjType(l_('method'),   'meth'),
        'member':   ObjType(l_('member'),   'memb'),
        'type':     ObjType(l_('type'),     'type')
    }

    directives = {
        'message':      MpidlMessageObject,
        'service':      MpidlServiceObject,
        'method':       MpidlMethodObject,
        'member':       MpidlMemberObject,
        'type':         MpidlTypeObject,
    }

    roles = {
        'serv':  MpidlXRefRole(),
        'meth':  MpidlXRefRole(fix_parens=True),
        'memb':  MpidlXRefRole(),
        'type':  MpidlXRefRole()
    }

    initial_data = {
        'objects': {},  # fullname -> docname, objtype
    }

    def clear_doc(self, docname):
        for fullname, (fn, _, _) in self.data['objects'].items():
            if fn == docname:
                del self.data['objects'][fullname]

    def resolve_xref(self, env, fromdocname, builder,
                     typ, target, node, contnode):
        def _create_refnode(expr):
            name = unicode(expr)
            if name not in self.data['objects']:
                return None
            obj = self.data['objects'][name]
            types = self.objtypes_for_role(typ)
            if types == None or obj[1] not in types:
                return None
            return make_refnode(builder, fromdocname, obj[0], obj[2],
                                contnode, name)

        parser = DefinitionParser(target)
        try:
            expr = parser.parse_type().get_name()
            parser.skip_ws()
            if not parser.eof or expr is None:
                raise DefinitionError('')
        except DefinitionError:
            env.warn_node('unparseable MPIDL definition: %r' % target, node)
            return None

        parent = node.get('mpidl:parent', None)

        rv = _create_refnode(expr)
        if rv is not None or parent is None:
            return rv
        parent = parent.get_name()

        rv = _create_refnode(expr.prefix(parent))
        if rv is not None:
            return rv

        parent, name = parent.split_owner()
        return _create_refnode(expr.prefix(parent))

    def get_objects(self):
        for refname, (docname, type, theid) in self.data['objects'].iteritems():
            yield (refname, refname, type, docname, refname, 1)


def setup(app):
    app.add_domain(MpidlDomain)
