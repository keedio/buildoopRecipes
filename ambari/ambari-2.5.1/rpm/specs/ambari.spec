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
%define ambari_name ambari
%define release_version 4
%define ambari_home /usr/lib/ambari
%define etc_ambari /etc/%{name}
%define config_ambari %{etc_ambari}/conf
%define ambari_user ambari
%define ambari_group ambari
%define ambari_user_home /var/lib/%{ambari_name}
%global initd_dir %{_sysconfdir}/rc.d/init.d
# prevent binary stripping - not necessary at all.
# Only for prevention.
%global __os_install_post %{nil}

%define ambari_version 2.5.1
%define ambari_base_version 2.5.1
%define ambari_release 2.0.0%{?dist}


Name: %{ambari_name}
Version: %{ambari_version}
Release: %{ambari_release}
Summary: The Apache Ambari project is aimed at making Hadoop management simpler by developing software for provisioning, managing, and monitoring Apache Hadoop clusters.
License: Apache License Version 2012
URL: https://github.com/apache/ambari
Vendor: The Keedio Team
Packager: Alessio Comisso  <acomisso@keedio.com>
Group: Development/Libraries
Source0: apache-ambari-%{ambari_version}-src.tar.gz
Source8: rpm-build-stage
Source9: install_ambari.sh
Patch0: storm-sink.patch
Patch1: remove-metrics.patch 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Requires: sh-utils, textutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service
Provides: ambari
BuildArch: x86_64

%description
he Apache Ambari project is aimed at making Hadoop management simpler by developing software for provisioning, managing, and monitoring Apache Hadoop clusters. Ambari provides an intuitive, easy-to-use Hadoop management web UI backed by its RESTful APIs.
Ambari enables System Administrators to:
    Provision a Hadoop Cluster
        Ambari provides a step-by-step wizard for installing Hadoop services across any number of hosts.
        Ambari handles configuration of Hadoop services for the cluster.
    Manage a Hadoop Cluster
        Ambari provides central management for starting, stopping, and reconfiguring Hadoop services across the entire cluster.
    Monitor a Hadoop Cluster
        Ambari provides a dashboard for monitoring health and status of the Hadoop cluster.
        Ambari leverages Ambari Metrics System for metrics collection.
        Ambari leverages Ambari Alert Framework for system alerting and will notify you when your attention is needed (e.g., a node goes down, remaining disk space is low, etc).

%package server
Summary: The Ambari server
Group: System/Daemons
Requires: jdk
Requires: openssl 
Requires: postgresql-server >= 8.1
Requires: python >= 2.6
autoprov: yes
autoreq: no
%description server
The main Ambari server 

%package agent
Summary: The Ambari agent
Group: System/Daemons
Requires: openssl
Requires: zlib
Requires: python >= 2.6 
autoprov: yes
autoreq: no
 
%description agent
The agent.



%prep
%setup -n apache-ambari-%{ambari_version}-src

%patch0 -p1
#%patch1 -p1
#%patch2 -p1
#%patch3 -p1

%build
bash %{SOURCE8}

%clean
rm -rf %{buildroot}

%install
%__rm -rf $RPM_BUILD_ROOT
bash %{SOURCE9} \
	  --build-dir=$PWD \
	  --initd-dir=$RPM_BUILD_ROOT%{initd_dir} \
	  --prefix=$RPM_BUILD_ROOT 
	  
#%pre
#getent group %{ambari_group} >/dev/null || groupadd -r %{ambari_group}
#getent passwd %{ambari_user} >/dev/null || /usr/sbin/useradd --comment "Storm Daemon User" --shell /sbin/nologin -M -r -g %{ambari_group} --home %{ambari_user_home} %{ambari_user}

