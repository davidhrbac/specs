Summary:          Utility library for 389 administration
Name:             389-adminutil
Version:          1.1.8
Release:          4%{?dist}
License:          LGPLv2
URL:              http://port389.org/wiki/AdminUtil
Group:            Development/Libraries
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    nspr-devel
BuildRequires:    nss-devel
BuildRequires:    svrcore-devel
BuildRequires:    mozldap-devel
BuildRequires:    libicu-devel
BuildRequires:    icu
Provides:         adminutil = %{version}-%{release}
Obsoletes:        adminutil < 1.1.8-2

Source0:          http://port389.org/sources/%{name}-%{version}.tar.bz2

%description
%{name} is libraries of functions used to administer directory
servers, usually in conjunction with the admin server.  %{name} is
broken into two libraries - libadminutil contains the basic
functionality, and libadmsslutil contains SSL versions and wrappers
around the basic functions.  The PSET functions allow applications to
store their preferences and configuration parameters in LDAP, without
having to know anything about LDAP.  The configuration is cached in a
local file, allowing applications to function even if the LDAP server
is down.  The other code is typically used by CGI programs used for
directory server management, containing GET/POST processing code as
well as resource handling (ICU ures API).

%package devel
Summary:  Development and header files for %{name}
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: nspr-devel
Requires: nss-devel
Requires: svrcore-devel
Requires: mozldap-devel
Requires: libicu-devel
Provides:  adminutil-devel = %{version}-%{release}
Obsoletes: adminutil-devel < 1.1.8-2

%description devel
Development files and header files necessary to build applications
that use %{name}.

%prep
%setup -q

%build

%configure --disable-tests
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/lib*.a
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README NEWS
%{_libdir}/*.so.*
%{_datadir}/%{name}

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/*.so
%{_includedir}/libadminutil
%{_includedir}/libadmsslutil

%changelog
* Wed Aug 12 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.8-4
- final 1.1.8 release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 12 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.8-2
- rename to 389-adminutil

* Tue Mar 31 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.8-1
- this is the 1.1.8 release

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 27 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.7-1
- Resolves bug 454060   -  ViewLog CGI crash with new adminutil
- Resolves bug 413531   -  Web browser accepted languages configuration causes dsgw CGI binaries to segfault

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.6-2
- fix license tag

* Mon Mar  3 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.6-1
- Resolves bug 245248 - dsgw doesn't escape filename in error message
- The new dsgw hasn't been released yet, and the old one doesn't use
- this code.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.5-2
- Autorebuild for GCC 4.3

* Thu Oct 18 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.5-1
- bump version to 1.1.5
- fix icu linking issue
- disable libtool rpath by default - added --enable-rpath option to configure

* Fri Aug 17 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.4-2
- remove >= version from icu build requires to fix rawhide build problem

* Wed Aug  1 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.4-1
- updated to version 1.1.4
- fixes bugzilla 250526

* Wed Jul 25 2007 Warren Togami <wtogami@redhat.com> - 1.1.3-1.1
- binutils/gcc bug rebuild (#249435)

* Tue Jul 24 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.3-1
- updated to version 1.1.3
- fixes bugzillas 246124 and 247192

* Fri Jun 22 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.2-1
- Updated version to 1.1.2
- This version fixes some memory leaks and invalid memory use
- issues

* Wed May 23 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.1-3
- more fedora review stuff - use macros consistently
- make sure install preserves timestamps
- use lgpl instead of gpl for acclanglist.c
- fix undefined weak symbols in libadmsslutil

* Fri May 18 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.1-2
- pkgconfig is a requires not a build requires

* Thu May 17 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.1-1
- Many bug fixes - bumped version to 1.1.1
- fixed concerns from Fedora package review

* Wed Mar 28 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1
- Initial version - based largely on svrcore.spec
