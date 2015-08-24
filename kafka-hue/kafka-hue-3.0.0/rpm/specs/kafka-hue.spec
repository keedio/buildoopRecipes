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

%define kafka_hue_version 3.0.0
%define kafka_hue_base_version 3.0.0
%define kafka_hue_release openbus_1.2.0

Name:    kafka-hue
Version: %{kafka_hue_version}
Release: %{kafka_hue_release}
Group: Applications/Engineering
Summary: Apache Kafka HUE Application
License: ASL 2.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id} -u -n)
Source0: kafka-hue.git.tar.gz
Source1: install_kafka-hue.sh
URL: https://github.com/keedio/kafka-hue
Requires: hue
Requires: kafka-core

############### DESKTOP SPECIFIC CONFIGURATION ##################

# customization of install spots
%define hue_dir /usr/lib/hue
%define username hue
%define apps_dir %{hue_dir}/apps
%define kafka_hue_app_dir %{hue_dir}/apps/kafka

%post
%{hue_dir}/build/env/bin/python %{hue_dir}/tools/app_reg/app_reg.py --install %{apps_dir}/kafka --relative-paths \
chown -R hue:hue /var/log/hue /var/lib/hue

%description
Kafka-HUE is a HUE application to admin and manage a pool of Apache Kafka clusters.

%prep
%setup -n %{name}.git

%install
%__rm -rf $RPM_BUILD_ROOT
sh %{SOURCE1} \
          --build-dir=. \
          --prefix=$RPM_BUILD_ROOT

%files
%{kafka_hue_app_dir}

%clean
%__rm -rf $RPM_BUILD_ROOT
