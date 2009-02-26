# Ugly, but we need headers from a kernel to rebuild against
%define kernel %(rpm -q kernel-devel --qf '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}\\n' 2>/dev/null | head -1)

Summary: HA monitor built upon LVS, VRRP and service pollers
Name: keepalived
Version: 1.1.16
Release: 1%{?dist}
License: GPLv2+
Group: Applications/System
URL: http://www.keepalived.org/
Source: http://www.keepalived.org/software/keepalived-%{version}.tar.gz
Patch0: keepalived-1.1.14-installmodes.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service, /sbin/chkconfig
Requires(postun): /sbin/service
BuildRequires: openssl-devel
# We need both of these for proper LVS support
BuildRequires: kernel, kernel-devel
# We need popt, popt-devel is split out of rpm in Fedora 8+
%if 0%{?fedora} >= 8
BuildRequires: popt-devel
%endif

%description
The main goal of the keepalived project is to add a strong & robust keepalive
facility to the Linux Virtual Server project. This project is written in C with
multilayer TCP/IP stack checks. Keepalived implements a framework based on
three family checks : Layer3, Layer4 & Layer5/7. This framework gives the
daemon the ability to check the state of an LVS server pool. When one of the
servers of the LVS server pool is down, keepalived informs the linux kernel via
a setsockopt call to remove this server entry from the LVS topology. In
addition keepalived implements an independent VRRPv2 stack to handle director
failover. So in short keepalived is a userspace daemon for LVS cluster nodes
healthchecks and LVS directors failover.


%prep
%setup -q
%patch0 -p1 -b .installmodes
# Fix file mode (600 as of 1.1.13)
%{__chmod} a+r doc/samples/sample.misccheck.smbcheck.sh
# Included as doc, so disable its dependencies
%{__chmod} -x goodies/arpreset.pl


%build
%configure --with-kernel-dir="/lib/modules/%{kernel}/build"
%{__make} %{?_smp_mflags} STRIP=/bin/true


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
# Remove "samples", as we include them in %%doc
%{__rm} -rf %{buildroot}%{_sysconfdir}/keepalived/samples/


%check
# A build could silently have LVS support disabled if the kernel includes can't
# be properly found, we need to avoid that.
if ! grep -q "IPVS_SUPPORT='_WITH_LVS_'" config.log; then
    echo "ERROR: We do not want keeepalived lacking LVS support."
    exit 1
fi


%clean
%{__rm} -rf %{buildroot}


%post
/sbin/chkconfig --add keepalived

%preun
if [ $1 -eq 0 ]; then
    /sbin/service keepalived stop &>/dev/null || :
    /sbin/chkconfig --del keepalived
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service keepalived condrestart &>/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc AUTHOR ChangeLog CONTRIBUTORS COPYING README TODO
%doc doc/keepalived.conf.SYNOPSIS doc/samples/ goodies/arpreset.pl
%dir %{_sysconfdir}/keepalived/
%config(noreplace) %{_sysconfdir}/keepalived/keepalived.conf
%config(noreplace) %{_sysconfdir}/sysconfig/keepalived
%{_sysconfdir}/rc.d/init.d/keepalived
%{_bindir}/genhash
%{_sbindir}/keepalived
%{_mandir}/man1/genhash.1*
%{_mandir}/man5/keepalived.conf.5*
%{_mandir}/man8/keepalived.8*


%changelog
* Tue Feb 17 2009 David Hrbáč <david@hrbac.cz> - 1.1.16-1
- Update to 1.1.16

* Sat Apr 12 2008 David Hrbáč <david@hrbac.cz> - 1.1.15-4
- CentOS rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.15-4
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.1.15-3
 - Rebuild for deps

* Mon Oct 22 2007 Matthias Saou <http://freshrpms.net/> 1.1.15-2
- Update to latest upstream sources, identical except for the included spec.

* Mon Sep 17 2007 Matthias Saou <http://freshrpms.net/> 1.1.15-1
- Update to 1.1.15.
- Remove merged genhashman and include patches.

* Fri Sep 14 2007 Matthias Saou <http://freshrpms.net/> 1.1.14-2
- Include patch from Shinji Tanaka to fix conf include from inside some
  directives like vrrp_instance.

* Thu Sep 13 2007 Matthias Saou <http://freshrpms.net/> 1.1.14-1
- Update to 1.1.14.
- Remove all upstreamed patches.
- Remove our init script and sysconfig files, use the same now provided by the
  upstream package (will need to patch for LSB stuff soonish).
- Include new goodies/arpreset.pl in %%doc.
- Add missing scriplet requirements.

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-8
- Rebuild for new BuildID feature.

* Sun Aug  5 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-7
- Update License field.

* Mon Mar 26 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-6
- Fix doc/samples/sample.misccheck.smbcheck.sh mode (600 -> 644).

* Thu Mar 22 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-5
- Include types patch to fix compile on F7 (David Woodhouse).
- Fix up file modes (main binary 700 -> 755 and config 600 -> 640).

* Tue Feb 13 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-4
- Add missing \n to the kernel define, for when multiple kernels are installed.
- Pass STRIP=/bin/true to "make" in order to get a useful debuginfo package.

* Tue Feb 13 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-3
- Add %%check section to make sure any build without LVS support will fail.

* Mon Feb  5 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-2
- Use our own init script, include a sysconfig entry used by it for options.

* Thu Jan 25 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-1
- Update to 1.1.13.
- Change mode of configuration file to 0600.
- Don't include all of "doc" since it meant re-including all man pages.
- Don't include samples in the main configuration path, they're in %%doc.
- Include patch to add an optional label to interfaces.

* Sat Apr 08 2006 Dries Verachtert <dries@ulyssis.org> - 1.1.12-1.2
- Rebuild for Fedora Core 5.

* Sun Mar 12 2006 Dag Wieers <dag@wieers.com> - 1.1.12-1
- Updated to release 1.1.12.

* Fri Mar 04 2005 Dag Wieers <dag@wieers.com> - 1.1.11-1
- Updated to release 1.1.11.

* Wed Feb 23 2005 Dag Wieers <dag@wieers.com> - 1.1.10-2
- Fixed IPVS/LVS support. (Joe Sauer)

* Tue Feb 15 2005 Dag Wieers <dag@wieers.com> - 1.1.10-1
- Updated to release 1.1.10.

* Mon Feb 07 2005 Dag Wieers <dag@wieers.com> - 1.1.9-1
- Updated to release 1.1.9.

* Sun Oct 17 2004 Dag Wieers <dag@wieers.com> - 1.1.7-2
- Fixes to build with kernel IPVS support. (Tim Verhoeven)

* Fri Sep 24 2004 Dag Wieers <dag@wieers.com> - 1.1.7-1
- Updated to release 1.1.7. (Mathieu Lubrano)

* Mon Feb 23 2004 Dag Wieers <dag@wieers.com> - 1.1.6-0
- Updated to release 1.1.6.

* Mon Jan 26 2004 Dag Wieers <dag@wieers.com> - 1.1.5-0
- Updated to release 1.1.5.

* Mon Dec 29 2003 Dag Wieers <dag@wieers.com> - 1.1.4-0
- Updated to release 1.1.4.

* Fri Jun 06 2003 Dag Wieers <dag@wieers.com> - 1.0.3-0
- Initial package. (using DAR)

