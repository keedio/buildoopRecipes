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
%define thrift_version 0.9.2
%define thrift_base_version 0.9.2
%define thrift_release openbus_1.3.0

Name: thrift
Version: %{thrift_version}
Release: %{thrift_release}
Summary: Thrift Python Software Library
URL: http://pypi.python.org/pypi/thrift
Vendor: Keedio
Group: Development/Libraries
License: ASL 2.0 
Source0: thrift-%{thrift_base_version}.tar.gz
BuildRequires:  python-devel

%description 
nagiosplugin is a Python class library which helps writing Nagios 
(or Icinga) compatible plugins easily in Python. It cares for much 
of the boilerplate code and default logic commonly found in Nagios 
checks.

%prep
%setup -n thrift-%{thrift_base_version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%files 
%defattr(-,root,root,-)
%{python_sitearch}/*

%clean
%__rm -rf $RPM_BUILD_ROOT

%changelog

