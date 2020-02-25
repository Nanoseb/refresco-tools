#!/bin/bash

# CMAKE_FOLDER=cmake-trunk-gnu
# SOURCE_DIR=$HOME/ReFRESCO/Dev/trunk
CMAKE_FOLDER=cmake-overset
SOURCE_DIR=$HOME/ReFRESCO/Dev/branches/overset

REFRESCO_INSTALL_DIR=$HOME/ReFRESCO/$CMAKE_FOLDER/install
REFRESCO_BUILD_DIR=$HOME/ReFRESCO/$CMAKE_FOLDER/build-refresco
EXTLIBS_BUILD_DIR=$HOME/ReFRESCO/$CMAKE_FOLDER/build-extlibs

mkdir -p $REFRESCO_INSTALL_DIR 
mkdir -p $REFRESCO_BUILD_DIR 
mkdir -p $EXTLIBS_BUILD_DIR 

# Build ext lib
cd $EXTLIBS_BUILD_DIR 
cmake $SOURCE_DIR/SuperBuild -Dsuperbuild_install_location=$REFRESCO_INSTALL_DIR/extLibs \
                             -DENABLE_suggar=ON \
                             -DENABLE_p3d=ON \
                             -DENABLE_dirtlib=ON \
                             -DENABLE_licensing=OFF \
                             -DENABLE_paraview=OFF \
                             -DENABLE_pfunit=ON \
                             -DENABLE_xri=OFF
make refrescolibs 

# Build ReFRESCO
cd $REFRESCO_BUILD_DIR
cmake $SOURCE_DIR -DCMAKE_INSTALL_PREFIX=$REFRESCO_INSTALL_DIR -DREFRESCO_EXTLIBS_DIR=$REFRESCO_INSTALL_DIR/extLibs \
                  -DENABLE_COPROCESSING=OFF \
                  -DENABLE_LICENSING=OFF \
                  -DENABLE_XMF=OFF \
                  -DENABLE_OVERSET=ON

# make -j 8 install_code install_tools


echo
echo "-----------------------------"
echo "To put in .bashrc:

export REFRESCO_INSTALL_DIR=$REFRESCO_INSTALL_DIR
export REFRESCO_EXTLIBS_DIR=$REFRESCO_INSTALL_DIR
export REFRESCO_CODE_DIR=$SOURCE_DIR/Code

source $REFRESCO_INSTALL_DIR/bin/refresco-run.sh
"


