Jubatus Website
===============


About
-----

This repository holds Sphinx source files for http://jubat.us/ website.

Contributions are always welcomed, from tiny typos to enhancements.
Feel free to make pull-requests to this repository.


Requirements
------------

* Sphinx 1.1.3 + pngmath + blockdiag

Easy setup for Ubuntu 12.04 systems:

```
# apt-get install python-sphinx latex-cjk-japanese texlive-latex-extra dvipng
# pip install sphinxcontrib-blockdiag
```

How to Edit
-----------

First of all, clone this repository (if you don't have a commit access, use your fork).

```
$ git clone git@github.com:jubatus/website.git
```

Edit the document.

```
$ edit source/index.rst
```

Build and preview the changes you made.

```
$ omake html
$ open build/html/index.html
```

Looks good? Now, push it.

```
$ git push origin master
```

Then open a pull-request.

For Jubatus members: you can deploy it to http://jubat.us/ website.

```
$ ./publish.sh
```


Copyright
---------

(C) PFI & NTT
