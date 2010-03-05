Name:           rasqal
Version:        0.9.17
Release:        2%{?dist}
Summary:        RDF Query Library

Group:          System Environment/Libraries
License:        LGPLv2+ or ASL 2.0
URL:            http://librdf.org/rasqal/
Source:         http://download.librdf.org/source/%{name}-%{version}.tar.gz
# Fix DSO linking error. Note that this is fixed in upstream trunk
# http://bugs.librdf.org/mantis/view.php?id=347
# But their fix requires an autoreconf cycle. We just do a
# simple hack for the time being. This patch will be dropped
# in the next version after 0.9.17
Patch0:         %{name}-0.9.17-linking.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libxml2-devel
BuildRequires:  mpfr-devel
BuildRequires:  pcre-devel
BuildRequires:  raptor-devel >= 1.4.18
# for the testsuite
BuildRequires:  perl(XML::DOM)

#Requires: raptor >= 1.4.18

%description
Rasqal is a library providing full support for querying Resource
Description Framework (RDF) including parsing query syntaxes, constructing
the queries, executing them and returning result formats.  It currently
handles the RDF Data Query Language (RDQL) and SPARQL Query language.

%package        devel
Summary:        Development files for the Rasqal RDF libraries
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gtk-doc
Requires:       pkgconfig
Requires:       raptor-devel
%description    devel
Libraries, includes etc to develop with the Rasqal RDF query language library.


%prep
%setup -q
%patch0 -p1 -b .linking.fix

# hack to nuke rpaths
%if "%{_libdir}" != "/usr/lib"
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif


%build

%configure --enable-release --with-raptor=system --disable-static

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la


%check
%ifarch ppc64
make -k check ||:
%else
make -k check
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYING.LIB ChangeLog LICENSE.txt NEWS README
%doc LICENSE-2.0.txt NOTICE
%doc *.html
%{_bindir}/roqet
%{_libdir}/librasqal.so.2*
%{_mandir}/man1/roqet.1*

%files devel
%defattr(-,root,root,-)
%doc docs/README.html
%{_bindir}/rasqal-config
%{_includedir}/rasqal/
%{_libdir}/librasqal.so
%{_libdir}/pkgconfig/rasqal.pc
%{_mandir}/man1/rasqal-config.1*
%{_mandir}/man3/librasqal.3*
%{_datadir}/gtk-doc/html/rasqal/


%changelog
* Sat Feb 13 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.9.17-2
- Fix DSO linking error RHBZ#564859

* Sun Jan 03 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.9.17-1
- rasqal-0.9.17

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.9.15-5
- slightly less ugly rpath hacks
- cleanup %%files

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.9.15-3
- disable testsuite so this builds
- rebuild for pkg-config Provides

* Sun Nov 23 2008 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.15-2
- update summary
- not rebuilt yet

* Sat Feb 09 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.9.15-1
- Update to 0.9.15 (for redland 1.0.7, also lots of bugfixes)
- Update minimum raptor version
- BR perl(XML::DOM) (needed by the testsuite)

* Mon Oct 15 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.9.14-2
- Update minimum raptor version

* Mon Oct 15 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.9.14-1
- Update to 0.9.14 (for redland 1.0.6, also lots of bugfixes)
- Specify LGPL version in License tag

* Mon Dec 18 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.12-5
- added pcre-devel and libxml2-devel buildrequires

* Wed Dec 13 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.12-4
- Requires: pkgconfig in -devel package (Kevin Fenzi)

* Fri Nov 17 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.12-3
- rpmlint cleanup

* Thu Oct 26 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.12-2
- Surrender and use DESTDIR install

* Sat Jun 17 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.12-2
- fixed x86_64 rpath issue with an ugly hack
- removed OPTIMIZE from make invocation
- added smp flags
- added make check
- updated license

* Sun May 14 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.12-1
- new upstream release

* Fri Apr 07 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.11-1: packaged for Fedora Extras

* Wed Aug 11 2005  Dave Beckett <dave.beckett@bristol.ac.uk>
- Update Source:
- Use makeinstall macro

* Wed Aug 10 2005  Dave Beckett <dave.beckett@bristol.ac.uk>
- Use configure macro.

* Fri Jul 28 2005  Dave Beckett <dave.beckett@bristol.ac.uk>
- Updated for gtk-doc locations

* Fri Oct 22 2004 <Dave.Beckett@bristol.ac.uk>
- License now LGPL/Apache 2
- Added LICENSE-2.0.txt and NOTICE

* Wed May 5 2004 <Dave.Beckett@bristol.ac.uk>
- Ship roqet and roqet.1

* Sat May 1 2004 <Dave.Beckett@bristol.ac.uk>
- Requires raptor 1.3.0

* Mon Feb 24 2004 <Dave.Beckett@bristol.ac.uk>
- Requires raptor

* Mon Aug 11 2003 <Dave.Beckett@bristol.ac.uk>
- Initial packaging
