#!/bin/bash -ue

WEBROOT="jubatus.github.com"

# Make sure that we're on `master` branch
if [ "$(git rev-parse --abbrev-ref HEAD)" != "master" ]; then
  echo "You must be on the master branch to publish."
  exit 1
fi

omake clean html

if [ ! -d "${WEBROOT}" ]; then
	git clone git@github.com:jubatus/jubatus.github.com.git "${WEBROOT}"
fi

pushd "${WEBROOT}"

git checkout master
git pull

find . -mindepth 1 -and \
	! \( -path "./.*" -or -name CNAME \) \
	-delete

cp -a ../build/html/* .
git add -A
git commit -m "autocommit by publish.sh"
git push origin master

popd
