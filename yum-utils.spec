# Things talking about Fedora specifically?
%define docs_fed 0
# Things that we don't want to ship for RHEL, or don't work with RHN
%define keep_non_rhn 1
# These are "old", and were shipped in Fedora before yum itself got the features
%define keep_old 0

Summary: Utilities based around the yum package manager
Name: yum-utils
Version: 1.1.16
Release: 13%{?dist}.1
License: GPLv2+
Group: Development/Tools
Source: http://linux.duke.edu/yum/download/yum-utils/%{name}-%{version}.tar.gz
Patch1: kmod-kabi.patch
Patch2: yum-filter-data-typo.patch
Patch3: reposync-parens.patch
Patch4: yum-security-numbers.patch
Patch5: yum-keys-repoid.patch
Patch6: yum-secureity-has-id.patch
Patch7: yum-keys-dynamic-columns-ui.patch
Patch8: yum-utils-downloadonly-errors.patch
Patch9: repodiff-pre-delete-data.patch
Patch10: repoquery-manual-repo-expire.patch
Patch11: yum-groups-manager-utf8.patch
Patch12: yum-list-data-groups-help.patch
Patch13: yum-utils-timestamp_check.patch
Patch14: yum-complete-trans-import.patch
Patch15: yum-utils-changelog-no-datetime.patch

Patch99: yum-utils-C4-1.1.16-allowrun.path

URL: http://linux.duke.edu/yum/download/yum-utils/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: python, yum >= 3.2.19-16
# yum-3.0.1-5.el5     is the dist-5E             version
# yum-3.2.8-9.el5     is the dist-5E-U2          version
# yum-3.2.8-9.el5_2.1 is the dist-5E-U3-fastrack version
# yum-3.2.19-18.el5   is the dist-5E-U3          version (current candidate)

%description
yum-utils is a collection of utilities and examples for the yum package
manager. It includes utilities by different authors that make yum easier and
more powerful to use. These tools include: debuginfo-install, package-cleanup,
repoclosure, repodiff, repo-graph, repomanage, repoquery, repo-rss, reposync,
repotrack, verifytree, yum-builddep, yum-complete-transaction, yumdownloader,
yum-debug-dump and yum-groups-manager.

%package -n yum-updateonboot
Summary: Run yum update on system boot
Group: System Environment/Base
Requires: python, yum >= 2.4
Requires(pre): chkconfig
Requires(post): chkconfig

%description -n yum-updateonboot
Runs yum update on system boot. This allows machines that have been turned
off for an extended amount of time to become secure immediately, instead of
waiting until the next early morning cron job.

%package -n yum-changelog
Summary: Yum plugin for viewing package changelogs before/after updating
Group: System Environment/Base
Requires: yum >= 3.0
# Needs to be a suggest, it's in EPEL and adds functionality
# Requires: python-dateutil

%description -n yum-changelog
This plugin adds a command line option to allow viewing package changelog
deltas before or after updating packages.

%package -n yum-fastestmirror
Summary: Yum plugin which chooses fastest repository from a mirrorlist
Group: System Environment/Base
Requires: yum >= 3.0

%description -n yum-fastestmirror
This plugin sorts each repository's mirrorlist by connection speed
prior to downloading packages.

%package -n yum-kmod
Summary: Yum plugin to handle fedora kernel modules.
Group: System Environment/Base
Requires: yum >= 3.0

%description -n yum-kmod
Plugin for Yum to handle installation of kmod-foo type of kernel modules,
when new kernel versions are installed.
%if %{docs_fed}
kmod-foo kernel modules is described by the Fedora Extras packaging standards.
%endif

%package -n yum-protectbase
Summary: Yum plugin to protect packages from certain repositories.
Group: System Environment/Base
Requires: yum >= 3.0

%description -n yum-protectbase
This plugin allows certain repositories to be protected. Packages in the
protected repositories can't be overridden by packages in non-protected
repositories even if the non-protected repo has a later version.

%package -n yum-versionlock
Summary: Yum plugin to lock specified packages from being updated
Group: System Environment/Base
Requires: yum >= 3.0

