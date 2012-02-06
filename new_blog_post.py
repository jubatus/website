import sys
import datetime
import getpass
import os

class BlogPost:
    def __init__(self, title):
        self.date = datetime.datetime.now().strftime("%Y/%m-%d-%H-%M")
        self.date_text = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        self.title = sys.argv[1]
        self.username = getpass.getuser()
        self.filename = '%s-%s' % (self.date, self.title)

    def finished(self):
        message = """

created source/blog/%s.rst. all you have to do is
  
  $ <edit your blog post on source/blog/%s.rst>
  $ git add source/blog/%s.rst
  $ git add source/blog/index.rst
  $ git commit -m "your comment here"
  $ omake html
  $ cd build
  $ git clone git@github.com:jubatus/website.git
  $ sh publish.sh
  $ git push origin master
  
""" % (self.filename, self.filename, self.filename)
        print(message)

    def create_post_file(self):
        underbar = '-' * len(self.title)

        template = """
%s
%s

on %s

by %s
""" % (self.title, underbar, self.date_text, self.username)

        year = datetime.datetime.now().strftime("%Y")
        try:    os.mkdir('source/blog/%s' % year)
        except: pass
        f = open('source/blog/' + self.filename + '.rst', "w")
        f.write(template)
        f.close()

    def modify_index(self):
        index0 = 'source/blog/index.rst'
        index = 'source/blog/index.rst.bak'
        f = open(index0, "r")
        g = open(index, "w")

        for line in f.readlines():
            g.write(line)
            if line[0:10] == '================='[0:10]:
                newline = "- :doc:`%s` by %s on %s\n" % (self.filename, self.username, self.date_text)
                g.write(newline)
#            if line[0:8] == '.. toctree'[0:8]:
#                newline = "   %s\n" % self.filename
#                g.write(newline)

        f.close()
        g.close()
        os.rename(index, index0)


if __name__ == '__main__':
    post = BlogPost(sys.argv[1])
    post.create_post_file()
    post.modify_index()
    post.finished()

