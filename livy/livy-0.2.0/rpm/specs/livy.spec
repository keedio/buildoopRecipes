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
%define lib_flume /usr/lib/flume
%define livy_base_version 0.2.0
%define livy_release 1.4.0%{?dist}
%define etc_flume /etc/flume/conf

%if  %{?suse_version:1}0

# Only tested on openSUSE 11.4. le'ts update it for previous release when confirmed
%if 0%{suse_version} > 1130
%define suse_check \# Define an empty suse_check for compatibility with older sles
%endif

# SLES is more strict and check all symlinks point to valid path
# But we do point to a hadoop jar which is not there at build time
# (but would be at install time).
# Since our package build system does not handle dependencies,
# these symlink checks are deactivated
%define __os_install_post \
    %{suse_check} ; \
    /usr/lib/rpm/brp-compress ; \
    %{nil}

%define alternatives_cmd update-alternatives
%global initd_dir %{_sysconfdir}/rc.d

%else
%define alternatives_cmd alternatives
%global initd_dir %{_sysconfdir}/rc.d/init.d

%endif

Name: livy
Version: %{livy_base_version}
Release: %{livy_release}
Summary: Livy is  a REST service for SPARK
URL: https://livy.io
Vendor: Keedio
Packager: Alessio Comisso <acomisso@keedio.org>
Group: Development/Libraries
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
BuildArch: noarch
License: APL2
Source0: livy.git.tar.gz
Source1: rpm-build-stage
Source2: install-livy.sh
#Requires: flume

%if  0%{?mgaversion}
Requires: bsh-utils
%else
Requires: sh-utils
%endif

%description 
Livy is  a REST service for SPARK

%prep
%setup -n livy.git

%build
sh %{SOURCE1}

%install
%__rm -rf $RPM_BUILD_ROOT
sh %{SOURCE2} \
          --build-dir=. \
          --prefix=$RPM_BUILD_ROOT

%pre
getent group livy >/dev/null || /usr/sbin/groupadd -r livy >/dev/null
getent passwd livy >/dev/null || /usr/sbin/useradd --comment "Livy User" --shell /bin/false -M -r -g livy --home /usr/lib/livy livy >/dev/null



%post
/sbin/chkconfig --add livy 



%preun
if [ "$1" = 0 ]; then
  /sbin/service livy stop > /dev/null
  /sbin/chkconfig --del livy
fi

%postun
if [ $1 -ge 1 ]; then
  /sbin/service livy condrestart > /dev/null
fi

%files 
%defattr(755,livy,livy,755)
%dir /usr/lib/livy
/usr/lib/livy/*
/var/log/livy
/var/run/livy
%config(noreplace) /etc/livy/
%attr(0755,root,root) /etc/init.d/livy

