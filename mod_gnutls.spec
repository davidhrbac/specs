Summary:	mod_gnutls is a DSO module for the apache Web server.
Name:		mod_gnutls
Version:	0.5.5
Release:	1%{?dist}
Group:		System Environment/Daemons
URL:		http://www.outoforder.cc/projects/apache/mod_gnutls/
Source:		http://www.outoforder.cc/downloads/mod_gnutls/%{name}-%{version}.tar.bz2
Source1:	mod_gnutls.conf
License:	Apache Software License
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	httpd-devel >= 2.0.52
BuildRequires:	gnutls >= 2.4, gnutls-devel >= 2.4, gnutls-utils >= 2.4, apr-devel
Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel)
Requires:	gnutls >= 2.4
#Requires:	gnutls >= 2.1, httpd >= 2.0.52
Requires:	httpd >= %(rpm -q httpd --qf "%%{version}-%%{release}\n")

%description
mod_gnutls uses the GnuTLS library to provide SSL v3, TLS 1.0 and TLS 1.1
encryption for Apache HTTPD.  It is similar to mod_ssl in purpose, but does
not use OpenSSL.

%prep
%setup -q

%build

%configure \
  --with-apxs=%{_sbindir}/apxs \
  --with-libgnutls=%{_bindir}/libgnutls-config


make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -m755 src/.libs/lib%{name}.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules
%{__mv} $RPM_BUILD_ROOT%{_libdir}/httpd/modules/lib%{name}.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/%{name}.so

# Install the config file and the rsa and dh keys
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf
#install -m 640 data/{dh,rsa}file \
 #  $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/

#Create a cache directory
mkdir -p -m 0700 $RPM_BUILD_ROOT%{_var}/cache/mod_gnutls_cache

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc LICENSE NOTICE README
%{_libdir}/httpd/modules/*.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf
#%{_sysconfdir}/httpd/conf/dhfile
#%{_sysconfdir}/httpd/conf/rsafile
%attr(0700, apache, apache) %{_var}/cache/mod_gnutls_cache

%changelog
* Sun Jun 14 2009 David Hrbáč <david@hrbac.cz> - 0.5.5-1
- new upstream release

* Sat Sep 13 2008 David Hrbáč <david@hrbac.cz> - 0.4.3-2
- corrected httpd requires 

* Mon Jun 30 2008 David Hrbáč <david@hrbac.cz> - 0.4.3-1
- update to new version 0.4.3

* Sat Feb 23 2008 David Hrbáč <david@hrbac.cz> - 0.4.2.1-1.el4.hrb
- update to new version 0.4.2.1

* Fri Feb 22 2008 David Hrbáč <david@hrbac.cz> - 0.4.1-1.el4.hrb
- update to new version 0.4.1
 
* Mon Jan 21 2008 David Hrbáč <david@hrbac.cz> - 0.4.0-1.el4.hrb
- update to httpd-2.0.52-38.ent.centos4.2
 
* Tue Dec  4 2007 David Hrbáč <david@hrbac.cz> - 0.4.0-1.el4.hrb
- update to the latest version

* Fri Aug 17 2007 David Hrbáč <david@hrbac.cz> - 0.2.0-2.el4.hrb
- rename libmod_gnutls to mod_gnutls

* Mon Aug 13 2007 David Hrbáč <david@hrbac.cz> - 0.2.0-1.el4.hrb
- C4 rebuild

* Fri Aug 10 2007 Johnny Hughes <johnny@centos.org> 0.2.0-1
- Initial Build on CentOS
