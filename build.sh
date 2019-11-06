#!/bin/bash -uex

# Remove dist directory.
rm -rf build

# Build Sphinx.
for lang in "en" "ja"
do
    sphinx-build -b html -c source "source/${lang}" "build/${lang}"
done

# Copy index.html to build directory.
cp supplement/index.html build
