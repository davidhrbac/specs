Name:           liboggz
Version:        0.9.7
Release:        1%{?dist}
Summary:        Simple programming interface for Ogg files and streams

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.annodex.net/
Source:         http://www.annodex.net/software/liboggz/download/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libogg-devel >= 1.0
BuildRequires:  doxygen
BuildRequires:  docbook-utils

# libtool
BuildRequires:  gcc-c++

%description
Oggz provides a simple programming interface for reading and writing Ogg files
and streams. Ogg is an interleaving data container developed by Monty at
Xiph.Org, originally to support the Ogg Vorbis audio format.

%package devel
Summary:	Files needed for development using liboggz
Group:          Development/Libraries
Requires:       liboggz = %{version}
Requires:       libogg-devel >= 1.0
Requires:       pkgconfig

%description devel
Oggz provides a simple programming interface for reading and writing Ogg files
and streams. Ogg is an interleaving data container developed by Monty at
Xiph.Org, originally to support the Ogg Vorbis audio format.

This package contains the header files and documentation needed for
development using liboggz.

%prep
%setup -q -n %{name}-%{version}

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall docdir=$RPM_BUILD_ROOT%{_datadir}/doc/%{name}-devel-%{version}

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# not particularly interested in the tex docs, the html version has everything
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-devel-%{version}/latex

%clean
rm -rf $RPM_BUILD_ROOT
                                                                                
%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING README
# 0 length NEWS file
# %doc NEWS
%{_libdir}/liboggz.so.*
%{_mandir}/man1/*
%{_bindir}/oggz*

%files devel
%defattr(-,root,root)
%{_includedir}/oggz
%{_libdir}/liboggz.so
%{_libdir}/liboggz.a
%{_libdir}/pkgconfig/oggz.pc
%doc %{_docdir}/%{name}-devel-%{version}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Sun Sep 21 2008 David Hrbáč <david@hrbac.cz> - 0.9.7-1
- new upstream version

* Sat Sep 20 2008 David Hrbáč <david@hrbac.cz> - 0.9.5-2
- initial rebuild

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.5-2
- Autorebuild for GCC 4.3

* Fri Jan 12 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.5-1
- new upstream release

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.9.4-3
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.4-2
- rebuilt

* Sun Mar 05 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.4-1
- new upstream release
- removed patch, was applied upstream

* Sat Nov 12 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.3-1
- new upstream release

* Mon Jul 18 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.2-1
- new upstream version
- removed patches
- moved devel docs to versioned location

* Mon Jun 13 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.1-2: rpmlint cleanup

* Fri Jun 03 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.1-1: initial package
