Summary: A C library for multiple-precision floating-point computations
Name: mpfr
Version: 2.4.2
Release: 1%{?dist}
URL: http://www.mpfr.org/
Source0: http://www.mpfr.org/mpfr-current/%{name}-%{version}.tar.bz2
License: LGPLv2+ and GPLv2+ and GFDL
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: autoconf libtool gmp-devel
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: gmp >= 4.2.1

%description
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and 
also has a well-defined semantics. It copies the good ideas from the 
ANSI/IEEE-754 standard for double-precision floating-point arithmetic 
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

%package devel
Summary: Development tools A C library for mpfr library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: gmp-devel

%description devel
The static libraries, header files and documentation for using the MPFR 
multiple-precision floating-point library in applications.

If you want to develop applications which will use the MPFR library,
you'll need to install the mpfr-devel package.  You'll also need to
install the mpfr package.

%prep
%setup -q

%build

%configure --disable-assert
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
iconv  -f iso-8859-1 -t utf-8 mpfr.info >mpfr.info.aux
mv mpfr.info.aux mpfr.info
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libmpfr.la
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/libmpfr.a
cd ..
mkdir $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT/%{_docdir}/%{name}/ $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}/


%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
if [ -f %{_infodir}/mpfr.info.gz ]; then
    /sbin/install-info %{_infodir}/mpfr.info.gz %{_infodir}/dir || :
fi

%preun devel
if [ "$1" = 0 ]; then
    if [ -f %{_infodir}/mpfr.info.gz ]; then
	/sbin/install-info --delete %{_infodir}/mpfr.info.gz %{_infodir}/dir || :
    fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LIB NEWS README
%{_libdir}/libmpfr.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libmpfr.so
%{_includedir}/*.h
%{_infodir}/mpfr.info*

%changelog
* Fri Dec 18 2009 Ivana Hutarova Varekova <varekova@redhat.com> 2.4.2-1
- update to 2.4.2

* Fri Nov 13 2009 Ivana Varekova <varekova@redhat.com> 2.4.1-5
- fix 537328 - mpfr-devel should "Requires: gmp-devel"

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.4.1-4
- Use lzma compressed upstream tarball.

* Mon Aug 10 2009 Ivana Varekova <varekova redhat com> 2.4.1-3
- fix installation with --excludedocs option (#515958)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 11 2009 Ivana Varekova <varekova@redhat.com> - 2.4.1-1
- update to 2.4.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb  4 2009 Ivana Varekova <varekova@redhat.com> - 2.4.0-1
- update to 2.4.0

* Wed Oct 15 2008 Ivana Varekova <varekova@redhat.com> - 2.3.2-1
- update to 2.3.2

* Mon Jul 21 2008 Ivana Varekova <varekova@redhat.com> - 2.3.1-1
- update to 2.3.1

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.3.0-3
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 Ivana Varekova <varekova@redhat.com> 2.3.0-2
- rebuilt

* Thu Sep 20 2007 Ivana Varekova <varekova@redhat.com> 2.3.0-1
- update to 2.3.0
- fix license flag

* Mon Aug 20 2007 Ivana Varekova <varekova@redhat.com> 2.2.1-2
- spec file cleanup (#253440)

* Mon Jan 16 2007 Ivana Varekova <varekova@redhat.com> 2.2.1-1
- started

