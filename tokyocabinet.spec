Summary:	A modern implementation of a DBM
Name:		tokyocabinet
Version:	1.4.46
Release:	1%{?dist}
License:	LGPLv2+
Group:		Development/Libraries
URL:		http://1978th.net/tokyocabinet/
Source:         http://1978th.net/%{name}/%{name}-%{version}.tar.gz
Patch0:		tokyocabinet-fedora.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	pkgconfig zlib-devel bzip2-devel autoconf

%description
Tokyo Cabinet is a library of routines for managing a database. It is the 
successor of QDBM. Tokyo Cabinet runs very fast. For example, the time required
to store 1 million records is 1.5 seconds for a hash database and 2.2 seconds
for a B+ tree database. Moreover, the database size is very small and can be up
to 8EB. Furthermore, the scalability of Tokyo Cabinet is great.

%package devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
This package contains the libraries and header files needed for
developing with %{name}.

%prep
%setup -q
%patch0 -p0 -b .fedora

%build
autoconf
%configure --enable-off64 CFLAGS="$CFLAGS"
make %{?_smp_mflags}
										
%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

rm -rf %{buildroot}%{_datadir}/%{name}
rm -rf %{buildroot}%{_libdir}/lib%{name}.a

%check
make check

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc ChangeLog COPYING README
%{_bindir}/tc*
%{_libdir}/libtokyocabinet.so.*
%{_libexecdir}/tcawmgr.cgi
%{_mandir}/man1/tc*.gz

%files devel
%defattr(-, root, root, -)
%{_includedir}/tc*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/t*.gz
%doc doc/*

%changelog
* Fri Aug 27 2010 David Hrbáč <david@hrbac.cz> - 1.4.46-1
- new upstream release

* Tue May 04 2010 David Hrbáč <david@hrbac.cz> - 1.4.44-1
- new upstream release

* Tue May 04 2010 David Hrbáč <david@hrbac.cz> - 1.4.43-2
- enable 64-bit file offset support

* Sat Mar 13 2010 David Hrbáč <david@hrbac.cz> - 1.4.43-1
- new upstream release

* Sun Feb 28 2010 David Hrbáč <david@hrbac.cz> - 1.4.42-1
- new upstream release

* Thu Jan 07 2010 David Hrbáč <david@hrbac.cz> - 1.4.41-1
- new upstream release

* Wed Nov 11 2009 David Hrbáč <david@hrbac.cz> - 1.4.33-1
- initial rebuild

* Wed Sep 30 2009 Deji Akingunola <dakingun@gmail.com> - 1.4.33-1
- Update to 1.4.33

* Fri Aug 28 2009 Deji Akingunola <dakingun@gmail.com> - 1.4.32-1
- Update to 1.4.32

* Mon Aug 10 2009 Deji Akingunola <dakingun@gmail.com> - 1.4.30-1
- New upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 03 2009 Deji Akingunola <dakingun@gmail.com> - 1.4.23-1
- Update to version 1.4.23

* Tue Mar 03 2009 Deji Akingunola <dakingun@gmail.com> - 1.4.9-1
- Update to version 1.4.9

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 13 2009 Deji Akingunola <dakingun@gmail.com> - 1.3.27-1
- Update to version 1.3.27

* Mon Aug 25 2008 Deji Akingunola <dakingun@gmail.com> - 1.3.4-1
- Update to 1.3.4

* Sun May 25 2008 Masahiro Hasegawa <masahase@gmail.com> - 1.2.6-1
- Update to 1.2.6

* Mon Apr 28 2008 Deji Akingunola <dakingun@gmail.com> - 1.2.5-1
- Update to 1.2.5

* Fri Feb 08 2008 Deji Akingunola <dakingun@gmail.com> - 1.1.14-1
- Update to 1.1.14

* Fri Jan 11 2008 Deji Akingunola <dakingun@gmail.com> - 1.1.7-1
- Update to 1.1.7

* Tue Dec 18 2007 Deji Akingunola <dakingun@gmail.com> - 1.1.4-1
- Update to 1.1.4

* Sat Nov 24 2007 Deji Akingunola <dakingun@gmail.com> - 1.0.8-1
- Update to 1.0.8

* Sat Nov 24 2007 Deji Akingunola <dakingun@gmail.com> - 1.0.6-1
- Initial package
