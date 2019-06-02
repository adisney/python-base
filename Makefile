.PHONEY: test watch lint do-lint deploy push-archive extract upgrade git-tag git-porcelain err
SHELL=/bin/bash

VERSION_NUM?=$(shell cat .current-version)
VERSION?=${VERSION_NUM}

TARBALL=${VERSION}.tar.gz
REMOTE_DIR=/home/deploy_user/python-base

duplicates_cmd := find python_base/test -mindepth 1 -type f | sed "s/.*\///" | sort | uniq -d
duplicates := $(shell $(duplicates_cmd))
define line-break


endef
ifdef duplicates
    ERR = $(error Cannot have multiple test files with same name.$(line-break)$(duplicates))
endif

err: ; $(ERR)

test: err
	pipenv run python -B -m green -vvv

watch:
	find . -name '*.py' | entr -dc sh -c '\
	    find . -type f -name "*.py[co]" -delete;\
	    find . -type d -name "__pycache__" -delete;\
	    ctags -R > /dev/null 2>&1;\
	    if [ -z "$(duplicates)" ]; then\
		pipenv run python -B -m green -vvv;\
	    else\
		echo "Cannot have multiple test files with same name.\n"$(duplicates);\
	    fi'

lint:
	pipenv run flake8

do-lint:
	find . -name '*.py' | xargs -I {} autopep8 {} -i

git-porcelain:
	@[[ -z "`git status --porcelain`" ]]

git-tag: git-porcelain
	git tag ${VERSION}
	git push --tags

builds/${TARBALL}:
	mkdir -p builds
	tar zcvf $@ .current-version run config Pipfile Pipfile.lock

deploy: test git-tag builds/${TARBALL} push-archive extract

push-archive:
	scp builds/${TARBALL} ${HOST}:${REMOTE_DIR}/builds/${TARBALL}

extract:
	ssh -t ${HOST} "\
	    cd ${REMOTE_DIR}; \
	    mkdir -p app/${VERSION}; \
	    tar xzf builds/${TARBALL} --directory app/${VERSION}; \
	    sudo chgrp -R production app/${VERSION}/; \
	    cd app/${VERSION};"

upgrade:
	ssh -t ${HOST} "\
	    cd ${REMOTE_DIR}/app; \
	    rm current; \
	    ln -s ${VERSION} current; \
	    cd current; \
	    /usr/local/bin/pipenv sync;"
