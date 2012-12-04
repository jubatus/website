#!/bin/bash -ue

WEBROOT="jubatus.github.com"

omake clean html

if [ ! -d "${WEBROOT}" ]; then
	git clone git@github.com:jubatus/jubatus.github.com.git "${WEBROOT}"
fi

pushd "${WEBROOT}"

git checkout master

find . -mindepth 1 -and \
	! \( -path "./.*" -or -name CNAME \) \
	-delete

cp -a ../build/html/* .
git add -A
git commit -m "autocommit by publish.sh"
git push origin master

popd
