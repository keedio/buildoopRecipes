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
%define kafka_name kafka
%define lib_kafka /usr/lib/%{kafka_name}
%define etc_kafka /etc/%{kafka_name}
%define etc_rcd /etc
%define config_kafka %{etc_kafka}/conf
%define log_kafka /var/log/%{kafka_name}
%define run_kafka /var/run/%{kafka_name}
%define man_dir /usr/share/man
%define kafka_user_home /var/lib/kafka

%define kafka_version 0.8.2.2
%define kafka_base_version 0.8.2.2
%define kafka_release 2.0.0%{?dist}

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
%define doc_kafka %{_docdir}/kafka
%define alternatives_cmd update-alternatives
%define alternatives_dep update-alternatives
%global initd_dir %{_sysconfdir}/systemd/system
%else
%define doc_kafka %{_docdir}/kafka-%{kafka_version}
%define alternatives_cmd alternatives
%define alternatives_dep chkconfig
%global initd_dir %{_sysconfdir}/systemd/system
%endif

# disable repacking jars
%define __os_install_post %{nil}

Name: kafka
Version: %{kafka_version}
Release: %{kafka_release}
Summary: A high-throughput distributed messaging system.
URL: http://kafka.apache.org
Vendor: Keedio
Packager: Systems <systems@keedio.com>
Group: Development/Libraries
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
License: APL2
Source0: %{name}-%{kafka_base_version}-src.tgz
Source1: rpm-build-stage
Source2: install_%{name}.sh
Source3: kafka.service
Patch0: log_path.patch
BuildArch: noarch
BuildRequires: autoconf, automake
Requires(pre): coreutils, /usr/sbin/groupadd, /usr/sbin/useradd
Requires(post): %{alternatives_dep}
Requires(preun): %{alternatives_dep}
Requires: jdk, redhat-lsb
Requires: kafka-core
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
Kafka is a high-throughput distributed messaging system.

%package core
Version: %{version}
Release: %{release}
Summary:  Core Kafka components
URL: http://incubator.apache.org/oozie/
Group: Development/Libraries
License: APL2
BuildArch: noarch

%description core
 Core components required by Kafka-HUE

    
%prep
%setup -n %{name}-%{kafka_base_version}-src
%patch0 -p1

%build
bash $RPM_SOURCE_DIR/rpm-build-stage

%install
%__rm -rf $RPM_BUILD_ROOT
sh $RPM_SOURCE_DIR/install_kafka.sh \
          --build-dir=`pwd`         \
          --prefix=$RPM_BUILD_ROOT
%__install -d -m 0755 $RPM_BUILD_ROOT/%{initd_dir}/
init_file=$RPM_BUILD_ROOT/%{initd_dir}/%{name}.service
orig_init_file=%{SOURCE3}
%__cp $orig_init_file $init_file
chmod 755 $init_file

%pre core
getent group kafka >/dev/null || groupadd -r kafka
getent passwd kafka > /dev/null || useradd -c "Kafka" -s /sbin/nologin -g kafka -r -d %{lib_kafka} kafka 2> /dev/null || :

%__install -d -o kafka -g kafka -m 0755 %{run_kafka}
%__install -d -o kafka -g kafka -m 0755 %{log_kafka}
%__install -d -o kafka -g kafka -m 0755 %{lib_kafka}

%post
systemctl enable %{name}

%post core
%{alternatives_cmd} --install %{config_kafka} %{kafka_name}-conf %{config_kafka}.dist 30

%preun
/etc/init.d/kafka stop

%preun core
if [ "$1" = 0 ]; then
        %{alternatives_cmd} --remove %{kafka_name}-conf %{config_kafka}.dist || :
fi

#######################
#### FILES SECTION ####
#######################
%files
%{etc_rcd}/systemd/system/kafka.service
%files core 
%defattr(-,root,root,755)
%config(noreplace) %{config_kafka}.dist
%attr(0755,kafka,kafka) %{kafka_user_home}
%{config_kafka}
%{lib_kafka}/bin/*
%{lib_kafka}/libs/*.jar
%{lib_kafka}/config
