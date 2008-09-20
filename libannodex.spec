Name:           libannodex
Version:        0.7.3
Release:        10%{?dist}
Summary:        Library for annotating and indexing networked media

Group:          System Environment/Libraries
License:        BSD
URL:		http://www.annodex.net/
Source:		http://www.annodex.net/software/libannodex/download/%{name}-%{version}.tar.gz
Patch:          libannodex.man.patch
Patch1:         libannodex-0.7.3-macropen.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post): /sbin/ldconfig

BuildRequires:	doxygen
BuildRequires:	docbook-utils
BuildRequires:	libogg-devel >= 1.0
BuildRequires:	liboggz-devel >= 0.9.1
BuildRequires:	libcmml-devel >= 0.8
BuildRequires:	libsndfile-devel

# because of patch
BuildRequires:  libtool
BuildRequires:  autoconf
BuildRequires:  automake

# libtool
BuildRequires:	gcc-c++

%description
libannodex is a library to provide reading and writing of Annodex
files and streams.

%package devel
Summary:	Files needed for development using libannodex
Group:          Development/Libraries
Requires:       libannodex = %{version}
Requires:       liboggz-devel >= 0.9.1
Requires:       pkgconfig

%description devel
libannodex is a library to provide reading and writing of Annodex
files and streams.

This package contains the header files and documentation needed for
development using libannodex.

%prep
%setup -q -n %{name}-%{version}
%patch
%patch1 -p1 -b .macropen

aclocal -I m4
libtoolize
autoconf
automake

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall docdir=`pwd`/doxygen

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/annodex/importers/*.la

# remove doxygen build stamp; fixed in upstream CVS
rm -f $RPM_BUILD_ROOT%{_datadir}/doc/libannodex/doxygen-build.stamp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING README
# NEWS is empty in 0.6.2
# %doc NEWS
%{_libdir}/libannodex.so.*
%{_bindir}/anx*
%dir %{_libdir}/annodex
%dir %{_libdir}/annodex/importers
%{_libdir}/annodex/importers/libanx*.so*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%doc doxygen/html
%{_libdir}/libannodex.so
%{_libdir}/libannodex.a
%{_libdir}/pkgconfig/annodex.pc
%{_includedir}/annodex
%{_libdir}/annodex/importers/libanx*.a

%post
/sbin/ldconfig
# this allows the library to have text relocations
# this is needed so that mod_annodex does not stop httpd from starting
chcon -t texrel_shlib_t %{_libdir}/libannodex.so.*
exit 0


%postun -p /sbin/ldconfig

%changelog
* Sat Sep 20 2008 David Hrbáč <david@hrbac.cz> - 0.7.3-10
- initial rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.7.3-10
- Autorebuild for GCC 4.3

* Tue Oct 16 2007 Joe Orton <jorton@redhat.com> 0.7.3-9
- rebuild for expat 2.x

* Wed Aug  8 2007 Joe Orton <jorton@redhat.com> 0.7.3-8
- fix build with new glibc

* Mon Apr 23 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.3-7
- Own another directory.  Fixes #233859.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.7.3-5
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.3-4
- rebuilt

* Sun Mar 05 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.3-3
- added docbook-utils, needed for man page build

* Sun Mar 05 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.3-2
- added patch for man pages

* Sun Mar 05 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.3-1
- new upstream release

* Sun Nov 13 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.2-1: new upstream release

* Mon Jun 13 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.6.2-2: add dist tag

* Fri Jun 03 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.6.2-1: initial package
