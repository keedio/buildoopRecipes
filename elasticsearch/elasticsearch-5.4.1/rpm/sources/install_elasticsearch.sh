#!/bin/bash

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

set -e

usage() {
  echo "
usage: $0 <options>
  Required not-so-options:
     --build-dir=DIR             path to Whirr dist.dir
     --prefix=PREFIX             path to install into

  Optional options:
     --doc-dir=DIR               path to install docs into [/usr/share/doc/whirr]
     --lib-dir=DIR               path to install Whirr home [/usr/lib/whirr]
  "
  exit 1
}

OPTS=$(getopt \
  -n $0 \
  -o '' \
  -l 'prefix:' \
  -l 'doc-dir:' \
  -l 'lib-dir:' \
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
        --build-dir)
        BUILD_DIR=$2 ; shift 2
        ;;
        --doc-dir)
        DOC_DIR=$2 ; shift 2
        ;;
        --lib-dir)
        LIB_DIR=$2 ; shift 2
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

for var in PREFIX BUILD_DIR ; do
  if [ -z "$(eval "echo \$$var")" ]; then
    echo Missing param: $var
    usage
  fi
done

TARGET_RELEASE=distribution/tar/build/distributions/elasticsearch-5.4.1.tar.gz
SHARE_DIR=${SHARE_DIR:-/usr/lib/elasticsearch}
#SHARE_DIR=${SHARE_DIR:-usr/share/elasticsearch}
SRC=${BUILD_DIR}/working/elasticsearch-5.4.1

mkdir -p ${PREFIX}/${SHARE_DIR}
tar xzf ${BUILD_DIR}/${TARGET_RELEASE} -C ${PREFIX}/${SHARE_DIR} --strip 1


mkdir -p ${PREFIX}/${SHARE_DIR} ${PREFIX}/etc/ ${PREFIX}/etc/elasticsearch

mv ${PREFIX}/${SHARE_DIR}/config ${PREFIX}/etc/elasticsearch/conf.d
ln -s /etc/elasticsearch/conf.d ${PREFIX}/etc/elasticsearch/conf
ln -s /etc/elasticsearch/conf ${PREFIX}/${SHARE_DIR}/config

# logs
mkdir -p ${PREFIX}/var/log/elasticsearch
mkdir -p ${PREFIX}/etc/logrotate.d/
install -m 644 ${RPM_SOURCE_DIR}/elasticsearch.logrotate ${PREFIX}/etc/logrotate.d/elasticsearch

# sysconfig and init
mkdir -p ${PREFIX}/etc/systemd/system
mkdir -p ${PREFIX}/etc/sysconfig
mkdir -p ${PREFIX}/usr/lib/sysctl.d
install -m 755 ${RPM_SOURCE_DIR}/elasticsearch.service ${PREFIX}/etc/systemd/system/elasticsearch.service
install -m 755 ${RPM_SOURCE_DIR}/elasticsearch.sysconfig ${PREFIX}/etc/sysconfig/elasticsearch
install -m 755 ${RPM_SOURCE_DIR}/elasticsearch.conf ${PREFIX}/usr/lib/sysctl.d/elasticsearch.conf

mkdir -p ${PREFIX}/var/run/elasticsearch
mkdir -p ${PREFIX}/var/lib/elasticsearch
mkdir -p ${PREFIX}/lock/subsys/elasticsearch


