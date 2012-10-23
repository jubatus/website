#!/bin/sh

omake html
cd build
rm -rf jubatus.github.com/_static
rm -rf jubatus.github.com/_sources
LANG=C diff html jubatus.github.com | egrep '^Only in jubatus.github.com' | awk '{print $4}' | grep '^[^\.A-Z].*$' | xargs -i rm -rf jubatus.github.com/{}
cp -r html/* jubatus.github.com
cd jubatus.github.com
git status | grep deleted: | awk '{print $3}' | xargs git rm -r
git add *.html
git add en/*.html
git add ja/*.html
git add _static/*
git add _sources/*
git add _images/*
git commit -m "autocommit by publish.sh"
git push

