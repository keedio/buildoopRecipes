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
%define couchbase_name couchbase
%define couchbase_home /usr/lib/couchbase
%define couchbase_user couchbase
%define couchbase_user_home /var/lib/couchbase
%define couchbase_group couchbase

%define couchbase_version 4.6.2
%define couchbase_release 2.0.0%{?dist}
%define debug_package %{nil}

Name:           %{couchbase_name}
Version:        %{couchbase_version}
Release:        %{couchbase_release}
Summary:        Couchbase Server, originally known as Membase, is an open-source, distributed multi-model NoSQL document-oriented database software package that is optimized for interactive applications.

Group:          Applications/web
License:        ASL 2.0
URL:            http://www.couchbase.org
Vendor:	        Keedio	
Packager:	Alessio Comisso <acomisso@keedio.org>
#Source0:        %{couchbase_name}.git.tar.gz

#Patch0: 	couchbase-scripts-paths.patch
Source1:	install_couchbase.sh

Source3:        rpm_build_stage	

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
BuildArch:      x86_64 

AutoReqProv: 	no

%description
Couchbase Server, originally known as Membase, is an open-source, distributed multi-model NoSQL document-oriented database software package that is optimized for interactive applications.

%prep
#%setup -n %{couchbase_name}-%{couchbase_version}-linux-x64
#%patch0 -p1

%build
sh %{SOURCE3} %{couchbase_version} $PWD

%clean
rm -rf %{buildroot}

%install
bash %{SOURCE1} \
          --prefix=$RPM_BUILD_ROOT \
	   --build-dir=$PWD


%pre
#!/bin/sh

if test X"$RPM_INSTALL_PREFIX0" = X"" ; then
  RPM_INSTALL_PREFIX0=/usr/lib/couchbase
fi

if test X"$RPM_INSTALL_PREFIX1" = X"" ; then
  RPM_INSTALL_PREFIX1=/usr/lib/systemd/system
fi

getent group couchbase >/dev/null || \
   groupadd -r couchbase || exit 1
getent passwd couchbase >/dev/null || \
   useradd -r -g couchbase -d $RPM_INSTALL_PREFIX0 -s /sbin/nologin \
           -c "Couchbase system user" couchbase || exit 1

# If Couchbase was previously installed here, stop it
if [ -x $RPM_INSTALL_PREFIX1/couchbase-server.service ]
then
  /etc/init.d/couchbase-server stop || true
fi
if [ -x $RPM_INSTALL_PREFIX1/couchbase-server.service ]
then
  /etc/init.d/couchbase-server stop || true
fi
# Also check for legacy installs
if [ -x /etc/init.d/couchbase-server ]
then
  /etc/init.d/couchbase-server stop || true
fi

if [ -d /usr/lib/couchbase ]
then
  find /usr/lib/couchbase -maxdepth 1 -type l | xargs rm -f || true
fi

if test -f /sys/kernel/mm/transparent_hugepage/enabled ; then
  if ! grep -q "\[never\]" /sys/kernel/mm/transparent_hugepage/enabled ; then
    cat <<EOF
Warning: Transparent hugepages looks to be active and should not be.
Please look at http://bit.ly/1ZAcLjD as for how to PERMANENTLY alter this setting.
EOF
  fi
fi

if test -f /sys/kernel/mm/redhat_transparent_hugepage/enabled ; then
  if ! grep -q "\[never\]" /sys/kernel/mm/redhat_transparent_hugepage/enabled ; then
    cat <<EOF
Warning: Transparent hugepages looks to be active and should not be.
Please look at http://bit.ly/1ZAcLjD as for how to PERMANENTLY alter this setting.
EOF
  fi
fi

SWAPPINESS=`cat /proc/sys/vm/swappiness`
if [ "$SWAPPINESS" -ne "0" ]
then
    cat <<EOF
Warning: Swappiness is not set to 0.
Please look at http://bit.ly/1k2CtNn as for how to PERMANENTLY alter this setting.
EOF
fi

