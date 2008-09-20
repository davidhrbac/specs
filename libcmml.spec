Name:           libcmml
Version:        0.9.1
Release:        5%{?dist}
Summary:        Library for handling Continuous Media Markup Language

Group:          System Environment/Libraries
License:        BSD
URL:		http://www.annodex.net/
Source:		http://www.annodex.net/software/libcmml/download/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	doxygen
BuildRequires:	expat-devel

# libtool
BuildRequires:	gcc-c++

%description
Libcmml is a library which enables the handling of documents
written in CMML (Continuous Media Markup Language) for the
Continuous Media Web (CMWeb).

It provides a very simple API for reading files marked up with the
Continuous Media Markup Language (CMML), and returns C structures
containing this information in a format which can be used by an
Annodexer for creating ANNODEX(tm) format documents (ANX).

%package devel
Summary:	Files needed for development using libcmml
Group:          Development/Libraries
Requires:       libcmml = %{version}
Requires:       pkgconfig
Requires:	expat-devel

%description devel
Libcmml is a library which enables the handling of documents
written in CMML (Continuous Media Markup Language) for the
Continuous Media Web (CMWeb).

It provides a very simple API for reading files marked up with the
Continuous Media Markup Language (CMML), and returns C structures
containing this information in a format which can be used by an
Annodexer for creating ANNODEX(tm) format documents (ANX).

This package contains the header files and documentation needed for
development using libcmml.

%prep
%setup -q -n %{name}-%{version}

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall docdir=`pwd`/doxygen

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# remove doxygen build stamp; fixed in upstream CVS
rm -f $RPM_BUILD_ROOT%{_datadir}/doc/libcmml/doxygen-build.stamp

%clean
rm -rf $RPM_BUILD_ROOT
                                                                                
%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README
# zero length NEWS file
# %doc NEWS
%{_libdir}/libcmml.so.*
%{_bindir}/cmml*

%files devel
%defattr(-,root,root)
%doc doxygen/html
%{_libdir}/libcmml.so
%{_libdir}/libcmml.a
%{_libdir}/pkgconfig/cmml.pc
%{_includedir}/cmml.h

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Sat Sep 20 2008 David Hrbáč <david@hrbac.cz> - 0.9.1-5
- initial rebuild

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.1-5
- Autorebuild for GCC 4.3

* Tue Oct 16 2007 Joe Orton <jorton@redhat.com> 0.9.1-4
- rebuild for expat 2.x (#296301)

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.9.1-3
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.1-2
- rebuilt

* Sun Mar 05 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.1-1
- new upstream release

* Thu Jun 16 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.0-2: suggestions from Ville

* Sat Jun 04 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.0-1: initial package
