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

%define fw1_loggrabber_base_version 2.2
%define fw1_loggrabber_release openbus_1.2.5
%define etc_fw1 /etc/fw1-loggrabber

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

Name: fw1-loggrabber
AutoReq: 0
Version: %{fw1_loggrabber_base_version}
Release: %{fw1_loggrabber_release}
Summary: Command line Checkpoint tool (Requires external OPSEC SDK)
URL: https://github.com/keedio/fw1-loggrabber 
Vendor: The Redoop Team
Packager: Alessio Comisso <acomisso@keedio.com> 
Group: Development/Libraries
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
#BuildArch: i386
License: APL2
Source0: fw1-loggrabber.git.tar.gz 
Source1: rpm-build-stage 
Source2: install-fw1-loggrabber.sh
Requires:  compat-libstdc++-33%{_isa}
%if %{__isa_bits} == 64
Requires: compat-libstdc++-33(%{__isa_name}-32)
%endif	 
Requires:  elfutils-libelf%{_isa}
%if %{__isa_bits} == 64
Requires: elfutils-libelf(%{__isa_name}-32)
%endif
Requires:  pam%{_isa}
%if %{__isa_bits} == 64
Requires: pam(%{__isa_name}-32)
%endif
Requires: curl
Requires: wget
%if  0%{?mgaversion}
Requires: bsh-utils
%else
Requires: sh-utils
%endif

%description 
Command line Checkpoint tool (Requires external OPSEC SDK)

%prep
%setup -n fw1-loggrabber.git

%pre

%build
sh %{SOURCE1}

%install
%__rm -rf $RPM_BUILD_ROOT
sh %{SOURCE2} \
          --build-dir=. \
          --prefix=$RPM_BUILD_ROOT

%files 
%defattr(744,root,root,755)
/usr/bin/fw1-loggrabber
/usr/bin/fw1-loggrabber-setup.sh
%dir %{etc_fw1}
%config(noreplace) %{etc_fw1}/*

