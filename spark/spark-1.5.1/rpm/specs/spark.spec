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
%define spark_name spark
%define lib_spark /usr/lib/%{spark_name}
%define etc_spark /etc/%{spark_name}
%define etc_rcd /etc/rc.d
%define config_spark %{etc_spark}/conf
%define log_spark /var/log/%{spark_name}
%define run_spark /var/run/%{spark_name}
%define man_dir /usr/share/man
%define spark_user_home /var/lib/spark
%define rc_dir /etc/init.d

%define spark_version 1.5.1
%define spark_base_version 1.5.1
%define spark_release 1.3.0

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
%define doc_spark %{_docdir}/spark
%define alternatives_cmd update-alternatives
%define alternatives_dep update-alternatives
%global initd_dir %{_sysconfdir}/rc.d
%else
%define doc_spark %{_docdir}/spark-%{spark_version}
%define alternatives_cmd alternatives
%define alternatives_dep chkconfig
%global initd_dir %{_sysconfdir}/rc.d/init.d
%endif

# disable repacking jars
%define __os_install_post %{nil}

Name: spark
Version: %{spark_version}
Release: %{spark_release}
Summary: Apache Spark is a fast and general engine for big data processing
URL: http://spark.apache.org
Vendor: Keedio
Packager: Alessio Comisso <acomisso@keedio.com>
Group: Development/Libraries
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
License: APL2
Source0: %{name}-%{version}.tgz
Source1: rpm-build-stage
Source2: install_%{name}.sh
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
Apache Spark™ is a fast and general engine for large-scale data processing. 
    
%prep
%setup  %{name}-%{spark_base_version}.tgz 
#cd $RPM_SOURCE_DIR
#%patch0 -p1

%build
bash $RPM_SOURCE_DIR/rpm-build-stage
ls .

%install
%__rm -rf $RPM_BUILD_ROOT
sh $RPM_SOURCE_DIR/install_spark.sh \
          --build-dir=`pwd`         \
          --prefix=$RPM_BUILD_ROOT
%__install -d -m 0755 $RPM_BUILD_ROOT/%{initd_dir}/


%post
%{alternatives_cmd} --install /usr/lib/spark/default spark  /usr/lib/spark/%{name}-%{spark_base_version}-bin-2.4.0 30

%preun
if [ "$1" = 0 ]; then
        %{alternatives_cmd} --remove spark  /usr/lib/spark/%{name}-%{spark_base_version}-bin-2..0  || :
fi

#######################
#### FILES SECTION ####
#######################
%files 
%defattr(-,spark,hadoop,755)
/usr/lib/%{name}/*
%config(noreplace) /etc/%{name}/*
%attr(0755,root,root) %{rc_dir}/spark-history-server
/var/log/spark-history-server
