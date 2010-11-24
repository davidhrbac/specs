Name: libgcrypt
Version: 1.4.6
Release: 1%{?dist}
Source0: ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-%{version}.tar.bz2.sig

#Source0: ftp://ftp.gnupg.org/gcrypt/alpha/libgcrypt/libgcrypt-%{version}.tar.bz2
#Source1: ftp://ftp.gnupg.org/gcrypt/alpha/libgcrypt/libgcrypt-%{version}.tar.bz2.sig

Source2: wk@g10code.com
Patch0: libgcrypt-1.2.2-lib64.patch
License: LGPL
Summary: A general-purpose cryptography library.
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libgpg-error-devel pkgconfig
Group: System Environment/Libraries

%package devel
Summary: Development files for the %{name} package.
Group: Development/Libraries
PreReq: /sbin/install-info
Requires: libgpg-error-devel >= 1.4
Requires: %{name} = %{version}-%{release}

%description
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.  This is a development version.

%description devel
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.  This package contains files needed to develop
applications using libgcrypt.

%prep
%setup -q
#%patch0 -p1 -b .lib64

%build
%configure 
#--disable-asm
make
make check

%install
rm -fr $RPM_BUILD_ROOT
%makeinstall

# Change /usr/lib64 back to /usr/lib.  This saves us from having to patch the
# script to "know" that -L/usr/lib64 should be suppressed, and also removes
# a file conflict between 32- and 64-bit versions of this package.
sed -i -e 's,^libdir="/usr/lib.*"$,libdir="/usr/lib",g' $RPM_BUILD_ROOT/%{_bindir}/libgcrypt-config

rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir ${RPM_BUILD_ROOT}/%{_libdir}/*.la
/sbin/ldconfig -n $RPM_BUILD_ROOT/%{_libdir}

%clean
rm -fr $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/gcrypt.info.gz %{_infodir}/dir

%preun devel
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gcrypt.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
#%{_libdir}/%{name}

%files devel
%defattr(-,root,root)
%{_bindir}/%{name}-config
%{_bindir}/dumpsexp
%{_bindir}/hmac256
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_datadir}/aclocal/*
#%{_datadir}/%{name}

%{_infodir}/gcrypt.info*

%changelog
* Thu Nov 18 2010 David Hrbáč <david@hrbac.cz> - 1.4.6-1
- new upstream release

* Tue Dec  4 2007 David Hrbáč <david@hrbac.cz> - 1.3.1-1.el4.hrb
- update to the latest version

* Mon Aug 13 2007 David Hrbáč <david@hrbac.cz> - 1.2.3-1.el4.hrb
- C4 rebuild

* Fri Sep  1 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.2.3-1
- update to 1.2.3

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.2-3.1
- rebuild

* Mon Jun 05 2006 Jesse Keating <jkeating@redhat.com> 1.2.2-3
- Added missing buildreq pkgconfig

* Tue May 16 2006 Nalin Dahyabhai <nalin@redhat.com> 1.2.2-2
- remove file conflicts in libgcrypt-config by making the 64-bit version
  think the libraries are in /usr/lib (which is wrong, but which it also
  prunes from the suggest --libs output, so no harm done, hopefully)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.2-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.2-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Oct  5 2005 Nalin Dahyabhai <nalin@redhat.com> 1.2.2-1
- update to 1.2.2

* Wed Mar 16 2005 Nalin Dahyabhai <nalin@redhat.com> 1.2.1-1
- update to 1.2.1

* Fri Jul 30 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- another try to package the symlink

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun May  2 2004 Bill Nottingham <notting@redhat.com> - 1.2.0-1
- update to official 1.2.0

* Fri Apr 16 2004 Bill Nottingham <notting@redhat.com> - 1.1.94-1
- update to 1.1.94

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Feb 21 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- add symlinks to shared libs at compile time

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Mar 20 2003 Jeff Johnson <jbj@redhat.com> 1.1.12-1
- upgrade to 1.1.12 (beta).

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Jeff Johnson <jbj@redhat.com>
- update to 1.1.7
- change license to LGPL.
- include splint annotations patch.
- install info pages.

* Tue Apr  2 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.6-1
- update to 1.1.6

* Thu Jan 10 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.5-1
- fix the Source tag so that it's a real URL

* Wed Dec 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- initial package
