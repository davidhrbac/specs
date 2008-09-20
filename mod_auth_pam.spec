Name:           mod_auth_pam
Version:        1.1.1
Release:        5%{?dist}
Summary:        PAM authentication module for Apache

Group:          System Environment/Daemons
License:        Distributable
URL:            http://pam.sourceforge.net/mod_auth_pam/
Source0:        http://pam.sourceforge.net/mod_auth_pam/dist/%{name}-2.0-%{version}.tar.gz
Source1:        mod_auth_pam-auth_pam.conf
Source2:        COPYING-mod_auth_pam
Source3:        mod_auth_pam-httpd.pam
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel pam-devel
Requires:       httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)

%description
The PAM authentication module implements Basic authentication on top of the
Pluggable Authentication Module library. Thereby it supports standard unix
passwd, shadow, NIS, SMB auth and radius authentication transparently and
easily interchangeable, wherever the HTTP protocol allows it.

%prep
%setup -q -n %{name}
find -name CVS -type d | xargs rm -r
install -p -m 644 %{SOURCE2} COPYING

%build
make %{?_smp_mflags} APXS=%{_sbindir}/apxs

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -m 755 .libs/%{name}.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -m 755 .libs/mod_auth_sys_group.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/auth_pam.conf

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/httpd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING README doc samples
%{_libdir}/httpd/modules/*.so
%config(noreplace) %{_sysconfdir}/pam.d/*
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf

%changelog
* Wed Sep 17 2008 David Hrbáč <david@hrbac.cz> - 1.1.1-5
- initial rebuild

* Wed Sep  5 2007 Brandon Holbrook <fedora at theholbrooks.org> 1.1.1-5
- Rebuild for new APR libs

* Tue Mar 20 2007 Brandon Holbrook <fedora at theholbrooks.org> 1.1.1-4
- Rebuild for Fedora 7

* Mon Sep  4 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.1.1-4
- Rebuild for Fedora Extras 6

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.1-4
- Rebuild for Fedora Extras 5

* Thu Dec 15 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.1-3
- Bump for Apache 2.2.0

* Fri Oct  7 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.1-2
- Use include instead of pam_stack

* Sat Sep 27 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.1-1
- Initial RPM release
