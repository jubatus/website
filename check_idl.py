#!/usr/bin/env python

import argparse
import json
import glob
import os
import re
import sys

ident = r'[a-z0-9_<>, ]+'
arg = r'[0-9]+: *%s +%s' % (ident, ident)

idl_message_pattern = re.compile(r'message ([a-z0-9_]+)(\(.*\))? {')
idl_member_pattern = re.compile(r' *([0-9]+: %s +%s)' % (ident, ident))
idl_method_pattern = re.compile(r'\s*(%s +%s\( *(%s( *, *%s)*)? *\))\s*(#.*)?'
                                % (ident, ident, arg, arg))

rst_message_pattern = re.compile(r'\.\. mpidl:message:: ([0-9a-z_]+)')
rst_member_pattern = re.compile(r'   \.\. mpidl:member:: ([0-9]+: %s %s)' % (ident, ident))
rst_service_pattern = re.compile(r'\.\. mpidl:service:: ([0-9a-z_]+)')
rst_method_pattern = re.compile(r'   \.\. mpidl:method:: (%s +%s\( *(%s( *, *%s)*)? *\))'
                                 % (ident, ident, arg, arg))

def find_idl_message(lines):
    messages = []
    message = None
    members = []
    for l in lines:
        if message:
            m = idl_member_pattern.match(l)
            if m:
                members.append(m.group(1))
            if '}' in l:
                messages.append({"name": message, "members": members})
                message = None
                members = []
        else:
            m = idl_message_pattern.match(l)
            if m:
                message = m.group(1)
    return messages

def find_idl_service(lines):
    methods = []
    internal = False
    for line in lines:
        m = idl_method_pattern.match(line)
        if m:
            if not internal:
                methods.append(m.group(1))
            internal = False
        internal = '@internal' in line

    # clear() API is not documented int rst now.
    if 'bool clear()' in methods:
        methods.remove('bool clear()')
        
    return methods

def read_idl(path):
    with open(path) as io:
        lines = [l for l in io]
    messages = find_idl_message(lines)
    services = find_idl_service(lines)
    services.sort()
    return {
        'messages': messages,
        'services': services,
        }

def find_rst_message(lines):
    messages = []
    message = None
    members = []
    for line in lines:
        if message:
            m = rst_member_pattern.match(line)
            if m:
                members.append(m.group(1))
            if line.strip() != '' and line[0] != ' ':
                messages.append({'name': message, 'members': members})
                message = None
                members = []

        m = rst_message_pattern.match(line)
        if m:
            message = m.group(1)
    return messages

def find_rst_service(lines):
    methods = []
    for line in lines:
        m = rst_method_pattern.match(line)
        if m:
            methods.append(m.group(1))
    return methods

def read_rst(path):
    with open(path) as io:
        lines = [l for l in io]
    messages = find_rst_message(lines)
    services = find_rst_service(lines)
    services.sort()
    return {
        'messages': messages,
        'services': services,
        }

def compare_idl_and_rst(idl_path, rst_path):
    idl = read_idl(idl_path)    
    rst = read_rst(rst_path)

    error = False
    if idl['messages'] != rst['messages']:
        print rst_path
        print 'idl:', idl['messages']
        print 'rst:', rst['messages']
        error = True

    if idl['services'] != rst['services']:
        print rst_path
        print 'idl:', idl['services']
        print 'rst:', rst['services']
        error = True

    return error

def run(langs, jubatus_root, document_root):
    error = False
    for lang in langs:
        # find in JUBATUS_root/jubatus/server/server/*.idl
        pattern = os.path.join(jubatus_root, 'jubatus', 'server', 'server', '*.idl')
        for idl_path in glob.glob(pattern):
            api = os.path.splitext(os.path.basename(idl_path))[0]
            rst_path = os.path.join(document_root, 'source', lang, 'api_%s.rst' % api)
            if not os.path.exists(rst_path):
                print ('RST is not found: %s' % rst_path)
            else:
                error |= compare_idl_and_rst(idl_path, rst_path)
    if error:
        sys.exit(-1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--jubatus', required=True,
                        help='path to Jubatus directory')
    parser.add_argument('-d', '--document', default='.',
                        help='path to document direcotry (default: ".")')
    parser.add_argument('-l', '--lang', action='append', default=['ja', 'en'],
                        help='language to check (default: "ja", "en")')

    args = parser.parse_args()
    run(args.lang, args.jubatus, args.document)
