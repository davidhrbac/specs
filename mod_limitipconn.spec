Summary: Simultaneous connection limiting module for Apache
Name: mod_limitipconn
Version: 0.23
Release: 1%{?dist}
Group: System Environment/Daemons
License: ASL 2.0
URL: http://dominia.org/djao/limitipconn2.html
Source0: http://dominia.org/djao/limit/mod_limitipconn-%{version}.tar.bz2
Source1: mod_limitipconn.conf
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: httpd
Requires: httpd-mmn = %([ -a %{_includedir}/httpd/.mmn ] && cat %{_includedir}/httpd/.mmn || echo missing)
BuildRequires: httpd-devel

%description
Apache module which allows web server administrators to limit the number of
simultaneous downloads permitted from a single IP address. 

%prep
%setup -q


%build
%{_sbindir}/apxs -Wc,"%{optflags}" -c mod_limitipconn.c


%install
rm -rf %{buildroot}
install -D -p -m 0755 .libs/mod_limitipconn.so \
    %{buildroot}%{_libdir}/httpd/modules/mod_limitipconn.so
install -D -p -m 0644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/limitipconn.conf


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README INSTALL LICENSE
%config(noreplace) %{_sysconfdir}/httpd/conf.d/limitipconn.conf
%{_libdir}/httpd/modules/mod_limitipconn.so


%changelog
* Thu Apr 28 2009 David Hrbáč <david@hrbac.cz> - 0.23-1
- initial rebuild

* Mon Dec  1 2008 Matthias Saou <http://freshrpms.net/> 0.23-1
- Initial RPM release.

