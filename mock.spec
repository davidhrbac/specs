%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: Builds packages inside chroots
Name: mock
Version: 0.9.10
Release: 1%{?dist}.1
License: GPL
Group: Development/Tools
#Source: http://fedoraproject.org/projects/mock/releases/%{name}-%{version}.tar.gz
Source: http://fedorahosted.org/mock/attachment/wiki/MockTarballs/%{name}-%{version}.tar.gz
Patch0: mock-centos-configs.patch
Patch1: mock-centos-FunctionalNet.patch
URL: http://fedoraproject.org/wiki/Projects/Mock
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: python >= 2.4, yum >= 2.4, tar, gzip, python-ctypes, python-decoratortools, usermode
Requires(pre): shadow-utils
BuildRequires: python-devel


%description
Mock takes a srpm and builds it in a chroot

%prep
%setup -q
%patch0 -p1
#%patch1 -p1

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT/var/lib/mock
ln -s consolehelper $RPM_BUILD_ROOT/usr/bin/mock
# make the default.cfg link
cd $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}
ln -s centos-5-i386.cfg default.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ $1 -eq 1 ]; then
    groupadd -r mock >/dev/null 2>&1 || :
fi

%files
%defattr(-, root, root)

# executables
%{_bindir}/mock
%attr(0755, root, root) %{_sbindir}/mock

# python stuff
%{python_sitelib}/*

# config files
%dir  %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*.cfg
%config(noreplace) %{_sysconfdir}/%{name}/*.ini
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}

# docs
%{_mandir}/man1/mock.1*
%doc ChangeLog

# build dir
%attr(02775, root, mock) %dir /var/lib/mock

%changelog
* Thu Jul  3 2008 David Hrbáč <david@hrbac.cz> - 0.9.10-1
- update to new version 0.9.10
- removed mock-centos-FunctionalNet.patch
- changed mock-centos-configs.patch

* Tue May 15 2007 Karanbir Singh <kbsingh@karan.org> - 0.6.13-1.el5.kb.1
- Added mock-centos-FunctionalNet.patch

* Mon May  7 2007 Karanbir Singh <kbsingh@karan.org> - 0.6.13-1.el5.kb
- Updated to 0.6.13
- Fix for runuser on CentOS-3

* Mon Apr 30 2007 Karanbir Singh <kbsingh@karan.org> - 0.6.12-1.el5.kb.1
- rolled in CentOS Configs
- Added CentOS Default target handling ( most popular target )

* Fri Feb 16 2007 Clark Williams <williams@redhat.com> - 0.6.12-1
- added safety symlink for yum.conf

* Tue Feb  6 2007 Clark Williams <williams@redhat.com> - 0.6.11-1
- added error() calls to print command output on failed commands
- added installdeps command for long-term chroot management

* Mon Jan  8 2007 Clark Williams <williams@redhat.com> - 0.6.10-1
- Added Josh Boyer's EPEL config files

* Tue Nov 21 2006 Clark Williams <williams@redhat.com> - 0.6.9-1
- applied Eric Work's patch to fix defaults vs. command line option problem
  (BZ 215168)
- use /etc/mock/defaults.cfg if --configdir specified and no defaults found
  in the specified configdir
  (BZ 209407)
- applied Jesse Keatings patch for arch specifi config files
  (BZ 213516)

* Mon Nov  6 2006 Jesse Keating <jkeating@redhat.com> - 0.6.8-4
- Fix a couple typos pointing fc6 chroots to fe5.

* Sat Nov  4 2006 Jesse Keating <jkeating@redhat.com> - 0.6.8-3
- Fix a typo in the patch that added x86_64 repos for fc4ppc

* Fri Nov  3 2006 Jesse Keating <jkeating@redhat.com> - 0.6.8-2
- Add patch to fix repo files to use arch specific repos (#213516)

* Mon Oct 30 2006 Clark Williams <williams@redhat.com> - 0.6.8-1
- respun tarballs without buildsys rpms

* Mon Oct 30 2006 Clark Williams <williams@redhat.com> - 0.6.7-1
- updated for FC6 release

* Sat Oct 21 2006 Clark Williams <williams@redhat.com> - 0.6.6-1
- bumped version to 0.6.6 (fixed tarball problem)

* Wed Oct 04 2006 Jesse Keating <jkeating@redhat.com> - 0.6.5-1
- new upstream version to fix #151255

* Tue Aug 29 2006 Jesse Keating <jkeating@redhat.com> - 0.6.4-1
- new upstream version to fix #204051

* Wed Aug 23 2006 Jesse Keating <jkeating@redhat.com> - 0.6.2-1
- new upstream version

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 0.6.1-1
- new upstream version
- Fixes in spec from upstream
 - Added buildsys-build specfile to docs

* Fri Jun 23 2006 Jesse Keating <jkeating@redhat.com> - 0.6-4
- And fix the link syntax.

* Wed Jun 21 2006 Jesse Keating <jkeating@redhat.com> - 0.6-3
- Add patch symlink fedora-6 to development, not 5.

* Tue Jun 20 2006 Jesse Keating <jkeating@redhat.com> - 0.6-1
- New upstream version 0.6

* Tue Mar 21 2006 Dan Williams <dcbw@redhat.com> - 0.4-8
- bump release for fc5/fc6 split

* Tue Mar 21 2006 Dan Williams <dcbw@redhat.com> - 0.4-7
- Update to mock CVS; add symlinks for /dev/std[in|out|err] to buildroots

* Thu Mar  2 2006 Seth Vidal <skvidal at linux.duke.edu> - 0.4-6
- iterate for gcc rebuild and fc5 final

* Tue Jan 24 2006 Dan Williams <dcbw@redhat.com> - 0.4-5
- Back out setpgrp patch, found a better way to do it in plague

* Tue Jan 24 2006 Dan Williams <dcbw@redhat.com> - 0.4-4
- Add option to create new process group so mock and its children
    may be more easily killed

* Wed Jan 18 2006 Dan Williams <dcbw@redhat.com> - 0.4-3
- Add unpackaged files fix from RH#163576 (Adrian Reber)

* Tue Dec 27 2005 Seth Vidal <skvidal@phy.duke.edu>
- add patch from Andreas Thienemann - adds man page

* Tue Aug 16 2005 Matthias Saou <http://freshrpms.net/> 0.4-2
- Fix ?fedora check when not defined (would fail to parse).

* Thu Aug  4 2005 Seth Vidal <skvidal@phy.duke.edu>
- 0.4
- update urls
- add in selinux buildreq and mock-yum file

* Sun Jun 12 2005 Jeremy Katz <katzj@redhat.com> 
- set default.cfg based on both arch and distro built for

* Sat Jun 11 2005 Seth Vidal <skvidal@phy.duke.edu>
- security fix in mock-helper

* Sat Jun 11 2005  Seth Vidal <skvidal@phy.duke.edu>
- mock 0.3 - security release
- mock-helper allowed execution of arbitrary commands by member of mock
  group

* Sun Jun  5 2005 Seth Vidal <skvidal@phy.duke.edu>
- clean up packaging for fedora extras

* Thu May 19 2005 Seth Vidal <skvidal@phy.duke.edu>
- second packaging and backing down the yum ver req

* Sun May 15 2005 Seth Vidal <skvidal@phy.duke.edu>
- first version/packaging
