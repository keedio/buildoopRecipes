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

%define ambari_version 1.7.0
%define ambari_base_version 1.7.0
%define ambari_release openbus_1.3.0


Name: %{ambari_name}
Version: %{ambari_version}
Release: %{ambari_release}
Summary: Storm is a distributed realtime computation system.
License: Apache License Version 2012
URL: https://github.com/apache/ambari
Vendor: The Keedio Team
Packager: Alessio Comisso  <acomisso@keedio.com>
Group: Development/Libraries
Source0: %{ambari_name}-%{ambari_version}.tar.gz
Source8: rpm-build-stage
Source9: install_ambari.sh
Patch0: ambari.patch
Patch1: remove-metrics.patch 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Requires: sh-utils, textutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service
Provides: ambari
BuildArch: noarch

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
BuildArch: noarch
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
 
BuildArch: noarch 
%description agent
The agent.



%prep
%setup -n %{ambari_name}-%{ambari_version}

%patch0 -p1
%patch1 -p1
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
%defattr(644,root,root,755)
 /usr/lib/ambari-server/spring-security-core-3.1.2.RELEASE.jar
 /usr/lib/ambari-server/jetty-continuation-7.6.7.v20120910.jar
 /usr/lib/ambari-server/spring-tx-3.0.7.RELEASE.jar
 /usr/lib/ambari-server/activation-1.1.jar
 /usr/lib/ambari-server/objenesis-tck-1.2.jar
 /usr/lib/ambari-server/guice-persist-3.0.jar
 /usr/lib/ambari-server/c3p0-0.9.1.1.jar
 /usr/lib/ambari-server/apacheds-protocol-ldap-1.5.5.jar
 /usr/lib/ambari-server/jersey-json-1.11.jar
 /usr/lib/ambari-server/apacheds-xdbm-search-1.5.5.jar
 /usr/lib/ambari-server/jersey-multipart-1.11.jar
 /usr/lib/ambari-server/apacheds-bootstrap-partition-1.5.5.jar
 /usr/lib/ambari-server/apacheds-xdbm-tools-1.5.5.jar
 /usr/lib/ambari-server/eclipselink-2.4.0.jar
 /usr/lib/ambari-server/cglib-2.2.2.jar
 /usr/lib/ambari-server/derby-10.9.1.0.jar
 /usr/lib/ambari-server/jersey-core-1.11.jar
 /usr/lib/ambari-server/apacheds-protocol-shared-1.5.5.jar
 /usr/lib/ambari-server/jackson-mapper-asl-1.9.2.jar
 /usr/lib/ambari-server/jetty-webapp-7.6.7.v20120910.jar
 /usr/lib/ambari-server/jetty-servlet-7.6.7.v20120910.jar
 /usr/lib/ambari-server/jersey-servlet-1.11.jar
 /usr/lib/ambari-server/shared-asn1-0.9.17.jar
 /usr/lib/ambari-server/jackson-core-asl-1.9.9.jar
 /usr/lib/ambari-server/javax.servlet-2.5.0.v201103041518.jar
 /usr/lib/ambari-server/commons-collections-3.2.1.jar
 /usr/lib/ambari-server/asm-3.3.1.jar
 /usr/lib/ambari-server/guava-14.0.1.jar
 /usr/lib/ambari-server/apacheds-core-jndi-1.5.5.jar
 /usr/lib/ambari-server/httpclient-4.2.5.jar
 /usr/lib/ambari-server/spring-asm-3.0.7.RELEASE.jar
 /usr/lib/ambari-server/quartz-2.2.1.jar
 /usr/lib/ambari-server/jackson-xc-1.9.9.jar
 /usr/lib/ambari-server/ambari-views-1.7.0.0.jar
 /usr/lib/ambari-server/jetty-http-7.6.7.v20120910.jar
 /usr/lib/ambari-server/postgresql-9.3-1101-jdbc4.jar
 /usr/lib/ambari-server/apacheds-jdbm-1.5.5.jar
 /usr/lib/ambari-server/spring-ldap-core-1.3.1.RELEASE.jar
 /usr/lib/ambari-server/antlr-2.7.7.jar
 /usr/lib/ambari-server/shared-ldap-constants-0.9.17.jar
 /usr/lib/ambari-server/jetty-server-7.6.7.v20120910.jar
 /usr/lib/ambari-server/slf4j-log4j12-1.7.2.jar
 /usr/lib/ambari-server/apacheds-bootstrap-extract-1.5.5.jar
 /usr/lib/ambari-server/commons-codec-1.8.jar
 /usr/lib/ambari-server/shared-ldap-0.9.17.jar
 /usr/lib/ambari-server/spring-context-3.0.7.RELEASE.jar
 /usr/lib/ambari-server/spring-expression-3.0.7.RELEASE.jar
 /usr/lib/ambari-server/mimepull-1.6.jar
 /usr/lib/ambari-server/apacheds-core-avl-1.5.5.jar
 /usr/lib/ambari-server/jaxb-api-2.2.2.jar
 /usr/lib/ambari-server/mina-core-2.0.0-M6.jar
 /usr/lib/ambari-server/spring-web-3.0.7.RELEASE.jar
 /usr/lib/ambari-server/servlet-api-2.5.jar
 /usr/lib/ambari-server/jersey-server-1.11.jar
 /usr/lib/ambari-server/jetty-io-7.6.7.v20120910.jar
 /usr/lib/ambari-server/jersey-client-1.11.jar
 /usr/lib/ambari-server/httpcore-4.2.4.jar
 /usr/lib/ambari-server/gson-2.2.2.jar
 /usr/lib/ambari-server/commons-logging-1.1.1.jar
 /usr/lib/ambari-server/commons-io-2.1.jar
 /usr/lib/ambari-server/guice-assistedinject-3.0.jar
 /usr/lib/ambari-server/commons-lang-2.5.jar
 /usr/lib/ambari-server/jetty-util-7.6.7.v20120910.jar
 /usr/lib/ambari-server/spring-security-ldap-3.1.2.RELEASE.jar
 /usr/lib/ambari-server/apacheds-schema-registries-1.5.5.jar
 /usr/lib/ambari-server/bcprov-jdk15-140.jar
 /usr/lib/ambari-server/aopalliance-1.0.jar
 /usr/lib/ambari-server/commons-net-1.4.1.jar
 /usr/lib/ambari-server/guice-3.0.jar
 /usr/lib/ambari-server/quartz-jobs-2.2.1.jar
 /usr/lib/ambari-server/apacheds-utils-1.5.5.jar
 /usr/lib/ambari-server/slf4j-api-1.7.2.jar
 /usr/lib/ambari-server/jsr305-1.3.9.jar
 /usr/lib/ambari-server/apacheds-xdbm-base-1.5.5.jar
 /usr/lib/ambari-server/javax.inject-1.jar
 /usr/lib/ambari-server/spring-security-web-3.1.2.RELEASE.jar
 /usr/lib/ambari-server/spring-security-config-3.1.2.RELEASE.jar
 /usr/lib/ambari-server/spring-aop-3.0.7.RELEASE.jar
 /usr/lib/ambari-server/apacheds-schema-extras-1.5.5.jar
 /usr/lib/ambari-server/jersey-guice-1.11.jar
 /usr/lib/ambari-server/apacheds-core-1.5.5.jar
 /usr/lib/ambari-server/shared-asn1-codec-0.9.15.jar
 /usr/lib/ambari-server/oro-2.0.8.jar
 /usr/lib/ambari-server/apacheds-schema-bootstrap-1.5.5.jar
 /usr/lib/ambari-server/guice-servlet-3.0.jar
 /usr/lib/ambari-server/log4j-1.2.16.jar
 /usr/lib/ambari-server/spring-core-3.0.7.RELEASE.jar
 /usr/lib/ambari-server/commons-httpclient-3.1.jar
 /usr/lib/ambari-server/apacheds-core-constants-1.5.5.jar
 /usr/lib/ambari-server/stax-api-1.0-2.jar
 /usr/lib/ambari-server/jackson-jaxrs-1.9.9.jar
 /usr/lib/ambari-server/javax.persistence-2.0.4.v201112161009.jar
 /usr/lib/ambari-server/apacheds-core-entry-1.5.5.jar
 /usr/lib/ambari-server/velocity-1.7.jar
 /usr/lib/ambari-server/guice-multibindings-3.0.jar
 /usr/lib/ambari-server/jaxb-impl-2.2.3-1.jar
 /usr/lib/ambari-server/spring-beans-3.0.7.RELEASE.jar
 /usr/lib/ambari-server/commonj.sdo-2.1.1.v201112051852.jar
 /usr/lib/ambari-server/apacheds-jdbm-store-1.5.5.jar
 /usr/lib/ambari-server/spring-jdbc-3.0.7.RELEASE.jar
 /usr/lib/ambari-server/jetty-xml-7.6.7.v20120910.jar
 /usr/lib/ambari-server/jetty-security-7.6.7.v20120910.jar
 /usr/lib/ambari-server/apacheds-kerberos-shared-1.5.5.jar
 /usr/lib/ambari-server/apacheds-core-shared-1.5.5.jar
 /usr/lib/ambari-server/shared-cursor-0.9.15.jar
 /usr/lib/ambari-server/web
 /usr/lib/ambari-server/ambari-server-1.7.0.0.jar
 /usr/lib/ambari-server/lib/ambari_commons
 /usr/lib/ambari-server/lib/resource_management