%description -n yum-versionlock
This plugin takes a set of name/versions for packages and excludes all other
versions of those packages (including optionally following obsoletes). This
allows you to protect packages from being updated by newer versions,
for example.

%package -n yum-tsflags
Summary: Yum plugin to add tsflags by a commandline option
Group: System Environment/Base
Requires: yum >= 3.0

%description -n yum-tsflags
This plugin allows you to specify optional transaction flags on the yum
command line

%package -n yum-kernel-module
Summary: Yum plugin to handle kernel-module-foo type of kernel module
Group: System Environment/Base
Requires: yum >= 3.0

%description -n yum-kernel-module
This plugin handle installation of kernel-module-foo type of kernel modules when new version of
kernels are installed.


%package -n yum-downloadonly
Summary: Yum plugin to add downloadonly command option
Group: System Environment/Base
Requires: yum >= 3.0

%description -n yum-downloadonly
This plugin adds a --downloadonly flag to yum so that yum will only download
the packages and not install/update them.

%package -n yum-allowdowngrade
Summary: Yum plugin to enable manual downgrading of packages
Group: System Environment/Base
Requires: yum >= 3.0

%description -n yum-allowdowngrade
This plugin adds a --allow-downgrade flag to yum to make it possible to
manually downgrade packages to specific versions.

%package -n yum-skip-broken
Summary: Yum plugin to handle skiping packages with dependency problems
Group: System Environment/Base
Requires: yum >= 3.0

%description -n yum-skip-broken
This plugin adds a --skip-broken to yum to make it possible to
check packages for dependency problems and skip the one with problems.

%package -n yum-priorities
Summary: plugin to give priorities to packages from different repos
Group: System Environment/Base
Requires: yum >= 3.0

%description -n yum-priorities
This plugin allows repositories to have different priorities.
Packages in a repository with a lower priority can't be overridden by packages
from a repository with a higher priority even if repo has a later version.

%package -n yum-refresh-updatesd
Summary: Tell yum-updatesd to check for updates when yum exits
Group: System Environment/Base
Requires: yum >= 3.0
Requires: yum-updatesd

%description -n yum-refresh-updatesd
yum-refresh-updatesd tells yum-updatesd to check for updates when yum exits.
This way, if you run 'yum update' and install all available updates, puplet
will almost instantly update itself to reflect this.

%package -n yum-merge-conf
Summary: Yum plugin to merge configuration changes when installing packages
Group: System Environment/Base
Requires: yum >= 3.0

%description -n yum-merge-conf
This yum plugin adds the "--merge-conf" command line option. With this option,
Yum will ask you what to do with config files which have changed on updating a
package.

%package -n yum-security
Summary: Yum plugin to enable security filters
Group: System Environment/Base
Requires: yum >= 3.2.18

%description -n yum-security
This plugin adds the options --security, --cve, --bz and --advisory flags
to yum and the list-security and info-security commands.
The options make it possible to limit list/upgrade of packages to specific
security relevant ones. The commands give you the security information.

%package -n yum-protect-packages
Summary: Yum plugin to prevents Yum from removing itself and other protected packages
Group: System Environment/Base
Requires: yum >= 3.0

%description -n yum-protect-packages
this plugin prevents Yum from removing itself and other protected packages.
By default, yum is the only package protected, but by extension this
automatically protects everything on which yum depends (rpm, python, glibc,
and so on).Therefore, the plugin functions well even without
compiling careful lists of all important packages.

%package -n yum-basearchonly
Summary: Yum plugin to let Yum install only basearch packages.
Group: System Environment/Base
Requires: yum >= 3.0

%description -n yum-basearchonly
this plugin makes Yum only install basearch packages on multiarch systems.
If you type 'yum install foo' on a x68_64 system, only 'foo-x.y.x86_46.rpm' is installed.
If you want to install the foo-x.y.i386.rpm, you have to type 'yum install foo.i386'.
The plugin only works with 'yum install'.

%package -n yum-upgrade-helper
Summary: Yum plugin to help upgrades to the next distribution version
Group: System Environment/Base
Requires: yum >= 3.0

%description -n yum-upgrade-helper
this plugin allows yum to erase specific packages on install/update based on an additional
metadata file in repositories. It is used to simplify distribution upgrade hangups.

