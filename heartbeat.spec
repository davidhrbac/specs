%define           ENABLE_SNMP_SUBAGENT 0
%define           ENABLE_MGMT 1
%define           uid 24
%define           gname haclient
%define           uname hacluster
Summary:          Heartbeat subsystem for High-Availability Linux
Name:             heartbeat
Version:          2.1.4
Release:          6%{?dist}
License:          GPLv2 and LGPLv2+
URL:              http://linux-ha.org/
Group:            System Environment/Daemons
Source0:          http://hg.linux-ha.org/lha-2.1/archive/STABLE-%{version}.tar.bz2
Patch0:           heartbeat-fedora-pam.patch
Patch1:           heartbeat-2.1.4-default-init.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
BuildRequires:    glib2-devel
BuildRequires:    iputils
BuildRequires:    libnet-devel
BuildRequires:    libtool-ltdl-devel
BuildRequires:    net-snmp-devel 
BuildRequires:    bzip2-devel 
BuildRequires:    ncurses-devel
BuildRequires:    openssl-devel
BuildRequires:    libtool
BuildRequires:    libxml2-devel
BuildRequires:    gettext
BuildRequires:    bison
BuildRequires:    flex
%if %{ENABLE_MGMT}
BuildRequires:    gnutls-devel 
BuildRequires:    pam-devel
BuildRequires:    python-devel
BuildRequires:    swig
%endif
Requires:         ldirectord = %{version}-%{release}
Requires:	  PyXML
Requires(pre):	  shadow-utils
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/chkconfig
%if %{ENABLE_MGMT}
Requires:         gettext
%endif

%description
heartbeat is a basic high-availability subsystem for Linux-HA.
It will run scripts at initialization, and when machines go up or down.
This version will also perform IP address takeover using gratuitous ARPs.
It supports "n-node" clusters with significant capabilities for managing
resources and dependencies.

In addition it continues to support the older release 1 style of
2-node clustering.

It implements the following kinds of heartbeats:
        - Serial ports
        - UDP/IP multicast (ethernet, etc)
        - UDP/IP broadcast (ethernet, etc)
        - UDP/IP heartbeats
        - "ping" heartbeats (for routers, switches, etc.)
           (to be used for breaking ties in 2-node systems)

%package ldirectord
Summary:          Monitor daemon for maintaining high availability resources
Group:            System Environment/Daemons
Requires:         ipvsadm
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/chkconfig
Provides: ldirectord = %{version}-%{release}
Obsoletes: ldirectord < 2.1.4-5

