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
%define base_version 1.0.0
%define release openbus_1.3.0

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

Name: flume-plugins
Version: %{base_version}
Release: %{release}
Summary: Flume Plugins meta-installer
Vendor: The Redoop Team
Packager: Alessio Comisso <acomisso@keedio.com> 
Group: Development/Libraries
Buildroot: %{_topdir}/%{name}-%{version}
BuildArch: noarch
License: APL2
Requires: flume, flume-ftp-source, flume-sql-source, flume-opsec-source, flume-taildir, flume-xmlwinevent, cacheable_interceptor, flume-enrichment-interceptor, flume-filedump-interceptor, flume-kafka-avro-sink, flume-kafka-sink, flume-snmp-source

%description 
Flume Plugins meta-installer

%prep

%build

%install
mkdir -p %{buildroot}
echo "Flume plugins %{version}" > %{buildroot}/.installed_%{name}-%{version}
%files
%defattr(-,root,root,-) 
/.installed_%{name}-%{version}
