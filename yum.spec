%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: RPM installer/updater
Name: yum
Version: 3.2.19
Release: 18%{?dist}.3
License: GPLv2+
Group: System Environment/Base
Source0: http://linux.duke.edu/projects/yum/download/3.2/%{name}-%{version}.tar.gz
Source1: yum.conf.centos
Source2: yum-updatesd.conf.fedora

#  See: http://people.redhat.com/jantill/gits/yum branch el-5.3-master
# and the el5.3* branches for the individual patches.

# Fedora patches we might as well carry
Patch0: installonlyn-enable.patch
Patch1: yum-mirror-priority.patch
Patch2: yum-manpage-files.patch
Patch3: yum-ia64-multilib.patch
# NOTE: We don't carry this as it'd change the policy mid cycle
# Patch3: yum-multilib-policy-best.patch

# Work around python-2.4.z's gettext ... maybe not needed post 5.3
Patch102: yum-hack-python-gettext-workaround.patch
# SSL, although it's still done in RHN-plugin
Patch103: yum-ssl-ca-cert.patch

# Python-2.* is just too sucky to enable this
Patch104: yum-i18n-off.patch

# Minor post 3.2.19 release changes (probably almost 3.2.20)
Patch105: yum-exclude-arch-obs.patch
Patch106: yum-configparser-compat.patch
Patch107: yum-search-full-arch.patch
Patch108: yum-rm-only-ts.patch
Patch109: yum-install-single-provider.patch
Patch110: yum-total-download-cb-log.patch
Patch111: yum-complete-trans-warn.patch
Patch112: yum-large-patterns-speed-fix.patch
Patch113: yum-includepkgs-speed-fix.patch
Patch114: yum-loaded-plugins-ui.patch
Patch115: yum-dynamic-columns-ui.patch
Patch116: yum-check-signals-exit.patch
Patch117: yum-wrap-rpm-callbacks.patch
Patch118: yum-rpm-no-progress-quiet.patch
Patch119: yum-timestamp_check.patch
Patch120: yum-shell-repo-manpage.patch
Patch121: yum-shell-rm+inst.patch
Patch122: yum-i18n-info.patch

Patch900: yum-C4-3.2.19-allowrun.patch
Patch901: yum-C4-3.2.19-allowrun2.patch
Patch902: yum-C4-3.2.19-allowrun3.patch


URL: http://linux.duke.edu/yum/
BuildArchitectures: noarch
BuildRequires: python
BuildRequires: gettext
BuildRequires: intltool
Conflicts: pirut < 1.1.4
#Requires: python >= 2.4, rpm-python, rpm >= 0:4.4.2
Requires: python, rpm-python, rpm
Requires: python-iniparse
Requires: python-sqlite
Requires: urlgrabber >= 3.1.0
Requires: python-elementtree
Requires: yum-fastestmirror
# Make sure metadata code is updated too
Requires: yum-metadata-parser >= 1.1.0
Conflicts: yum-rhn-plugin < 0.5.2-1.el5
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes: yum-skip-broken
Conflicts: yum-skip-broken
Obsoletes: yum-basearchonly
Obsoletes: yum-repolist
Conflicts: yum-basearchonly
# yum-complete-transaction from 1.1.10-9.el5 has problems:
Conflicts: yum-utils < 1.1.16-11
# We don't require this in RHEL, although it'll use it if you have it
# suggests would be ok, if it worked and if pygpgme wasn't in EPEL :).
# Requires: pygpgme

%description
Yum is a utility that can check for and automatically download and
install updated RPM packages. Dependencies are obtained and downloaded 
automatically prompting the user as necessary.

%package updatesd
Summary: Update notification daemon
Group: Applications/System
Requires: yum = %{version}-%{release}
Requires: dbus-python
Requires: pygobject2
Requires(preun): /sbin/chkconfig
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(post): /sbin/service

%description updatesd
yum-updatesd provides a daemon which checks for available updates and 
can notify you when they are available via email, syslog or dbus. 

%prep
%setup -q

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%patch102 -p1
%patch103 -p1

%patch104 -p1

%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1
%patch115 -p1
%patch116 -p1
%patch117 -p1
%patch118 -p1
%patch119 -p1
%patch120 -p1
%patch121 -p1
%patch122 -p1

%patch900 -p1
%patch901 -p1
%patch902 -p1