%description ldirectord
ldirectord is a stand-alone daemon to monitor services of real 
for virtual services provided by The Linux Virtual Server
(http://www.linuxvirtualserver.org/). It is simple to install 
and works with the heartbeat code (http://www.linux-ha.org/).

%package stonith
Requires:       net-snmp-libs
Summary:        Provides an interface to Shoot The Other Node In The Head 
Group:          System Environment/Daemons
Provides: stonith = %{version}-%{release}
Obsoletes: stonith < 2.1.4-5

%description stonith
The STONITH module (a.k.a. STONITH) provides an extensible interface
for remotely powering down a node in the cluster.  The idea is quite simple:
When the software running on one machine wants to make sure another
machine in the cluster is not using a resource, pull the plug on the other 
machine. It's simple and reliable, albeit admittedly brutal.

%package pils
Summary:        Provides a general plugin and interface loading library
Group:          System Environment/Daemons
Provides: pils = %{version}-%{release}
Obsoletes: pils < 2.1.4-5

%description pils
PILS is an generalized and portable open source Plugin and Interface Loading 
System. PILS was developed as part of the Open Cluster Framework reference 
implementation, and is designed to be directly usable by a wide variety of 
other applications.
PILS manages both plugins (loadable objects), and the interfaces these plugins 
implement. PILS is designed to support any number of plugins implementing any 
number of interfaces.

%package devel 
Summary:        Heartbeat development package 
Group:          System Environment/Daemons
Requires:       heartbeat = %{version}-%{release}

%description devel
Heartbeat development package

%package gui
Summary: Provides a gui interface to manage heartbeat clusters
Group: System Environment/Daemons
Requires: heartbeat = %{version}-%{release}
Requires: PyXML
Requires: pygtk2 >= 2.4

%description gui
GUI client for Heartbeat clusters

%prep
%setup -q -n Heartbeat-STABLE-2-1-STABLE-%{version}
%patch0 -p1
%patch1 -p1
 
%build
./bootstrap
# disable-fatal-warnings flag used to disable gcc4.x warnings of 'difference in signedness'
CFLAGS=${RPM_OPT_FLAGS} \
%configure \
  --with-ocf-root=%{_datadir}/ocf \
  --disable-fatal-warnings \
  --disable-static \
%if %{ENABLE_MGMT}
  --enable-mgmt
%else
  --disable-mgmt
%endif

# get rid of rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# cleanup
[ -d $RPM_BUILD_ROOT/usr/man ] && rm -rf $RPM_BUILD_ROOT/usr/man
[ -d $RPM_BUILD_ROOT/usr/share/libtool ] && rm -rf $RPM_BUILD_ROOT/usr/share/libtool
find $RPM_BUILD_ROOT -type f -name *.la -exec rm -f {} ';'

sed -i -e '1i# -*-Shell-script-*-' $RPM_BUILD_ROOT/%{_libdir}/heartbeat/ocf-shellfuncs 
sed -i -e '1i# -*-Shell-script-*-' $RPM_BUILD_ROOT/%{_sysconfdir}/ha.d/shellfuncs
chmod -x $RPM_BUILD_ROOT/%{_libdir}/heartbeat/ocf-shellfuncs
chmod -x $RPM_BUILD_ROOT/%{_sysconfdir}/ha.d/shellfuncs
chmod -x $RPM_BUILD_ROOT/%{_libdir}/heartbeat-gui/pymgmt.py

# fix some wrong line endings issues
sed -i 's/\r//' $RPM_BUILD_ROOT/%{_datadir}/ocf/resource.d/heartbeat/SAPDatabase
sed -i 's/\r//' $RPM_BUILD_ROOT/%{_datadir}/ocf/resource.d/heartbeat/SAPInstance

%find_lang haclient

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group %{gname} >/dev/null || groupadd -r %{gname}
getent passwd %{uname} >/dev/null || \
useradd -r -g %{gname} -d /var/lib/heartbeat/cores/hacluster -s /sbin/nologin \
-c "heartbeat user" %{uname}
exit 0

%post
/sbin/ldconfig
/sbin/chkconfig --add heartbeat

%postun -p /sbin/ldconfig

%preun
if [ $1 = 0 ] ; then
    /sbin/service heartbeat stop
    /sbin/chkconfig --del heartbeat
fi

/sbin/ldconfig

%post ldirectord
/sbin/chkconfig --add ldirectord

%postun ldirectord -p /sbin/ldconfig

%preun ldirectord
/sbin/chkconfig --del ldirectord

%post stonith -p /sbin/ldconfig

%postun stonith -p /sbin/ldconfig

%post pils -p /sbin/ldconfig

%postun pils -p /sbin/ldconfig

%files -f haclient.lang
%doc %{_datadir}/doc/%{name}-%{version}
%defattr(-,root,root,-)
%dir %{_sysconfdir}/ha.d
%{_sysconfdir}/ha.d/harc
%config(noreplace) %{_sysconfdir}/ha.d/shellfuncs
%{_sysconfdir}/ha.d/rc.d
%config(noreplace) %{_sysconfdir}/ha.d/README.config
%{_libdir}/heartbeat
%{_libdir}/libapphb.so.*
%{_libdir}/libccmclient.so.*
%{_libdir}/libcib.so.*
%{_libdir}/libclm.so.*
%{_libdir}/libcrmcommon.so.*
%{_libdir}/libtransitioner.so.*
%{_libdir}/libhbclient.so.*
%{_libdir}/liblrm.so.*
%{_libdir}/libpengine.so.*
%{_libdir}/libplumb.so.*
%{_libdir}/libplumbgpl.so.*
%{_libdir}/librecoverymgr.so.*
%{_libdir}/libstonithd.so.*
%{_libdir}/libpe_rules.so.*
%{_libdir}/libpe_status.so.*
%{_datadir}/heartbeat/
%{_datadir}/ocf/
%{_sysconfdir}/ha.d/resource.d/
%exclude %{_sysconfdir}/ha.d/resource.d/ldirectord
%{_sysconfdir}/init.d/heartbeat
%config(noreplace) %{_sysconfdir}/logrotate.d/heartbeat
%dir %{_var}/lib/heartbeat
%dir %{_var}/lib/heartbeat/cores
%dir %attr (0755, root, root) %{_var}/lib/heartbeat/cores/root
%dir %attr (0755, nobody, nobody) %{_var}/lib/heartbeat/cores/nobody
%dir %attr (0755, hacluster, haclient) %{_var}/lib/heartbeat/cores/hacluster
%dir %{_var}/run/heartbeat
%attr (2755, hacluster, haclient) %{_bindir}/cl_status
%{_bindir}/cl_respawn
%{_sbindir}/ciblint
%{_sbindir}/hb_report
%{_sbindir}/crmadmin
%{_sbindir}/cibadmin
%{_sbindir}/ccm_tool
%{_sbindir}/crm_diff
%{_sbindir}/crm_uuid
%{_sbindir}/crm_mon
%{_sbindir}/crm_sh
%{_sbindir}/iso8601
%{_sbindir}/crm_master
%{_sbindir}/crm_standby
%{_sbindir}/crm_attribute
%{_sbindir}/crm_resource
%{_sbindir}/crm_verify
%{_sbindir}/attrd_updater
%{_sbindir}/crm_failcount
%{_sbindir}/ocf-tester
%{_sbindir}/ha_logger
%{_sbindir}/ptest
%dir %attr (755, hacluster, haclient) %{_var}/run/heartbeat/ccm
%dir %attr (755, hacluster, haclient) %{_var}/run/heartbeat/crm
%dir %attr (755, hacluster, haclient) %{_var}/lib/heartbeat/crm
%dir %attr (755, hacluster, haclient) %{_var}/lib/heartbeat/pengine
%{_mandir}/man1/cl_status.1*
%{_mandir}/man1/ha_logger.1*
%{_mandir}/man1/hb_standby.1*
%{_mandir}/man1/hb_takeover.1*
%{_mandir}/man1/hb_addnode.1*
%{_mandir}/man1/hb_delnode.1*
%{_mandir}/man8/heartbeat.8*
%{_mandir}/man8/apphbd.8*
%{_mandir}/man8/ha_logd.8*
%{_mandir}/man8/cibadmin.8.gz
%{_mandir}/man8/crm_resource.8.gz
%if %{ENABLE_SNMP_SUBAGENT}
/LINUX-HA-MIB.mib
%endif
%if %{ENABLE_MGMT}
%{_libdir}/libhbmgmt.so.*
%{_libdir}/libhbmgmtclient.so.*
%{_libdir}/libhbmgmtcommon.so.*
%{_libdir}/libhbmgmttls.so.*
%config(noreplace) %{_sysconfdir}/pam.d/hbmgmtd
%endif

%files ldirectord
%doc doc/COPYING 
%doc doc/README
%doc ldirectord/ldirectord.cf
%defattr(-,root,root,-)
%{_sbindir}/ldirectord
%config(noreplace) %{_sysconfdir}/logrotate.d/ldirectord
%{_sysconfdir}/init.d/ldirectord
%{_sysconfdir}/ha.d/resource.d/ldirectord
%{_mandir}/man8/ldirectord.8*

%files stonith
%doc doc/COPYING 
%doc doc/README
%defattr(-,root,root,-)
%{_libdir}/libstonith.so.*
%{_libdir}/stonith/
%{_sbindir}/stonith
%{_sbindir}/meatclient
%{_mandir}/man8/stonith.8*
%{_mandir}/man8/meatclient.8*

%files pils
%doc doc/COPYING 
%doc doc/README
%defattr(-,root,root,-)
/usr/include/pils
%{_libdir}/libpils.*
%{_libdir}/pils/

%files devel
%doc %{_datadir}/doc/%{name}-%{version}
%defattr(-,root,root,-)
%{_includedir}/heartbeat/
%{_includedir}/clplumbing/
%{_includedir}/saf/
%{_includedir}/ocf/
%{_includedir}/stonith/
%{_includedir}/pils/
%{_libdir}/*.so

%files gui
%defattr(-,root,root)
%{_libdir}/heartbeat-gui
%{_datadir}/heartbeat-gui
%{_bindir}/hb_gui

%changelog
* Tue Feb 24 2009 Kevin Fenzi <kevin@tummy.com> - 2.1.4-6
- Remove symlink thats no longer needed. 

* Mon Feb 23 2009 Kevin Fenzi <kevin@tummy.com> - 2.1.4-5
- Remove fedora-usermgmt
- Change subpackage names to match all the other heartbeat packages out there.

* Sat Jan 17 2009 Kevin Fenzi <kevin@tummy.com> - 2.1.4-4
- Main package shouldn't require pygtk2 (#480157)

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> - 2.1.4-3
- rebuild with new openssl

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.1.4-2
- Rebuild for Python 2.6

* Mon Dec 01 2008 Kevin Fenzi <kevin@tummy.com> - 2.1.4-1
- Update to 2.1.4
- Drop upstreamed patch
- Add patch to disable init script by default (#441286)

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.1.3-4
- Rebuild for Python 2.6

* Tue Oct 21 2008 Lon Hohberger <lhh@redhat.com> - 2.1.3-3
- Fix requires line to include PyXML (#467807)

* Wed Jun 25 2008 Tomas Mraz <tmraz@redhat.com> - 2.1.3-2
- rebuild with new gnutls

* Mon Feb 25 2008 Kevin Fenzi <kevin@tummy.com> - 2.1.3-1
- Update to 2.1.3
- Add management GUI
- Drop upstreamed patches
- Add patch for IPAddr (bz #434653)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.1.2-4
- Autorebuild for GCC 4.3

* Fri Dec 07 2007 Release Engineering <rel-eng at fedoraproject dot org> - 2.1.2-3
- Rebuild for deps

* Tue Aug 29 2007 Kevin Fenzi <kevin@tummy.com> - 2.1.2-2
- Update sources

* Tue Aug 29 2007 Kevin Fenzi <kevin@tummy.com> - 2.1.2-1
- Upgrade to 2.1.2
- Update license tag for new guidelines. 
- Patch open function issues. 

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.0.8-4
- Rebuild for selinux ppc32 issue.

* Tue Jun 26 2007 Kevin Fenzi <kevin@tummy.com> - 2.0.8-3
- Add openssl-devel BuildRequires
- Remove restart from postun (bz #223949)
- Fix up Requires (bz #245704)
- Remove duplicate libraries in subpackages (bz #245704)
- Add smp_mflags
- Fix typo in stonith subpackage description
- Simplify clean section. 
- Use find_lang macro
- Fix some multilib issues with ocf dir (bz #228165)
- Kill rpath
- Add ldconfig to postun

* Fri Feb  9 2007 Joost Soeterbroek <joost.soeterbroek@gmail.com> - 2.0.8-2
- change condrestart -> restart (bz #223949)

* Sun Jan 21 2007 Joost Soeterbroek <joost.soeterbroek@gmail.com> - 2.0.8-1
- upstream version 2.0.8
- fix cl_status commands fail (bz #219765)

* Thu Nov 30 2006 Joost Soeterbroek <joost.soeterbroek@gmail.com> - 2.0.7-5
- add Requires net-snmp-libs to stonith , add BuildReqs net-snmp-devel >= 5.4

* Tue Nov 28 2006 Joost Soeterbroek <joost.soeterbroek@gmail.com> - 2.0.7-4
- rebuild for updated net-snmp, soname change

* Sun Oct 29 2006 Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.7-3
- fix preun, postun to check for upgrade (#212133)

* Wed Aug 30 2006 Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.7-2
- rebuild for Fedora Extras 6

* Wed Aug 16 2006  Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.7-1
- upstream version 2.0.7

* Sat Jul 15 2006  Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.6-2
- added BuildReqs: ncurses-devel

* Fri Jul 14 2006  Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.6-1
- upstream version 2.0.6

* Fri Jun 16 2006  Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.5-2
- bump for gnutls change in devel

* Thu Apr 27 2006  Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.5-1
- upstream version 2.0.5
- removed patch2 - ownership of /heartbeat/crm/cib.xml is no longer
  set in cts/CM_LinuxHAv2.py.in

* Wed Mar 29 2006  Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.4-2
- Version 2.0.4

* Wed Mar  1 2006  Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.3-9
- changed user creation
- added patch2 heartbeat-2.0.3-fedora-ccmuser.patch  

* Wed Mar  1 2006  Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.3-8
- specifically excluded ldirectord symlink from heartbeat package
- removed user and group deletion in postun
- renamed subpackages ldirectord, pils and stonith to lose prefix heartbeat
  by using -n

* Tue Feb 28 2006  Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.3-7
- fixed more rpmlint errors and warnings

* Sat Feb 25 2006  Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.3-6
- fixed number of rpmlint warnings and errors (still ignores some..)
- generate 'predictable' uid and gid with fedora-usermgmt to use with 
  configure flag -with-ccmuser-id and groupadd, useradd
- added Buildreq's: libtool-ltdl-devel, fedora-usermgmt-setup
  net-snmp-devel, bzip2-devel 
- removed *.so duplication in heartbeat and heartbeat-devel
- changed file sections

* Fri Feb 24 2006  Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.3-5
- useradd with fedora-usermgmt
- added *.so file to -devel sub-package

* Sat Feb 18 2006  Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.3-4
- removed all perl requires; should be picked up by rpmbuild automagically
- changed system user creation hacluster part to use baseid:
  (http://fedoraproject.org/wiki/Packaging/UserCreation)

* Thu Feb 16 2006  Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.3-3
- removed Requires: python and gnutls
- changed _libdir/ocf -> _prefix/lib/ocf
- reversed subpackages depend on basepackage
- removed Req swig (kept BuildReq)
- added Req pygtk2

* Wed Feb 15 2006  Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.3-2
- fixes for various rpmlint errors and warnings 
- fixed setup -q
- make subpackages depend on basepackage, not reverse
- clean buildroot at beginning of install
- replaced a number of hardcoded paths with RPM macros
- Changed Group from Networking/Daemons to System Environment/Daemons
- enable mgmt option

* Sun Feb 12 2006  Joost Soeterbroek <fedora@soeterbroek.com> - 2.0.3-1
- rebuilt for Fedora Extras

* Fri Feb 10 2006  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 2.0.3 - Bug fixes and significant new features.
  + Management Daemon/Library and GUI client
    + provide a management library for manamgement daemon and CIM provider
    + provide a management daemon and a basic GUI management tool
  + CIM enablement
    + CIM (Common Information Model) enablement - works with
      sblim-sfcb, OpenWBEM, and Pegasus CIMOMs
    - not yet compiled into our binary RPMs because of dependencies
  + CRM (Cluster Resource Manager) General
    + All shutdowns go via the PE/TE - preserves inter-resource ordering
    + Support for future changes to the CIB (depreciation of cib_fragment)
    + Overhaul of IPC and HA channel callback logic
    + Many improvments to the quality and quantity (reduced) of logging
  + CRMd
    + Timerless elections - when everyone has voted we're done
    + Use the replace notification from the CIB to re-update our copy with 
      our view of our peers.
    + Reliably detect if the LRM connection is still active.
    + Elections
      + newer versions defer to older ones in DC elections 
        (opposite of current behavior)
      + this means that only once the complete cluster has been upgraded will
        we start acting like the new version and accept new config options
      + it also means newer PE's and TE's (the most complex pieces) don't need
        "act like the old version" options and can rely on all slaves being at
        least as up-to-date as they are
      + people can run mixed clusters as long as they want
        (until they want the new PE features)
      + new DCs only update the version number in the CIB if they have a 
        higher value
      + nodes that start and have a lower version than that stored in the CIB
        shut themselves down (the CRM part anyway)
      + this prevents an admin from introducing old nodes back into an upgraded
        cluster. It probably doesn't fully understand the config and may not
        support the actions the PE/TE requires.
  + CIB (Common Information Base daemon)
    + Make sure "query only" connections cant modify the CIB
    + Periodically dump some stats about what the CIB has been doing.
    + Verify there are no memory leaks
    + Performance enhancements
    + Prevent a single CIB client from blocking everyone else
    + Clients Can be notified of full CIB replacements
    + record_config_changes option in ha.cf for those worried about 
      the amount of logging.  Defaults to "on".
    + suppress_cib_writes CIB option replaced with in enable_config_writes ha.cf 
      (enable_config_writes to be removed in 2.0.4)
    + Never write the status section to disk
    + Check permissions for the on-disk CIB at startup
    + Dont trash unreadable on-disk CIBs
    + Fix for updates made against the whole CIB (not just one section) 
  + PEngine (Policy Engine)
    + Many improvements to the handling of resource groups
    + Support "anonymous" clones
    + Fix stonith ordering
    + Order DC shutdowns after everyone else's
    + Support short resource names (for group and clone resources)
    + The ordering and colocation of grouped resources is now optional
    + Support probing new nodes for active resources.
    + All "probe" actions are controlled by the PE.
      + No resource may be started until the probing is complete.
      + Do not probe for resources we know to be active on unprobed nodes
    + When looking for monitor ops, only mark it optional if it was already
      active on the node we're interested in.
    + Detect changes to class/type/provider/parameters and force a restart
      of the resource
    + New record_pengine_inputs option in ha.cf for those worried about 
      the amount of logging.  Defaults to "on".
    + Differentiate between config and processing errors
      + reduces the frequency that we need to log the complete CIB
    + Make notify for master/slave work
    + New CIB option: stop_orphan_actions (boolean)
      If a resource is no longer defined, we can optionally stop it
    + New CIB option: stop_orphan_actions (boolean)
      If a monitor op for a given interval is no longer defined, we can
      optionally stop it
    + Add support for time and phase-of-the-moon based constraints
    + Improved failure handling: avoiding false positives
    + Always create orphaned resources - so they show up in crm_mon
    + Do not require sequential clone numbers starting at 0
  + TEngine (transition engine)
    + Detect old stonith ops
  + CLIs (Command Line interfaces)
    + Create a --one-shot option for crm_mon
    + Switch a number of CLI tools to use the new syncronous connections
    + Log errors to stderr where they will be seen and therefore useful
    + Support migration and un-migration of resources and resource groups
    + Create crm_verify for checking configuration validity
    + Simplify the passing of XML to cibadmin
  + Known open bugs worth mentioning:
    + 1075, 1080, 1081, 1084, 1085, 1064, 1069, 756, 984
    + 1050, 1082, 1037, 1079
    
* Thu Sep 22 2005  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 2.0.2 - small bug fix only release
  + Fixed a bug in ping directive - it works again
  + Added a check to BasicSanityCheck to check ping and ping_group directives
  + fixed cl_status nodestatus to return 0 if a node has status "ping"
  + fixed a memory leak in the CRM's LRM interface code
  + fixed code which deterimines which version of the CRM becomes
    the DC when basic CIB schema versions differ.  It now prefers
    the older version to be DC instead of the newer version.

* Wed Sep 14 2005  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 2.0.1 - 
  + Communication Layer
    + netstring encoding format is changed to be more efficient
    + add compression capability for big messages
  + Add man pages for hb_standby/hb_takeover	
  + The assert triggered by 2.0.0 has been fixed
  + CIB can now contain XML comments and/or be in DOS format	
  + Includes implementation of the ISO8601 date format
  + New CLI tools for changing cluster preferences, node attributes 
    and node standby
  + Improved recovery and placement of group resources
  + Detection of failed nodes by the Policy Engine is fixed
  + New Policy Engine features 
    http://www.linux-ha.org/ClusterResourceManager/DTD1.0/Annotated :
      sections 1.5.[8,9,10,12]
    + Constraints and instance attributes can now be active conditionally
    + Rules can now contain other rules
    + Date/Time based expressions are supported
    + Cloned resources can now optionally be notified before and after
      any of its peers are stopped or started.
    + The cluster can re-evaluate the configuration automatically after
      a defined interval of idleness
  + Removed a flow control message which was very annoying when operating
    in a mixed 1.x/2.x environment
  -- Known Bugs :-( --
    - Bug 859 - FSA took too long to complete action - fully recovered from
    - Bug 882 - IPC channel not connected during shutdown - harmless
    - Bug 879 - Failed actions cause extra election - harmless
 Each of these occurs about once or twice in 5000 test iterations
       - This is probably > 10K failovers
    - rsc_location constraints cannot have rules that contain other rules
      (fixed in CVS after release) 
* Fri Jul 29 2005  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 2.0.0 - First stable release of the next generation of the Linux-HA project
  + Basic Characteristics described here:
	http://linux-ha.org/FactSheetv2
  + Core infrastructure improvments:
    + Messaging (message acknowledging and flow control)
    + Logging   (logging daemon)
  + Release 1.x style (2-node) clusters fully supported
  + Multi-node support (so far up to 16-node clusters tested)
	See http://linux-ha.org/GettingStartedV2 for more information
  + New components:
    + Cluster Information Base    (replicated resource configuration)
    + Cluster Resource Manager    (supporting 1->N nodes)
    + Modular Policy Engine       (controlling resource placement)
    + Local Resource Manager      (policy free, not cluster aware)
    + Stonith Daemon              (stand-alone fencing  subsytem)
  + Support for OCF and LSB resource agents
  + Support for composite resource types (groups, clones)
  + Support for a rich set of resource location and ordering constraints
  + Conversion tool for existing haresources
  + Resources monitored by request
  + Resource "maintenance" mode
  + Several failback, failure and "No Quorum" behaviours to choose from
        (global defaults and per action or resource)
  + Sample cluster state and configuration monitoring tools

  Known issues in 2.0.0:
    - Under some rare circumstances the cluster manager will time out
      while stabilizing a new cluster state.  This appears to be
	otherwise harmless - the cluster is actually fine.
	http://www.osdl.org/developer_bugzilla/show_bug.cgi?id=770
    - Under some rare circumstances, a dev assert will be triggered
	in unpack.c.  This results in the pengine getting restarted.
	This is annoying, but not a disaster.
	http://www.osdl.org/developer_bugzilla/show_bug.cgi?id=797

* Tue May 23 2005  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.99.5 - Near-final beta of 2.0.0 release
  + many bug fixes - code looks very stable at this point
    -- well tested at this point on 4 and 8 node clusters.

* Thu Apr 07 2005  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.99.4 - Near-final beta of 2.0.0 release
  + many bug fixes since 1.99.1
  + new external STONITH model - fully supports scripting interface
  + tested through 12 node clusters successfully
  + No serious defects found in testing
  + Easier-to-understand locational constraints model
  + Many bug fixes of many kinds
  + Important bug fixes to OCF IPaddr resource agent
  + Resources are monitored only on request
  + See http://wiki.linux-ha.org/ClusterResourceManager/Setup
    for basic ideas about getting started.
  + Release 1 style (2-node) clusters still fully supported
  + Release 2 style clusters support 1-N node clusters
	(where N is probably something like 8-32)

* Tue Mar 20 2005  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.99.3 - Near-final beta "technology preview" of 2.0.0 release
  + many bug fixes since 1.99.1
  + tested through 12 node clusters with reasonable success
  + new STONITH API

* Sun Feb 20 2005  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.99.2 - Near-final beta "technology preview" of 2.0.0 release
  + Many many many changes.  Far too many to describe here.
  + See http://wiki.linux-ha.org/ClusterResourceManager/Setup
    for certain basic ideas about getting started.

* Mon Oct 11 2004  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.99.1 - *early* beta series - preparing for 2.0.0
  + Andrew provided a number of fixes to the CRM and 2.0 features
  + Fixed a problem with retrying failed STONITH operations

* Mon Oct 11 2004  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.99.0 - *early* beta series - preparing for 2.0.0
  + All STABLE changes noted below have been ported to this branch
  + Included in this release is a beta of the next generation of Heartbeat
	resource manager developed by Andrew Beekhof.  
	http://linuxha.trick.ca/NewHeartbeatDesign is a good place to learn
	more about this effort. Please examine crm/README, crm/test/README
	and crm/crm-1.0.dtd for example usage and configuration.
  + Also included is the L(ocal) R(esource) M(anager) developed by IBM China
	which is an integral part of the NewHeartbeatDesign.
  + Known caveats:
    - STONITH as a whole has seen a code cleanup and should be tested
      carefully.
    - The external STONITH plug-in has undergone major surgery and
      probably doesn't work yet.
    - the new CRM is not perfectly stable with 3 nodes yet.
  + PLEASE see http://osdl.org/developer_bugzilla/enter_bug.cgi?product=Linux-HA
    and use it to report quirks and issues you find!
  
* Sat Sep 18 2004  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.2.3 (stable)
  + fixed a serious error which causes heartbeat to misbehave after about
        10 months of continuous operation
  + Made our ARP packets more RFC compliant
  + Extended apcmastersnmp code to deal with new devices
  + fixed a bug concerning simultaneous stops of both machines causing one
        of them to not shut down.
  + added an option to suppress reporting on packet corruption
  + fixed it so that we don't create the FIFO by the RPM
  + made cl_status setgid so anyone can run it, and fixed exit codes
  + eliminated a serious memory leak associated with client code
  + packaged doc files which had been missed before
  + fixed many many small bugs and memory leaks detected by BEAM
  + added several new test cases
  + fixed longstanding bug in plugin unloading
  + fixed a shutdown hang problem
  + several fixes for Solaris, FreeBSD
  + Solaris packaging now included in base
  + fixed a bug related to the apache resource agent not handling
        quoted parameters
  + added use_apphbd parameter to have heartbeat register
        with apphbd instead of watchdog device when desired
  + changed apphbd to default its config file to /etc
  + added snmp subagent code
  + added hbaping communications plugin
  + added external STONITH plugin
  + ldirectord: fixed a bug where real servers that were are
        present in multiple virtual services will only be added
        to one virtual service.

* Mon May 11 2004  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.2.2 (stable)
  + Fixed several format string errors in communication plugins
  + Fixed a bug which kept us from diagnosing errors in non-aliased interfaces
  + Fixed a bug in ipaddr which caused an infinite loop when auto_failback on
  + Updated Debian things...
  + Added IPv6addr resource agent
  + Added ibmhmc STONITH plugin
  + Added cl_status command
  + Fixed a bug regarding restarts when auto_failback is on...
  + Fixed a couple of bugs in sha1 authentication method for very long keys
  + Fixed a bug in the portblock resource agent so that it no longer blocks
          ports on the loopback interface
  + Increased the time allowed for split brain test before it declares failure

+ Version 1.2.1 (stable)
  + Netstrings can now be used for our on-the-wire data format
  + Perl/SWIG bindings added for some heartbeat libraries
  + Significant improvements to SAF data checkpointing API
  + Implemented unbuffered ipcsocket code for SAF APIs
  + Many Solaris fixes -- except for ipfail, Solaris works
  + Significant library restructuring
  + Watchdog device NOWAYOUT is now overridded if defaulted
  + Watchdog device now kills machine instantly after deadtime
        instead of after one minute
  + Hostnames should now be treated case-independently...
  + Added new client status APIs - client_status() and cstatus_callback()
  + Fixed bug with auto_failback and quick full restarts
  + We now automatically reboot when resources fail to stop correctly...
  + We now check the status of the configured STONITH device hourly...
  + STONITH operations repeat after a 5 second delay, not immediately...
  + Added hb_takeover command - complement to hb_standby
  + Added documentation on how to use evlog/TCP to enable testing to
        take place without losing messages due to UDP message forwarding
  + Several new tests from Mi, Jun - split brain, bandwidth, failure
        detection time.
  + Fix to LVM resource from Harald Milz <hm@muc.de>
  + Fixed FreeBSD authentication problems breaking ipfail
  + Fixed .so loading on Debian
  + Fixed false complaints about resource scripts (from Jens Schmalzing)
  + Fixed false stop failure from LinuxSCSI  (from Jens Schmalzing <j.s@lmu.de>)



* Thu Apr 15 2004  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.3.0 - beta series
  + Netstrings can now be used for our on-the-wire data format
  + Perl/SWIG bindings added for some heartbeat libraries
  + Significant improvements to SAF data checkpointing API
  + Implemented unbuffered ipcsocket code for SAF APIs
  + Many Solaris fixes -- except for ipfail, Solaris works
  + Significant library restructuring
  + Watchdog device NOWAYOUT is now overridded if defaulted
  + Watchdog device now kills machine instantly after deadtime
 	instead of after one minute
  + Hostnames should now be treated case-independently...
  + Added new client status APIs - client_status() and cstatus_callback()
  + Fixed bug with auto_failback and quick full restarts
  + We now automatically reboot when resources fail to stop correctly...
  + We now check the status of the configured STONITH device hourly...
  + STONITH operations repeat after a 5 second delay, not immediately...
  + Added hb_takeover command - complement to hb_standby
  + Added documentation on how to use evlog/TCP to enable testing to
	take place without losing messages due to UDP message forwarding
  + Several new tests from Mi, Jun - split brain, bandwidth, failure
	detection time.
  + Fix to LVM resource from Harald Milz <hm@muc.de>

* Tue Feb 16 2004  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.2.0
  + Replaced the nice_failback option with the auto_failback option.
	THIS OBSOLETES THE NICE_FAILBACK OPTION. READ THE DOCS FOR HOW
	TO UPGRADE SMOOTHLY.
  + Added a new feature to hb_standby which allows you to give up
	  any specific category of resources:  local, foreign, or all.
	The old behavior is "all" which is the default.
	This allows you to put a auto_failback no cluster into
	  an active/active configuration on demand.
  + ipfail now works properly with auto_failback on (active/active)
  + ipfail now has "hysteresis" so that it doesn't respond immediately
	to a network failure, but waits a little while so that the
	damage can be properly assessed and extraneous takeovers avoided
  + Added new ping node timeout directive "deadping"
  + Made sure heartbeat preallocated stack and heap, and printed a
	message if we allocate heap once we're started up...
  + IPMILan STONITH plugin added to CVS
  + Added IPaddr2 resource script
  + Made the APC smart UPS ups code compatible with more UPSes
  + Added a (preliminary?) ordered messaging facility from Yi Zhu
  + Changed IPaddr's method of doing ARPs in background so that
	certain timing windows were closed.
  + Added OCF (wrapper) resource script
  + Allow respawn programs to take arguments
  + Added pinggroups (where any node being up is OK)
  + SIGNIFICANT amount of internal rearchitecture.
  + Many bug fixes.
  + Several documentation updates.

* Tue Feb 10 2004  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.1.5
  + ipfail now has "hysteresis" so that it doesn't respond immediately
	to a network failure, but waits a little while so that the
	damage can be properly assessed and extraneous takeovers avoided
  + Several fixes to cl_poll()
  + More fixes to the IPC code - especially handling data reception
	after EOF
  + removed some unclean code from GSource for treating EOF conditions
  + Several bugs concerning hanging when shutting down early during startup
  + A few BasicSanityCheck bug fixes
  + CTS now allows a single machine to be able to monitor several clusters
  + Most former CTS options are now either unneeded or on the command line
  + Increased number of ARPs and how long they're being sent out
  + Fixed uncommon (authorization) memory leak
  + Some Solaris portability fixes.
  + Made init script handle standby correctly for new config files
  + Improved the fast failure detection test
  + Added some backwards compatibility for nice_failback and some default
	authentication directives
  + Corrected the 1.1.4 change log
  

* Fri Jan 22 2004  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.1.4
  + ipfail now works properly with auto_failback on (active/active)
  + Changed the API to use sockets (IPC library) instead of FIFOs.
  + Added new apiauth directives to provide authorization information
	formerly provided by the FIFO permissions.
  + Added Intel's implementation of the SAF data checkpointing API and daemon
  + Added a cleanup suggested by Emily Ratliff.
  + IPMILan STONITH plugin added to CVS
  + Added IPaddr2 resource script
  + Various cleanups due to horms.
  + Fixed authentication to work on 64-bit platforms(!)
  + Fixed the cl_poll() code to handle corner cases better
  + Made heartbeat close watchdog device before re-execing itself
  + New CTS improvements from Mi, Jun <jun.mi@intel.com>
  + Various minor bug fixes.
      . Several shutdown bugs addressed
      . fixed sendarp to make a pid file, so we can shut it down
          when we shut everything else down in case it's still running.
      . Lots of minor bug fixes to IPC code
      . Lots of minor bug fixes to ipctest program
      . made BasicSanityCheck more tolerant of delays
      . Fixed IPC code to authenticate based on ints, not int*s.
      . Check properly for strnlen instead of strlen...
      . Several signed/unsigned fixes
      . A few uninitialized vars now are inited
      . Switched to compiling lex/yacc sources the automake way
      . Lots of minor CTS fixes...

  + ldirectord bug fixes:
    . When new real servers are added on initialisation or when
        the configuration file is reread they are marked with status
        of -1 (uninitialised) so they will be checked and inserted
        into the virtual service as required
    . All checks use the checkport if set, otherwise the port set for
        the individual real server. This was the case for http and
        connect checks, but others had variations on this theme.
    . When the configuration file is reread because it changed
        on disk and autoreload is set, check the real servers
        immediately rather than waiting for checkinterval to expire
    . Already running message sent to stderr instead of stdout
    . Support alternate server in real-server specific URL
    . Treat the same real server with different weights as a different
        real server. Fixes bug reported by Philip Hayward whereby the same
        real-server would always have the same weight, regardless of
        the ldirectord.cf

* Fri Sep 26 2003  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.1.3
  + Bugfix for heartbeat starting resources twice concurrently if
    auto_failback was set to "legacy".
  + Bugfix for messages getting lost if messages were sent in quick
    succession. (Kurosawa Takahiro)
  + Bugfix for Filesystem resource checking for presence of filesystem
    support before loading the module.
  + BasicSanityCheck extended to cover more basic tests.
  + Bugfix for findif not working correctly for CIDR netmasks.
  + Minor bugfix for ldirectord recognizing new schedulers correctly and
    timeout settings are now being honoured.
  + Enhanced the message giving a better explanation of how to set up node
    names properly when current node not found in the ha.cf file
  + Send a message to the cluster whenever we have a node which doesn't
    need STONITHing - even though it's gone down.  This fix needed
    by CCM, which is in turn needed by EVMS.
  + Enhanced the messages for missing ha.cf and missing haresources files
    explaining that sample config files are found in the documentation. 
  + Fix for memory leak from Forrest Zhao<forrest.zhao@intel.com>
  + Added a (preliminary?) ordered messaging facility from Yi Zhu
  + FAQ updates
  + Added Xinetd resource script
  + Added OCF (wrapper) resource script
  + Allow respawn programs to take arguments
  + Added pinggroups (where any node being up is OK)
  + fixed ldirectord negotiatetimeout for HTTP
  + fixed a bug which caused -d flag to be ignored
  + failing resource scripts are now ERRORs not WARNings
  + now shuts down correctly when auto_failback == legacy


* Mon Jul 13 2003  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.1.2
  + Replaced the nice_failback option with the auto_failback option.
	THIS OBSOLETES THE NICE_FAILBACK OPTION. READ THE DOCS FOR HOW
	TO UPGRADE SMOOTHLY.
  + Changed IPaddr to not do ARPs in background, and shortened time 
	between ARPs.  Also made these things tunable...
  + changed our comm ttys to not become our controlling TTYs
  + Enhanced the ServeRAID script to fix a critical bug by using a new feature
  + Added a new DirectoryMap to CVS - tells where everything is...
  + significantly enhanced the BasicSanityCheck script, and the tests
	it calls.
  + added a new option to use a replacement poll function for improved
	real-time performance.
  + added the ability to have a cluster node's name be different
	from it's uname -n
  + Moved where CTS gets installed to /usr/lib/heartbeat/cts
  + Big improvements to the CTS README from IBM test labs in Austin.
  + bug fixes to the WTI NPS power switch
  + new client API calls:
	return arbitrary configuration parameters
	return current resource status
  + Added a new clplumbing function: mssleep()
  + added new capabilities for supporting pseudo-resources
  + added new messages which come out after initial takeover is done
	 (improves CTS results)
  + LOTS of documentation updates.
  + fixed a security vulnerability
  + fixed a bug where heartbeat would shut down while in the middle
	of processing resource movement requests.
  + changed compilation flags to eliminate similar future security
	issues
  + went to even-more-strict gcc flags
  + fixed several "reload" bugs.  Now reload works ;-)
  + fixed STONITH bug when other node never heard from.
  + Minor bug fixes (cleaned up corrupted message)
  + Two different client API bugs fixed.
  + changed the configure script to test which warning flags are
	supported by the current gcc.
  + enhanced the API test program to test new capabilities...


* Wed May 21 2003  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.1.1
  + Significant restructuring of the processes in heartbeat
  + Added a new feature to hb_standby which allows you to give up
	  any specific category of resources:  local, foreign, or all.
	The old behavior is "all" which is the default.
	This allows you to put a nice_failback cluster into
	  an active/active configuration
  + Enhancements to the ServeRAID code to make it work with the new
    (supported) version of IPSSEND from the ServeRAID folks...
  + Added STONITH code for the Dell remote access controller
  + Fixed a major bug which kept it from taking over correctly after 246
	days or so
  + Fixed a major bug where heartbeat didn't lock itself into memory
	properly
  + Added new ping node timeout directive "deadping"
  + Made sure heartbeat preallocated stack and heap, and printed a
	message if we allocate heap once we're started up...
  + Minor heartbeat API bug fixes
  + Minor documentation fixes
  + Minor fix to allow IP addresses with /32 masks...
  + Fixed a timing window for !nice_failback resource acquisition
  + Added several CCM bug fixes
  + Made the APC smart UPS ups code compatible with more UPSes
  + Fixed a bug in respawn
  + Enhanced internal checking for malloc errors...
  + Added IP alias search optimization from Sean Reifscheneider

* Wed Mar 19 2003  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.0.2:
  + Fixed comment errors in heartbeat init script to allow it to run on RH 8.0
  + Changed apphbd to use poll(2) instead of sigtimedwait(2)
  + Put missing files into tarball
  + Documentation improvements for IPaddr and other things
  + Fixed an error in hb_standby which kept it from working if releasing 
    resources takes more than 10 seconds
  + Added a fix to allow heartbeat to run on systems without writable disk
    (like routers booting from CD-ROM)
  + Added configuration file for apphbd
  + Added fix from Adam Li to keep recoverymgr stop looping at high priority
  + Added fix to ServeRAID resource to make it work with (new) supported 
    hardware
  + Added Delay resource script
  + Added fix to Filesystem to allow it to support NFS mounts and allow
    user to specify mount options
  + Added fix to IPaddr to make tmp directory for restoring loopback device
  + Added fix to ipcsocket code to deal correctly with EAGAIN when sending
    message body

* Mon Feb 17 2003  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.0.1:
  + Fixed some compile errors on different platforms, and library versions
  + Disable ccm from running on 'ping' nodes
  + Put in Steve Snodgrass' fix to send_arp to make it work on non-primary
	interfaces.

* Thu Feb 13 2003  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 1.0.1 beta series

  0.4.9g:
  + Changed default deadtime, warntime, and heartbeat interval
  + Auto* tool updates
  + VIP loopback fixes for IP address takeover
  + Various Solaris and FreeBSD fixes
  + added SNMP agent
  + Several CCM bug fixes
  + two new heartbeat API calls
  + various documentation fixes, including documentation for ipfail
  + Numerous minor cleanups.
  + Fixed a few bugs in the IPC code.
  + Fixed the (IPC) bug which caused apphbd to hang the whole machine.
  + Added a new IPC call (waitout)
  + Wrote a simple IPC test program.
  + Clarified several log messages.
  + Cleaned up the ucast communications plugin
  + Cleaned up for new C compilers
  + Fixed permissions bug in IPC which caused apphbd to not be usable by all
  + Added a new rtprio option to the heartbeat config file
  + updated apphbtest program
  + Changed ipfail to log things at same level heartbeat does


* Sat Nov 30 2002  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
+ Version 0.5 beta series (now renamed to 1.0.1 beta series).
  0.4.9f:
  + Added pre-start, pre-stop, post-stop and pre-stop constructs in init script
  + various IPC fixes
  + Fix to STONITH behavior: STONITH unresponsive node right after we reboot
  + Fixed extreme latency in IPC code
  + various configure.in cleanups
  + Fixed memory leak in IPC socket code
  + Added streamlined mainloop/IPC integration code
  + Moved more heartbeat internal communication to IPC library
  + Added further support for ipfail
  + Added supplementary groups to the respawn-ed clients
  + Added standby to init script actions
  + Lots of minor CCM fixes
  + Split (most) resource management code into a separate file.
  + Fixes to accommodate different versions of libraries
  + Heartbeat API client headers fixup
  + Added new API calls
  + Simplified (and fixed) handling of local status.  This would sometimes cause
	obscure failures on startup.
  + Added new IPsrcaddr resource script

  KNOWN BUGS:
  + apphbd goes into an infinite loop on some platforms

* Wed Oct 9 2002  Alan Robertson <alanr@unix.sh> (see doc/AUTHORS file)
  0.4.9e:
  + Changed client code to keep write file descriptor open at all times
        (realtime improvement)
  + Added a "poll replacement"  function based on sigtimedwait(2), which
        should be faster for those cases that can use it.
  + Added a hb_warntime() call to the application heartbeat API.
  + Changed all times in the configuration file to be in milliseconds
        if specified with "ms" at the end.  (seconds is still the default).
  + Fixes to serious security issue due to Nathan Wallwork <nwallwo@pnm.com>
  + Changed read/write child processes to run as nobody.
  + Fixed a bug where ping packets are printed incorrectly when debugging.
  + Changed heartbeat code to preallocate a some heap space.
  + CCM daemon API restructuring
  + Added ipc_channel_pair() function to the IPC library.
  + Changed everything to use longclock_t instead of clock_t
  + Fixed a bug concerning the ifwalk() call on ping nodes in the API
  + Made apphbd run at high priority and locked into memory
  + Made a library for setting priority up.
  + Made ucast comm module at least be configurable and loadable.
  + Fixed a startup/shutdown timing problem.

  0.4.9d:
  + removed an "open" call for /proc/loadavg (improve realtime behavior)
  + changed API code to not 1-char reads from clients
  + Ignored certain error conditions from API clients
  + fixed an obscure error message about trying to retransmit a packet
	which we haven't sent yet.  This happens after restarts.
  + made the PILS libraries available in a separate package
  + moved the stonith headers to stonith/... when installed
  + improved debugging for NV failure cases...
  + updated AUTHORS file and simplified the changelog authorship
	(look in AUTHORS for the real story)
  + Added Ram Pai's CCM membership code
  + Added the application heartbeat code
  + Added the Kevin Dwyer's ipfail client code to the distribution
  + Many fixes for various tool versions and OS combinations.
  + Fixed a few bugs related to clients disconnecting.
  + Fixed some bugs in the CTS test code.
  + Added BasicSanityCheck script to tell if built objects look good.
  + Added PATH-like capabilities to PILS
  + Changed STONITH to use the new plugin system.
  + *Significantly* improved STONITH usage message (from Lorn Kay)
  + Fixed some bugs related to restarting.
  + Made exit codes more LSB-compliant.
  + Fixed various things so that ping nodes don't break takeovers.

  0.4.9c and before:
  + Cluster partitioning  now handled correctly (really!)
  + Complete rearchitecture of plugin system
  + Complete restructure of build system to use automake and port things
	to AIX, FreeBSD and solaris.
  + Added Lclaudio's "standby" capability to put a node into standby
	mode on demand.
  + Added code to send out gratuitous ARP requests as well as gratuitous
	arp replies during IP address takeover.
  + Suppress stonith operations for nodes which went down gracefully.
  + Significantly improved real-time performance
  + Added new unicast heartbeat type.
  + Added code to make serial ports flush stale data on new connections.
  + The Famous CLK_TCK compile time fixes (really!)
  + Added a document which describes the heartbeat API
  + Changed the code which makes FIFOs to not try and make the FIFOs for
        named clients, and several other minor API client changes.
  + Fixed a fairly rare client API bug where it would shut down the
        client for no apparent reason.
  + Added stonith plugins for: apcmaster, apcmastersnmp switches, and ssh
        module (for test environments only)
  + Integrated support for the Baytech RPC-3 switch into baytech module
  + Fixes to APC UPS plugin
  + Got rid of "control_process: NULL message" message
  + Got rid of the "controlfifo2msg: cannot create message" message
  + Added -h option to give usage message for stonith command...
  + Wait for successful STONITH completion, and retry if its configured.
  + Sped up takeover code.
  + Several potential timing problems eliminated.
  + Cleaned up the shutdown (exit) code considerably.
  + Detect the death of our core child processes.
  + Changed where usage messages go depending on exit status from usage().
  + Made some more functions static.
  + Real-time performance improvement changes
  + Updated the faqntips document
  + Added a feature to heartbeat.h so that log messages get checked as
        printf-style messages on GNU C compilers
  + Changed several log messages to have the right parameters (discovered
        as a result of the change above)
  + Numerous FreeBSD, Solaris and OpenBSD fixes.
  + Added backwards compatibility kludge for udp (versus bcast)
  + Queued messages to API clients instead of throwing them away.
  + Added code to send out messages when clients join, leave.
  + Added support for spawning and monitoring child clients.
  + Cleaned up error messages.
  + Added support for DB2, ServeRAID and WAS, LVM, and Apache (IBMhttp too),
    also ICP Vortex controller.
  + Added locking when creating new IP aliases.
  + Added a "unicast" media option.
  + Added a new SimulStart and standby test case.
  + Diddled init levels around...
  + Added an application-level heartbeat API.
  + Added several new "plumbing" subsystems (IPC, longclock_t, proctrack, etc.)
  + Added a new "contrib" directory.
  + Fixed serious (but trivial) bug in the process tracking code which caused
	it to exit heartbeat - this occured repeatably for STONITH operations.
  + Write a 'v' to the watchdog device to tell it not to reboot us when
	we close the device.
  + Various ldirectord fixes due to Horms
  + Minor patch from Lorn Kay to deal with loopback interfaces which might
	have been put in by LVS direct routing
  + Updated AUTHORS file and moved list of authors over

* Fri Mar 16 2001  Alan Robertson <alanr@unix.sh>
+ Version 0.4.9

  + Split into 3 rpms - heartbeat, heartbeat-stonith heartbeat-ldirectord

  + Made media modules and authentication modules and stonith modules
	dynamically loadable.

  + Added Multicast media support
  + Added ping node/membership/link type for tiebreaking.  This will
	be useful when implementing quorum on 2-node systems.
	(not yet compatible with nice_failback(?))
  + Removed ppp support

  + Heartbeat client API support

  + Added STONITH API library
    +   support for the Baytech RPC-3A power switch
    +   support for the APCsmart UPS
    +   support for the VACM cluster management tool
    +	support for WTI RPS10
    +	support for Night/Ware RPC100S
    +	support for "Meatware" (human intervention) module
    +	support for "null" (testing only) module

  + Fixed startup timing bugs
  + Fixed shutdown sequence bugs: takeover occured before
	resources were released by other system
  + Fixed various logging bugs
  + Closed holes in protection against replay attacks

  + Added checks that complain if all resources aren't idle on startup.
  + IP address takeover fixes
      + Endian fixes
      + Removed the 8-alias limitation
      + Takeovers now occur faster (ARPs occur asynchronously)

  + Port number changes
    + Use our IANA port number (694) by default
    + Recognize our IANA port number ("ha-cluster") if it's in /etc/services

  + Moved several files, etc. from /var/run to /var/lib/heartbeat
  + Incorporated new ldirectord version
  + Added late heartbeat warning for late-arriving heartbeats
  + Added detection of and partial recovery from cluster partitions
  + Accept multiple arguments for resource scripts
  + Added Raid1 and Filesystem resource scripts
  + Added man pages
  + Added debian package support

* Fri Jun 30 2000 Alan Robertson <alanr@unix.sh>
+ Version 0.4.8
  + Incorporated ldirectord version 1.9 (fixes memory leak)
  + Made the order of resource takeover more rational:  Takeover is now
    left-to-right, and giveup is right-to-left
  + Changed the default port number to our official IANA port number (694)
  + Regularized more messages, eliminated some redundant ones.
  + Print the version of heartbeat when starting.
  + Print exhaustive version info when starting with debug on.
  + Hosts now have 3 statuses {down, up, active} active means that it knows
	that all its links are operational, and it's safe to send cluster
	messages
  + Significant revisions to nice_failback (mainly due to lclaudio)
  + More SuSE-compatibility. Thanks to Friedrich Lobenstock <fl@fl.priv.at>
  + Tidied up logging so it can be to files, to syslog or both (Horms)
  + Tidied up build process (Horms)
  + Updated ldirectord to produce and install a man page and be
    compatible with the fwmark options to The Linux Virtual Server (Horms)
  + Added log rotation for ldirectord and heartbeat using logrotate
    if it is installed
  + Added Audible Alarm resource by Kirk Lawson <lklawson@heapy.com> 
    and myself (Horms)
  + Added init script for ldirectord so it can be run independently
    of heartbeat (Horms)
  + Added sample config file for ldirectord (Horms)
  + An empty /etc/ha.d/conf/ is now part of the rpm distribution
    as this is where ldirectord's configuration belongs (Horms)
  + Minor startup script tweaks.  Hopefully, we should be able to make core
    files should we crash in the future.  Thanks to Holger Kiehl for diagnosing
    the problem!
  + Fixed a bug which kept the "logfile" option from ever working.
  + Added a TestCluster test utility.  Pretty primitive so far...
  + Fixed the serial locking code so that it unlocks when it shuts down.
  + Lock heartbeat into memory, and raise our priority
  + Minor, but important fix from lclaudio to init uninited variable.

* Sat Dec 25 1999 Alan Robertson <alanr@unix.sh>
+ Version 0.4.7
  + Added the nice_failback feature. If the cluster is running when
	the primary starts it acts as a secondary. (Luis Claudio Goncalves)
  + Put in lots of code to make lost packet retransmission happen
  + Stopped trying to use the /proc/ha interface
  + Finished the error recovery in the heartbeat protocol (and got it to work)
  + Added test code for the heartbeat protocol
  + Raised the maximum length of a node name
  + Added Jacob Rief's ldirectord resource type
  + Added Stefan Salzer's <salt@cin.de> fix for a 'grep' in IPaddr which
	wasn't specific enough and would sometimes get IPaddr confused on
	IP addresses that prefix-matched.
  + Added Lars Marowsky-Bree's suggestion to make the code almost completely
	robust with respect to jumping the clock backwards and forwards
  + Added code from Michael Moerz <mike@cubit.at> to keep findif from
	core dumping if /proc/route can't be read.

* Mon Nov 22 1999 Alan Robertson <alanr@unix.sh>
+ Version 0.4.6
  + Fixed timing problem in "heartbeat restart" so it's reliable now
  + Made start/stop status compatible with SuSE expectations
  + Made resource status detection compatible with SuSE start/stop expectations
  + Fixed a bug relating to serial and ppp-udp authentication (it never worked)
  + added a little more substance to the error recovery for the HB protocol.
  + Fixed a bug for logging from shell scripts
  + Added a little logging for initial resource acquisition
  + Added #!/bin/sh to the front of shell scripts
  + Fixed Makefile, so that the build root wasn't compiled into pathnames
  + Turned on CTSRTS, enabling for flow control for serial ports.
  + Fixed a bug which kept it from working in non-English environments

* Wed Oct 13 1999 Alan Robertson <alanr@unix.sh>
+ Version 0.4.5
  + Mijta Sarp added a new feature to authenticate heartbeat packets
	using a variety of strong authentication techniques
  + Changed resource acquisition and relinquishment to occur in heartbeat,
       instead of in the start/stop script.  This means you don't *really*
       have to use the start/stop script if you don't want to.
  + Added -k option to gracefully shut down current heartbeat instance
  + Added -r option to cause currently running heartbeat to reread config files
  + Added -s option to report on operational status of "heartbeat"
  + Sped up resource acquisition on master restart.
  + Added validation of ipresources file at startup time.
  + Added code to allow the IPaddr takeover script to be given the
        interface to take over, instead of inferring it.  This was requested
        by Lars Marowsky-Bree
  + Incorporated patch from Guenther Thomsen to implement locking for
        serial ports used for heartbeats
  + Incorporated patch from Guenther Thomsen to clean up logging.
        (you can now use syslog and/or file logs)
  + Improved FreeBSD compatibility.
  + Fixed a bug where the FIFO doesn't get created correctly.
  + Fixed a couple of uninitialized variables in heartbeat and /proc/ha code
  + Fixed longstanding crash bug related to getting a SIGALRM while in malloc
	or free.
  + Implemented new memory management scheme, including memory stats

* Thu Sep 16 1999 Alan Robertson <alanr@unix.sh>
+ Version 0.4.4
  + Fixed a stupid error in handling CIDR addresses in IPaddr.
  + Updated the documentation with the latest from Rudy.

* Wed Sep 15 1999 Alan Robertson <alanr@unix.sh>
+ Version 0.4.3
  + Changed startup scripts to create /dev/watchdog if needed
  + Turned off loading of /proc/ha module by default.
  + Incorporated bug fix from Thomas Hepper <th@ant.han.de> to IPaddr for
	PPP configurations
  + Put in a fix from Gregor Howey <ghowey@bremer-nachrichten.de>
	where Gregor found that I had stripped off the ::resourceid part
	of the string in ResourceManager resulting in some bad calls later on.
  +  Made it compliant with the FHS (filesystem hierarchy standard)
  +  Fixed IP address takeover so we can take over on non-eth0 interface
  +  Fixed IP takeover code so we can specify netmasks and broadcast addrs,
	or default them at the user's option.
  +  Added code to report on message buffer usage on SIGUSR[12]
  +  Made SIGUSR1 increment debug level, and SIGUSR2 decrement it.
  +  Incorporated Rudy's latest "Getting Started" document
  +  Made it largely Debian-compliant.  Thanks to Guenther Thomsen, Thomas
	Hepper, Iñaki Fernández Villanueva and others.
  +  Made changes to work better with Red Hat 6.1, and SMP code.
  +  Sometimes it seems that the Master Control Process dies :-(

* Sat Aug 14 1999 Alan Robertson <alanr@unix.sh>
+ Version 0.4.2
  + Implemented simple resource groups
  + Implemented application notification for groups starting/stopping
  + Eliminated restriction on floating IPs only being associated with eth0
  + Added a uniform resource model, with IP resources being only one kind.
	(Thanks to Lars Marowsky-Bree for a good suggestion)
  + Largely rewrote the IP address takeover code, making it clearer, fit
	into the uniform resource model, and removing some restrictions.
  + Preliminary "Getting Started" document by Rudy Pawul
  + Improved the /proc/ha code
  + Fixed memory leak associated with serial ports, and problem with return
	of control to the "master" node.
	(Thanks to Holger Kiehl for reporting them, and testing fixes!)

* Tue Jul 6 1999 Alan Robertson <alanr@unix.sh>
+ Version 0.4.1
  + Fixed major memory leak in 0.4.0 (oops!)
  + Added code to eliminate duplicate packets and log lost ones
  + Tightened up PPP/UDP startup/shutdown code
  + Made PPP/UDP peacefully coexist with "normal" udp
  + Made logs more uniform and neater
  + Fixed several other minor bugs
  + Added very preliminary kernel code for monitoring and controlling
	heartbeat via /proc/ha.  Very cool, but not really done yet.

* Wed Jun 30 1999 Alan Robertson <alanr@unix.sh>
+ Version 0.4.0
  + Changed packet format from single line positional parameter style
	to a collection of {name,value} pairs.  A vital change for the future.
  + Fixed some bugs with regard to forwarding data around rings
  + We now modify /etc/ppp/ip-up.local, so PPP-udp works out of the box
	(at least for Red Hat)
  + Includes the first version of Volker Wiegand's Hardware Installation Guide
	(it's pretty good for a first version!)

* Wed Jun 09 1999 Alan Robertson <alanr@unix.sh>
+ Version 0.3.2
  + Added UDP/PPP bidirectional serial ring heartbeat
	(PPP ensures data integrity on the serial links)
  + fixed a stupid bug which caused shutdown to give unpredictable
	results
  + added timestamps to /var/log/ha-log messages
  + fixed a couple of other minor oversights.

* Sun May 10 1999  Alan Robertson <alanr@unix.sh>
+ Version 0.3.1
  + Make ChangeLog file from RPM specfile
  + Made ipresources only install in the DOC directory as a sample

* Sun May 09 1999 Alan Robertson <alanr@unix.sh>
+ Version 0.3.0
  + Added UDP broadcast heartbeat (courtesy of Tom Vogt)
  + Significantly restructured code making it easier to add heartbeat media
  + added new directives to config file:
    + udp interface-name
    + udpport port-number
    + baud    serial-baud-rate
  + made manual daemon shutdown easier (only need to kill one)
  + moved the sample ha.cf file to the Doc directory

* Sat Mar 27 1999 Alan Robertson <alanr@unix.sh>
+ Version 0.2.0
  + Make an RPM out of it
  + Integrated IP address takeover gotten from Horms
  + Added support to tickle a watchdog timer whenever our heart beats
  + Integrated enough basic code to allow a 2-node demo to occur
  + Integrated patches from Andrew Hildebrand <andrew@pdi.com> to allow it
    to run under IRIX.
  - Known Bugs
    - Only supports 2-node clusters
    - Only supports a single IP interface per node in the cluster
    - Doesn't yet include Tom Vogt's ethernet heartbeat code
    - No documentation
    - Not very useful yet :-)

###########################################################
