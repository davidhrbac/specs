Summary:       Raptor RDF Parser Toolkit for Redland
Name:          raptor
Version:       1.4.21
Release:       1%{?dist}
License:       LGPLv2+ or ASL 2.0
Group:         System Environment/Libraries
Source:        http://download.librdf.org/source/raptor-%{version}.tar.gz
# Make the raptor-config file multilib friendly (RHBZ#477342)
Patch0:        raptor-config-multilib.patch
URL:           http://librdf.org/raptor/
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libxml2-devel libxslt-devel curl-devel

%description
Raptor is the RDF Parser Toolkit for Redland that provides
a set of standalone RDF parsers, generating triples from RDF/XML
or N-Triples.

%package devel
Summary: Libraries, includes etc to develop with Raptor RDF parser library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Libraries, includes etc to develop with Raptor RDF parser library.
It provides a set of standalone RDF parsers, generating triples from
RDF/XML or N-Triples.

%prep
%setup -q
%patch0 -p1 -b .multilib

# Fix encoding
iconv -f ISO-8859-1 -t UTF8 NEWS > NEWS.tmp
touch -r NEWS NEWS.tmp
mv -f NEWS.tmp NEWS

# hack to nuke rpaths
%if "%{_libdir}" != "/usr/lib"
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
rm -f ${RPM_BUILD_ROOT}%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS COPYING COPYING.LIB ChangeLog LICENSE-2.0.txt LICENSE.html
%doc LICENSE.txt  NEWS NEWS.html NOTICE README README.html RELEASE.html
%{_mandir}/man1/rapper.1*
%{_libdir}/libraptor.so.1*
%{_bindir}/rapper


%files devel
%defattr(-, root, root)
# include instuctions on how to build from source? omit for now, flog
# me with a wet noodle if I'm wrong  -- Rex
#doc INSTALL.html
%{_mandir}/man1/raptor-config.1*
%{_mandir}/man3/libraptor.3*
%doc %{_datadir}/gtk-doc/html/raptor/
%{_libdir}/libraptor.so
%{_libdir}/pkgconfig/raptor.pc
%{_includedir}/raptor.h
%{_bindir}/raptor-config

%changelog
* Sun Feb 14 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.4.21-1
- New bugfix release

* Sat Dec 12 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.4.20-1
- New version.

* Thu Oct 29 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.4.18-5
- Fix multilib conflict (RHBZ#477342)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 01 2009 Rex Dieter <rdieter@fedoraproject.org> 1.4.18-3
- nuke rpaths
- touchup %%files
- -devel: omit dup'd %%doc's included in main pkg

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 08 2008 Anthony Green <green@redhat.com> 1.4.18-1
- Update sources.

* Sat Feb 9 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.4.16-2
- Rebuild for GCC 4.3.

* Fri Oct 12 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.4.16-1
- Update to 1.4.16 (for Soprano 2, also lots of bugfixes).
- Specify LGPL version in License tag.
- Update URLs.

* Mon Feb 26 2007 Anthony Green <green@redhat.com> 1.4.14-3
- Update sources.

* Tue Feb 13 2007 Anthony Green <green@redhat.com> 1.4.14-2
- Upgrade to 1.4.14.
- Remove pkgconfig and config patches.

* Fri Nov 3 2006 Anthony Green <green@redhat.com> 1.4.9-6
- Rebuild for new libcurl.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.4.9-5
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Anthony Green <green@redhat.com> 1.4.9-4
- Fix release tag.

* Mon Sep 18 2006 Anthony Green <green@redhat.com> 1.4.9-3.1
- Rebuild.

* Mon Sep  4 2006 Anthony Green <green@redhat.com> 1.4.9-3
- BuildRequire pkgconfig in the devel package.

* Sun May  7 2006 Anthony Green <green@redhat.com> 1.4.9-2
- Move libraptor man page to devel package.
- Update sources to 1.4.9.

* Wed Apr 26 2006 Anthony Green <green@redhat.com> 1.4.8-5
- Add raptor-1.4.8-config.patch from Michael Schwendt.
- Remove some Requires from the devel package.

* Sun Apr 23 2006 Anthony Green <green@redhat.com> 1.4.8-4
- Add raptor-1.4.8-pkgconfig.patch from Michael Schwendt.

* Sun Apr 23 2006 Anthony Green <green@redhat.com> 1.4.8-3
- Many spec file fixes from Michael Schwendt.
- Add many Requires to the -devel package.

* Tue Apr 18 2006 Anthony Green <green@redhat.com> 1.4.8-1
- Upgrade sources.  
- Install with DESTDIR.
- Build for Fedora Extras.

* Fri Nov  7 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.0.0-1
- build for Planet CCRMA, clean up spec file

* Thu Apr 17 2003 Dave Beckett <Dave.Beckett@bristol.ac.uk>

- Added pkgconfig raptor.pc, raptor-config
- Requires curl

* Mon Jan 13 2003 Dave Beckett <Dave.Beckett@bristol.ac.uk>

- rdfdump now rapper

* Thu Jan  9 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu>
- built for planet ccrma
- one file conflicts with rdfdump in the nasm-rdoff package, so rename
  the binary to rdf-rdfdump for now. Maybe we should make this a
  "Conflict:" with nasm-rdoff and leave the file as is...

* Fri Dec 20 2002 Dave Beckett <Dave.Beckett@bristol.ac.uk>

- Updated to have two RPMs for raptor and raptor-devel.  Depend on
  libxml2 as XML parser.
