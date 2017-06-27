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
%define storm_name storm
%define release_version 4
%define storm_home /usr/lib/storm
%define etc_storm /etc/%{name}
%define config_storm %{etc_storm}/conf
%define storm_user storm
%define storm_group storm
%define storm_user_home /var/lib/%{storm_name}
%global initd_dir %{_sysconfdir}/rc.d/init.d
# prevent binary stripping - not necessary at all.
# Only for prevention.
%global __os_install_post %{nil}

%define storm_version 1.0.3
%define storm_base_version 1.0.3
%define storm_release 2.0.0%{?dist}

%define kafka_version 0.8.2.2


Name: %{storm_name}
Version: %{storm_version}
Release: %{storm_release}
Summary: Storm is a distributed realtime computation system.
License: APL2
URL: https://github.com/apache/storm
Vendor: Keedio
Packager: Luca Rosellini <lrosellini@keedio.com>
Group: Development/Libraries
Source0: apache-%{storm_name}-%{storm_version}-src.tar.gz
Source1: cluster.xml
Source2: storm-ui.init
Source3: storm-supervisor.init
Source4: storm
Source5: storm.nofiles.conf
Source6: storm-nimbus.init
Source7: storm-drpc.init
Source8: rpm-build-stage
Source9: install_storm.sh
Source10: storm-logviewer.init
#Patch0: storm-kafka-shaded.patch
#Patch1: storm-bin-0.9.4.patch
#Patch2: storm-hbase-dependency.patch
#Patch3: STORM-643.patch 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Requires: sh-utils, textutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service
Provides: storm
BuildArch: noarch

%description
Storm is a distributed realtime computation system. Similar to how Hadoop
provides a set of general primitives for doing batch processing, Storm provides
a set of general primitives for doing realtime computation. 

It's a distributed real-time computation system for processing fast, 
large streams of data. Storm adds reliable real-time data processing 
capabilities to Apache Hadoop 2.x. Storm in Hadoop helps capture new 
business opportunities with low-latency dashboards, security alerts, 
and operational enhancements integrated with other applications 
running in their Hadoop cluster.

%package nimbus
Summary: The Storm Nimbus node manages the Storm cluster.
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description nimbus
Nimbus role is the Master Node of Storm, is responsible for distributing code 
around the Storm cluster, assigning tasks to machines, and monitoring for failures. 

%package ui
Summary: The Storm UI exposes metrics for the Storm cluster.
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description ui
The Storm UI exposes metrics on a web interface on port 8080 to give you
a high level view of the cluster.

%package supervisor
Summary: The Storm Supervisor is a worker process of the Storm cluster.
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description supervisor
The Supervisor role is the Worker Node, listens for work assigned to its 
machine and starts and stops worker processes as necessary based on what 
Nimbus has assigned to it. Each worker node executes a subset of a topology. 
A topology in Storm runs across many worker nodes on different machines.

%package drpc
Summary: Storm Distributed RPC daemon.
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description drpc
The DRPC server coordinates receiving an RPC request, sending the request to
the Storm topology, receiving the results from the Storm topology, and sending
the results back to the waiting client. 

%package jms
Summary: JMS connector for Storm.
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description jms
Storm JMS is a generic framework for integrating JMS messaging within the Storm framework.

%package flux
Summary: Flux connector for Storm.
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description flux 
Apache Storm 0.10.0 now includes Flux, which is a framework and set of utilities that make defining and deploying Storm topologies less painful and developer-intensive. A common pain point mentioned by Storm users is the fact that the wiring for a Topology graph is often tied up in Java code, and that any changes require recompilation and repackaging of the topology jar file. Flux aims to alleviate that pain by allowing you to package all your Storm components in a single jar, and use an external text file to define the layout and configuration of your topologies.

%package sql
Summary: SQL connector for Storm.
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description sql 
The Storm SQL integration allows users to run SQL queries over streaming data in Storm. Not only the SQL interface allows faster development cycles on streaming analytics, but also opens up the opportunities to unify batch data processing like Apache Hive and real-time streaming data analytics. At a very high level StormSQL compiles the SQL queries to Trident topologies and executes them in Storm clusters. This document provides information of how to use StormSQL as end users. For people that are interested in more details in the design and the implementation of StormSQL please refer to the this page.

%package cassandra
Summary: Cassandra Bolt for Storm.
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description cassandra
This library provides core storm bolt on top of Apache Cassandra. Provides simple DSL to map storm Tuple to Cassandra Query Language Statement.

%package elasticsearch
Summary: Elasticsearch connector  for Storm.
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description elasticsearch
EsIndexBolt, EsPercolateBolt and EsState allows users to stream data from storm into Elasticsearch directly. For detailed description, please refer to the following.

