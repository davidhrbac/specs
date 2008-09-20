Name:           mod_dnssd
Version:        0.5
Release:        6%{?dist}
Summary:        An Apache HTTPD module which adds Zeroconf support

Group:          System Environment/Daemons
License:        Apache Software License
URL:            http://0pointer.de/lennart/projects/mod_dnssd/
Source0:        http://0pointer.de/lennart/projects/mod_dnssd/%{name}-%{version}.tar.gz
Source1:        mod_dnssd.conf-httpd
Patch0:         mod_dnssd-r63-uid.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel avahi-devel e2fsprogs-devel

%description
mod_dnssd is an Apache HTTPD module which adds Zeroconf support via DNS-SD
using Avahi.

%prep
%setup -q
%patch0 -p2 -b .uid

%build
%configure --disable-lynx
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
install -Dp -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/mod_dnssd.conf
install -Dp src/.libs/mod_dnssd.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/mod_dnssd.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE doc/README doc/README.html
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_dnssd.conf
%{_libdir}/httpd/modules/mod_dnssd.so

%changelog
* Wed Sep 17 2008 David Hrbáč <david@hrbac.cz> - 0.5-6
- initial rebuild

* Sun Feb 10 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.5-6
- Rebuild for GCC 4.3

* Mon Sep  3 2007 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.5-5
- Rebuild for new 32-bit APR ABI

* Tue Aug 21 2007 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.5-4
- Fix License tag
- Rebuild for F8t2

* Tue Jul 24 2007 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.5-3
- Add upstream patch to fix UID issue

* Mon Jun 25 2007 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.5-2
- Add LoadModule to the config file

* Mon Jun 18 2007 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.5-1
- Initial RPM release
