%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{default_extdir})
%{!?php_version:%define php_version %(php-config --version 2>/dev/null || echo %{default_version})}

Summary: Extremely fast and powerfull template engine
Name: php-blitz
Version: 0.6.10
Release: 1%{?dist}
License: GPL
Group: Development/Languages
URL: http://blitz.lighttpd.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: php
Provides: php-zend_extension
BuildRequires: php, php-devel
BuildRequires: autoconf, automake, libtool
Source:  http://downloads.sourceforge.net/project/blitz-templates/blitz-templates/%{version}/blitz-%{version}.tar.gz

%description
Blitzs is extremely fast and powerfull template engine for very big
internet projects.

%prep
%setup -n blitz-%{version}

%build
phpize
%configure 

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
#%{__install} -D -m 0644 blitz.ini %{buildroot}%{_sysconfdir}/php.d/blitz.ini


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
#%doc blitz.ini admin/
#%config(noreplace) %{_sysconfdir}/php.d/blitz.ini
#%config %{_sysconfdir}/php.d/blitz.ini
%{php_extdir}/blitz.so

%changelog
* Wed Jan 20 2010 David Hrbáč <david@hrbac.cz> - 0.6.10-1
- initial rebuild
