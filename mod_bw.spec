Summary: Bandwidth administration module for the Apache Web server
Name: mod_bw
Version: 0.8
Release: 1%{?dist}
License: Apache Software License
Group: System Environment/Daemons
URL: http://www.ivn.cl/apache/
Source0: http://www.ivn.cl/apache/files/source/%{name}-%{version}.tgz
Source1: %{name}-0.8.conf
Requires: httpd >= 2.0.0
BuildRequires: httpd-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
%{name} is a bandwidth administration module for the Apache Web server.
The module has the following features:

- Restrict the number of simultaneous connections per vhost/dir
- Limit the bandwidth for files on vhost/dir

%prep
%setup -q -n %{name}

%build
%{_sbindir}/apxs -c %{name}.c

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{_libdir}/httpd/modules
%{__install} -d %{buildroot}%{_sysconfdir}/httpd/conf.d
%{__install} -m 0755 -p .libs/%{name}.so %{buildroot}%{_libdir}/httpd/modules/
%{__install} -m 0644 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog LICENSE TODO mod_bw.txt
%{_libdir}/httpd/modules/%{name}.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf

%changelog
* Tue Sep  9 2008 David Hrbáč <david@hrbac.cz> - 0.8-1
- Initial release

