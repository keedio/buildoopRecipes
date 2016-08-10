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
%define lib_hadoop_lzo /usr/lib/hadoop/lib
%define lib_hadoop_lzo_native  /usr/lib/hadoop/lib/native
%define hadoop_lzo_base_version 0.4.19
%define hadoop_lzo_release 1.4.0%{?dist}


# SLES is more strict and check all symlinks point to valid path
# But we do point to a hadoop jar which is not there at build time
# (but would be at install time).
# Since our package build system does not handle dependencies,
# these symlink checks are deactivated

Name: hadoop-lzo 
Version: %{hadoop_lzo_base_version}
Release: %{hadoop_lzo_release}
Summary: hadoop-lzo 
URL: https://github.com/keedio/flume-ftp-source/
Vendor: Keedio 
Packager: Alessio Comisso <acomisso@keedio.org>
Group: Development/Libraries
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
BuildArch: x86_64 
License: APL2
Source0: hadoop-lzo.git.tar.gz
Source1: rpm-build-stage
Source2: install-hadoop-lzo.sh
Requires: hadoop /usr/lib64/liblzo2.so.2 /usr/lib/liblzo2.so.2 %{name}-native = %{version}-%{release} 

%if  0%{?mgaversion}
Requires: bsh-utils
%else
Requires: sh-utils
%endif

%define debug_package %{nil}

%package native
Summary: Native libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
%description
Splittable LZO compression for HDFS , Twitter version

%description native 
Native libraries for lzo compression

%prep
%setup -n hadoop-lzo.git

%build
sh %{SOURCE1}

%install
%__rm -rf $RPM_BUILD_ROOT
sh %{SOURCE2} \
          --build-dir=. \
          --prefix=$RPM_BUILD_ROOT

%files 
%defattr(644,root,root,755)
%{lib_hadoop_lzo}/*.jar

%files native 
%defattr(644,root,root,755)
%{lib_hadoop_lzo_native}/*
