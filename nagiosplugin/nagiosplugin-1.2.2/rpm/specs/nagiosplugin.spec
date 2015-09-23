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
%define nagiosplugin_version 1.2.2
%define nagiosplugin_base_version 1.2.2
%define nagiosplugin_release openbus_1.3.0

Name: nagiosplugin
Version: %{nagiosplugin_version}
Release: %{nagiosplugin_release}
Summary: Library which helps writing Nagios (or Icinga) compatible plugins easily
URL: https://projects.gocept.com/projects/nagiosplugin/wiki
Vendor: Keedio
Group: Development/Libraries
License: ASL 2.0 
Source0: nagiosplugin-%{nagiosplugin_base_version}.tar.gz
BuildArch: noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description 
nagiosplugin is a Python class library which helps writing Nagios 
(or Icinga) compatible plugins easily in Python. It cares for much 
of the boilerplate code and default logic commonly found in Nagios 
checks.

%prep
%setup -q -n nagiosplugin-%{version}
# move away examples from src dir and put them to doc dir
%{__mv} %{_builddir}/nagiosplugin-%{version}/src/nagiosplugin/examples \
        %{_builddir}/nagiosplugin-%{version}
# corrects wrong shebang in examples
for example in %{_builddir}/nagiosplugin-%{version}/examples/*.py; do
 %{__sed} -i 's/\#\!/\#\!\/usr\/bin\//1' $example
 %{__chmod} a-x $example
done

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%files 
%{python_sitelib}/*

%clean
%__rm -rf $RPM_BUILD_ROOT

%changelog

