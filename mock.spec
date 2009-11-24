# next four lines substituted by autoconf
%define major 1
%define minor 0
%define sub 0
%define extralevel %{nil}
%define release_name mock
%define release_version %{major}.%{minor}.%{sub}%{extralevel}

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: Builds packages inside chroots
Name: mock
Version: %{release_version}
Release: 1%{?dist}
License: GPLv2+
Group: Development/Tools
Source: https://fedorahosted.org/mock/attachment/wiki/MockTarballs/%{name}-%{version}.tar.gz
#Patch0: 0001-default-build-arch-to-i586-for-rawhide-to-match-fedo.patch
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
#%patch0 -p1
%if "%{?dist}" == ".fc8"
pushd etc/mock
sed -i -e 's/^#exclude=/exclude=/' -e '/^# The above is not/d' \
    fedora-9-x86_64.cfg fedora-rawhide-x86_64.cfg
popd
%endif

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT/var/lib/mock
mkdir -p $RPM_BUILD_ROOT/var/cache/mock
ln -s consolehelper $RPM_BUILD_ROOT/usr/bin/mock

# compatibility symlinks
# (probably be nuked in the future)
pushd $RPM_BUILD_ROOT/etc/mock
ln -s epel-4-i386.cfg   fedora-4-i386-epel.cfg
ln -s epel-4-ppc.cfg    fedora-4-ppc-epel.cfg
ln -s epel-4-x86_64.cfg fedora-4-x86_64-epel.cfg
ln -s epel-5-i386.cfg   fedora-5-i386-epel.cfg
ln -s epel-5-ppc.cfg    fedora-5-ppc-epel.cfg
ln -s epel-5-x86_64.cfg fedora-5-x86_64-epel.cfg
# more compat, from devel/rawhide rename
ln -s fedora-rawhide-i386.cfg fedora-devel-i386.cfg
ln -s fedora-rawhide-x86_64.cfg fedora-devel-x86_64.cfg
ln -s fedora-rawhide-ppc.cfg fedora-devel-ppc.cfg
ln -s fedora-rawhide-ppc64.cfg fedora-devel-ppc64.cfg
popd

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

# cache dir
%attr(02775, root, mock) %dir /var/cache/mock

%changelog
* Tue Nov 24 2009 David Hrbáč <david@hrbac.cz> - 1.0.0-1
- new upstream release

* Wed Feb 29 2009 Dennis Gilmore <dennis@ausil.us> - 0.9.14-3
- add patch defaulting i386 to build i586 on rawhide 

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Clark Williams <williams@redhat.com> - 0.9.14-1
- logging cleanup (mikem)
- add new exception for resultdir not available (mebrown)
- moved mock cache dir to /var/cache/mock (williams)
- added version variable and version banner to logs (williams)
- removed import of popen2 to whack deprecated message (williams)
- prevent disabling ccache on epel-5 (tmz)
- added configs for sparc and s390 (dgilmore)
- fixed git log command used in build (tmz)
- added copy of spec/sources for building srpms (mebrown)
- changed unlink to rmdir (mebrown)
- set HOME directory globally (mikeb)
- commented out privlege drop in --copyin (williams)

* Thu Nov 06 2008 Jesse Keating <jkeating@redhat.com> - 0.9.13-1
- Add configs for F10 (jkeating)

* Tue Oct 14 2008 Clark Williams <williams@redhat.com> - 0.9.12-1
- internal setarch support for s390/s390x (mikem)
- Refer to the .newkey location of current Fedora 8/9 updates. (jkeating)
- [bz458234] Picked up corrected patch (pmatilai)

* Thu Sep  4 2008 Clark Williams <williams@redhat.com> - 0.9.11-1
- added workarounds for rawhide rpm (BZ 455387 and 458234)
- disabled tmpfs plugin on epel-4-x86_64
- fixed autotools breakage in configure.ac

* Tue May 20 2008 Jesse Keating <jkeating@redhat.com> - 0.9.10-1
- added fix for building F-8 mock (clark)
- Update epel configs

* Tue Apr 22 2008 Jesse Keating <jkeating@redhat.com> - 0.9.9-1
- Update config files for Fedora 9
- Comment out multilib excludes, no longer needed in F9+ with yum multilib changes

