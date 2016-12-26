#!/bin/bash -ue

# Failsafe
set -ue

WEBROOT="jubatus.github.com"
JUBAKIT="jubakit"

# Make sure that we're on `master` branch of website repository
if [ "$(git rev-parse --abbrev-ref HEAD)" != "master" ]; then
  echo "You must be on the master branch to publish."
  exit 1
fi

# Build Jubatus documents
omake clean html

# Build Jubakit documents
if [ ! -d "${JUBAKIT}" ]; then
    git clone git@github.com:jubatus/jubakit.git "${JUBAKIT}"
fi
pushd "${JUBAKIT}"
git checkout master
git pull
pushd "doc"
./build.sh
popd
popd

# Clone hosting repository
if [ ! -d "${WEBROOT}" ]; then
	git clone git@github.com:jubatus/jubatus.github.com.git "${WEBROOT}"
fi
pushd "${WEBROOT}"
git checkout master
git pull

# Remove existing files in hosting repository
find . -mindepth 1 -and \
	! \( -path "./.*" -or -name CNAME \) \
	-delete

# Copy Jubatus documents
cp -a ../build/html/* .

# Copy Jubakit documents
cp -a ../${JUBAKIT}/doc/_build/html/* en/jubakit
cp -a ../${JUBAKIT}/doc/_build/html/* ja/jubakit

# To test this script without actually publishing the docs, exit here.
# exit

# Commit and publish
git add -A
if git commit -m "autocommit by publish.sh"; then
  git push origin master
else
  echo "Nothing to commit: website is up-to-date."
fi
