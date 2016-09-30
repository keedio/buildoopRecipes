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

%define lib_storm_tcp %{_usr}/lib/storm

%define storm_tcp_version 1.0.6
%define storm_tcp_base_version 1.0.6
%define storm_tcp_release 1.4.0%{?dist}
%define storm_user storm
%define storm_group storm

%define storm_home /usr/lib/storm

Name: storm-tcp
Version: %{storm_tcp_version}
Release: %{storm_tcp_release}
Summary: Storm TCP connector
URL: https://github.com/keedio/Storm-TCP-Topology
Vendor: Keedio
Packager: Rodrigo Olmo <rolmo@keedio.org>
Group: Development/Libraries
BuildArch: noarch
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{storm_tcp_version}-%{storm_tcp_release}-XXXXXX)
License: ASL 2.0
# Source from commit 3aa7020d84dc158537eb9c95fb26697d686ebbde
Source0: storm-tcp-bolt.git.tar.gz
Source1: rpm-build-stage
Source2: install_storm-tcp.sh

%description
Storm TCP connector 

%prep
%setup -n storm-tcp-bolt.git

%build
bash %{SOURCE1}

%install
%__rm -rf $RPM_BUILD_ROOT
bash %{SOURCE2} \
          --build-dir=. \
          --prefix=$RPM_BUILD_ROOT

%files
%defattr(-,%{storm_user},%{storm_group})
%{lib_storm_tcp}

%post
ln -s %{storm_home}/external/storm-tcp/storm-tcp-bolt-%{storm_tcp_version}.jar \
        %{storm_home}/lib/storm-tcp-bolt-%{storm_tcp_version}.jar
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/storm-tcp-bolt-%{storm_tcp_version}.jar

%changelog

