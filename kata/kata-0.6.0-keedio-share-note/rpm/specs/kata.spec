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
%define kata_name kata
%define lib_kata /usr/lib/%{kata_name}
%define etc_kata /etc/%{kata_name}
%define etc_rcd /etc/rc.d
%define config_kata %{etc_kata}/conf
%define log_kata /var/log/%{kata_name}
%define run_kata /var/run/%{kata_name}
%define man_dir /usr/share/man
%define kata_user_home /var/lib/kata

%define kata_version 0.6.0_keedio_share_note 
%define kata_base_version 0.6.0_keedio_share_note
%define kata_release 1.3.0

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
%define doc_kata %{_docdir}/kata
%define alternatives_cmd update-alternatives
%define alternatives_dep update-alternatives
%global initd_dir %{_sysconfdir}/rc.d
%else
%define doc_kata %{_docdir}/kata-%{kata_version}
%define alternatives_cmd alternatives
%define alternatives_dep chkconfig
%global initd_dir %{_sysconfdir}/init.d
%endif

# disable repacking jars
%define __os_install_post %{nil}

Name: kata
Version: %{kata_version}
Release: %{kata_release}
Summary: "A web-based notebook that enables interactive data analytics. You can make beautiful data-driven, interactive and collaborative documents with SQL, Scala and more. " 
URL: http://kata.apache.org
Vendor: Keedio 
Packager: Alessio Comisso <acomisso@keedio.com>
Group: Development/Libraries
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
License: APL2
Source0: %{name}.git.tar.gz
Source1: rpm-build-stage
Source2: install_%{name}.sh
Source3: kata.init
#Patch0: 5545.diff 
BuildArch: noarch
BuildRequires: autoconf, automake
Requires(pre): coreutils, /usr/sbin/groupadd, /usr/sbin/useradd
Requires: jdk, redhat-lsb, hadoop-client, hadoop-yarn
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
A web-based notebook that enables interactive data analytics.
You can make beautiful data-driven, interactive and collaborative documents with SQL, Scala and more.  
    
%prep
%setup -n %{name}.git  
#cd $RPM_SOURCE_DIR
#%patch0 -p1

%build
bash $RPM_SOURCE_DIR/rpm-build-stage
ls .

%install
%__rm -rf $RPM_BUILD_ROOT
sh $RPM_SOURCE_DIR/install_kata.sh \
          --build-dir=`pwd`         \
          --prefix=$RPM_BUILD_ROOT
%__install -d -m 0755 $RPM_BUILD_ROOT/%{initd_dir}/



# Install init script
init_file=$RPM_BUILD_ROOT/%{initd_dir}/kata
%__cp %{SOURCE3} $init_file
ls $RPM_BUILD_ROOT/%{initd_dir}
chmod 755 $init_file

%pre
getent passwd %{name} >/dev/null || /usr/sbin/useradd --comment "Kata service user" --shell /sbin/nologin -M -r -g root -M kata



#######################
#### FILES SECTION ####
#######################
%files 
%defattr(-,%{name},root,755)
/usr/lib/%{name}/*
%config(noreplace) /usr/lib/%{name}/notebook/*
%config(noreplace) /etc/%{name}/*
%attr(0755,root,root) /etc/init.d/kata
/var/run/kata
/var/log/kata
