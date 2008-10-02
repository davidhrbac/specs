Name:           mod_auth_cas
Version:        1.0.7
Release:        1%{?dist}
Summary:        Apache authentication module for the CAS Single Sign-On service

Group:          System Environment/Daemons
License:        GPL
URL:            http://www.ja-sig.org/wiki/display/CASC/mod_auth_cas
Source0:        mod_auth_cas-%{version}.tar.gz
Source1:        mod_auth_cas.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel, openssl-devel
Requires:       httpd-mmn = %([ -a %{_includedir}/httpd/.mmn ] && %{__cat} %{_includedir}/httpd/.mmn || echo missing)

%description
mod_auth_cas is an Apache 2.0/2.2 compliant module that supports the
CASv1 and CASv2 protocols.  The purpose of this module is to allow
an Apache web server to interact with an authentication server that
conforms to the CAS version 1 or 2 protocol as specified by Yale/JA-SIG.
At the time of this writing, the CAS protocol specification is here:

http://www.ja-sig.org/products/cas/overview/protocol/index.html


%prep
%setup -q
cp -p %{SOURCE1} auth_cas.conf
apache_version=$(/usr/sbin/httpd -v | grep 'Server version:' | cut -f 2 -d /)
if [ ${apache_version%\.[0-9]*} = '2.0' ] ; then
	sed -i 's/#undef APACHE2_0/#define APACHE2_0/' mod_auth_cas.h
fi


%build
/usr/sbin/apxs -c mod_auth_cas.c


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/httpd/modules 
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
/usr/sbin/apxs -i -S LIBEXECDIR=%{buildroot}%{_libdir}/httpd/modules mod_auth_cas.la 
cp -p auth_cas.conf %{buildroot}%{_sysconfdir}/httpd/conf.d
install -d -m 700 %{buildroot}%{_localstatedir}/run/mod_auth_cas


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/httpd/modules/mod_auth_cas.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/auth_cas.conf
%attr(-,apache,apache) %{_localstatedir}/run/mod_auth_cas


%changelog
* Thu Sep 25 2008 David Hrbáč <david@hrbac.cz> - 1.0.7-1
- initial rebuild

* Mon Aug 18 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 1.0.7-1%{dist}
- Rebuilt on CentOS 5

* Thu May 22 2008 Jehan Procaccia <Jehan.Procaccia@it-sudparis.eu> 1.0.7
- Upgrade to version 1.0.7

* Sat Jan 26 2008 Jehan Procaccia <Jehan.Procaccia@it-sudparis.eu> 1.0.6
- Upgrade to version 1.0.6

* Tue Sep 11 2007 Josh Kelley <josh@jbc.edu> 1.0-1
- Upgrade to version 1.0

* Tue Aug 14 2007 Josh Kelley <josh@jbc.edu> 0.9.7-1
- Upgrade to version 0.9.7

* Wed Aug 01 2007 Josh Kelley <josh@jbc.edu> 0.9.4-3
- Remove explicit /usr/lib64 path

* Wed Aug 01 2007 Josh Kelley <josh@jbc.edu> 0.9.4-2
- Increase SSL verify depth to permit use of chained certificates

* Tue Jul 31 2007 Josh Kelley <josh@jbc.edu> 0.9.4-1
- Initial package
