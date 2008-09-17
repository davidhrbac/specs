Name:           mod_extract_forwarded
Version:        2.0.2
Release:        3%{?dist}
Summary:        Extract real source IP for forwarded HTTP requests

Group:          System Environment/Daemons
License:        Apache Software License
URL:            http://www.openinfo.co.uk/apache/
Source0:        http://www.openinfo.co.uk/apache/extract_forwarded-%{version}.tar.gz
Source1:	mod_extract_forwarded.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel >= 2.0.38
Requires:       httpd httpd-mmn = %([ -a %{_includedir}/httpd/.mmn ] && cat %{_includedir}/httpd/.mmn || echo missing)

%description
mod_extract_forwarded hooks itself into Apache's header parsing phase and looks 
for the X-Forwarded-For header which some (most?) proxies add to the proxied 
HTTP requests. It extracts the IP from the X-Forwarded-For and modifies the 
connection data so to the rest of Apache the request looks like it came from 
that IP rather than the proxy IP.

%prep
%setup -q -n extract_forwarded


%build
/usr/sbin/apxs -Wc,"%{optflags}" -c mod_extract_forwarded.c


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/httpd/modules/
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install -p .libs/mod_extract_forwarded.so %{buildroot}/%{_libdir}/httpd/modules/
install -m644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/

# Docs don't need to be executable
chmod -x INSTALL README

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc INSTALL README
%{_libdir}/httpd/modules/mod_extract_forwarded.so
%config(noreplace) /etc/httpd/conf.d/mod_extract_forwarded.conf


%changelog
* Wed Sep 17 2008 David Hrbáč <david@hrbac.cz> - 2.0.2-3
- initial rebuild

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.2-3
- Autorebuild for GCC 4.3

* Sat Sep 09 2006 Tim Jackson <rpm@timj.co.uk> 2.0.2-2
- Rebuild for FE6

* Wed Jan 11 2006 Tim Jackson <rpm@timj.co.uk> 2.0.2-1
- Initial build
