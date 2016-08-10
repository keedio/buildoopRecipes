# Avoid unnecessary debug-information (native code)
%define		debug_package %{nil}

# Avoid CentOS 5/6 extras processes on contents (especially brp-java-repack-jars)
%define __os_install_post %{nil}

# Se definen los directorios de trabajo para la instalacion
%define etc_jmxtrans /etc/jmxtrans/config.dist
%define bin_jmxtrans /usr/lib/jmxtrans
%define lib_jmxtrans /usr/lib/jmxtrans/lib
%define log_jmxtrans /var/log/jmxtrans

# Estas definiciones son mias para hacer independiente el SPEC
# JAVI: flume_base_version -> esta definida en bigtop.mk
# apache-flume-1.5.2-src.tar.gz
#
%define jmxtrans_base_version v246
%define jmxtrans_release 1.4.0%{?dist}

Name: jmxtrans
Version: %{jmxtrans_base_version}
Release: %{jmxtrans_release}
Summary: JMX Transformer - more than meets the eye
Group: Development/Libraries
URL: https://github.com/jmxtrans/jmxtrans/
Vendor: Keedio 
Packager: Rodrigo Olmo <rolmo@keedio.org>
License: APL2
BuildArch:  noarch

Source0: %{name}.git.tar.gz
Source1: jmxtrans.init
Source2: systemd
Source3: rpm-build-stage
Source4: install_jmxtrans.sh
Source5: KafkaMetrics.json
BuildRoot: %{_topdir}/INSTALL/%{name}-%{version}

Requires(pre):   /usr/sbin/groupadd
Requires(pre):   /usr/sbin/useradd
Patch0: jmxtranspatch-1.0.patch
Patch1: jmxtranspatch-1.1.patch

%define xuser       jmxtrans

%define xappdir         %{bin_jmxtrans}
%define xlibdir         %{lib_jmxtrans}
%define xlogdir         %{log_jmxtrans}
%define xconf           %{etc_jmxtrans}

%define _systemdir        /lib/systemd/system
%define _initrddir        %{_sysconfdir}/init.d

%description
jmxtrans is very powerful tool which reads json configuration files of servers/ports and jmx domains - attributes - types.
Then outputs the data in whatever format you want via special 'Writer' objects which you can code up yourself.
It does this with a very efficient engine design that will scale to querying thousands of machines.

%prep
%setup -q -n %{name}.git
%patch0 -p1
%patch1 -p1

%build
bash %{SOURCE3}

%install
# Prep the install location.
#rm -rf   %{buildroot}
#mkdir -p %{buildroot}%{_bindir}
#mkdir -p %{buildroot}%{xappdir}
#mkdir -p %{buildroot}%{xappdir}/lib
#mkdir -p %{buildroot}%{xlibdir}
#mkdir -p %{buildroot}%{xlogdir}
#mkdir -p %{buildroot}%{_initrddir}
#mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
#mkdir -p %{buildroot}%{_systemdir}

# remove source (unneeded here) 
#cp  *.* %{buildroot}%{xappdir}
#cp  lib/* %{buildroot}%{xappdir}/lib
#cp  target/jmxtrans-1.0.0-all.jar %{buildroot}%{xappdir}
#cp  %{SOURCE1} %{buildroot}%{_initrddir}/jmxtrans

# copy yaml2jmxtrans.py to bin
#cp tools/yaml2jmxtrans.py %{buildroot}%{_bindir}
#chmod 755 %{buildroot}%{_bindir}/yaml2jmxtrans.py

# copy doc (if existing)
#cp -rf doc %{buildroot}%{xappdir}

# Setup Systemd
#cp %{SOURCE2} %{buildroot}%{_systemdir}/jmxtrans.service

# ensure shell scripts are executable

#chmod 755 %{buildroot}%{xappdir}/*.sh

bash %{SOURCE4}\
	--build-dir=$PWD \
     	--prefix=%{buildroot} \
	--source-dir=$RPM_SOURCE_DIR

%clean
#rm -rf %{buildroot}

