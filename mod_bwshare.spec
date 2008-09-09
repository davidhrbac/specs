Name:           mod_bwshare
Version:        0.2.1
Release:        1%{?dist}
Summary:        Bandwidth limiting for apache
Group:          System Environment/Daemons
License:        GPL
URL:            http://www.topology.org/src/bwshare/README.html
Source0:        http://www.topology.org/src/bwshare/mod_bwshare-%{version}.zip
Source1:        mod_bwshare.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  httpd-devel
Requires:   	httpd httpd-mmn = %([ -a %{_includedir}/httpd/.mmn ] && cat %{_includedir}/httpd/.mmn || echo missing)    

%description
The Apache module mod_bwshare throttles HTTP requests to Apache 1 and 2
servers for each client IP address independently.  The mod_bwshare module
accepts or rejects HTTP requests from each client IP address based on
past downloads by that client IP address.  If the HTTP client's download
rate exceeds specified levels, the reponse to the HTTP client is an HTML
warning message.  A human browser will see a warning message indicating
how long to wait.

%prep
%setup -q -n mod_bwshare-%{version}


%build
/usr/sbin/apxs -c mod_bwshare.c

%install
rm -rf %{buildroot}
install -D -m755 .libs/mod_bwshare.so %{buildroot}/%{_libdir}/httpd/modules/mod_bwshare.so
install -D -m644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/mod_bwshare.conf

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENCE doc.html README.html changes.html
%{_libdir}/httpd/modules/mod_bwshare.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_bwshare.conf

%changelog
* Tue Sep  9 2008 David Hrbáč <david@hrbac.cz> - 0.2.0-1
- Initial release
