Summary:	Simple module allows you to change server header.
Name:		mod_sesehe
Version:	0.1.0
Release:	1%{?dist}
Group:		System Environment/Daemons
URL:		http://jok.is-a-geek.net/mod_sesehe.php
#Source:		http://jok.is-a-geek.net/code/mod_sesehe.c
Source:         mod_sesehe.tar.gz
Source1:	%{name}.conf
License:	Apache Software License
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	httpd-devel >= 2.0.52
Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel)
Requires:       httpd >= %(rpm -q httpd --qf "%%{version}-%%{release}\n")

%description
Simple module allows you to change server header. Despite what some people are
saying, even mod_headers can't suppress it.

%prep
%setup -q -c -n %{name} 
%build
apxs -c %{name}.c
#configure 

#make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/httpd/modules

install -m0755 .libs/*.so %{buildroot}%{_libdir}/httpd/modules

# Install the config file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf
%attr(0755,root,root) %{_libdir}/httpd/modules/%{name}.so

%changelog
* Sun Jun 28 2009 David Hrbáč <david@hrbac.cz> - 0.1.0-2
- updated URL

* Mon Sep 15 2008 David Hrbáč <david@hrbac.cz> - 0.1.0-1
- initial build
