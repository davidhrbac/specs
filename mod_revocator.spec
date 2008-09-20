Name: mod_revocator
Version: 1.0.2
Release: 4%{?dist}
Summary: CRL retrieval module for the Apache HTTP server
Group: System Environment/Daemons
License: Apache Software License
URL: http://directory.fedora.redhat.com/wiki/Mod_revocator
Source: http://directory.fedora.redhat.com/sources/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: nspr-devel >= 4.6, nss-devel >= 3.11
BuildRequires: nss-pkcs11-devel >= 3.11
BuildRequires: httpd-devel >= 0:2.0.52, apr-devel, apr-util-devel
BuildRequires: pkgconfig
BuildRequires: openldap-devel >= 2.2.29
Requires: httpd >= 0:2.0.52
Requires: nspr >= 4.6
Requires: nss >= 3.11, nss-tools >= 3.11
Requires: mod_nss >= 1.0.3
Patch1: mod_revocator-libpath.patch

%description
The mod_revocator module retrieves and installs remote
Certificate Revocate Lists (CRLs) into an Apache web server. 

%prep
%setup -q
%patch1 -p1

%build

CFLAGS="$RPM_OPT_FLAGS"
export CFLAGS

NSPR_INCLUDE_DIR=`/usr/bin/pkg-config --variable=includedir nspr`
NSPR_LIB_DIR=`/usr/bin/pkg-config --variable=libdir nspr`

NSS_INCLUDE_DIR=`/usr/bin/pkg-config --variable=includedir nss`
NSS_LIB_DIR=`/usr/bin/pkg-config --variable=libdir nss`

NSS_BIN=`/usr/bin/pkg-config --variable=exec_prefix nss`

%configure \
    --with-nss-lib=$NSS_LIB_DIR \
    --with-nss-inc=$NSS_INCLUDE_DIR \
    --with-nspr-lib=$NSPR_LIB_DIR \
    --with-nspr-inc=$NSPR_INCLUDE_DIR \
    --with-apr-config --enable-openldap

make %{?_smp_flags} all

%install
# The install target of the Makefile isn't used because that uses apxs
# which tries to enable the module in the build host httpd instead of in
# the build root.
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
mkdir -p $RPM_BUILD_ROOT%{_libdir}/httpd/modules
mkdir -p $RPM_BUILD_ROOT%{_bindir}

install -m 644 revocator.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/
install -m 755 .libs/libmodrev.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/mod_rev.so
# Ugh, manually create the ldconfig symbolic links
version=`grep -v '^\#' ./libtool-version`
current=`echo $version | cut -d: -f1`
revision=`echo $version | cut -d: -f2`
age=`echo $version | cut -d: -f3`
install -m  755 .libs/librevocation.so.$current.$revision.$age $RPM_BUILD_ROOT%{_libdir}/
(cd $RPM_BUILD_ROOT%{_libdir} && ln -s librevocation.so.$current.$revision.$age librevocation.so.0)
(cd $RPM_BUILD_ROOT%{_libdir} && ln -s librevocation.so.$current.$revision.$age  librevocation.so)
install -m 755 ldapget $RPM_BUILD_ROOT%{_bindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README LICENSE docs/mod_revocator.html
%config(noreplace) %{_sysconfdir}/httpd/conf.d/revocator.conf
%{_libdir}/httpd/modules/mod_rev.so
# rpmlint will complain that librevocation.so is a shared library but this
# must be ignored because this file is loaded directly by name by the Apache
# module.
%{_libdir}/librevocation.*so*
%{_bindir}/ldapget

%changelog
* Sat Sep 20 2008 David Hrbáč <david@hrbac.cz> - 1.0.2-4
- initial rebuild

* Mon Feb 25 2008 Rob Crittenden <rcritten@redhat.com> 1.0.2-4
- The nss package changed the location of the NSS shared libraries to /lib from
  /usr/lib. Static libraries remained in /usr/lib. They then updated their
  devel package to put symlinks back from /lib to /usr. Respin to pick that up.
  BZ 434395.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.2-3
- Autorebuild for GCC 4.3

* Wed Dec  5 2007 Rob Crittenden <rcritten@redhat.com> 1.0.2-2
- Respin to pick up new openldap

* Mon Oct 16 2006 Rob Crittenden <rcritten@redhat.com> 1.0.2-1
- Initial build
