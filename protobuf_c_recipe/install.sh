#! /bin/bash

#
# Copyright (c) 2023 Krai Ltd.
#
# SPDX-License-Identifier: BSD-3-Clause.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

PROTOBUF_VERS=${PROTOBUF_VERS:-3.11.4}

function exit_if_error() {
  if [ "${?}" != "0" ]; then
    echo ""
    echo "ERROR: $1"
    exit 1
  fi
}

############################################################
echo ""
echo "Downloading Protobuf source to ${INSTALL_DIR}/src ..."

rm -rf ${INSTALL_DIR}/src
rm -rf ${INSTALL_DIR}/install

mkdir -p ${INSTALL_DIR}/src
git clone -b v${PROTOBUF_VERS} https://github.com/protocolbuffers/protobuf.git ${INSTALL_DIR}/src

cd ${INSTALL_DIR}/src
git submodule update --init --recursive

############################################################
echo ""
echo "Configuring CMake ..."

mkdir -p ${INSTALL_DIR}/obj
cd ${INSTALL_DIR}/obj

mkdir -p ${INSTALL_DIR}/install
_CONFIGURE_FLAGS="-DCMAKE_CXX_STANDARD=14 -Dprotobuf_BUILD_TESTS=OFF -DCMAKE_INSTALL_PREFIX=${INSTALL_DIR}/install -DCMAKE_C_COMPILER=/usr/bin/gcc -DCMAKE_CXX_COMPILER=/usr/bin/g++ -DCMAKE_AR=/usr/bin/ar "
if [[ ! -z "${FOR_QAIC}" ]]; then
  _CONFIGURE_FLAGS="${_CONFIGURE_FLAGS}:-DBUILD_SHARED_LIBS=ON"
else
  _CONFIGURE_FLAGS="${_CONFIGURE_FLAGS}:-DBUILD_SHARED_LIBS=OFF"
fi
_CMAKE_CMD="cmake ${_CONFIGURE_FLAGS} -B . -S ../src/cmake"
echo "${_CMAKE_CMD}"

${_CMAKE_CMD}

exit_if_error "Failed to configure CMake!"

############################################################
_NUM_OF_PROCESSOR="$(nproc)" # TODO: add option to override
echo ""
echo "Building package with make using ${_NUM_OF_PROCESSOR} threads ..."
make -j ${_NUM_OF_PROCESSOR}

exit_if_error "Failed to build package!"

############################################################
echo ""
echo "Installing package ..."

rm -rf install
make install

exit_if_error "Failed to install package!"

############################################################
echo ""
echo "Cleaning obj directory ..."

cd ${INSTALL_DIR}
rm -rf obj