%package -n yum-aliases
Summary: Yum plugin to enable aliases filters
Group: System Environment/Base
Requires: yum >= 3.0.5

%description -n yum-aliases
This plugin adds the command alias, and parses the aliases config. file to
enable aliases.

%package -n yum-list-data
Summary: Yum plugin to list aggregate package data
Group: System Environment/Base
Requires: yum >= 3.0.5

%description -n yum-list-data
This plugin adds the commands list- vendors, groups, packagers, licenses,
arches, committers, buildhosts, baseurls, package-sizes, archive-sizes and
installed-sizes.

%package -n yum-filter-data
Summary: Yum plugin to list filter based on package data
Group: System Environment/Base
Requires: yum >= 3.2.17

%description -n yum-filter-data
This plugin adds the options --filter- vendors, groups, packagers, licenses,
arches, committers, buildhosts, baseurls, package-sizes, archive-sizes and
installed-sizes. Note that each package must match at least one pattern/range in
each category, if any were specified.

%package -n yum-tmprepo
Summary: Yum plugin to add temporary repositories
Group: System Environment/Base
Requires: yum >= 3.2.11
Requires: createrepo

%description -n yum-tmprepo
This plugin adds the option --tmprepo which takes a url to a .repo file
downloads it and enables it for a single run. This plugin tries to ensure
that temporary repositories are safe to use, by default, by not allowing
gpg checking to be disabled.

%package -n yum-verify
Summary: Yum plugin to add verify command, and options
Group: System Environment/Base
Requires: yum >= 3.2.12

%description -n yum-verify
This plugin adds the commands verify, verify-all and verify-rpm. There are
also a couple of options. This command works like rpm -V, to verify your
installation.

%package -n yum-keys
Summary: Yum plugin to deal with signing keys
Group: System Environment/Base
Requires: yum >= 3.2.19

%description -n yum-keys
This plugin adds the commands keys, keys-info, keys-data and keys-remove. They
allow you to query and remove signing keys.

%package -n yum-NetworkManager-dispatcher
Summary: NetworkManager dispatcher plugin to help yum, when changing networks
Group: System Environment/Base
Requires: yum >= 3.2.17

%description -n yum-NetworkManager-dispatcher
This plugin forces yum to check it's cache if/when a new network connection
happens in NetworkManager. Note that currently there is no checking of
previous data, so if your WiFi keeps going up and down (or you suspend/resume
a lot) yum will recheck it's cached data a lot.

%prep
%setup -q

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

%patch99 -p1

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
make -C updateonboot DESTDIR=$RPM_BUILD_ROOT install

# Plugins to install
xplugins=""
%if %{keep_non_rhn}
xplugins="\
 tsflags \
 kernel-module \
 allowdowngrade \
 priorities \
 refresh-updatesd \
 merge-conf \
 upgrade-helper"
%endif

yplugins=""
%if %{keep_old}
yplugins="\
 basearchonly \
 skip-broken \
"
%endif

plugins="\
 changelog \
 fastestmirror \
 fedorakmod \
 protectbase \
 versionlock \
 downloadonly \
 security \
 protect-packages \
 aliases \
 list-data \
 filter-data \
 tmprepo \
 verify \
 keys \
 $xplugins \
 $yplugins \
"

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/yum/pluginconf.d/ $RPM_BUILD_ROOT/usr/lib/yum-plugins/

