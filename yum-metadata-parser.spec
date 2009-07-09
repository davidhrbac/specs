%{!?python_sitelib_platform: %define python_sitelib_platform %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}


Summary: A fast metadata parser for yum
Name: yum-metadata-parser
Version: 1.1.2
Release: 12%{?dist}
Source0: http://linux.duke.edu/projects/yum/download/%{name}/%{name}-%{version}.tar.gz
Patch0: yum-metadata-parser-1.1.2-null-pkgid.patch
Patch1: yum-metadata-parser-exclusive-lock.patch
Patch2: yum-metadata-parser-1.1.2-delay-indexes.patch
Patch3: yum-metadata-parser-1.1.2-no-updates.patch
License: GPLv2
Group: Development/Libraries
URL: http://linux.duke.edu/projects/yum/
Conflicts: yum < 3.2.0
BuildRequires: python-devel
BuildRequires: glib2-devel
BuildRequires: libxml2-devel
BuildRequires: sqlite-devel
BuildRequires: pkgconfig
Requires: glib2 >= 2.15
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Fast metadata parser for yum implemented in C.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

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

#%{python_sitelib_platform}/*egg-info

%changelog
* Thu Jul  9 2009 David Hrbáč <david@hrbac.cz> - 1.1.2-12
- Centos rebuild
- removed egg-info

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 1.1.2-11
- Rebuild for Python 2.6

* Tue Oct 14 2008 James Antill <james at fedoraproject.org> 1.1.2-10
- Add delay indexes and no updates patches from upstream.
- Resolves: bug 465898

* Thu Feb 14 2008 Seth Vidal <skvidal at fedoraproject.org> 1.1.2-8
- bump for gcc 

* Fri Jan 25 2008 Seth Vidal <skvidal at fedoraproject.org> 1.1.2-7
- apply exclusive lock patch

* Thu Jan 24 2008 Seth Vidal <skvidal at fedoraproject.org> 1.1.2-6
- add explicit dep on glib2 > 2.15

* Tue Jan 22 2008 Seth Vidal <skvidal at fedoraproject.org> 1.1.2-5
- rebuild

* Tue Jan 08 2008 James Bowes <jbowes@redhat.com> 1.1.2-4
- egg-info is under the arch specific dir

* Tue Jan 08 2008 James Bowes <jbowes@redhat.com> 1.1.2-3
- Include the egg-info dir.

* Tue Nov 27 2007 Paul Nasrat <pauln at truemesh.com> 1.1.2-2
- Fix segmentation fault with no pkgId

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

