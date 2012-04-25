#!/bin/bash

PYYAML_URL='http://pyyaml.org/download/pyyaml/PyYAML-3.09.tar.gz'
NLTK_URL='http://nltk.googlecode.com/files/nltk-2.0.1rc1.tar.gz'
MAXENT_URL='https://github.com/lzhang10/maxent.git'

BUILD_DIR=build
PYYAML_DIR=$(basename $PYYAML_URL | perl -npe 's/\.tar\.gz//')
NLTK_DIR=$(basename $NLTK_URL | perl -npe 's/\.tar\.gz//')
MAXENT_DIR=$(basename $MAXENT_URL | perl -npe 's/\.git//')

[ -d $BUILD_DIR ] || mkdir $BUILD_DIR

# Install PyYaml
( 
cd $BUILD_DIR; 
wget $PYYAML_URL; 
tar xzf `basename $PYYAML_URL`;
cd $PYYAML_DIR; 
python setup.py install --user;
)

# Install NLTK
(
cd $BUILD_DIR; 
wget $NLTK_URL;
tar xzf `basename $NLTK_URL`;
cd $NLTK_DIR;
python setup.py install --user;
)

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