* Mon Mar 31 2008 Jesse Keating <jkeating@redhat.com> - 0.9.8-1
- modify rootcache logic to rebuild cache if config files have newer timestamp
- For Fedora 8 and higher, use priority failover method
- Point to the correct static-repo for rawhide stuff.
- Move "devel" to "rawhide" to match current Fedora naming schemes.

* Thu Jan 31 2008 Michael Brown <mebrown@michaels-house.net> - 0.9.7-1
- redo mock.util.do() to use python subprocess module, which should be
  much more maintainable than our old homegrown code.
- Fix exclude= lines once again. Yum fnmatch parser doesnt understand [!x]
  notation
- add --unpriv and --cwd options to run chroot commands without elevated privs
  and in a specific working directory (under the root).
- mount all filesystems when running chroot commands
- remove redundant ccache init since we now source /etc/profile.d/ccache.sh

* Wed Jan 16 2008 Clark Williams <williams@redhat.com> - 0.9.6-1
- renamed configs and put compat symlinks in place
- misc cleanups (whitespace fixes, info messages, etc.)
- tmpfs plugin fix
- split --target and --arch command line arguments
- changed from -l to --login on bash invocations
- create /dev/full in chroot

* Thu Dec 20 2007 Michael Brown <mebrown@michaels-house.net> - 0.9.5-1
- really fix file-based BuildRequires

* Wed Dec 19 2007 Michael Brown <mebrown@michaels-house.net> - 0.9.4-1
- Result dir was not honoring --uniqueext=
- make rpmbuild run under a chroot login shell
- mock is now noarch due to drop of all binary components
- add tmpfs plugin (disabled by default)
- slightly more friendly logs.

* Fri Dec 14 2007 Clark Williams <williams@redhat.com> - 0.9.3-1
- added '--copyin' and '--copyout' modes
- added makeChrootPath() method to Root
- replaced most ad hock usages of .rootdir with makeChrootPath()
- updated man page && added test cases
- added 'help' target to Makefile.am

* Thu Dec 13 2007 Michael Brown <mebrown@michaels-house.net> - 0.9.2-1
- add '--update' mode
- fix '--shell' mode

* Tue Dec 11 2007 Michael Brown <mebrown@michaels-house.net> - 0.9.1-1
- fix 'mock shell' command when passing more than one arg.
- add --orphanskill mode which only does orphankill
- make 'mock --shell' noninteractive and logged to root.log
- fix for file-based BuildRequires
- add sparcs to constant list for auto-setarch

* Tue Dec 11 2007 Michael Brown <mebrown@michaels-house.net> - 0.8.17-1
- fix 'mock shell' command when passing more than one arg.
- add --orphanskill mode which only does orphankill
- make 'mock --shell' noninteractive and logged to root.log
- fix for file-based BuildRequires
- add sparcs to constant list for auto-setarch

* Sun Dec 09 2007 Michael Brown <mebrown@michaels-house.net> - 0.9.0-1
- drop suid helper and use consolehelper instead.
- add unshare() call rather than clone(CLONE_NEWNS...)

* Sun Dec 09 2007 Michael Brown <mebrown@michaels-house.net> - 0.8.16-1
- drop FC6 configs. FC6 no longer supported
- add --trace cmdline parameter
- make logs slightly less verbose

* Wed Dec 05 2007 Michael Brown <mebrown@michaels-house.net> - 0.8.15-1
- fix traceback when root cache doesnt exist.
- add "--with", "--without", and "--define" cmdline parameters which are passed
  to rpmbuild (courtesy Todd Zullinger)

* Tue Dec 04 2007 Michael Brown <mebrown@michaels-house.net> - 0.8.14-1
- fix traceback when cache dir was not found

* Tue Dec 04 2007 Michael Brown <mebrown@michaels-house.net> - 0.8.13-1
- brown-paper-bag bug where built rpm didnt work due to lack of path 
  substitution in mock.py

* Mon Dec 03 2007 Michael Brown <mebrown@michaels-house.net> - 0.8.12-1
- fix builds of multiple srpms
- fix 'mock install'
- use python-decoratortools for better python 2.3 back compat

