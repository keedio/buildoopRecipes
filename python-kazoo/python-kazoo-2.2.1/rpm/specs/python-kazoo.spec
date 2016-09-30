# Created by pyp2rpm-1.0.1
%global pypi_name kazoo

%if 0%{?fedora}
%global with_python3 1
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           python-%{pypi_name}
Version:        2.2.1
Release:        1.4.0%{?dist} 
Summary:        Higher level Python Zookeeper client

License:        ASL 2.0
URL:            https://kazoo.readthedocs.org
Source0:	kazoo.git.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
# For building documentation
BuildRequires:  python-sphinx
Vendor: Keedio
Packager: Juan Carlos Fernandez <jcfernandez@keedio.com>
%description
Kazoo is a Python library designed to make working with Zookeeper a more
hassle-free experience that is less prone to errors.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Higher level Python Zookeeper client
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# For building documentation
BuildRequires:  python3-sphinx

%description -n python3-%{pypi_name}
Kazoo is a Python library designed to make working with Zookeeper a more
hassle-free experience that is less prone to errors.
%endif

#%package doc
#Summary:    Documentation for %{name}
#Group:      Documentation
#License:    ASL 2.0

#%description doc
#Kazoo is a Python library designed to make working with Zookeeper a more
#hassle-free experience that is less prone to errors.

#This package contains documentation in HTML format.

%prep
%setup -q -n kazoo.git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# generate html docs
#sphinx-build docs html
# remove the sphinx-build leftovers
#rm -rf html/.{doctrees,buildinfo}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
# generate html docs
sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%endif # with_python3


%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

#delete tests
rm -fr %{buildroot}%{python2_sitelib}/%{pypi_name}/tests/
rm -fr %{buildroot}%{python3_sitelib}/%{pypi_name}/tests/

%files
%doc README.rst LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}dev-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

#%files doc
#%doc html


%changelog
* Tue Aug 26 2014 Nejc Saje <nsaje@redhat.com> - 2.0-2
- Remove documentation's dependency on the base package.

* Thu Jul 31 2014 Nejc Saje <nsaje@redhat.com> - 2.0-1
- Initial package.