%attr(755,root,root) /usr/lib/ambari-server/lib/ambari_jinja2
%attr(755,root,root) /usr/sbin/ambari-server.py
%attr(755,root,root) /usr/sbin/ambari-server
%attr(755,root,root) /var/lib/ambari-server//ambari-python-wrap
%config  /etc/ambari-server/conf
%attr(700,root,root) /var/lib/ambari-server//ambari-env.sh
%attr(700,root,root) /var/lib/ambari-server//install-helper.sh
 /var/lib/ambari-server/keys/ca.config
%attr(700,root,root) /var/lib/ambari-server/keys/db
%dir  /var/run/ambari-server/bootstrap
%dir  /var/run/ambari-server/stack-recommendations
%dir  /var/log/ambari-server
 /var/lib/ambari-server/resources/Ambari-DDL-Postgres-DROP.sql
 /var/lib/ambari-server/resources/role_command_order.json
 /var/lib/ambari-server/resources/Ambari-DDL-MySQL-CREATE.sql
 /var/lib/ambari-server/resources/Ambari-DDL-Postgres-CREATE.sql
 /var/lib/ambari-server/resources/Ambari-DDL-MySQL-DROP.sql
 /var/lib/ambari-server/resources/Ambari-DDL-Oracle-DROP.sql
 /var/lib/ambari-server/resources/Ambari-DDL-Postgres-EMBEDDED-CREATE.sql
 /var/lib/ambari-server/resources/Ambari-DDL-Postgres-EMBEDDED-DROP.sql
 /var/lib/ambari-server/resources/Ambari-DDL-Oracle-CREATE.sql
 /var/lib/ambari-server/resources/DBConnectionVerification.jar
