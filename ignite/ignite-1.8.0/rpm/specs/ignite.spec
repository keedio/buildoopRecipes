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
%define ignite_name ignite
%define lib_ignite /usr/lib/%{ignite_name}
%define etc_ignite /etc/%{ignite_name}
%define etc_rcd /etc/rc.d
%define config_ignite %{etc_ignite}/conf
%define log_ignite /var/log/%{ignite_name}
%define run_ignite /var/run/%{ignite_name}
%define man_dir /usr/share/man
%define ignite_user_home /var/lib/ignite
%define rc_dir /etc/systemd/system

%define ignite_version 1.8.0
%define hadoop_version 2.7.2
%define ignite_base_version 1.8.0
%define ignite_release 1.4.0%{?dist}

# Disable post hooks (brp-repack-jars, etc) that just take forever and sometimes cause issues
%define __os_install_post \
    %{!?__debug_package:/usr/lib/rpm/brp-strip %{__strip}} \
%{nil}
%define __jar_repack %{nil}
%define __prelink_undo_cmd %{nil}

# Disable debuginfo package, since we never need to gdb
# our own .sos anyway
%define debug_package %{nil}

%if  %{?suse_version:1}0
%define doc_ignite %{_docdir}/ignite
%define alternatives_cmd update-alternatives
%define alternatives_dep update-alternatives
%global initd_dir %{_sysconfdir}/rc.d
%else
%define doc_ignite %{_docdir}/ignite-%{ignite_version}
%define alternatives_cmd alternatives
%define alternatives_dep chkconfig
%global initd_dir %{_sysconfdir}/rc.d/init.d
%endif

# disable repacking jars
%define __os_install_post %{nil}

Name: ignite
Version: %{ignite_version}
Release: %{ignite_release}
Summary: Apache Ignite is an in meroy hadoop accelerator
URL: http://ignite.apache.org
Vendor: Keedio
Packager: Alessio Comisso <acomisso@keedio.com>
Group: Development/Libraries
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
License: APL2
Source0: %{version}.tar.gz
Source1: rpm-build-stage
Source2: install_%{name}.sh
BuildArch: noarch
BuildRequires: autoconf, automake
Requires(pre): coreutils, /usr/sbin/groupadd, /usr/sbin/useradd
Requires: redhat-lsb, hadoop-client, hadoop-yarn
%if  %{?suse_version:1}0
# Required for init scripts
Requires: insserv
%endif

%if  0%{?mgaversion}
# Required for init scripts
Requires: initscripts
%endif

%if %{!?suse_version:1}0 && %{!?mgaversion:1}0
# Required for init scripts
Requires: redhat-lsb
%endif

%description 
Apache Ignitetm In-Memory Data Fabric is a high-performance, integrated and distributed in-memory platform for computing and transacting on large-scale data sets in real-time, orders of magnitude faster than possible with traditional disk-based or flash-based technologies.
    
%prep
%setup  %{ignite_base_version}.tgz 
#cd $RPM_SOURCE_DIR
#%patch0 -p1
#%patch1 -p0

%build
bash $RPM_SOURCE_DIR/rpm-build-stage
ls .

%install
%__rm -rf $RPM_BUILD_ROOT
sh $RPM_SOURCE_DIR/install_ignite.sh \
          --build-dir=`pwd`         \
          --prefix=$RPM_BUILD_ROOT
%__install -d -m 0755 $RPM_BUILD_ROOT/%{initd_dir}/


%post
%{alternatives_cmd} --install /usr/lib/ignite/default ignite  /usr/lib/ignite/%{name}-%{ignite_base_version}-bin-%{hadoop_version} 32
systemctl enable ignite-history-server

%preun
if [ "$1" = 0 ]; then
        %{alternatives_cmd} --remove ignite  /usr/lib/ignite/%{name}-%{ignite_base_version}-bin-2..0  || :
fi

#######################
#### FILES SECTION ####
#######################
%files 
%defattr(-,ignite,hadoop,755)
/usr/lib/%{name}/*
%config(noreplace) /etc/%{name}/*
%attr(0755,root,root) %{rc_dir}/ignite-history-server.service
/var/log/ignite-history-server