%files server
%attr(-,root,root)  "/etc/ambari-server/conf/metrics.properties"
%attr(-,root,root)  "/etc/ambari-server/conf/log4j.properties"
%attr(-,root,root)  "/etc/ambari-server/conf/krb5JAASLogin.conf"
%attr(-,root,root)  "/etc/ambari-server/conf/ambari.properties"
%attr(-,root,root)  "/etc/init/ambari-server.conf"
%attr(-,root,root)  "/etc/init.d/ambari-server"
%attr(-,root,root)  "/usr/sbin/ambari-server.py"
%attr(-,root,root)  "/usr/sbin/ambari_server_main.py"
%attr(-,root,root) "/usr/lib/ambari-server"
%attr(-,root,root) "/var/lib/ambari-server"
%attr(-,root,root) "/usr/lib/python2.6/site-packages"
%attr(-,root,root) "/var/log/ambari-server"
%attr(-,root,root) "/var/run/ambari-server"

%files agent
%attr(-,root,root)  "/etc/init/ambari-agent.conf"
%attr(-,root,root)  "/etc/ambari-agent/conf/ambari-agent.ini"
%attr(-,root,root)  "/etc/ambari-agent/conf/logging.conf.sample"
%attr(-,root,root)  "/etc/init.d/ambari-agent"
%attr(-,root,root)  "/usr/sbin/ambari-agent"
%attr(755,root,root) "/usr/lib/ambari-agent"
%attr(755,root,root) "/usr/lib/python2.6/site-packages"
%attr(755,root,root) "/var/lib/ambari-agent"
%attr(644,root,root)  "/var/lib/ambari-agent/cred/lib/slf4j-api-1.7.2.jar"
%attr(644,root,root)  "/var/lib/ambari-agent/cred/lib/commons-io-2.1.jar"
%attr(644,root,root)  "/var/lib/ambari-agent/cred/lib/guava-16.0.jar"
%attr(644,root,root)  "/var/lib/ambari-agent/cred/lib/commons-configuration-1.6.jar"
%attr(644,root,root)  "/var/lib/ambari-agent/cred/lib/commons-collections-3.2.2.jar"
%attr(644,root,root)  "/var/lib/ambari-agent/cred/lib/commons-logging-1.1.1.jar"
%attr(644,root,root)  "/var/lib/ambari-agent/cred/lib/hadoop-auth-2.7.3.jar"
%attr(644,root,root)  "/var/lib/ambari-agent/cred/lib/commons-cli-1.3.1.jar"
%attr(644,root,root)  "/var/lib/ambari-agent/cred/lib/commons-lang-2.5.jar"
%attr(644,root,root)  "/var/lib/ambari-agent/cred/lib/htrace-core-3.1.0-incubating.jar"
%attr(644,root,root)  "/var/lib/ambari-agent/cred/lib/hadoop-common-2.7.3.jar"
%attr(644,root,root)  "/var/lib/ambari-agent/tools/jcepolicyinfo.jar"
%attr(644,root,root)  "/var/lib/ambari-agent/tools/zkmigrator.jar"
%attr(644,root,root)  "/var/lib/ambari-agent/cache/stacks/HDP/2.1.GlusterFS/services/STORM/package/files/wordCount.jar"
%attr(644,root,root)  "/var/lib/ambari-agent/cache/stacks/HDP/2.0.6/hooks/before-START/files/fast-hdfs-resource.jar"
%attr(644,root,root)  "/var/lib/ambari-agent/cache/common-services/STORM/0.9.1/package/files/wordCount.jar"
%attr(-,root,root) "/var/log/ambari-agent"
%attr(-,root,root) "/var/run/ambari-agent"
#%define service_macro() \
#%files %1 \
#%defattr(-,root,root) \
#%{initd_dir}/%{ambari_name}-%1 \
#%post %1 \
#chkconfig --add %{ambari_name}-%1 \
#\
#%preun %1 \
#if [ $1 = 0 ]; then \
#  service %{ambari_name}-%1 stop > /dev/null 2>&1 \
#  chkconfig --del %{ambari_name}-%1 \
#fi

##%service_macro server 
##%service_macro agent 