%pre
%if 0%{?suse_version} > 1140
%service_add_pre jmxtrans.service
%endif
/usr/sbin/useradd -c "JMXTrans" \
        -s /sbin/nologin -r -d %{xappdir} %{xuser} 2> /dev/null || :

%post
%if 0%{?suse_version} > 1140
%service_add_post jmxtrans.service
%endif
if [ $1 = 1 ]; then
  /sbin/chkconfig --add jmxtrans

  # get number of cores so we can set number of GC threads
  CPU_CORES=$(cat /proc/cpuinfo | grep processor | wc -l)
  NEW_RATIO=8

  # defaults for JVM
  HEAP_SIZE="512"
  HEAP_NUMBER=$(echo $HEAP_SIZE|sed 's/[a-zA-Z]//g')
  NEW_SIZE=$(expr $HEAP_SIZE / $NEW_RATIO)

  # populate sysconf file
  echo "# configuration file for package jmxtrans" > %{etc_jmxtrans}/jmxtrans.config
  echo "export JAR_FILE=\"/usr/lib/jmxtrans/jmxtrans-1.0.0-all.jar\"" >> %{etc_jmxtrans}/jmxtrans.config
  echo "export LOG_DIR=\"/var/log/jmxtrans\"" >> %{etc_jmxtrans}/jmxtrans.config
  echo "export SECONDS_BETWEEN_RUNS=60" >> %{etc_jmxtrans}/jmxtrans.config
  echo "export JSON_DIR=\"%{etc_jmxtrans}\"" >> %{etc_jmxtrans}/jmxtrans.config
  echo "export HEAP_SIZE=${HEAP_SIZE}" >> %{etc_jmxtrans}/jmxtrans.config
  echo "export NEW_SIZE=${NEW_SIZE}" >> %{etc_jmxtrans}/jmxtrans.config
  echo "export CPU_CORES=${CPU_CORES}" >> %{etc_jmxtrans}/jmxtrans.config
  echo "export NEW_RATIO=${NEW_RATIO}" >> %{etc_jmxtrans}/jmxtrans.config
  echo "#export LOG_LEVEL=debug" >> %{etc_jmxtrans}/jmxtrans.config
  echo "export PIDFILE=/var/run/jmxtrans.pid" >> %{etc_jmxtrans}/jmxtrans.config

fi
ln -s /etc/jmxtrans/config.dist /etc/jmxtrans/config

%preun
%if 0%{?suse_version} > 1140
%service_del_preun jmxtrans.service
%endif
if [ $1 = 0 ]; then
  /sbin/service jmxtrans stop > /dev/null 2>&1
  /sbin/chkconfig --del jmxtrans
  /usr/sbin/userdel %{xuser} 2> /dev/null
  rm -rf  %{xconf}
fi

%posttrans
/sbin/service jmxtrans condrestart >/dev/null 2>&1 || :

%postun
%if 0%{?suse_version} > 1140
%service_del_postun jmxtrans.service
%endif


%files
%defattr(-,root,root)
%{bin_jmxtrans}/*
%attr(0755, root,root)  %{_initrddir}/jmxtrans
%attr(0644,root,root)   %{_systemdir}/jmxtrans.service
%config(noreplace)      %{etc_jmxtrans}
%config(noreplace)      %{xlibdir}
%attr(0755,%{xuser}, %{xuser}) %{xlogdir}
%{xappdir}/*
%doc %{xappdir}/README.html
#%doc %{xappdir}/doc


%changelog
* Sat Mar 23 2013 Henri Gomez <henri.gomez@gmail.com> - 242-1
- jmxtrans v242 introduce a Graphite pool to keep connections low

* Thu Mar 21 2013 Henri Gomez <henri.gomez@gmail.com> - 241-2
- Added yaml2jmxtrans.py and docs

* Thu Mar 21 2013 Henri Gomez <henri.gomez@gmail.com> - 241-1
- Fixed LocalMBean Server issue.

* Wed Jul 19 2011 Henri Gomez <henri.gomez@gmail.com> - 223-1
- Initial RPM package to be used and build with ci systems.