* Thu Nov 29 2007 Clark Williams <williams@redhat.com> - 0.8.11-1
- fixes from mebrown:
-   added back -q and -v flags
-   print yum output by default
-   added --offline option
-   cleaned up uid handling

* Mon Nov 26 2007 Michael Brown <mebrown@michaels-house.net> - 0.8.10-1
- fix 'shell' command
- fix a couple different selinux avc denial messages (didnt affect functionality)

* Tue Nov 20 2007 Michael Brown <mebrown@michaels-house.net> - 0.8.9-1
- Fixes so that mock will run cleanly on RHEL5
- Add glib-devel.i386, glib2-devel.i386 to yum exclude list as it breaks
  builds.
- Add backwards-compatibility code for old-style 'automatically assume rebuild'
  convention
- automake symlink accidentally included in tarball rather than file
  (py-compile)
- update manpage

* Mon Nov 19 2007 Michael Brown <mebrown@michaels-house.net> - 0.8.8-1
- make it run correctly when called by the 'root' user
- internal_setarch: optionally run 'setarch' internally. This
  eliminates the need to run "setarch i386 mock ..." when building on
  target_arch != build_arch. This is turned on by default. Limitations:
  must have 'ctypes' python module available, which is only available
  by default in python 2.5, or as an extension module in <= 2.4.
  If the 'ctypes' module is not available, this feature will be
  disabled and you must manually run 'setarch'.
- Does not run 'clean' action for 'shell', 'chroot', 'install', or
  'installdeps' (docs updated)
- fix build for top_builddir != top_srcdir
- fix 'installdeps' so that it works with both rpms/srpms
- missing device file /dev/ptmx was causing 'expect' command to always
  fail. Affected any SRPM build that used 'expect'.
- hard spec file dep on python >= 2.4 due to python syntax changes.
- resultdir can now contain python-string substitutions for any
  variable in the chroot config.
  rebuild my.src.rpm
- add 'dist' variable to all chroot config files so that it is
  available for resultdir substitutions.
- give good error message when logging.ini cannot be found.
- change default logging format to remove verbosity from build.log.
- make logging format configurable from defaults.cfg or chroot cfg.
- less verbose state.log format

* Mon Oct 22 2007 Michael Brown <mebrown@michaels-house.net> - 0.8.4-1
- fix reported 'bad owner/group' from rpm in some configurations.

* Mon Oct 22 2007 Michael Brown <mebrown@michaels-house.net> - 0.8.3-1
- BZ# 336361 -- cannot su - mockbuild
- BZ# 326561 -- update manpage
- BZ# 235141 -- error with immutable bit

* Fri Oct 20 2007 Michael Brown <mebrown@michaels-house.net> - 0.8.0-1
- huge number of changes upstream
- convert to setuid wrapper instead of old setuid helper
- lots of bugfixes and improvements
- /var/cache/yum now saved and bind-mounted
- ccache integration
- rootcache improvements (formerly called autocache)

* Mon Aug 27 2007 Michael Brown <mebrown@michaels-house.net> - 0.7.6-1
- ensure /etc/hosts is created in chroot properly

* Mon Aug 13 2007 Clark Williams <williams@redhat.com> - 0.7.5-2
- build fix from Roland McGrath to fix compile of selinux lib

