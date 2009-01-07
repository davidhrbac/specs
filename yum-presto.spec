%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: Presto plugin for yum
Name: yum-presto
Version: 0.4.5
Release: 1%{?dist}
License: GPLv2+
Group: Development/Tools
Source: http://www.lesbg.com/jdieter/presto/%{name}-%{version}.tar.bz2
URL: http://www.lesbg.com/jdieter/presto/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python-setuptools-devel
Requires: python >= 2.4, yum >= 3.0, deltarpm >= 3.4-2

%description
Yum-presto is a plugin for yum that looks for deltarpms rather than rpms
whenever they are available.  This has the potential of saving a lot of
bandwidth when downloading updates.

A Deltarpm is the difference between two rpms.  If you already have foo-1.0
installed and foo-1.1 is available, yum-presto will download the deltarpm
for foo-1.0 => 1.1 rather than the full foo-1.1 rpm, and then build the full 
foo-1.1 package from your installed foo-1.0 and the downloaded deltarpm.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%doc README 
%doc COPYING
%doc ChangeLog
%{python_sitelib}/*
/usr/lib/yum-plugins/presto.py*
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/presto.conf

%changelog
* Thu Apr 10 2008 Jonathan Dieter <jdieter@gmail.com> - 0.4.5-1
- Fix bug in showing savings

* Mon Apr  7 2008 Jonathan Dieter <jdieter@gmail.com> - 0.4.4-1
- Show savings
- Use setuptools for installation
- Get Python Egg stuff working for F9

* Sat Nov 17 2007 Jonathan Dieter <jdieter@gmail.com> - 0.4.3-1
- Fix README so it is now accurate for 0.4.x
- Fix a small bug that caused AVC denials when SELinux is enabled

* Fri Sep 28 2007 Jonathan Dieter <jdieter@gmail.com> - 0.4.2-1
- Fix a couple of typos that caused yum to hang if certain error paths were
  hit.

* Sun Aug  5 2007 Jonathan Dieter <jdieter@gmail.com> - 0.4.1-1
- Applied small patch by Luke Macken to fix problems when not run directly
  from yum.
- Fix for situation where repository may be removed and then added again

* Wed Jul 11 2007 Jonathan Dieter <jdieter@gmail.com> - 0.4.0-1
- Complete rewrite (thanks, Jeremy)
- Many features removed in preparation for inclusion in Fedora 8

* Tue May  1 2007 Jonathan Dieter <jdieter@gmail.com> - 0.3.10-1
- Use new -a option to deltarpm to only check against a certain architecture.
  This allows us to work completely correctly on x86_64.
- Add "*" to repository of deltarpm as it *doesn't* screw up depsolving.

* Sun Apr 15 2007 Jonathan Dieter <jdieter@gmail.com> - 0.3.9-1
- Modifications to make yum-presto compatible with both FC6 and Rawhide
- Many other bugfixes - see ChangeLog

* Fri Apr  6 2007 Jonathan Dieter <jdieter@gmail.com> - 0.3.8-1
- Small bugfix

* Thu Apr  5 2007 Jonathan Dieter <jdieter@gmail.com> - 0.3.7-1
- Conf file cleanup

* Thu Apr  5 2007 Jonathan Dieter <jdieter@gmail.com> - 0.3.6-1
- Housecleaning in preparation for Extras

* Wed Apr  4 2007 Jonathan Dieter <jdieter@gmail.com> - 0.3.5-1
- Fix many small bugs
- Improve logging
- Use full path to yum-plugins rather than macro to fix x86_64 bug

* Tue Apr  3 2007 Jonathan Dieter <jdieter@gmail.com> - 0.3.4-1
- Build rpms in separate thread to help performance
- Fix miscellaneous spec file errors

* Fri Mar 30 2007 Jonathan Dieter <jdieter@gmail.com> - 0.3.3-1
- Upstream changed way the presto.xml.gz stores sequence information

* Fri Mar 30 2007 Jonathan Dieter <jdieter@gmail.com> - 0.3.2-2
- Take ownership of %%{_datadir}/presto

* Thu Mar 29 2007 Jonathan Dieter <jdieter@gmail.com> - 0.3.2-1
- Changes to remove rpmlint complaints

* Thu Mar 29 2007 Jonathan Dieter <jdieter@gmail.com> - 0.3.1-1
- Fix minor bug with importing public gpg keys.
- Update README

* Wed Mar 28 2007 Jonathan Dieter <jdieter@gmail.com> - 0.3.0-1
- Take over downloading of deltarpms so we can fallback to
  yum if the building of the rpm fails.

* Mon Mar 26 2007 Jonathan Dieter <jdieter@gmail.com> - 0.2.9-1
- Added logging to /var/log/presto.log
- Fixed crash bug
- Properly exit when unable to apply deltarpm
- Do a full (slow) MD5 check when checking to see if
  delta will apply cleanly

* Sat Mar 24 2007 Jonathan Dieter <jdieter@gmail.com> - 0.2.3-1
- Rebase to upstream

* Fri Mar 23 2007 Jonathan Dieter <jdieter@gmail.com> - 0.2.1-1
- Rebase to upstream

* Thu Mar 22 2007 Jonathan Dieter <jdieter@gmail.com> - 0.2-1
- Initial release
