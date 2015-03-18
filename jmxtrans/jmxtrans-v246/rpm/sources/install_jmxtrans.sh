#!/bin/sh
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -ex

usage() {
  echo "
usage: $0 <options>
  Required not-so-options:
     --build-dir=DIR             path to flumedist.dir
     --prefix=PREFIX             path to install into
     --source-dir=SRC_DIR 	 path to rpms sources

  Optional options:
     --doc-dir=DIR               path to install docs into [/usr/share/doc/flume]
     --lib-dir=DIR               path to install flume home [/usr/lib/flume]
     --bin-dir=DIR               path to install bins [/usr/bin]
     --examples-dir=DIR          path to install examples [doc-dir/examples]
     ... [ see source for more similar options ]
  "
  exit 1
}

OPTS=$(getopt \
  -n $0 \
  -o '' \
  -l 'prefix:' \
  -l 'source-dir:' \
  -l 'doc-dir:' \
  -l 'lib-dir:' \
  -l 'bin-dir:' \
  -l 'examples-dir:' \
  -l 'build-dir:' -- "$@")

if [ $? != 0 ] ; then
    usage
fi

eval set -- "$OPTS"

while true ; do
    case "$1" in
        --prefix)
        PREFIX=$2 ; shift 2
        ;;
        --source-dir)
        SRC_DIR=$2 ; shift 2
        ;;
        --build-dir)
        BUILD_DIR=$2 ; shift 2
        ;;
        --doc-dir)
        DOC_DIR=$2 ; shift 2
        ;;
        --lib-dir)
        LIB_DIR=$2 ; shift 2
        ;;
        --bin-dir)
        BIN_DIR=$2 ; shift 2
        ;;
        --examples-dir)
        EXAMPLES_DIR=$2 ; shift 2
        ;;
        --)
        shift ; break
        ;;
        *)
        echo "Unknown option: $1"
        usage
        exit 1
        ;;
    esac
done

for var in PREFIX BUILD_DIR SRC_DIR; do
  if [ -z "$(eval "echo \$$var")" ]; then
    echo Missing param: $var
    usage
  fi
done

echo "SSSSSSSSSSSSSSSSSSSSSSSSSS"
cd ${BUILD_DIR}
echo  $PWD

MAN_DIR=${MAN_DIR:-/usr/share/man/man1}
DOC_DIR=${DOC_DIR:-/usr/share/doc/jmxtrans}
LIB_DIR=${LIB_DIR:-/usr/lib/jmxtrans}
BIN_DIR=${BIN_DIR:-/usr/lib/jmxtrans}
CONF_DIST_DIR=/etc/jmxtrans/conf/
LOG_DIR=/var/log/jmxtrans
SYSTEM_DIR=/lib/systemd/system
INITR_DIR=/etc/init.d

echo "Directorio init.r"
echo $INITR_DIR

# Take out useless things or we've installed elsewhere


#!/bin/bash

# Detect JAVA_HOME if not defined

rm -rf   $PREFIX
mkdir -p $PREFIX$BIN_DIR
mkdir -p $PREFIX$LIB_DIR
mkdir -p $PREFIX$LIB_DIR/lib
#mkdir -p %{PREFIX}%{xlibdir}
mkdir -p $PREFIX$LOG_DIR
mkdir -p $PREFIX$INITR_DIR
mkdir -p $PREFIX%{_sysconfdir}/sysconfig
mkdir -p $PREFIX$SYSTEM_DIR
#mkdir -p $PREFIX$INITR_DIR/jmxtrans
mkdir  -p $PREFIX/etc/jmxtrans/config.dist
# remove source (unneeded here) 
install -p  *.* $PREFIX$BIN_DIR
install -p  lib/* $PREFIX$LIB_DIR/lib
install -p  target/jmxtrans-1.0.0-all.jar $PREFIX$BIN_DIR
install -p   $SRC_DIR/jmxtrans.init $PREFIX$INITR_DIR/jmxtrans
install -p   $SRC_DIR/KafkaMetrics.json $PREFIX/etc/jmxtrans/config.dist
# copy yaml2jmxtrans.py to bin
install -p tools/yaml2jmxtrans.py $PREFIX$BIN_DIR
chmod 755 $PREFIX$BIN_DIR/yaml2jmxtrans.py

# copy doc (if existing)
#cp -rf doc %{PREFIF}%{xappdir}

# Setup Systemd
install -p $SRC_DIR/systemd $PREFIX$SYSTEM_DIR/jmxtrans.service

# ensure shell scripts are executable

chmod 755 $PREFIX$BIN_DIR/*.sh