#%files ui
#%defattr(-,root,root)
#%{initd_dir}/%{ambari_name}-ui
#%{ambari_home}/public/*

#%post ui
#chkconfig --add %{ambari_name}-ui

#%preun ui
#if [ $1 = 0 ]; then
#  service %{ambari_name}-ui stop > /dev/null 2>&1
#  chkconfig --del %{ambari_name}-ui
#fi
%pre server

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
# limitations under the License

STACKS_FOLDER="/var/lib/ambari-server/resources/stacks"
STACKS_FOLDER_OLD=/var/lib/ambari-server/resources/stacks_$(date '+%d_%m_%y_%H_%M').old

if [ -d "/etc/ambari-server/conf.save" ]
then
    mv /etc/ambari-server/conf.save /etc/ambari-server/conf_$(date '+%d_%m_%y_%H_%M').save
fi

if [ -d "$STACKS_FOLDER" ]
then
    cp -r "$STACKS_FOLDER" "$STACKS_FOLDER_OLD"
fi

exit 0
%post server

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
# limitations under the License

if [ -e "/etc/init.d/ambari-server" ]; then # Check is needed for upgrade
    # Remove link created by previous package version
    rm /etc/init.d/ambari-server
fi

ln -s /usr/sbin/ambari-server /etc/init.d/ambari-server

case "$1" in
  1) # Action install
    if [ -f "/var/lib/ambari-server/install-helper.sh" ]; then
        /var/lib/ambari-server/install-helper.sh install
    fi
    chkconfig --add ambari-server
  ;;
  2) # Action upgrade
    if [ -f "/var/lib/ambari-server/install-helper.sh" ]; then
        /var/lib/ambari-server/install-helper.sh upgrade
    fi
  ;;
esac

exit 0
%preun server

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
# limitations under the License

# WARNING: This script is performed not only on uninstall, but also
# during package update. See http://www.ibm.com/developerworks/library/l-rpm2/
# for details

if [ "$1" -eq 0 ]; then  # Action is uninstall
    /usr/sbin/ambari-server stop > /dev/null 2>&1
    if [ -d "/etc/ambari-server/conf.save" ]; then
        mv /etc/ambari-server/conf.save /etc/ambari-server/conf_$(date '+%d_%m_%y_%H_%M').save
    fi

    if [ -e "/etc/init.d/ambari-server" ]; then
        # Remove link created during install
        rm /etc/init.d/ambari-server
    fi

    mv /etc/ambari-server/conf /etc/ambari-server/conf.save

    if [ -f "/var/lib/ambari-server/install-helper.sh" ]; then
      /var/lib/ambari-server/install-helper.sh remove
    fi

    chkconfig --list | grep ambari-server && chkconfig --del ambari-server
fi

exit 0
%posttrans server

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
# limitations under the License


RESOURCE_MANAGEMENT_DIR="/usr/lib/python2.6/site-packages/resource_management"
RESOURCE_MANAGEMENT_DIR_SERVER="/usr/lib/ambari-server/lib/resource_management"
JINJA_DIR="/usr/lib/python2.6/site-packages/ambari_jinja2"
JINJA_SERVER_DIR="/usr/lib/ambari-server/lib/ambari_jinja2"

# remove RESOURCE_MANAGEMENT_DIR if it's a directory
if [ -d "$RESOURCE_MANAGEMENT_DIR" ]; then  # resource_management dir exists
  if [ ! -L "$RESOURCE_MANAGEMENT_DIR" ]; then # resource_management dir is not link
    rm -rf "$RESOURCE_MANAGEMENT_DIR"
  fi
fi
# setting resource_management shared resource
if [ ! -d "$RESOURCE_MANAGEMENT_DIR" ]; then
  ln -s "$RESOURCE_MANAGEMENT_DIR_SERVER" "$RESOURCE_MANAGEMENT_DIR"
fi

# setting jinja2 shared resource
if [ ! -d "$JINJA_DIR" ]; then
  ln -s "$JINJA_SERVER_DIR" "$JINJA_DIR"
