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

%define confdir /etc/%{name}/conf
%define grafana_name grafana
%define grafana_home /usr/lib/grafana
%define grafana_user grafana
%define grafana_user_home /var/lib/grafana
%define grafana_group grafana

%define grafana_version 4.0.0
%define grafana_release 1.4.0%{?dist}
%define debug_package %{nil}

# Added a 4 for compatibility issues with grafana 3
Name:           %{grafana_name}
Version:        %{grafana_version}
Release:        %{grafana_release}
Summary:        Grafana is a web tool to visualize and represent data

Group:          Applications/web
License:        ASL 2.0
URL:            http://www.grafana.org
Vendor:	        Keedio	
Packager:	Alessio Comisso <acomisso@keedio.org>
Source0:        %{grafana_name}.git.tar.gz

#Patch0: 	grafana-scripts-paths.patch
Source1:	install_grafana.sh
Source2:        grafana.init	
Source3:        rpm_build_stage	
Source4:        grafana-env	
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
BuildArch:      x86_64 

#AutoReqProv: 	no

%description
Grafana is a web tool to visualize and represent elasticsearch data

%prep
#%setup -n %{grafana_name}-%{grafana_version}-linux-x64
#%patch0 -p1

%build
sh %{SOURCE3}

%clean
rm -rf %{buildroot}

%install
bash %{SOURCE1} \
          --prefix=$RPM_BUILD_ROOT \
	   --build-dir=$PWD

# Install init script
init_file=${RPM_BUILD_ROOT}/etc/init.d/grafana
env_file=${RPM_BUILD_ROOT}/etc/sysconfig/grafana
%__cp %{SOURCE2} $init_file
%__cp %{SOURCE4} $env_file
#chmod 755 $init_file

%pre
# create grafana group
if ! getent group grafana >/dev/null; then
  groupadd -r grafana
fi

# create grafana user
if ! getent passwd grafana >/dev/null; then
  useradd -r -g grafana -d %{grafana_user_home} -s /sbin/nologin -c "Grafana user" -M -r -g %{grafana_group} --home %{grafana_user_home} %{grafana_user}
fi

%post
/sbin/chkconfig --add grafana 

%preun
/sbin/service grafana stop > /dev/null
/sbin/chkconfig --del grafana

%postun 
if [ $1 -ge 1 ]; then
  /sbin/service grafana condrestart > /dev/null
fi
%files
%defattr(-,%{grafana_user},%{grafana_group})
%dir %attr(755, %{grafana_user},%{grafana_group}) %{grafana_home}
%{grafana_home}/*
%attr(0755,root,root) /etc/init.d/grafana 
%config(noreplace) /etc/grafana/*
%config(noreplace) /etc/sysconfig/*
%{grafana_user_home}
/var/log/grafana
%changelog
