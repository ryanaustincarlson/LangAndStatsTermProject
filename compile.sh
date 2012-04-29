#!/bin/bash

MAXENT_URL='git://github.com/lzhang10/maxent.git'
SRILM_TARBALL=`pwd -P`/resources/srilm.tgz

BUILD_DIR=build
MAXENT_DIR=$(basename $MAXENT_URL | perl -npe 's/\.git//')
SRILM_DIR=srilm

[ -d $BUILD_DIR ] || mkdir $BUILD_DIR

# Install maxent
(
cd $BUILD_DIR;
git clone $MAXENT_URL;
cd $MAXENT_DIR;
./configure;
make;
cd python;
python setup.py build;
python setup.py install --user;
)

