%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: A high-level cross-protocol url-grabber
Name: python-urlgrabber
Version: 3.1.0
Release: 2%{?dist}
Source0: urlgrabber-%{version}.tar.gz
Patch0: urlgrabber-keepalive.patch
License: LGPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Url: http://linux.duke.edu/projects/urlgrabber/
Provides: urlgrabber
Requires: m2crypto >= 0.16-5

%description
A high-level cross-protocol url-grabber for python supporting HTTP, FTP 
and file locations.  Features include keepalive, byte ranges, throttling,
authentication, proxies and more.

%prep
%setup -n urlgrabber-%{version}
%patch0 -p0

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_docdir}/urlgrabber-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog LICENSE README TODO
%dir %{python_sitelib}/urlgrabber
%{python_sitelib}/urlgrabber/*
%{_bindir}/urlgrabber

%changelog
* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 3.1.0-2
- fix keepalive (#218268)

* Mon Oct 23 2006 James Bowes <jbowes@redhat.com> - 3.1.0-1
- update to 3.1.0

* Mon Jul 17 2006 James Bowes <jbowes@redhat.com> - 2.9.9-2
- Add support for byte ranges and keepalive over HTTPS

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.9.9-1.1
- rebuild

* Tue May 16 2006 Jeremy Katz <katzj@redhat.com> - 2.9.9-1
- update to 2.9.9

* Tue Mar 14 2006 Jeremy Katz <katzj@redhat.com> - 2.9.8-2
- catch read errors so they trigger the failure callback.  helps catch bad cds

* Wed Feb 22 2006 Jeremy Katz <katzj@redhat.com> - 2.9.8-1
- update to new version fixing progress bars in yum on regets

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep 21 2005 Jeremy Katz <katzj@redhat.com> - 2.9.6-4
- don't use --record and list files by hand so that we don't miss 
  directories (#158480)

* Wed Sep 14 2005 Jeremy Katz <katzj@redhat.com> - 2.9.6-3
- add directory to file list (#168261)

* Fri Jun 03 2005 Phil Knirsch <pknirsch@redhat.com> 2.9.6-2
- Fixed the reget method to actually work correctly (skip completely transfered
  files, etc)

* Tue Mar  8 2005 Jeremy Katz <katzj@redhat.com> - 2.9.6-1
- update to 2.9.6

* Mon Mar  7 2005 Jeremy Katz <katzj@redhat.com> - 2.9.5-1
- import into dist
- make the description less of a book

* Mon Mar  7 2005 Seth Vidal <skvidal@phy.duke.edu> 2.9.5-0
- 2.9.5

* Thu Feb 24 2005 Seth Vidal <skvidal@phy.duke.edu> 2.9.3-0
- first package for fc3
- named python-urlgrabber for naming guideline compliance

