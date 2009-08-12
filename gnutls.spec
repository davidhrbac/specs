%define _with_guile 0
 
Summary: A TLS protocol implementation.
Name: gnutls
Version: 2.8.2
Release: 1%{?dist}
# The libgnutls library is LGPLv2+, utilities and remaining libraries are GPLv3+
License: GPLv3+ and LGPLv2+
Group: System Environment/Libraries
BuildRequires: libgcrypt-devel >= 1.3.1, gettext
BuildRequires: zlib-devel, readline-devel
BuildRequires: libtool, automake
#BuildRequires: guile-devel
URL: http://www.gnutls.org/
Source0: ftp://ftp.gnutls.org/pub/gnutls/%{name}-%{version}.tar.bz2
#Source1: ftp://ftp.gnutls.org/pub/gnutls/devel/%{name}-%{version}.tar.gz.sig
BuildRoot: %{_tmppath}/%{name}-root
Requires: libgcrypt >= 1.3.1
Source1: libgnutls-config

%if "%{centos_ver}" == "4"
  %ifarch x86_64
Provides: libgnutls.so.11(64bit)
Provides: libgnutls.so.11(GNUTLS_REL_1_0_9)(64bit)
  %else
Provides: libgnutls.so.11
Provides: libgnutls.so.11(GNUTLS_REL_1_0_9)
  %endif
%endif

%if "%{centos_ver}" == "5"
  %ifarch x86_64
Provides: libgnutls.so.13()(64bit)
Provides: libgnutls.so.13(GNUTLS_1_3)(64bit)
  %else
Provides: libgnutls.so.13
Provides: libgnutls.so.13(GNUTLS_1_3)
  %endif
%endif

%package devel
Summary: Development files for the %{name} package.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libgcrypt-devel
Requires: zlib-devel
Requires: pkgconfig
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%package utils
Summary: Command line tools for TLS protocol.
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%package guile
Summary: Guile bindings for the GNUTLS library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: guile

%description
GnuTLS is a project that aims to develop a library which provides a secure 
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.

%description devel
GnuTLS is a project that aims to develop a library which provides a secure
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.
This package contains files needed for developing applications with
the GnuTLS library.

%description utils
GnuTLS is a project that aims to develop a library which provides a secure
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.
This package contains command line TLS client and server and certificate
manipulation tools.

%description guile
GnuTLS is a project that aims to develop a library which provides a secure
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.
This package contains Guile bindings for the library.

%prep
%setup -q

for i in auth_srp_rsa.c auth_srp_sb64.c auth_srp_passwd.c auth_srp.c gnutls_srp.c ext_srp.c; do
    touch lib/$i
done

%build
#autoreconf
#%configure --with-libtasn1-prefix=%{_prefix} \
%configure --with-included-libcfg
#           --enable-guile
#           --disable-srp-authentication
make
cp lib/COPYING COPYING.LIB

%install
rm -fr $RPM_BUILD_ROOT
%makeinstall
#%if "%{centos_ver}" == "4"
#  ln -s $RPM_BUILD_ROOT%{_libdir}/libgnutls.so.26.1.6 $RPM_BUILD_ROOT%{_libdir}/libgnutls.so.13 
#%endif