* Wed Aug 8 2007 Clark Williams <williams@redhat.com> - 0.7.5-1
- orphanskill feature (BZ#221351)

* Wed Aug 8 2007 Michael Brown <mebrown@michaels-house.net> - 0.7.5-1
- add example configs to defaults.cfg
- dont rebuild cache if not clean build (BZ#250425)

* Wed Jul 18 2007 Michael Brown <mebrown@michaels-house.net> - 0.7.4-1
- return child exit status, so we properly report subcommand failures

* Fri Jul  6 2007 Michael Brown <mebrown@michaels-house.net> - 0.7.3-1
- remove redundant defaults.cfg entries.

* Wed Jun 20 2007 Michael Brown <mebrown@michaels-house.net> - 0.7.2-1
- fix exclude list
- remove legacy configs
- disable 'local' repos by default (koji-repos)

* Wed Jun 13 2007 Michael Brown <mebrown@michaels-house.net> - 0.7.1-1
- Fix problem with autocache where different users couldnt share same cache
- Fix problem creating resolv.conf in rootfs
- cleanup perms on rootfs /etc/

* Tue Jun 12 2007 Michael Brown <mebrown@michaels-house.net> - 0.7.1-1
- add EPEL 5 config files

* Mon Jun 11 2007 Clark Williams <williams@redhat.com> - 0.7-1
- fixed bind mount problems
- added code to allow multiple users to use --no-clean
- merged mock-0-6-branch to head and changed version

* Thu Jun  7 2007 Clark Williams <williams@redhat.com> - 0.6.17-1
- added F-7 config files (BZ#242276)
- modified epel configs for changed mirrorlist location (BZ#239981)
- added bind mount of /dev (BZ#236428)
- added copy of /etc/resolv.conf to chroot (BZ#237663 and BZ#238101)

* Tue May 01 2007 Clark Williams <williams@redhat.com> - 0.6.16-1
- timeout code adds new cmdline option that will kill build process after
  specified timeout. Useful for automated builds of things that may hang during
  build and you just want it to fail.

* Tue Apr 10 2007 Clark Williams <williams@redhat.com> - 0.6.15-1
- Fixed typo in FC4 -epel configs (BZ 235490)

* Sat Feb 24 2007 Clark Williams <williams@redhat.com> - 0.6.14-1
- Ville Skyttä's fix for RPM_OPT_FLAGS (BZ 226673)

* Tue Feb 20 2007 Clark Williams <williams@redhat.com> - 0.6.13-1
- Handle --no-clean option when doing yum.conf symlink (BZ 230824)

* Fri Feb 16 2007 Clark Williams <williams@redhat.com> - 0.6.12-1
- added safety symlink for yum.conf

* Wed Feb  7 2007 Clark Williams <williams@redhat.com> - 0.6.11-1
- added error() calls to print command output on failed commands

* Tue Feb  6 2007 Clark Williams <williams@redhat.com> - 0.6.11-1
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

* Mon Oct 30 2006 Clark Williams <williams@redhat.com> - 0.6.8-1
- respun tarballs without buildsys rpms

* Mon Oct 30 2006 Clark Williams <williams@redhat.com> - 0.6.7-1
- updated for FC6 release

* Sat Oct 21 2006 Clark Williams <williams@redhat.com> - 0.6.6-1
- bumped version to 0.6.6 (fixed tarball problem)

* Mon Sep 11 2006 Clark Williams <williams@redhat.com> - 0.6.5-1
- changed version number for patch from Karanbir Singh
  (rpm workaround on CentOS 4.4)

* Tue Aug 29 2006 Clark Williams <williams@redhat.com> - 0.6.3-1
- changed version number to indicate fix for bz 204051

* Tue Aug 29 2006 Clark Williams <williams@redhat.com> - 0.6.2-2
- bumped revision for bz 204051

* Wed Aug 23 2006 Clark Williams <williams@redhat.com> - 0.6.2-1
- Updated README
- Fixed link problem in etc/Makefile
- Bumped version number

* Wed Aug 16 2006 Clark Williams <williams@redhat.com>
- Added buildsys-build specfile to docs
- Added disttag
- Bumped release number

* Wed Jun  7 2006 Seth Vidal <skvidal at linux.duke.edu>
- version update

* Tue Apr 11 2006 Seth Vidal <skvidal at linux.duke.edu>
- specfile version iterate

* Tue Dec 27 2005 Seth Vidal <skvidal@phy.duke.edu>
- add patch from Andreas Thienemann - adds man page

* Sat Jun 11 2005 Seth Vidal <skvidal@phy.duke.edu>
- security fix in mock-helper

* Sun Jun  5 2005 Seth Vidal <skvidal@phy.duke.edu>
- clean up packaging for fedora extras

* Thu May 19 2005 Seth Vidal <skvidal@phy.duke.edu>
- second packaging and backing down the yum ver req

* Sun May 15 2005 Seth Vidal <skvidal@phy.duke.edu>
- first version/packaging

