Summary:	mod_clamav is an filter which scans the content delivered by the proxy module 
Name:		mod_clamav
Version:	0.22
Release:	1%{?dist}
Group:		System Environment/Daemons
URL:		http://software.othello.ch/mod_clamav/
Source:		http://software.othello.ch/mod_clamav/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
License:	GPL
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	httpd-devel >= 2.0.52
BuildRequires:  clamav-devel >= 0.92
BuildRequires:  gmp-devel
Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel)
Requires:       httpd >= %(rpm -q httpd --qf "%%{version}-%%{release}\n")

%description
mod_clamav takes the output of the proxy module, and scans it for viruses using
the Clamav library (local mode) or the Clamav daemon (daemon mode). This means
that in local mode, the virus scanning engine is part of the apache process,
thus virus scanning does not take an extra round-trip to a virus scanning proxy,
as with many other virus scanning products.

%prep
%setup -q  
perl -pi -e "s|apxs2|apxs|g" Makefile
%build
#apxs -c %{name}.c
%configure --with-apxs=/usr/sbin/apxs

#make 

#debug version
#%{_sbindir}/apxs -DCLAMAV_DEBUG=\"1\" -c %{name}.c -Wl,-lclamav -lbz2 -lz -lpthread -lgmp
%{_sbindir}/apxs -c %{name}.c -Wl,-lclamav -lbz2 -lz -lpthread -lgmp

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
%doc AUTHORS ChangeLog COPYING INSTALL README safepatterns.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf
%attr(0755,root,root) %{_libdir}/httpd/modules/%{name}.so

%changelog
* Mon Sep 15 2008 David Hrbáč <david@hrbac.cz> - 0.22-1
- initial build