rm -f $RPM_BUILD_ROOT%{_bindir}/srptool
rm -f $RPM_BUILD_ROOT%{_bindir}/gnutls-srpcrypt
cp -f %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/libgnutls-config
cp -f %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/libgnutls-extra-config
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/srptool.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/*srp*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libguile*.a
%find_lang libgnutls

cd $RPM_BUILD_ROOT%{_libdir}

%if "%{centos_ver}" == "4"
ln -s libgnutls-extra.so.26.1.6 libgnutls-extra.so.11
ln -s libgnutls-openssl.so.26.1.6 libgnutls-openssl.so.11
ln -s libgnutls.so.26.1.6 libgnutls.so.11
%endif

%if "%{centos_ver}" == "5"
ln -s libgnutls-extra.so.26.1.6 libgnutls-extra.so.13
ln -s libgnutls-openssl.so.26.1.6 libgnutls-openssl.so.13
ln -s libgnutls.so.26.1.6 libgnutls.so.13
%endif


%check
make check

%clean
rm -fr $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
if [ -f %{_infodir}/gnutls.info.gz ]; then
    /sbin/install-info %{_infodir}/gnutls.info.gz %{_infodir}/dir
fi

%preun devel
if [ $1 = 0 -a -f %{_infodir}/gnutls.info.gz ]; then
   /sbin/install-info --delete %{_infodir}/gnutls.info.gz %{_infodir}/dir
fi

%post guile -p /sbin/ldconfig

%postun guile -p /sbin/ldconfig

%files -f libgnutls.lang
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%doc COPYING COPYING.LIB README AUTHORS

%files devel
%defattr(-,root,root,-)
%{_bindir}/libgnutls*-config
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
#%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
%{_infodir}/gnutls*

%files utils
%defattr(-,root,root,-)
%{_bindir}/certtool
%{_bindir}/psktool
%{_bindir}/gnutls*
%{_mandir}/man1/*
%doc doc/certtool.cfg

%if %{_with_guile}
%files guile
%defattr(-,root,root,-)
%{_libdir}/libguile*.so*
%{_datadir}/guile/site/gnutls
%{_datadir}/guile/site/gnutls.scm
%endif

%changelog
* Wed Aug 12 2009 David Hrbáč <david@hrbac.cz> - 2.8.2-1
- new upstream version

* Mon Jul 20 2009 David Hrbáč <david@hrbac.cz> - 2.8.1-1
- new upstream version

* Sun Jun 14 2009 David Hrbáč <david@hrbac.cz> - 2.6.6-1
- new upstream version

* Tue May 19 2009 David Hrbáč <david@hrbac.cz> - 2.6.5-1
- new upstream version

* Tue May 19 2009 David Hrbáč <david@hrbac.cz> - 2.2.5-4
- dependency issue
- library symlinks

* Tue May 19 2009 David Hrbáč <david@hrbac.cz> - 2.2.5-3
- dependecy issue

* Mon May 18 2009 David Hrbáč <david@hrbac.cz> - 2.2.5-2
- dependecy issue

* Fri Mar 21 2008 David Hrbáč <david@hrbac.cz> - 2.1.7-3
- added libgnutls.so.13(GNUTLS_1_3) to fool dependencies

* Fri Dec 14 2007 David Hrbáč <david@hrbac.cz> - 2.1.7-2.el4.hrb
- added libgnutls.so.11(GNUTLS_REL_1_0_9) to fool dependencies

* Tue Dec  4 2007 David Hrbáč <david@hrbac.cz> - 2.1.7-1.el4.hrb
- update to the latest version

* Mon Aug 13 2007 David Hrbáč <david@hrbac.cz> - 1.4.1-2.el4.hrb
- C4 rebuild

* Thu Sep 14 2006 Tomas Mraz <tmraz@redhat.com> 1.4.1-2
- detect forged signatures - CVE-2006-4790 (#206411), patch
  from upstream

* Tue Jul 18 2006 Tomas Mraz <tmraz@redhat.com> - 1.4.1-1
- upgrade to new upstream version, only minor changes

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.4.0-1.1
- rebuild

* Wed Jun 14 2006 Tomas Mraz <tmraz@redhat.com> - 1.4.0-1
- upgrade to new upstream version (#192070), rebuild
  of dependent packages required

* Tue May 16 2006 Tomas Mraz <tmraz@redhat.com> - 1.2.10-2
- added missing buildrequires

* Mon Feb 13 2006 Tomas Mraz <tmraz@redhat.com> - 1.2.10-1
- updated to new version (fixes CVE-2006-0645)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 1.2.9-3
- rebuilt

* Fri Dec  9 2005 Tomas Mraz <tmraz@redhat.com> 1.2.9-2
- replaced *-config scripts with calls to pkg-config to
  solve multilib conflicts

* Wed Nov 23 2005 Tomas Mraz <tmraz@redhat.com> 1.2.9-1
- upgrade to newest upstream
- removed .la files (#172635)

* Sun Aug  7 2005 Tomas Mraz <tmraz@redhat.com> 1.2.6-1
- upgrade to newest upstream (rebuild of dependencies necessary)

* Mon Jul  4 2005 Tomas Mraz <tmraz@redhat.com> 1.0.25-2
- split the command line tools to utils subpackage

* Sat Apr 30 2005 Tomas Mraz <tmraz@redhat.com> 1.0.25-1
- new upstream version fixes potential DOS attack

* Sat Apr 23 2005 Tomas Mraz <tmraz@redhat.com> 1.0.24-2
- readd the version script dropped by upstream

* Fri Apr 22 2005 Tomas Mraz <tmraz@redhat.com> 1.0.24-1
- update to the latest upstream version on the 1.0 branch

* Wed Mar  2 2005 Warren Togami <wtogami@redhat.com> 1.0.20-6
- gcc4 rebuild

* Tue Jan  4 2005 Ivana Varekova <varekova@redhat.com> 1.0.20-5
- add gnutls Requires zlib-devel (#144069)

* Mon Nov 08 2004 Colin Walters <walters@redhat.com> 1.0.20-4
- Make gnutls-devel Require libgcrypt-devel

* Tue Sep 21 2004 Jeff Johnson <jbj@redhat.com> 1.0.20-3
- rebuild with release++, otherwise unchanged.

* Tue Sep  7 2004 Jeff Johnson <jbj@redhat.com> 1.0.20-2
- patent tainted SRP code removed.

* Sun Sep  5 2004 Jeff Johnson <jbj@redhat.com> 1.0.20-1
- update to 1.0.20.
- add --with-included-opencdk --with-included-libtasn1
- add --with-included-libcfg --with-included-lzo
- add --disable-srp-authentication.
- do "make check" after build.

* Fri Mar 21 2003 Jeff Johnson <jbj@redhat.com> 0.9.2-1
- upgrade to 0.9.2

* Tue Jun 25 2002 Jeff Johnson <jbj@redhat.com> 0.4.4-1
- update to 0.4.4.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat May 25 2002 Jeff Johnson <jbj@redhat.com> 0.4.3-1
- update to 0.4.3.

* Tue May 21 2002 Jeff Johnson <jbj@redhat.com> 0.4.2-1
- update to 0.4.2.
- change license to LGPL.
- include splint annotations patch.

* Tue Apr  2 2002 Nalin Dahyabhai <nalin@redhat.com> 0.4.0-1
- update to 0.4.0

* Thu Jan 17 2002 Nalin Dahyabhai <nalin@redhat.com> 0.3.2-1
- update to 0.3.2

* Wed Jan 10 2002 Nalin Dahyabhai <nalin@redhat.com> 0.3.0-1
- add a URL

* Wed Dec 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- initial package