%package eventhubs
Summary: Eventhubs connector  for Storm.
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description eventhubs
EsIndexBolt, EsPercolateBolt and EsState allows users to stream data from storm into Elasticsearch directly. For detailed description, please refer to the following.



%package hbase
Summary: Storm HBase Connector.
Group: Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description hbase
Storm-HBase provides Storm/Trident integration for Apache HBase.

%package kafka
Summary: Storm Kafka Connector.
Group: Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description kafka
Provides core storm and Trident spout implementations for consuming data from Apache Kafka 0.8.x.

%package kafka-client
Summary: Storm Kafka Client.
Group: Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description kafka-client
Provides core storm and Trident spout implementations for consuming data from Apache Kafka 0.8.x.

%package hdfs
Summary: Storm HDFS Connector.
Group: Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description hdfs
Storm-HDFS provides Storm components for interacting with HDFS file systems.

%package hive
Summary: Storm HIVE Connector.
Group: Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description hive
Hive offers streaming API that allows data to be written continuously into Hive. With the help of Hive Streaming API, HiveBolt and HiveState allows users to stream data from Storm into Hive directly. 

%package jdbc
Summary: Storm jdbc Connector.
Group: Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description jdbc
Storm/Trident integration for JDBC. This package includes the core bolts and trident states that allows a storm topology to either insert storm tuples in a database table or to execute select queries against a database and enrich tuples in a storm topology.

%package logviewer
Summary: The Storm LogViewer daemon
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description logviewer
New feature for debugging and monitoring topologies: The logviewer daemon.


%package mongodb
Summary: The Storm mongodb connector
Group: Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description mongodb
Storm/Trident integration for MongoDB. This package includes the core bolts and trident states that allows a storm topology to either insert storm tuples in a database collection or to execute update queries against a database collection in a storm topology.

%package mqtt
Summary: The Storm MQTT connector 
Group: Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description mqtt
MQTT is a lightweight publish/subscribe protocol frequently used in IoT applications.
Storm/Trident integration for MongoDB. This package includes the core bolts and trideddnt states that allows a storm topology to either insert storm tuples in a database collection or to execute update queries against a database collection in a storm topology.


%package redis
Summary: The Storm Redis connector 
Group: Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description redis
Storm/Trident integration for Redis

%package solr
Summary: The Storm SolR connector 
Group: Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description solr
Storm/Trident integration for SolR

%prep
%setup -n apache-%{storm_name}-%{storm_version}

#%patch0 -p1
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
	  --build-dir=$PWD/build \
	  --initd-dir=$RPM_BUILD_ROOT%{initd_dir} \
	  --prefix=$RPM_BUILD_ROOT 
	  
%pre
getent group %{storm_group} >/dev/null || groupadd -r %{storm_group}
getent passwd %{storm_user} >/dev/null || /usr/sbin/useradd --comment "Storm Daemon User" --shell /sbin/nologin -M -r -g %{storm_group} --home %{storm_user_home} %{storm_user}

