#!/bin/sh
set -xe

#rm api/*
sphinx-apidoc --no-toc -o api/ ../wagtail_graphql ../wagtail_graphql/tests
