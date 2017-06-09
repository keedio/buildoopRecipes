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

%define nagios_hadoop_version 1.1.1
%define nagios_hadoop_release 2.0.0%{?dist}

Name:    nagios-hadoop
Version: %{nagios_hadoop_version}
Release: %{nagios_hadoop_release}
Vendor: Keedio
Packager: Systems <systems@keedio.com>
Group: Applications/Engineering
Summary: Nagios-hadoop is a collection of nagios plugins to monitor Hadoop ecosystem.
License: ASL 2.0
Source0: nagios-hadoop.git.tar.gz
Source1: install_nagios-hadoop.sh
Requires: python-argparse
Requires: python-krbV
Requires: python-requests
Requires: python-requests-kerberos
Requires: nagiosplugin
Requires: thrift >= 0.9.2
Requires: python-storm
URL: http://github.com/keedio/nagios-hadoop

%define nagios_plugins_dir /usr/lib64/nagios/plugins

%description
Nagios-hadoop is a collection of nagios plugins to monitor Hadoop ecosystem. 

%prep
%setup -q -n %{name}.git

%install
%__rm -rf $RPM_BUILD_ROOT
sh %{SOURCE1} \
          --build-dir=. \
          --prefix=$RPM_BUILD_ROOT

%files
%defattr(755,'nrpe','nrpe')
%{nagios_plugins_dir}/*

%clean
%__rm -rf $RPM_BUILD_ROOT