%files
%defattr(-,%{storm_user},%{storm_group})
%dir %attr(755, %{storm_user},%{storm_group}) %{storm_home}
%dir %attr(755, %{storm_user},%{storm_group}) /etc/storm
%dir %attr(755, %{storm_user},%{storm_group}) /var/run/storm
%{storm_home}/CHANGELOG.md
%{storm_home}/LICENSE
%{storm_home}/NOTICE
%{storm_home}/README.markdown
%{storm_home}/RELEASE
%{storm_home}/conf
%{storm_home}/examples/*
%{storm_home}/lib/*
%{storm_home}/logback/*
%{storm_home}/bin/*
%config(noreplace) /etc/storm/*
/etc/default/storm
/var/log/*
/var/lib/storm/
%config(noreplace) /etc/sysconfig/storm
/etc/security/limits.d/storm.nofiles.conf
%attr(644,%{storm_user},%{storm_group}) %{storm_user_home}/.bash_profile


%define service_macro() \
%files %1 \
%defattr(-,root,root) \
%{initd_dir}/%{storm_name}-%1 \
%post %1 \
chkconfig --add %{storm_name}-%1 \
\
%preun %1 \
if [ $1 = 0 ]; then \
  service %{storm_name}-%1 stop > /dev/null 2>&1 \
  chkconfig --del %{storm_name}-%1 \
fi

%service_macro nimbus
%service_macro supervisor
%service_macro drpc
%service_macro logviewer

%files ui
%defattr(-,root,root)
%{initd_dir}/%{storm_name}-ui
%{storm_home}/public/*

%post ui
chkconfig --add %{storm_name}-ui

%preun ui
if [ $1 = 0 ]; then
  service %{storm_name}-ui stop > /dev/null 2>&1
  chkconfig --del %{storm_name}-ui
fi

%files jms
%defattr(-,%{storm_user},%{storm_group})
%{storm_home}/external/storm-jms/*


%post jms
ln -s  %{storm_home}/external/storm-jms/storm-jms-%{storm_version}.jar \
	%{storm_home}/lib/storm-jms-%{storm_version}.jar
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/storm-jms-%{storm_version}.jar

%postun jms
rm -f %{storm_home}/lib/storm-jms-%{storm_version}.jar

%files flux
%defattr(-,%{storm_user},%{storm_group})
%{storm_home}/external/flux/*


%post flux
ln -s %{storm_home}/external/flux/flux-core-%{storm_version}.jar \
	%{storm_home}/lib/flux-core-%{storm_version}.jar
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/flux-core-%{storm_version}.jar

%postun flux
rm -f %{storm_home}/lib/flux-core-%{storm_version}.jar

%files sql
%defattr(-,%{storm_user},%{storm_group})
%{storm_home}/external/sql/*

%post sql
ln -s %{storm_home}/external/sql/storm-sql-core/*.jar \
	%{storm_home}/lib/.
ln -s %{storm_home}/external/sql/storm-sql-kafka/storm-sql-kafka-%{storm_version}.jar \
	%{storm_home}/lib/.
ln -s %{storm_home}/external/sql/storm-sql-runtime/storm-sql-runtime-%{storm_version}.jar \
	%{storm_home}/lib/.
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/*.jar
%postun sql
rm -f %{storm_home}/lib/storm-sql-core-%{storm_version}.jar
rm -f %{storm_home}/lib/storm-sql-kafka-%{storm_version}.jar
rm -f %{storm_home}/lib/storm-sql-runtime-%{storm_version}.jar

%files cassandra
%defattr(-,%{storm_user},%{storm_group})
%{storm_home}/external/storm-cassandra/*


%post cassandra
ln -s %{storm_home}/external/storm-cassandra/storm-cassandra-%{storm_version}.jar \
	%{storm_home}/lib/storm-cassandra-%{storm_version}.jar
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/storm-cassandra-%{storm_version}.jar

%postun cassandra
rm -f %{storm_home}/lib/storm-cassandra-%{storm_version}.jar

%files elasticsearch
%defattr(-,%{storm_user},%{storm_group})
%{storm_home}/external/storm-elasticsearch/*


%post elasticsearch
ln -s %{storm_home}/external/storm-elasticsearch/storm-elasticsearch-%{storm_version}.jar \
	%{storm_home}/lib/storm-elasticsearch-%{storm_version}.jar
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/storm-elasticsearch-%{storm_version}.jar

%postun elasticsearch
rm -f %{storm_home}/lib/storm-elasticsearch-%{storm_version}.jar

%files eventhubs
%defattr(-,%{storm_user},%{storm_group})
%{storm_home}/external/storm-eventhubs/*


%post eventhubs
ln -s %{storm_home}/external/storm-eventhubs/storm-eventhubs-%{storm_version}.jar \
	%{storm_home}/lib/storm-eventhubs-%{storm_version}.jar
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/storm-eventhubs-%{storm_version}.jar

%postun eventhubs
rm -f %{storm_home}/lib/storm-eventhubs-%{storm_version}.jar

%files hive
%defattr(-,%{storm_user},%{storm_group})
%{storm_home}/external/storm-hive/*


%post hive
ln -s %{storm_home}/external/storm-hive/storm-hive-%{storm_version}.jar \
	%{storm_home}/lib/storm-hive-%{storm_version}.jar
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/storm-hive-%{storm_version}.jar

%postun hive
rm -f %{storm_home}/lib/storm-hive-%{storm_version}.jar

%files jdbc
%defattr(-,%{storm_user},%{storm_group})
%{storm_home}/external/storm-jdbc/*


%post jdbc
ln -s %{storm_home}/external/storm-jdbc/storm-jdbc-%{storm_version}.jar \
	%{storm_home}/lib/storm-jdbc-%{storm_version}.jar
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/storm-jdbc-%{storm_version}.jar

%postun jdbc
rm -f %{storm_home}/lib/storm-jdbc-%{storm_version}.jar

%files kafka-client
%defattr(-,%{storm_user},%{storm_group})
%{storm_home}/external/storm-kafka-client/*


%post kafka-client
ln -s %{storm_home}/external/storm-kafka-client/storm-kafka-client-%{storm_version}.jar \
	%{storm_home}/lib/storm-kafka-client-%{storm_version}.jar
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/storm-kafka-client-%{storm_version}.jar

%postun kafka-client
rm -f %{storm_home}/lib/storm-kafka-client-%{storm_version}.jar

%files kafka
%defattr(-,%{storm_user},%{storm_group})
%{storm_home}/external/storm-kafka/*

%post kafka
ln -s %{storm_home}/external/storm-kafka/storm-kafka-%{storm_version}.jar \
	%{storm_home}/lib/storm-kafka-%{storm_version}.jar
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/storm-kafka-%{storm_version}.jar

%postun kafka
rm -f %{storm_home}/lib/storm-kafka-%{storm_version}.jar

%files hdfs
%defattr(-,%{storm_user},%{storm_group})
%{storm_home}/external/storm-hdfs/*

%post hdfs
ln -s %{storm_home}/external/storm-hdfs/storm-hdfs-%{storm_version}.jar \
	%{storm_home}/lib/storm-hdfs-%{storm_version}.jar
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/storm-hdfs-%{storm_version}.jar

%postun hdfs
rm -f %{storm_home}/lib/storm-hdfs-%{storm_version}.jar

%files hbase
%defattr(-,%{storm_user},%{storm_group})
%{storm_home}/external/storm-hbase/*

%post hbase
ln -s %{storm_home}/external/storm-hbase/storm-hbase-%{storm_version}.jar \
	%{storm_home}/lib/storm-hbase-%{storm_version}.jar
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/storm-hbase-%{storm_version}.jar

%postun hbase
rm -f %{storm_home}/lib/storm-hbase-%{storm_version}.jar
  
%files mongodb
%defattr(-,%{storm_user},%{storm_group})
%{storm_home}/external/storm-mongodb/*


%post mongodb
ln -s %{storm_home}/external/storm-mongodb/storm-mongodb-%{storm_version}.jar \
	%{storm_home}/lib/storm-mongodb-%{storm_version}.jar
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/storm-mongodb-%{storm_version}.jar

%postun mongodb
rm -f %{storm_home}/lib/storm-mongodb-%{storm_version}.jar

%files mqtt
%defattr(-,%{storm_user},%{storm_group})
%{storm_home}/external/storm-mqtt/*


%post mqtt
ln -s %{storm_home}/external/storm-mqtt/storm-mqtt-%{storm_version}.jar \
	%{storm_home}/lib/storm-mqtt-%{storm_version}.jar
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/storm-mqtt-%{storm_version}.jar

%postun mqtt
rm -f %{storm_home}/lib/storm-mqtt-%{storm_version}.jar

%files redis
%defattr(-,%{storm_user},%{storm_group})
%{storm_home}/external/storm-redis/*


%post redis
ln -s %{storm_home}/external/storm-redis/storm-redis-%{storm_version}.jar \
	%{storm_home}/lib/storm-redis-%{storm_version}.jar
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/storm-redis-%{storm_version}.jar

%postun redis
rm -f %{storm_home}/lib/storm-redis-%{storm_version}.jar

%files solr
%defattr(-,%{storm_user},%{storm_group})
%{storm_home}/external/storm-solr/*


%post solr
ln -s %{storm_home}/external/storm-solr/storm-solr-%{storm_version}.jar \
	%{storm_home}/lib/storm-solr-%{storm_version}.jar
chown -h %{storm_user}:%{storm_group} %{storm_home}/lib/storm-solr-%{storm_version}.jar

%postun solr
rm -f %{storm_home}/lib/storm-solr-%{storm_version}.jar

%changelog
* Fri Nov 13 2015 Juan Carlos Fernandez <jcfernandez@keedio.com> - 0.9.4
- Service scripts refact
* Mon Mar 30 2015 Luca Rosellini <lrosellini@keedio.com> - 0.9.4
- Version bump to 0.9.4
* Mon Jul 31 2013 Nathan Milford <nathan@milford.io> - 0.9.0-wip16-4
- Removed postun macro. Caused scriptlet error on uninstall.
* Mon Jul 31 2013 Nathan Milford <nathan@milford.io> - 0.9.0-wip16-3
- Bumped RPM release version.
- Merged DRPC init script and package declaration by Vitaliy Fuks <https://github.com/vitaliyf>
- Merged init script additions by Daniel Damiani <https://github.com/ddamiani>
* Mon May 13 2013 Nathan Milford <nathan@milford.io> - 0.9.0-wip16
- Storm 0.9.0-wip16
* Wed Aug 08 2012 Nathan Milford <nathan@milford.io> - 0.8.0
- Storm 0.8.0
