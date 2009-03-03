%{!?python_sitelib_platform: %define python_sitelib_platform %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: A fast metadata parser for yum
Name: yum-metadata-parser
Version: 1.1.2
Release: 2%{?dist}
Source0: http://linux.duke.edu/projects/yum/download/%{name}/%{name}-%{version}.tar.gz
License: GPLv2
Group: Development/Libraries
URL: http://linux.duke.edu/projects/yum/
Conflicts: yum < 3.2.0
BuildRequires: python-devel
BuildRequires: glib2-devel
BuildRequires: libxml2-devel
BuildRequires: sqlite-devel
BuildRequires: pkgconfig
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Fast metadata parser for yum implemented in C.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --root=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README AUTHORS ChangeLog
%{python_sitelib_platform}/_sqlitecache.so
%{python_sitelib_platform}/sqlitecachec.py
%{python_sitelib_platform}/sqlitecachec.pyc
%{python_sitelib_platform}/sqlitecachec.pyo

%changelog
* Fri Jan 18 2008 James Antill <james.antill@redhat.com> - 1.1.2-2
- Import into RHEL-5
- Related: rhbz#384691

* Fri Aug 24 2007 Seth Vidal <skvidal at fedoraproject.org> 1.1.2-1
- 1.1.2-1
- hopefully fixes the mash issues

* Tue Jul 10 2007 James Bowes <jbowes@redhat.com>
- Use the 4 argument form of defattr

* Mon Jul  9 2007 Jeremy Katz <katzj@redhat.com> 
- conflict with yum < 3.2.0 (#247451)

* Tue May 15 2007 Jeremy Katz <katzj@redhat.com> - 1.1.0-2
- export dbversion so that things like createrepo can discover it (#239938)

* Fri Apr 27 2007 Jeremy Katz <katzj@redhat.com> - 1.1.0-1
- update to 1.1.0 for new sqlite db schema

* Wed Apr  4 2007 Jeremy Katz <katzj@redhat.com> - 1.0.4-1
- update to 1.0.4

* Tue Feb 13 2007 James Bowes <jbowes@redhat.com> - 1.0.3-2
- Spec file updates from the merge review: clean the buildroot.

* Mon Jan  8 2007 Jeremy Katz <katzj@redhat.com> - 1.0.3-1
- update to 1.0.3

* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 1.0-9
- rebuild for python 2.5, support new sqlite

* Wed Sep 27 2006 Jeremy Katz <katzj@redhat.com> - 1.0-8
- fix dep loop

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 
- rebuild

* Thu Jun 15 2006 Paul Nasrat <pnasrat@redhat.com> - 1.0-7
- add patch to correct population of packages.location_base

* Wed Jun 14 2006 Paul Nasrat <pnasrat@redhat.com> - 1.0-6
- add patch to correct table order of primary:files

* Tue Jun 13 2006 Jeremy Katz <katzj@redhat.com> - 1.0-5
- add patch to be quieter so that we don't break tree composes

* Mon Jun 12 2006 Jeremy Katz <katzj@redhat.com> - 1.0-4
- urls, build into fedora

* Mon Jun 05 2006 Tambet Ingo <tambet@ximian.com> - 1.0-3
- Require yum >= 2.6.2

* Sat Jun 04 2006 Terje Rosten <terje.rosten@pvv.org> - 1.0-2
- add buildrequires
- doc files
- url

* Fri Jun 02 2006 Terje Rosten <terje.rosten@pvv.org> - 1.0-0.1
- initial package

