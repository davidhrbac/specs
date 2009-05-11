Name:           mod_xsendfile
Version:        0.9
Release:        1%{?dist}
Summary:        Apache2 module that processes X-SENDFILE headers
Group:          System Environment/Daemons
License:        Apache License, Version 2.0
URL:            http://tn123.ath.cx/mod_xsendfile/
Source0:        http://tn123.ath.cx/mod_xsendfile/mod_xsendfile-%{version}.tar.gz
Source1:        mod_xsendfile.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  httpd-devel, apr-devel
Requires:   	httpd

%description
mod_xsendfile is a small Apache2 module that processes X-SENDFILE headers
registered by the original output handler. If it encounters the presence of such
header it will discard all output and send the file specified by that header
instead using Apache internals including all optimizations like caching-headers
and sendfile or mmap if configured. It is useful for processing script-output of
e.g. php, perl or any cgi.

%prep
%setup -q -n mod_xsendfile-%{version}


%build
apxs -c mod_xsendfile.c

%install
rm -rf %{buildroot}
install -D -m755 .libs/mod_xsendfile.so %{buildroot}/%{_libdir}/httpd/modules/mod_xsendfile.so
install -D -m644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/mod_xsendfile.conf

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc Readme.html
%{_libdir}/httpd/modules/mod_xsendfile.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_xsendfile.conf

%changelog
* Mon May 11 2009 David Hrbáč <david@hrbac.cz> - 0.9-1
- initial rebuild

* Thu Mar 19 2009 Serdar Bulut <serdar_bulut@phoenix.com> 0.9-1
- Centos 5 Release