%build
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/yum.conf

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/yum/pluginconf.d $RPM_BUILD_ROOT/usr/lib/yum-plugins

# for now, move repodir/yum.conf back
mv $RPM_BUILD_ROOT/%{_sysconfdir}/yum/repos.d $RPM_BUILD_ROOT/%{_sysconfdir}/yum.repos.d
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/yum/yum.conf

# yum-updatesd has moved to the separate source version
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/yum/yum-updatesd.conf 
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/yum-updatesd
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/dbus-1/system.d/yum-updatesd.conf
rm -f $RPM_BUILD_ROOT/%{_sbindir}/yum-updatesd
rm -f $RPM_BUILD_ROOT/%{_mandir}/man*/yum-updatesd*

rm -f $RPM_BUILD_ROOT/%{_datadir}/yum-cli/yumupd.py*

%find_lang %name

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-, root, root, -)
%doc README AUTHORS COPYING TODO INSTALL ChangeLog
%config(noreplace) %{_sysconfdir}/yum.conf
%dir %{_sysconfdir}/yum
%dir %{_sysconfdir}/yum.repos.d
%config(noreplace) %{_sysconfdir}/logrotate.d/yum
%dir %{_datadir}/yum-cli
%{_datadir}/yum-cli/*
%{_bindir}/yum
%{python_sitelib}/yum
%{python_sitelib}/rpmUtils
%dir /var/cache/yum
%dir /var/lib/yum
%{_mandir}/man*/yum.*
%{_mandir}/man*/yum-shell*
# plugin stuff
%dir %{_sysconfdir}/yum/pluginconf.d 
%dir /usr/lib/yum-plugins

%changelog
* Fri Jan 22 2010 David Hrbáč <david@hrbac.cz> - 3.2.19-18.el4.hrb.3
- improved patch

* Fri Jan 22 2010 David Hrbáč <david@hrbac.cz> - 3.2.19-18.el4.hrb.2
- better patch

* Fri Jan 22 2010 David Hrbáč <david@hrbac.cz> - 3.2.19-18.el4.hrb.1
- fixed patch

* Fri Jul 10 2009 David Hrbáč <david@hrbac.cz> - 3.2.19-18.el4.hrb
- initial rebuild
- drop python >= 2.4, rpm-python, rpm >= 0:4.4.2

* Thu Jan 22 2009 Karanbir Singh <kbsingh@centos.org> - 3.2.19-18.el5.centos
- Make yum require fastestmirror
- Obsolete for yum-repolist ( no longer needed )

* Tue Nov 25 2008 James Antill <jantill@redhat.com> - 3.2.19-18
- Fix utf8 in redhat-logos license
- Resolves: rhbz#472375

* Mon Nov 10 2008 James Antill <jantill@redhat.com> - 3.2.19-16
- Fix ia64 multilib for RHEL-5
- Resolves: rhbz#469271

* Tue Oct 28 2008 James Antill <jantill@redhat.com> - 3.2.19-14
- Fix yum shell when doing remove commands first.
- Resolves: rhbz#468754

* Thu Oct 23 2008 James Antill <jantill@redhat.com> - 3.2.19-13
- Add the timestamp_check option, so we can have repoids to random stuff
- Resolves: rhbz#466176
- Fix yum shell man page for repo command.
- Resolves: rhbz#467415
- Resolves: rhbz#454882

* Thu Oct 16 2008 James Antill <jantill@redhat.com> - 3.2.19-11
- Don't show rpm progress when in super quiet mode
- Resolves: rhbz#466911
- Resolves: rhbz#454882

* Mon Sep 29 2008 James Antill <jantill@redhat.com> - 3.2.19-10
- Fix/hide exceptions on rpm callbacks, to make rpm happier.
- Resolves: rhbz#463447
- Resolves: rhbz#454882

* Fri Sep 19 2008 James Antill <jantill@redhat.com> - 3.2.19-9
- Fix typo in checkSignals, we rpm has got a signal.
- Resolves: rhbz#462784
- Resolves: rhbz#454882

* Tue Sep 16 2008 James Antill <jantill@redhat.com> - 3.2.19-8
- Allow yum remove to work without downloading pkgSack MD.
- Only install a single package from a provider.
- Fix total download cb to use the logger.
- Add incomplete transactions warning.
- Speed fix for large patterns (notably large package name excludes).
- Speed fix for includepkgs.
- UI tweak for loaded plugins line.
- Dynamic columns support and list/groupinfo-v changes to use it.
- Add conflicts as well as obsoletes, so you can't reinstall skip-broken.
- Resolves: rhbz#462086
- Resolves: rhbz#454882

