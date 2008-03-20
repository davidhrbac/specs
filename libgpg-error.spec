Summary: libgpg-error
Name: libgpg-error
Version: 1.4
Release: 2%{?dist}
URL: ftp://ftp.gnupg.org/gcrypt/libgpg-error/
Source0: ftp://ftp.gnupg.org/gcrypt/libgpg-error/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/libgpg-error/%{name}-%{version}.tar.bz2.sig
Source2: wk@g10code.com
Source3: gpg-error.pc.in
Patch0:  libgpg-error-1.3-pkgconfig.patch
Group: System Environment/Libraries
License: LGPL
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prereq: /sbin/ldconfig

%description
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package devel
Summary: Development files for the %{name} package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future. This package
contains files necessary to develop applications using libgpg-error.

%prep
%setup -q
#%patch0 -p1 -b .pkgconfig
sed -i -e 's|^libdir=@libdir@$|libdir=@exec_prefix@/lib|g' src/gpg-error-config.in

%build
#cp -f %{SOURCE3} .
%configure
make

%install
rm -fr $RPM_BUILD_ROOT
%makeinstall
#mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
#cp -f gpg-error.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/gpg-error.pc
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT/%{_datadir}/common-lisp

%find_lang %{name}

%clean
rm -fr $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING COPYING.LIB AUTHORS README INSTALL NEWS ChangeLog
%{_bindir}/gpg-error
%{_libdir}/libgpg-error.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/gpg-error-config
%{_libdir}/libgpg-error.so
%{_libdir}/libgpg-error.a
#%{_libdir}/pkgconfig/gpg-error.pc
%{_includedir}/gpg-error.h
%{_datadir}/aclocal/gpg-error.m4

%changelog
* Tue Dec  4 2007 David Hrbáč <david@hrbac.cz> - 1.4-2.el4.hrb
- C4 rebuild

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.4-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 Bill Nottngham <notting@redhat.com> - 1.4-1
- update to 1.4
- don't ship lisp bindings

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.3-3.1
- rebuild

* Mon Jun  5 2006 Nalin Dahyabhai <nalin@redhat.com> 1.3-3
- give gpg-error-config libdir=@exec_prefix@/lib instead of @libdir@, so that
  it agrees on 32- and 64-bit arches (it suppresses the -L argument if @libdir@
  is /usr/lib, so this should be cleaner than adding a non-standard .pc file
  which upstream developers might inadvertently think they can depend to be on
  every system which provides this library)

* Mon May 15 2006 Karsten Hopp <karsten@redhat.de> 1.3-2
- switch to pkgconfig so that gpg-error-config can be the same on 
  32bit and 64bit archs

* Tue May  2 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.3-1
- update to version 1.3

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.1-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.1-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 30 2005 Karsten Hopp <karsten@redhat.de> 1.1-1
- update

* Wed Mar  2 2005 Bill Nottingham <notting@redhat.com> - 1.0-2
- we can rebuild it. we have the technology.

* Tue Aug 31 2004 Bill Nottingham <notting@redhat.com> - 1.0-1
- update to 1.0

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 16 2004 Bill Nottingham <notting@redhat.com> - 0.7-1
- adapt upstream specfile
