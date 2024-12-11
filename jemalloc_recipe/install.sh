#!/bin/bash

cd $SRC_DIR && ./autogen.sh && make && cp lib/*.so.2 $INSTALL_DIR