* Fri Aug 29 2008 James Antill <jantill@redhat.com> - 3.2.19-6
- Fix list searches for name.arch
- Resolves: rhbz#454882

* Thu Aug 28 2008 James Antill <jantill@redhat.com> - 3.2.19-5
- Fix minor API gitch in 3.2.19
- Obsolete yum-skip-broken, so it auto goes away on update
- Resolves: rhbz#454882

* Wed Aug 27 2008 James Antill <jantill@redhat.com> - 3.2.19-4
- Fix minor API gitch in 3.2.19
- Resolves: rhbz#454882

* Tue Aug 26 2008 James Antill <jantill@redhat.com> - 3.2.19-2
- Import next upstream 3.2.19.
- What will be in Fedora 9 soon.
- Resolves: rhbz#454882

* Wed Aug  6 2008 James Antill <jantill@redhat.com> - 3.2.17-0_beta_18_2
- Import next upstream 3.2.18 beta.
- What will be in Fedora 9 soon.
- Lots of bug fixes, changes for gpgcheck/repo_gpgcheck/update-minimal/etc.
- Resolves: rhbz#454882

* Mon Jul 21 2008 James Antill <jantill@redhat.com> - 3.2.17-0_beta_18_1
- Import upstream 3.2.18 beta.
- What will be in Fedora 9 soon.
- Resolves: rhbz#454882

* Mon Mar 24 2008 James Antill <jantill@redhat.com> - 3.2.8-10
- Allow URLs to work as arguments to -c (config. file)
- Resolves: rhbz#447271

* Mon Mar 24 2008 James Antill <jantill@redhat.com> - 3.2.8-9
- Minor man page fix
- Resolves: rhbz#438168
- Multilib arch problem fix
- Resolves: rhbz#437429

* Tue Mar 11 2008 James Antill <jantill@redhat.com> - 3.2.8-8
- Re-add the ssl-ca-cert patch
- Resolves: rhbz#436804
- Add unused patterns argument
- Resolves: rhbz#319491

* Thu Feb 21 2008 James Antill <jantill@redhat.com> - 3.2.8-7
- Hacky workaround for python split gettext bug.
- Resolves: rhbz#431073

* Sun Feb  3 2008 James Antill <jantill@redhat.com> - 3.2.8-6
- Tweak config. file for 3.2.8
- Resolves: rhbz#237773
- Set HTTP user-agent to specify this is yum, and which verison
- Resolves: rhbz#319461
- Create logdir if it doesn't exist.
- Resolves: rhbz#253960
- Add committer/comittime
- Relates: rhbz#319491


* Tue Jan 22 2008 James Antill <jantill@redhat.com> - 3.2.8-5
- Import some of the returnPackages() changes, to fix len() == -1 bug with
- some repos. And missing import sqlutils.
- Resolves: rhbz#429751

* Fri Jan 18 2008 James Antill <jantill@redhat.com> - 3.2.8-4
- Workaround the worst behaviour of yum install kernel.
- Import Fedora 8 yum base.
- Add lots of small bug fix patches from 3.2.9
- Resolves: rhbz#384691

