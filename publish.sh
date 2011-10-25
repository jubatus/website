#!/bin/sh

omake html
cd build
rm -rf jubatusi.github.com/_static
rm -rf jubatus.github.com/_sources
cp -r html/* jubatus.github.com/
cd jubatus.github.com
git add *.html
git add _static/*
git add _sources/*
git commit -m "autocommit by publish.sh"
git push