%dir %attr(755,root,root) /var/lib/ambari-server/data/tmp
%attr(755,root,root) /var/lib/ambari-server/resources/apps
%attr(755,root,root) /var/lib/ambari-server/resources/scripts
%attr(755,root,root) /var/lib/ambari-server/resources/views
%dir  /var/lib/ambari-server/resources/upgrade
 /var/lib/ambari-server/resources/upgrade/ddl
 /var/lib/ambari-server/resources/upgrade/dml
 /var/lib/ambari-server/resources/stacks/HDP
%attr(755,root,root) /var/lib/ambari-server/resources/stacks/stack_advisor.py
%attr(755,root,root) /usr/lib/python2.6/site-packages/ambari_server
%dir  /var/run/ambari-server
 /var/lib/ambari-server/resources/version
 /var/lib/ambari-server/resources/custom_action_definitions
%attr(755,root,root) /var/lib/ambari-server/resources/custom_actions


%files agent
%attr(-,root,root) /usr/lib/python2.6/site-packages/ambari_agent
%attr(755,root,root) /var/lib/ambari-agent//ambari-python-wrap
%attr(-,root,root) /usr/lib/ambari-agent/lib/ambari_commons
%attr(-,root,root) /usr/lib/ambari-agent/lib/resource_management
%attr(755,root,root) /usr/lib/ambari-agent/lib/ambari_jinja2
%attr(755,root,root) /usr/lib/ambari-agent/lib/examples
%attr(755,root,root) /etc/ambari-agent/conf
%attr(755,root,root) /usr/sbin/ambari-agent
%attr(700,root,root) /var/lib/ambari-agent/ambari-env.sh
%attr(700,root,root) /var/lib/ambari-agent/install-helper.sh
%dir %attr(755,root,root) /var/run/ambari-agent
%dir %attr(755,root,root) /var/lib/ambari-agent/data
%dir %attr(755,root,root) /var/lib/ambari-agent/data/tmp
%dir %attr(755,root,root) /var/lib/ambari-agent/keys
%dir %attr(755,root,root) /var/log/ambari-agent
%attr(755,root,root) /etc/rc.d/init.d
%attr(755,root,root) /var/lib/ambari-agent/data/version
%attr(755,root,root) /var/lib/ambari-agent/cache

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