RAM=`grep 'MemTotal' /proc/meminfo | sed 's/MemTotal:\s*//g' | sed 's/\skB//g' | awk '{printf "%.2f", $1/1024/1024}'`
CPU=`grep 'processor' /proc/cpuinfo | sort -u | wc -l`

cat <<EOF
Minimum RAM required  : 4 GB
System RAM configured : $RAM GB

Minimum number of processors required : 4 cores
Number of processors on the system    : $CPU cores

EOF

exit 0
%post
#!/bin/sh

if test X"$RPM_INSTALL_PREFIX0" = X"" ; then
  RPM_INSTALL_PREFIX0=/opt/couchbase
fi

`cd $RPM_INSTALL_PREFIX0 && ./bin/install/reloc.sh $RPM_INSTALL_PREFIX0`

if [ "`uname -m`" != "x86_64" ]
then
  cat <<EOF
ERROR: The machine architecture does not match this build
of the software.  For example, installing a 32-bit build
on a 64-bit machine, or vice-versa.  Please uninstall and
install a build with a matching architecture.

EOF
  exit 1
fi

# From http://www.rpm.org/max-rpm-snapshot/s1-rpm-inside-scripts.html
# The argument to the %post script is >1 on an upgrade.

if [ -n "$INSTALL_UPGRADE_CONFIG_DIR" -o $1 -gt 1 ]
then
  if [ -z "$INSTALL_UPGRADE_CONFIG_DIR" ]
  then
    INSTALL_UPGRADE_CONFIG_DIR=$RPM_INSTALL_PREFIX0/var/lib/couchbase/config
  fi
  echo Upgrading couchbase-server ...
  echo "  $RPM_INSTALL_PREFIX0/bin/install/cbupgrade -c $INSTALL_UPGRADE_CONFIG_DIR -a yes $INSTALL_UPGRADE_EXTRA"
  if [ "$INSTALL_DONT_AUTO_UPGRADE" != "1" ]
  then
    $RPM_INSTALL_PREFIX0/bin/install/cbupgrade -c $INSTALL_UPGRADE_CONFIG_DIR -a yes $INSTALL_UPGRADE_EXTRA 2>&1 || exit 1
  else
    echo Skipping cbupgrade due to INSTALL_DONT_AUTO_UPGRADE ...
  fi
fi

exit 0
######
%preun
#!/bin/sh

if test X"$RPM_INSTALL_PREFIX0" = X"" ; then
  RPM_INSTALL_PREFIX0=/usr/lib/couchbase
fi

# $1 will be 0 only if this is a full uninstall (as opposed to an upgrade)
if [ "$1" = "0" ]
then
  /etc/init.d/couchbase-server stop || true
fi

rm -f $RPM_INSTALL_PREFIX0/bin/*.bin

exit 0

%posttrans
#!/bin/sh


if test X"$RPM_INSTALL_PREFIX0" = X"" ; then
  RPM_INSTALL_PREFIX0=/usr/lib/couchbase
fi

chkconfig couchbase-server on
if [ "$INSTALL_DONT_START_SERVER" != "1" ]
then
  /etc/init.d/couchbase-server start
else
  echo Skipping server start due to INSTALL_DONT_START_SERVER ...
fi

cat <<EOF

You have successfully installed Couchbase Server.
Please browse to http://`hostname`:8091/ to configure your server.
Please refer to http://couchbase.com for additional resources.

Please note that you have to update your firewall configuration to
allow connections to the following ports:
4369, 8091 to 8094, 9100 to 9105, 9998, 9999, 11209 to 11211,
11214, 11215, 18091 to 18093, and from 21100 to 21299.
EOF

cat <<EOF

By using this software you agree to the End User License Agreement.
See $RPM_INSTALL_PREFIX0/LICENSE.txt.

EOF

exit 0

%postun 
if [ $1 -ge 1 ]; then
  /sbin/service couchbase condrestart > /dev/null
fi
%files
%defattr(-,%{couchbase_user},%{couchbase_group})
%dir %attr(755, %{couchbase_user},%{couchbase_group}) %{couchbase_home}
%{couchbase_home}/*
%attr(0755,root,root) /etc/init.d/couchbase-server 
/var/log/couchbase
%changelog