cd plugins
for plug in $plugins; do
    install -m 644 $plug/*.conf $RPM_BUILD_ROOT/%{_sysconfdir}/yum/pluginconf.d/
    install -m 644 $plug/*.py $RPM_BUILD_ROOT/usr/lib/yum-plugins/
done
install -m 644 aliases/aliases $RPM_BUILD_ROOT/%{_sysconfdir}/yum/aliases.conf

# FIXME: fixup yum-fedorakmod to yum-kmod by hand, due to package names etc.
mv $RPM_BUILD_ROOT/%{_sysconfdir}/yum/pluginconf.d/fedorakmod.conf \
   $RPM_BUILD_ROOT/%{_sysconfdir}/yum/pluginconf.d/kmod.conf
mv $RPM_BUILD_ROOT/usr/lib/yum-plugins/fedorakmod.py \
   $RPM_BUILD_ROOT/usr/lib/yum-plugins/kmod.py
install -m 644 versionlock/versionlock.list $RPM_BUILD_ROOT/%{_sysconfdir}/yum/pluginconf.d/

%clean
rm -rf $RPM_BUILD_ROOT

%post -n yum-updateonboot
/sbin/chkconfig --add yum-updateonboot >/dev/null 2>&1 || :;

%preun -n yum-updateonboot
if [ $1 = 0 ]; then
    /sbin/service yum-updateonboot stop >/dev/null 2>&1 || :;
    /sbin/chkconfig --del yum-updateonboot >/dev/null 2>&1 || :;
fi

%files
%defattr(-, root, root)
%doc README yum-util-cli-template
%doc COPYING
%doc plugins/README
%{_bindir}/debuginfo-install
%{_bindir}/package-cleanup
%{_bindir}/repoclosure
%{_bindir}/repodiff
%{_bindir}/repomanage
%{_bindir}/repoquery
%{_bindir}/repotrack
%{_bindir}/reposync
%{_bindir}/repo-graph
%{_bindir}/repo-rss
%{_bindir}/verifytree
%{_bindir}/yumdownloader
%{_bindir}/yum-builddep
%{_bindir}/yum-debug-dump
%{_bindir}/yum-groups-manager
%{_sbindir}/yum-complete-transaction
%{_mandir}/man1/yum-utils.1.*
%{_mandir}/man1/package-cleanup.1.*
%{_mandir}/man1/repo-rss.1.*
%{_mandir}/man1/repoquery.1.*
%{_mandir}/man1/reposync.1.*
%{_mandir}/man1/yum-builddep.1.*
%{_mandir}/man1/yum-debug-dump.1.*
%{_mandir}/man8/yum-complete-transaction.8.*
%{_mandir}/man1/yum-groups-manager.1.*
%{_mandir}/man1/yumdownloader.1.*

%files -n yum-updateonboot
%defattr(-, root, root)
%doc updateonboot/README
%config(noreplace) %{_sysconfdir}/sysconfig/yum-updateonboot
%{_initrddir}/yum-updateonboot

%files -n yum-changelog
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/changelog.conf
/usr/lib/yum-plugins/changelog.*
%{_mandir}/man1/yum-changelog.1.*
%{_mandir}/man5/yum-changelog.conf.5.*

%files -n yum-fastestmirror
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/fastestmirror.conf
/usr/lib/yum-plugins/fastestmirror*.*

%files -n yum-kmod
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/kmod.conf
/usr/lib/yum-plugins/kmod.*

%files -n yum-protectbase
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/protectbase.conf
/usr/lib/yum-plugins/protectbase.*

%files -n yum-versionlock
%defattr(-, root, root)
%doc plugins/versionlock/README
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/versionlock.conf
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/versionlock.list
/usr/lib/yum-plugins/versionlock.*
%{_mandir}/man1/yum-versionlock.1.*
%{_mandir}/man5/yum-versionlock.conf.5.*

%if %{keep_non_rhn}
%files -n yum-tsflags
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/tsflags.conf
/usr/lib/yum-plugins/tsflags.*

%files -n yum-kernel-module
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/kernel-module.conf
/usr/lib/yum-plugins/kernel-module.*
%endif

%files -n yum-downloadonly
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/downloadonly.conf
/usr/lib/yum-plugins/downloadonly.*

%if %{keep_non_rhn}
%files -n yum-allowdowngrade
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/allowdowngrade.conf
/usr/lib/yum-plugins/allowdowngrade.*
%endif

%if %{keep_old}
%files -n yum-skip-broken
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/skip-broken.conf
/usr/lib/yum-plugins/skip-broken.*
%endif

%if %{keep_non_rhn}
%files -n yum-priorities
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/priorities.conf
/usr/lib/yum-plugins/priorities.*

%files -n yum-refresh-updatesd
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/refresh-updatesd.conf
/usr/lib/yum-plugins/refresh-updatesd.*

%files -n yum-merge-conf
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/merge-conf.conf
/usr/lib/yum-plugins/merge-conf.*
%endif

%files -n yum-security
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/security.conf
/usr/lib/yum-plugins/security.*
%{_mandir}/man8/yum-security.8.*

%files -n yum-protect-packages
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/protect-packages.conf
/usr/lib/yum-plugins/protect-packages.*

%if %{keep_old}
%files -n yum-basearchonly
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/basearchonly.conf
/usr/lib/yum-plugins/basearchonly.*
%endif

%if %{keep_non_rhn}
%files -n yum-upgrade-helper
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/upgrade-helper.conf
/usr/lib/yum-plugins/upgrade-helper.*
%endif

%files -n yum-aliases
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/aliases.conf
%config(noreplace) %{_sysconfdir}/yum/aliases.conf
/usr/lib/yum-plugins/aliases.*
%{_mandir}/man1/yum-aliases.1.*

%files -n yum-list-data
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/list-data.conf
/usr/lib/yum-plugins/list-data.*
%{_mandir}/man1/yum-list-data.1.*

%files -n yum-filter-data
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/filter-data.conf
/usr/lib/yum-plugins/filter-data.*
%{_mandir}/man1/yum-filter-data.1.*

%files -n yum-tmprepo
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/tmprepo.conf
/usr/lib/yum-plugins/tmprepo.*

%files -n yum-verify
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/verify.conf
/usr/lib/yum-plugins/verify.*
%{_mandir}/man1/yum-verify.1.*

%files -n yum-keys
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/keys.conf
/usr/lib/yum-plugins/keys.*

%files -n yum-NetworkManager-dispatcher
%defattr(-, root, root)
/etc/NetworkManager/dispatcher.d/*

%changelog
* Mon Jun 13 2009 David Hrbáč <david@hrbac.cz> - 1.1.16-13.el4.hrb.1
- initial rebuild
- drop python >= 2.4

* Thu Jan 22 2009 Karanbir Singh <kbsingh@centos.org> - 1.1.16-13.el5.centos
- Enable all plugins

* Tue Nov 25 2008 James Antill <james.antill@redhat.com> - 1.1.16-13
- Fix the yum-changelog exit, when you pass it dates and ther is no datetime
- Resolves: rhbz#472389

* Tue Nov 11 2008 James Antill <james.antill@redhat.com> - 1.1.16-11
- Fix the yum-complete-transaction cleanup bug.
- Resolves: rhbz#470776

* Thu Oct 23 2008 James Antill <james.antill@redhat.com> - 1.1.16-10
- Add the timestamp_check option, so we can have repoids to random stuff
- Resolves: rhbz#466176
- Resolves: rhbz#454883

* Fri Oct 17 2008 James Antill <james.antill@redhat.com> - 1.1.16-9
- Have repoquery set metadata_expire to 0 for manual repos.
- Resolves: rhbz#466176
- Fix list-groups help output
- Resolves: rhbz#467191
- Fix yum-groups-manager i18n bugs
- Resolves: rhbz#466176
- Resolves: rhbz#454883

* Fri Sep 26 2008 James Antill <james.antill@redhat.com> - 1.1.16-8
- Fix repodiff when comparing against older repos. than ones you'd compared
- against before.
- Resolves: rhbz#444948
- Resolves: rhbz#454883

* Fri Sep 19 2008 James Antill <james.antill@redhat.com> - 1.1.16-7
- Fix downloadonly not showing errors
- Resolves: rhbz#462797
- Resolves: rhbz#454883

* Tue Sep 16 2008 James Antill <james.antill@redhat.com> - 1.1.16-6
- Add repoid to keys info output.
- Do dynamic columns in keys output.
- Fix --bz option in yum-security
- Resolves: rhbz#462374
- Resolves: rhbz#454883

* Fri Aug 29 2008 James Antill <james.antill@redhat.com> - 1.1.16-5
- Fix the numbers in the security plugin, to be close to listTransaction
- Resolves: rhbz#454883

* Wed Aug 27 2008 James Antill <james.antill@redhat.com> - 1.1.16-4
- Import upstream 1.1.16.
- Add group management application, networkmanger script. Bug fixes.
- Remove skip-broken/basearchonly plugins, as we never shipped them and
- core yum does their jobs now.
- Remove hard dep. on dateutil, as it's only in EPEL.
- Fix typo in filter-data plugin.
- Fix typo in reposync.
- Resolves: rhbz#454883
- Resolves: rhbz#449989
- Resolves: rhbz#450873

* Wed Aug  6 2008 James Antill <james.antill@redhat.com> - 1.1.14-0_beta_15_2
- Import next upstream 1.1.15 beta.
- gpgcheck/repo_gpgcheck change.
- include fastestmirror
- Resolves: rhbz#454883
- Related: rhbz#458131

* Tue Aug  5 2008 James Antill <james.antill@redhat.com> - 1.1.14-0_beta_15_1
- Import upstream 1.1.15 beta.
- What will be in Fedora 9 soon.
- Resolves: rhbz#454883

* Fri Apr 11 2008 James Antill <james.antill@redhat.com> - 1.1.10-9
- Fix yumdownloader --source
- Resolves: rhbz#391791

* Mon Mar 31 2008 James Antill <james.antill@redhat.com> - 1.1.10-8
- Backport man pages
- Resolves: rhbz#438169

* Wed Mar 12 2008 James Antill <james.antill@redhat.com> - 1.1.10-7
- Backport man page bug fix.
- Resolves: rhbz#437127

* Tue Feb  5 2008 James Antill <james.antill@redhat.com> - 1.1.10-6
- Rename yum groups <=> rpm groups
- Add yum groups, what was actually wanted.
- Fixup minor doc problems
- Resolves: rhbz#319491

* Mon Feb  4 2008 James Antill <james.antill@redhat.com> - 1.1.10-4
- Add man pages for list-data and filter-data
- Couple of minor tweaks.
- Resolves: rhbz#319491

* Sun Feb  3 2008 James Antill <james.antill@redhat.com> - 1.1.10-3
- Fixup repodiff
- Add docs.
- Add list-data and filter-data
- Resolves: rhbz#319491

* Fri Jan 18 2008 James Antill <james.antill@redhat.com> - 1.1.10-2
- Import into RHEL-5
- Related: rhbz#384691

* Thu Aug  9 2007 James Antill <jantill@redhat.com> - 1.0.4-3
- Re-integrate older security info printing.
- kabi patch for ClusterStorage, as it uses the new kABI
- Upload new tarball.
- Resolves: rhbz#251542

* Wed Aug  8 2007 James Antill <jantill@redhat.com> - 1.0.4-1
- Go back in time to upstream 1.0.4, which works with yum-3.0.1
- Resolves: rhbz#251542

* Tue Jul 24 2007 James Antill <jantill@redhat.com> - 1.1.5-3
- Fix yum-security to do "list updates" with newer yum
- Resolves: rhbz#234646

* Thu Jul 12 2007 James Antill <jantill@redhat.com> - 1.1.5-2
- Add resquires for updatesd to refresh-updatesd
- Remove a few of the plugins.
- Rename fedorakmod to kmod
- Resolves: rhbz#234646

* Tue Jun 26 2007 Dennis Gregorovic <dgregor@redhat.com> - 1.1.5
- Rebuild for RHEL 5
- Resolves: rhbz#234646

* Mon Jun 18 2007 Tim Lauridsen <tla@rasmil.dk>
- mark as 1.1.5

* Tue May 1 2007 Tim Lauridsen <tla@rasmil.dk>
- mark as 1.1.4

* Tue May 1 2007 Tim Lauridsen <tla@rasmil.dk>
- mark as 1.1.3

* Tue May  1 2007 Seth Vidal <skvidal at linux.duke.edu>
- added debuginfo-install

* Fri Apr 20 2007 Tim Lauridsen <tla@rasmil.dk>
- Added security plugin written by James Antill <james@and.org>

* Thu Apr 12 2007 Tim Lauridsen <tla@rasmil.dk>
- mark as 1.1.2
- Added merge-conf plugin written by Aurelien Bompard <abompard@fedoraproject.org>

* Mon Feb 19 2007 Tim Lauridsen <tla@rasmil.dk>
- mark it as 1.1.1

* Mon Feb 19 2007 Tim Lauridsen <tla@rasmil.dk>
- mark it as 1.1.0 (again)

* Thu Feb 15 2007 Tim Lauridsen <tla@rasmil.dk>
- removed versionlock.list installation.

* Wed Feb 14 2007 Tim Lauridsen <tla@rasmil.dk>
- Added versionlock.list installation.
- fixed skip-broken description (--ignore-broken -> --skip-broken)

* Tue Feb 13 2007 James Bowes <jbowes@redhat.com>
- Add yum-refresh-updatesd plugin

* Thu Feb 8 2007 Tim Lauridsen <tla@rasmil.dk>
- Added man dirs to yum-changelog files section

* Wed Feb 7 2007 Tim Lauridsen <tla@rasmil.dk>
- mark it as 1.1.0
- Requires: yum >= 3.1.1 for yum-utils.

* Tue Feb 6 2007 Tim Lauridsen <tla@rasmil.dk>
- Added %%{?dist} tag

* Sun Dec 31 2006 Tim Lauridsen <tla@rasmil.dk>
- mark it as 1.0.2

* Tue Oct 31 2006 Tim Lauridsen <tla@rasmil.dk>
- mark it as 1.0.1

* Fri Oct 27 2006 Tim Lauridsen <tla@rasmil.dk>
- Added priorities plugin written by Daniel de Kok <danieldk at pobox.com>

* Wed Oct  4 2006 Seth Vidal <skvidal at linux.duke.edu>
- mark it as 1.0
- change requires for the packages to yum 3.0

* Wed Sep 27 2006 Tim Lauridsen <tla@rasmil.dk>
- added skip-broken plugin

* Tue Sep 05 2006 Panu Matilainen <pmatilai@laiskianen.org>
- added allowdowngrade plugin

* Sun Aug 13 2006 Seth Vidal <skvidal at linux.duke.edu>
- fix the plugins/ doc issue

* Sat May  6 2006 Seth Vidal <skvidal at linux.duke.edu>
- bump version number
- added yum-downloadonly plugin
- fix minor item in tsflags description

* Sat Apr 29 2006 Seth Vidal <skvidal at linux.duke.edu>
- add reposync

* Fri Apr 28 2006 Tim Lauridsen <tla@rasmil.dk>
- added yum-fedorakmod plugin subpackage
- added yum-protectbase plugin subpackage.
- added yum-versionlock plugin subpackage.
- added yum-tsflags plugin subpackage.
- added yum-kernel-module plugin subpackage
- changed .py to .* in files sections for plugin subpackages to build rpms without error.

* Thu Feb 23 2006 Seth Vidal <skvidal at linux.duke.edu>
-  changed some of the yum version dependencies

* Fri Feb 10 2006 Seth Vidal <skvidal@linux.duke.edu>
- added repotrack to utils
- bumped version for 2.5.X-compatible release

* Tue Jan 10 2006 Brian Long <brilong@cisco.com>
- bump version to 0.4
- add yum-fastestmirror subpackage

* Mon Oct 17 2005 Panu Matilainen <pmatilai@laiskiainen.org>
- add repoquery man page

* Sat Sep 17 2005 Panu Matilainen <pmatilai@laiskiainen.org>
- version 0.3.1
- various enhancements and fixes to repoquery
- avoid tracebacks in yumex and pup when changelog plugin is enabled

* Mon Jul 25 2005 Panu Matilainen <pmatilai@laiskiainen.org>
- bump version to 0.3
- add yum-changelog subpackage
- add plugins as documentation to the main package
- require yum >= 2.3.4 (for getCacheDir)

* Tue Jun  21 2005 Gijs Hollestelle <gijs@gewis.nl>
- Added missing GPL COPYING file

* Wed Jun  1 2005 Seth Vidal <skvidal@phy.duke.edu>
- 0.2

* Mon May 23 2005 Panu Matilainen <pmatilai@laiskiainen.org>
- add yum-updateboot subpackage

* Mon May 16 2005 Gijs Hollestelle <gijs@gewis.nl>
- first version based on the mock spec file
