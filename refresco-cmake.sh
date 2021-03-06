#!/bin/bash

CMAKE_FOLDER=cmake-trunk
SOURCE_DIR=$HOME/ReFRESCO/Dev/trunk
# CMAKE_FOLDER=cmake-overset
# SOURCE_DIR=$HOME/ReFRESCO/Dev/branch/overset

REFRESCO_INSTALL_DIR=$HOME/ReFRESCO/$CMAKE_FOLDER/install
REFRESCO_BUILD_DIR=$HOME/ReFRESCO/$CMAKE_FOLDER/build-refresco
EXTLIBS_BUILD_DIR=$HOME/ReFRESCO/$CMAKE_FOLDER/build-extlibs

mkdir -p $REFRESCO_INSTALL_DIR 
mkdir -p $REFRESCO_BUILD_DIR 
mkdir -p $EXTLIBS_BUILD_DIR 

# Build ext lib
cd $EXTLIBS_BUILD_DIR 
cmake $SOURCE_DIR/SuperBuild -Dsuperbuild_install_location=$REFRESCO_INSTALL_DIR/extLibs
make refrescolibs 


# Build ReFRESCO
cd $REFRESCO_BUILD_DIR
cmake $SOURCE_DIR -DCMAKE_INSTALL_PREFIX=$REFRESCO_INSTALL_DIR -DREFRESCO_EXTLIBS_DIR=$REFRESCO_INSTALL_DIR/extLibs
make -j 16 install_code install_tools


echo
echo "-----------------------------"
echo "To put in .bashrc:

export REFRESCO_INSTALL_DIR=$REFRESCO_INSTALL_DIR
export REFRESCO_EXTLIBS_DIR=$REFRESCO_INSTALL_DIR
export REFRESCO_CODE_DIR=$SOURCE_DIR/Code

source $REFRESCO_INSTALL_DIR/bin/refresco-run.sh
"


