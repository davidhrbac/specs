Name:           cpanspec
Version:        1.78
Release:        4%{?dist}
Summary:        RPM spec file generation utility
License:        GPL+ or Artistic
Group:          Development/Tools
URL:            http://cpanspec.sourceforge.net/
Source0:        http://dl.sourceforge.net/cpanspec/cpanspec-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Module::Build)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       /usr/bin/curl
Requires:       /usr/bin/repoquery
Requires:       rpm-build

%description
cpanspec generates spec files (and, optionally, source or even binary
packages) for Perl modules from CPAN for Fedora.  The quality of the spec
file is our primary concern.  It is assumed that maintainers will need to
do some (hopefully small) amount of work to clean up the generated spec
file to make the package build and to verify that all of the information
contained in the spec file is correct.

%prep
%setup -q

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
rm -rf $RPM_BUILD_ROOT

./Build install destdir=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

# No tests.
#%check
#./Build test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Artistic BUGS Changes COPYING TODO
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Mon Jan 11 2010 David Hrbáč <david@hrbac.cz> - 1.78-4
- initial build

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.78-4
- rebuild against perl 5.10.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.78-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Steven Pritchard <steve@kspei.com> 1.78-1
- Update to 1.78.

* Mon Jun 16 2008 Steven Pritchard <steve@kspei.com> 1.77-1
- Update to 1.77.

* Mon Jun 16 2008 Steven Pritchard <steve@kspei.com> 1.76-1
- Update to 1.76.

* Thu Jun 12 2008 Steven Pritchard <steve@kspei.com> 1.75-2
- Require rpm-build.

* Mon May 05 2008 Steven Pritchard <steve@kspei.com> 1.75-1
- Update to 1.75 (which really fixes BZ#437804).
- Require curl instead of wget (BZ#438245).
- Update description.

* Mon Mar 17 2008 Steven Pritchard <steve@kspei.com> 1.74-3
- Fix to work properly with 5.10.0 (BZ#437804).

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.74-2
- Rebuild for new perl

* Tue Dec 11 2007 Steven Pritchard <steve@kspei.com> 1.74-1
- Update to 1.74.
- Update License tag.

* Sun Jul 22 2007 Steven Pritchard <steve@kspei.com> 1.73-1
- Update to 1.73.

* Fri Jul 13 2007 Steven Pritchard <steve@kspei.com> 1.72-1
- Update to 1.72.

* Fri Jun 29 2007 Steven Pritchard <steve@kspei.com> 1.71-1
- Update to 1.71.
- Remove "Extras" from the description.
- Use the __perl macro instead of calling perl directly.

* Mon Mar 12 2007 Steven Pritchard <steve@kspei.com> 1.70-1
- Update to 1.70.

* Mon Oct 16 2006 Steven Pritchard <steve@kspei.com> 1.69.1-1
- Update to 1.69.1.

* Tue Oct 03 2006 Steven Pritchard <steve@kspei.com> 1.69-1
- Update to 1.69.
- Use _fixperms macro instead of our own chmod incantation.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 1.68-2
- Fix find option order.

* Thu Jul 20 2006 Steven Pritchard <steve@kspei.com> 1.68-1
- Update to 1.68.
- Include Changes.

* Thu Jul 13 2006 Steven Pritchard <steve@kspei.com> 1.67-1
- Update to 1.67.

* Thu May 18 2006 Steven Pritchard <steve@kspei.com> 1.66-1
- Update to 1.66.
- Drop regex patch.
- cpanspec now uses repoquery.

* Thu May 04 2006 Steven Pritchard <steve@kspei.com> 1.65-2
- Add cpanspec-1.65-regex.patch (fix broken regex, from 1.66 CVS).

* Wed Apr 26 2006 Steven Pritchard <steve@kspei.com> 1.65-1
- Update to 1.65.
- cpanget requires wget.

* Wed Mar 24 2006 Steven Pritchard <steve@kspei.com> 1.64-1
- Update to 1.64.

* Wed Mar 24 2006 Steven Pritchard <steve@kspei.com> 1.63-1
- Update to 1.63.

* Wed Mar 22 2006 Steven Pritchard <steve@kspei.com> 1.62-1
- Update to 1.62.

* Sat Mar 11 2006 Steven Pritchard <steve@kspei.com> 1.61-1
- Update to 1.61.

* Tue Mar 07 2006 Steven Pritchard <steve@kspei.com> 1.60-1
- Update to 1.60.

* Wed Feb 01 2006 Steven Pritchard <steve@kspei.com> 1.59-2
- URL/Source0 on SourceForge.
- Use a more appropriate Group.

* Tue Sep 20 2005 Steven Pritchard <steve@kspei.com> 1.59-1
- Update to 1.59.

* Mon Sep 19 2005 Steven Pritchard <steve@kspei.com> 1.58-1
- Update to 1.58.
- Comment out bogus URL and Source0 URL.

* Fri Sep 16 2005 Steven Pritchard <steve@kspei.com> 1.55-1
- Update to 1.55.
- Include man page.
- Drop explicit module dependencies.  (rpmbuild will figure it out.)

* Fri Sep 16 2005 Steven Pritchard <steve@kspei.com> 1.54-1
- Update to 1.54.

* Mon Sep 05 2005 Steven Pritchard <steve@kspei.com> 1.49-1
- Update to 1.49.
- Remove unneeded BuildRequires (no tests).
- Remove explicit core module requirements.

* Sat Sep 03 2005 Steven Pritchard <steve@kspei.com> 1.46-1
- Initial rpm release.