fi

exit 0

%pre agent

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
# limitations under the License

if [ -d "/etc/ambari-agent/conf.save" ]
then
    mv /etc/ambari-agent/conf.save /etc/ambari-agent/conf_$(date '+%d_%m_%y_%H_%M').save
fi

BAK=/etc/ambari-agent/conf/ambari-agent.ini.old
ORIG=/etc/ambari-agent/conf/ambari-agent.ini

[ -f $ORIG ] && mv -f $ORIG $BAK

exit 0

%post agent

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
# limitations under the License


case "$1" in
  1) # Action install
    if [ -f "/var/lib/ambari-agent/install-helper.sh" ]; then
        /var/lib/ambari-agent/install-helper.sh install
    fi
  chkconfig --add ambari-agent
  ;;
  2) # Action upgrade
    if [ -d "/etc/ambari-agent/conf.save" ]; then
        cp -f /etc/ambari-agent/conf.save/* /etc/ambari-agent/conf
        mv /etc/ambari-agent/conf.save /etc/ambari-agent/conf_$(date '+%d_%m_%y_%H_%M').save
    fi

    if [ -f "/var/lib/ambari-agent/install-helper.sh" ]; then
        /var/lib/ambari-agent/install-helper.sh upgrade
    fi
  ;;
esac


BAK=/etc/ambari-agent/conf/ambari-agent.ini.old
ORIG=/etc/ambari-agent/conf/ambari-agent.ini

if [ -f $BAK ]; then
  SERV_HOST=`grep -e hostname\s*= $BAK | sed -r -e 's/hostname\s*=//' -e 's/\./\\\./g'`
  sed -i -r -e "s/(hostname\s*=).*/\1$SERV_HOST/" $ORIG
  rm $BAK -f
fi


exit 0
%preun agent

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
# limitations under the License

# WARNING: This script is performed not only on uninstall, but also
# during package update. See http://www.ibm.com/developerworks/library/l-rpm2/
# for details


if [ "$1" -eq 0 ]; then  # Action is uninstall
    /usr/sbin/ambari-agent stop > /dev/null 2>&1
    if [ -d "/etc/ambari-agent/conf.save" ]; then
        mv /etc/ambari-agent/conf.save /etc/ambari-agent/conf_$(date '+%d_%m_%y_%H_%M').save
    fi
    mv /etc/ambari-agent/conf /etc/ambari-agent/conf.save

    if [ -f "/var/lib/ambari-agent/install-helper.sh" ]; then
      /var/lib/ambari-agent/install-helper.sh remove
    fi

    chkconfig --list | grep ambari-server && chkconfig --del ambari-server
fi

exit 0

%posttrans agent

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
# limitations under the License


RESOURCE_MANAGEMENT_DIR="/usr/lib/python2.6/site-packages/resource_management"
RESOURCE_MANAGEMENT_DIR_AGENT="/usr/lib/ambari-agent/lib/resource_management"
JINJA_DIR="/usr/lib/python2.6/site-packages/ambari_jinja2"
JINJA_AGENT_DIR="/usr/lib/ambari-agent/lib/ambari_jinja2"

# remove RESOURCE_MANAGEMENT_DIR if it's a directory
if [ -d "$RESOURCE_MANAGEMENT_DIR" ]; then  # resource_management dir exists
  if [ ! -L "$RESOURCE_MANAGEMENT_DIR" ]; then # resource_management dir is not link
    rm -rf "$RESOURCE_MANAGEMENT_DIR"
  fi
fi
# setting resource_management shared resource
if [ ! -d "$RESOURCE_MANAGEMENT_DIR" ]; then
  ln -s "$RESOURCE_MANAGEMENT_DIR_AGENT" "$RESOURCE_MANAGEMENT_DIR"
fi

# setting jinja2 shared resource
if [ ! -d "$JINJA_DIR" ]; then
  ln -s "$JINJA_AGENT_DIR" "$JINJA_DIR"
fi

exit 0