* Wed Jan 10 2007 Jeremy Katz <katzj@redhat.com> - 3.0.1-5
- fix for 'yum localinstall' with multiarch (#220682)

* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 3.0.1-4
- revert to older version of rpmsack to not repeatedly open the rpmdb to 
  avoid problems (Related: #217285, #213963)

* Tue Nov 14 2006 Peter Jones <pjones@redhat.com> - 3.0.1-3
- don't consider arch when getting newest packages in a list (#212626)

* Fri Nov 10 2006 Jeremy Katz <katzj@redhat.com> - 3.0.1-2
- yum-updatesd fixes (#213622, #212494, #212507)
- sslcacert option (jbowes, #210977)

* Fri Nov  3 2006 Jeremy Katz <katzj@redhat.com> - 3.0.1-1
- update to 3.0.1

* Fri Oct 13 2006 Paul Nasrat <pnasrat@redhat.com> - 3.0-6
- fix package comparison for available packages

* Thu Oct 12 2006 Jeremy Katz <katzj@redhat.com> - 3.0-5
- fix traceback when syslog not available (#208773)
- fix package comparison not properly handling different arches (#210316)

* Tue Oct 10 2006 Jeremy Katz <katzj@redhat.com> - 3.0-4
- fix traceback on package download error (#210135, #210181, #210115)

* Thu Oct  5 2006 Jeremy Katz <katzj@redhat.com> - 3.0-3
- fix traceback referencing var (#209471)
- add dgregor's basepath patch

* Thu Oct  5 2006 Jeremy Katz <katzj@redhat.com> - 3.0-2
- fix traceback in yum-updatesd

* Wed Oct  4 2006 Jeremy Katz <katzj@redhat.com> - 3.0-1
- 3.0 

* Fri Sep 29 2006 Jeremy Katz <katzj@redhat.com> - 2.9.8-1
- update to 2.9.8 with the past two fixes as well as fixes for 
  exclude/include lines in config files

* Thu Sep 28 2006 Jeremy Katz <katzj@redhat.com> - 2.9.7-4
- fix trying to reget existing files (#208460)

* Wed Sep 27 2006 Jeremy Katz <katzj@redhat.com> - 2.9.7-3
- and better fix for upstream (jbowes)

* Wed Sep 27 2006 Jeremy Katz <katzj@redhat.com> - 2.9.7-2
- backout patch that breaks anaconda

* Wed Sep 27 2006 Jeremy Katz <katzj@redhat.com> - 2.9.7-1
- update to 2.9.7

* Thu Sep 21 2006 James Bowes <jbowes@redhat.com> - 2.9.6-2
- Remove unused imports in installonlyn

* Wed Sep  6 2006 Jeremy Katz <katzj@redhat.com> - 2.9.6-1
- update to 2.9.6

* Tue Sep  5 2006 Jeremy Katz <katzj@redhat.com> - 2.9.5-5
- update to current CVS snap (20060906) in advance of the final 2.9.6 tarball
- bring back the installonlyn fixes 

* Thu Aug 31 2006 Jeremy Katz <katzj@redhat.com> - 2.9.5-4
- revert installonlyn changes; they require changes that will only be in 2.9.6

* Wed Aug 30 2006 Jeremy Katz <katzj@redhat.com> - 2.9.5-3
- fix deprecation warnings in installonlyn (Jack Neely)

* Thu Aug 24 2006 Jeremy Katz <katzj@redhat.com> - 2.9.5-2
- add patch to fix case of an empty rpmdb (eg, at install time #204005)

* Wed Aug 23 2006 Jeremy Katz <katzj@redhat.com> - 2.9.5-1
- update to 2.9.5

* Fri Aug 18 2006 Chris Lumens <clumens@redhat.com> 2.9.4-4
- Add patch to fix pattern matching (#202974).

* Fri Aug 18 2006 Karsten Hopp <karsten@redhat.com> - 2.9.4-3
- revert last change

* Thu Aug 17 2006 Karsten Hopp <karsten@redhat.com> - 2.9.4-2
- Requires: libxml2-python for updatesd subpackage

* Wed Aug  9 2006 Jeremy Katz <katzj@redhat.com> - 2.9.4-1
- update to 2.9.4 (including logging fixes, gpg checking fix, 
  and fixes for #200901, #200346, #189483)

* Mon Jul 24 2006 Florian La Roche <laroche@redhat.com> - 2.9.3-2
- add patch to not require /dev/log (not present in chroots) #199558

* Wed Jul 12 2006 Jeremy Katz <katzj@redhat.com> - 2.9.3-1
- update to 2.9.3
- add fix for taking the yum lock more than once and a variable typo from CVS

* Wed Jul  5 2006 Jeremy Katz <katzj@redhat.com> - 2.9.2-3
- few other little api fixes (#197603, #197607)

* Mon Jul  3 2006 Jeremy Katz <katzj@redhat.com> - 2.9.2-2
- fix tyop (#197398)

* Wed Jun 28 2006 Jeremy Katz <katzj@redhat.com> - 2.9.2-1
- update to 2.9.2

* Tue Jun 27 2006 Jeremy Katz <katzj@redhat.com> - 2.9.1-2
- move yum-updatesd into a subpackage
- no longer ship the yum update cronjob, yum-updatesd can do this instead

* Tue Jun 20 2006 Jeremy Katz <katzj@redhat.com> - 2.9.1-1
- update to 2.9.1

* Mon Jun 19 2006 Paul Nasrat <pnasrat@redhat.com> - 2.9.0-8
- Fix resolvedeps

* Thu Jun 15 2006 Bill Nottingham <notting@redhat.com> 2.9.0-7
- require pygobject2 (for yum-updatesd)

* Thu Jun 15 2006 Chris Lumens <clumens@redhat.com> 2.9.0-6
- Fix compareEVR traceback.

* Wed Jun 14 2006 Paul Nasrat <pnasrat@redhat.com> - 2.9.0-5
- Various fixups (key grab and importing, composite exception handling)

* Tue Jun 13 2006 Jeremy Katz <katzj@redhat.com> - 2.9.0-4
- install yum-updatesd bits

* Tue Jun 13 2006 Jeremy Katz <katzj@redhat.com> - 2.9.0-3
- add patch to fix filelist crash installing/querying the filesystem package
- add patch to fix excludes

* Mon Jun 12 2006 Jeremy Katz <katzj@redhat.com> - 2.9.0-2
- add patch for mirror errors

* Mon Jun 12 2006 Jeremy Katz <katzj@redhat.com> - 2.9.0-1
- update to 2.9.0, require C-based metadata parser to speed things up

* Mon Jun  5 2006 Jeremy Katz <katzj@redhat.com> - 2.6.1-4
- handle PAE kernels in installonlyn (#194064)

* Thu May 25 2006 Paul Nasrat <pnasrat@redhat.com> - 2.6.1-3
- Rebuild with patch

* Wed May 24 2006 Paul Nasrat <pnasrat@redhat.com> - 2.6.1-2
- backport mirror failure callback 

* Wed Apr 26 2006 Jeremy Katz <katzj@redhat.com> - 2.6.1-1
- update to 2.6.1 with fixes for #181406, #185309, #161190, #185946

* Tue Apr 18 2006 Jeremy Katz <katzj@redhat.com> - 2.6.0-3
- more proxy fixing for non CLI use case (#185309)

* Mon Apr 10 2006 Jeremy Katz <katzj@redhat.com> - 2.6.0-2
- add fix for xen0/xenU kernels in installonlyn (#187894)
- add fix for proxies with the mirror list (#161190)

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 2.6.0-1
- update to 2.6.0 final containing fix for #176257

* Fri Mar 03 2006 Paul Nasrat <pnasrat@redhat.com> - 2.5.3-5
- Add support for patterns in YumBase.install()

* Thu Mar 02 2006 Paul Nasrat <pnasrat@redhat.com> - 2.5.3-4
- Cover pkg then group selection in conditional group support (#181858)

* Thu Mar 02 2006 Paul Nasrat <pnasrat@redhat.com> - 2.5.3-3
- Conditional group support (#181858)

* Fri Feb 24 2006 Jeremy Katz <katzj@redhat.com> - 2.5.3-2
- fix installyonlyn bug with tokeep > 2 (#176704)

* Wed Feb 22 2006 Jeremy Katz <katzj@redhat.com> - 2.5.3-1
- Update to 2.5.3 with fixes for lots of stuff (and all of our patches applied)
  (#177528, #177737, #179512, others)

* Fri Feb 10 2006 Paul Nasrat <pnasrat@redhat.com> - 2.5.1-5
- Merge patches from head for group plugin support and conditionals

* Fri Feb 03 2006 Paul Nasrat <pnasrat@redhat.com> - 2.5.1-4
- Fix group unselect traceback (cf #177737)

* Tue Jan 31 2006 Paul Nasrat <pnasrat@redhat.com> - 2.5.1-3
- Merge upstream patches (sortabletransactiondata, grouplists)

* Sun Jan 15 2006 Paul Nasrat <pnasrat@redhat.com> - 2.5.1-2
- Fix group removal traceback (#177737)

* Sun Jan  8 2006 Jeremy Katz <katzj@redhat.com> - 2.5.1-1
- seth loves me and made a 2.5.1 release.  so no cvs snap for you! 

* Sun Jan  8 2006 Jeremy Katz <katzj@redhat.com> - 2.5.1-0.20060108
- update to CVS snap

* Wed Dec 21 2005 Paul Nasrat <pnasrat@redhat.com> - 2.5.0-5
- Make txmbr hashable (#175975)

* Fri Dec 16 2005 Paul Nasrat <pnasrat@redhat.com> - 2.5.0-4
- Fix for KeyError when no location['base']

* Wed Dec 14 2005 Jeremy Katz <katzj@redhat.com> - 2.5.0-3
- better mirrorlist fix

* Wed Dec 14 2005 Jeremy Katz <katzj@redhat.com> - 2.5.0-2
- revert installyonlyn change that wasn't supposed to get committed
- better fix for #175647 that doesn't cause tracebacks when deps 
  need updating too
- fix mirrorlist corruption (#175436)

* Tue Dec 13 2005 Jeremy Katz <katzj@redhat.com> - 2.5.0-1
- update to 2.5.0
- add patch for traceback in #175647

* Sat Dec 10 2005 Jeremy Katz <katzj@redhat.com> - 2.5.0-0.20051210
- update to newer CVS

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Dec  7 2005 Jeremy Katz <katzj@redhat.com> - 2.5.0-0.20051207
- update to cvs snap for new group code and lots of other stuff

* Tue Dec  6 2005 Jeremy Katz <katzj@redhat.com> - 2.4.1-3
- ... and actually apply the patch

* Mon Dec  5 2005 Jeremy Katz <katzj@redhat.com> - 2.4.1-2
- add Panu's patch for cachecookie cleaning (#174715)
- change default cache time to 30 minutes to match new upstream

* Wed Nov 30 2005 Jeremy Katz <katzj@redhat.com> - 2.4.1-1
- update to 2.4.1
- add PLUGINS to the docs
- fix another installonlyn bug (#174001)

* Wed Nov 16 2005 Jeremy Katz <katzj@redhat.com> - 2.4.0-14
- really fix kernel-smp-devel

* Fri Nov 11 2005 Jeremy Katz <katzj@redhat.com> - 2.4.0-13
- handle installonlypkgs in provides too to handle, eg, 
  kernel-smp-devel (#172981)

* Thu Nov 10 2005 Jeremy Katz <katzj@redhat.com> - 2.4.0-12
- fix problem with custom kernel names in installonlyn (#172855)
- make it more obvious how to add more tokeep with installonlyn

* Wed Nov 09 2005 Paul Nasrat <pnasrat@redhat.com> - 2.4.0-11
- Expose location base from metadata

* Tue Nov  8 2005 Jeremy Katz <katzj@redhat.com> - 2.4.0-10
- fix problem in installonlyn that caillon hit where removing kernels 
  would trigger instead of only happening on update/install of kernels
- make plugin config files noreplace

* Mon Nov  7 2005 Jeremy Katz <katzj@redhat.com> - 2.4.0-9
- enable plugins by default
- add installyonlyn plugin so that we only keep two kernels around by default

* Mon Oct 24 2005 Jeremy Katz <katzj@redhat.com> - 2.4.0-8
- drop macro patch
- more fixes for returnByName* stuff -- need to leave best arch selection
  to the caller

* Sun Oct 23 2005 Paul Nasrat <pnasrat@redhat.com> - 2.4.0-7
- Drop anaconda flag patch
- Fix ppc64pseries/iseries basearch substitution

* Thu Oct 06 2005 Paul Nasrat <pnasrat@redhat.com> - 2.4.0-6
- Backport transaction constants
- Allow setting anaconda flag

* Tue Oct  4 2005 Jeremy Katz <katzj@redhat.com>
- add dirs for plugins

* Tue Sep 27 2005 Jeremy Katz <katzj@redhat.com> - 2.4.0-5
- add yum-cli dir (#169334)

* Wed Sep 21 2005 Jeremy Katz <katzj@redhat.com> - 2.4.0-4
- make returnByName* be consistent in what it returns (#168712)

* Fri Sep 16 2005 Jeremy Katz <katzj@redhat.com> - 2.4.0-3
- add two patches for anaconda that have been committed upstream
  * allow removal of packages from transaction
  * support search by name with sqlite

* Thu Sep 01 2005 Paul Nasrat <pnasrat@redhat.com> - 2.4.0-2
- Initial version of macro support patch

* Tue Aug 16 2005 Jeremy Katz <katzj@redhat.com> - 2.4.0-1
- update to 2.4.0

* Fri Jul  8 2005 Jeremy Katz <katzj@redhat.com> - 2.3.4-1
- update to 2.3.4
- use %%{python_sitelib} in the file list

* Wed Jun 15 2005 Jeremy Katz <katzj@redhat.com> - 2.3.3-1
- update to 2.3.3

* Wed May 25 2005 Paul Nasrat <pnasrat@redhat.com> - 2.3.2-7
- Drop erase reversal patch 

* Tue May 24 2005 Paul Nasrat <pnasrat@redhat.com> - 2.3.2-6
- Erase/remove reversing for yum cli (#158577)

* Tue May 24 2005 Jeremy Katz <katzj@redhat.com> - 2.3.2-5
- allow multiple packages _providing_ kernel-devel (or any installonlypkgs) 
  to be installed (#155988)

* Mon May 23 2005 Jeremy Katz <katzj@redhat.com> - 2.3.2-4
- fix traceback on out of disk space error

* Fri May 20 2005 Jeremy Katz <katzj@redhat.com> - 2.3.2-3
- add fixes from Seth for the shell to run depsolve and to clean up 
  output somewhat (#158267)

* Thu May  5 2005 Jeremy Katz <katzj@redhat.com> - 2.3.2-2
- handle ppc64/sparc64 "correctly"

* Mon Apr  4 2005 Jeremy Katz <katzj@redhat.com> - 2.3.2-1
- update to 2.3.2, now requires python-elementtree for xml parsing

* Tue Mar 15 2005 Jeremy Katz <katzj@redhat.com> - 2.3.1-3
- add patch from gijs for sqlite changes

* Mon Mar 14 2005 Florian La Roche <laroche@redhat.com>
- python-sqlite3 -> python-sqlite

* Mon Mar  7 2005 Jeremy Katz <katzj@redhat.com> - 2.3.1-1
- update to 2.3.1
- urlgrabber is split out into its own package now
- require python-sqlite3

* Tue Feb 22 2005 Jeremy Katz <katzj@redhat.com> - 2.3.0-2
- fix the duplicate repos with the same id bug

* Mon Feb 21 2005 Jeremy Katz <katzj@redhat.com> - 2.3.0-1
- update to 2.3.0

* Tue Jan 25 2005 Jeremy Katz <katzj@redhat.com> - 2.1.13-1
- update to 2.1.13

* Sat Jan 22 2005 Jeremy Katz <katzj@redhat.com> - 2.1.12-2
- allow multiple kernel-devel packages to be installed

* Wed Jan 12 2005 Florian La Roche <laroche@redhat.com>
- add small patch to fix dep reporting

* Mon Nov 29 2004 Jeremy Katz <katzj@redhat.com> - 2.1.12-1
- update to 2.1.12
- add hack from jbj to workaround python 2.4 urllib breakage (#138535)

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 2.1.11-4
- rebuild for python 2.4

* Sun Oct 31 2004 Bill Nottingham <notting@redhat.com> - 2.1.11-3
- fix multilib update patch to allow installing noarch (#135396, continued)

* Fri Oct 29 2004 Jeremy Katz <katzj@redhat.com> - 2.1.11-2
- add patch to fix multilib updates on ia32e (#135396)

* Thu Oct 28 2004 Jeremy Katz <katzj@redhat.com> - 2.1.11-1
- update to 2.1.11
  - fix config file error handling
  - better handling of empty lines/comments in mirror lists
  - improve some error messages

* Sun Oct 24 2004 Jeremy Katz <katzj@redhat.com> - 2.1.10-3.1
- make the cron job executable (#136764)

* Thu Oct 21 2004 Jeremy Katz <katzj@redhat.com> - 2.1.10-3
- actually remove the repositories

* Wed Oct 20 2004 Jeremy Katz <katzj@redhat.com> - 2.1.10-2
- remove repositories from being explicitly listed in yum.conf, 
  .repo files will be included in the fedora-release package

* Tue Oct 19 2004 Jeremy Katz <katzj@redhat.com> - 2.1.10-1
- update to 2.1.10
  * updated man pages
  * make more resilient to broken groups file
  * fix urlgrabber failure callback (#136178)

* Mon Oct 18 2004 Jeremy Katz <katzj@redhat.com> - 2.1.9-1
- 2.1.9 includes the path fix

* Mon Oct 18 2004 Jeremy Katz <katzj@redhat.com> - 2.1.8-2
- fix path in /usr/bin/yum
- turn on gpgchecking by default

* Mon Oct 18 2004 Bill Nottingham <notting@redhat.com> - 2.1.8-1
- 2.1.8, fixes #135735, #135998, #135775

* Wed Oct 13 2004 Jeremy Katz <katzj@redhat.com> - 2.1.7-2
- add yum-arch

* Wed Oct 13 2004 Jeremy Katz <katzj@redhat.com> - 2.1.7-1
- 2.1.7
- use mirror list by default

* Wed Oct  6 2004 Bill Nottingham <notting@redhat.com> - 2.1.6-1
- 2.1.6

* Mon Oct  4 2004 Jeremy Katz <katzj@redhat.com> - 2.1.5-1
- 2.1.5
- turn on obsoletes=1 by default in yum.conf

* Wed Sep 29 2004 Bill Nottingham <notting@redhat.com> - 2.1.4-1
- 2.1.4

* Fri Sep  3 2004 Bill Nottingham <notting@redhat.com> - 2.1.3-1
- 2.1.3

* Thu Sep  2 2004 Jeremy Katz <katzj@redhat.com> - 2.1.2-1
- 2.1.2

* Wed Sep  1 2004 Jeremy Katz <katzj@redhat.com> - 2.1.1-1
- 2.1.1

* Tue Aug 31 2004 Jeremy Katz <katzj@redhat.com> - 2.1.0-1
- update to 2.1.0

* Wed Jul 7 2004  Elliot Lee <sopwith@redhat.com> 2.0.7-3
- Back to rawhide

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 11 2004 Elliot Lee <sopwith@redhat.com> 2.0.7-1.1
- Update config again

* Fri May  7 2004 Jeremy Katz <katzj@redhat.com> 2.0.7-1
- update to 2.0.7
- change config to point to final FC2 locations

* Fri Apr 16 2004 Jeremy Katz <katzj@redhat.com> - 2.0.7-0.20040416
- new snap 

* Sat Apr  3 2004 Jeremy Katz <katzj@redhat.com> 2.0.7-0.20040403
- new snap, should fix yum -e name.arch

* Wed Mar 17 2004 Jeremy Katz <katzj@redhat.com> 2.0.6-1
- update to 2.0.6

* Wed Mar 10 2004 Jeremy Katz <katzj@redhat.com> 2.0.5.20040310-1
- update to today's snap

* Wed Mar  3 2004 Jeremy Katz <katzj@redhat.com> 2.0.5.20040303-1
- today's snap

* Tue Mar  2 2004 Jeremy Katz <katzj@redhat.com> - 2.0.5.20040229-1
- update again per seth's request

* Thu Feb 26 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- mv /etc/init.d -> /etc/rc.d/init.d

* Tue Feb 24 2004 Jeremy Katz <katzj@redhat.com> - 2.0.5.20040224-1
- newer

* Mon Feb 23 2004 Jeremy Katz <katzj@redhat.com> - 2.0.5.20040223-1
- update to current snapshot per skvidal's request
- add retries=20 to yum.conf

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 23 2004 Bill Nottingham <notting@redhat.com> 2.0.4.20040103-1
- update to current snapshot
- fix config for FC2 test 1

* Tue Dec 23 2003 Jeff Johnson <jbj@redhat.com> 2.0.4-5
- build yum daily snapshot for amd64 fix.

* Wed Nov 12 2003 Bill Nottingham <notting@redhat.com> 2.0.4-4
- patch for excluding dirs in yum-arch from CVS

* Thu Nov  6 2003 Jeremy Katz <katzj@redhat.com> 2.0.4-3
- patch to work with python 2.3 from Seth

* Wed Oct 29 2003 Elliot Lee <sopwith@redhat.com> 2.0.4-2
- Stick in a new yum.conf for FC1.

* Mon Oct 20 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- new upstream release 2.0.4

* Tue Sep 16 2003 Jeff Johnson <jbj@redhat.com> 2.0.3-1
- update to 2.0.3
- drop yum-init patch, merged into 2.0.3.
- change rpm version requirement to 4.1.1.

* Thu Jul 24 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- change init script to more current RHL style

* Wed Jul 23 2003 Nalin Dahyabhai <nalin@redhat.com>
- require libxml2-python, because yum does

* Thu Jul 17 2003 Jeff Johnson <jbj@redhat.com> 2.0-1
- update to 2.0.

* Thu May 22 2003 Jeff Johnson <jbj@redhat.com> 1.98-0.20030522
- update to snapshot.

* Mon May 12 2003 Jeff Johnson <jbj@redhat.com> 1.98-0.20030512
- create.
