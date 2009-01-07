%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{default_extdir})
%{!?php_version:%define php_version %(php-config --version 2>/dev/null || echo %{default_version})}

Summary: PHP accelerator, optimizer, encoder and dynamic content cacher
Name: php-xcache
Version: 1.2.2
Release: 1%{?dist}
License: GPL
Group: Development/Languages
URL: http://xcache.lighttpd.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: php
Provides: php-zend_extension
BuildRequires: php, php-devel
BuildRequires: autoconf, automake, libtool
Source: http://xcache.lighttpd.net/pub/Releases/%{version}/xcache-%{version}.tar.gz

%description
XCache is a fast, stable PHP opcode cacher that has been tested and is now
running on production servers under high load. It is tested (on linux) and
supported on all of the latest PHP cvs branches such as PHP_4_3 PHP_4_4
PHP_5_1 PHP_5_2 HEAD(6.x). ThreadSafe/Windows is also supported.

%prep
%setup -n xcache-%{version}
# Change paths in the example config
%{__perl} -pi -e 's|/usr/local/lib/php/extensions/non-debug-non-zts-xxx/|%{php_extdir}/|g' xcache.ini

%build
phpize
%configure --enable-xcache

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# The cache directory where pre-compiled files will reside
%{__mkdir_p} %{buildroot}%{_var}/cache/php-xcache
%{__mkdir_p} %{buildroot}%{_var}/www/html/xcache/

# Drop in the bit of configuration
%{__install} -D -m 0644 xcache.ini \
    %{buildroot}%{_sysconfdir}/php.d/xcache.ini
%{__install} -D -m 0644 admin/* \
    %{buildroot}%{_var}/www/html/xcache/


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc xcache.ini admin/
#%config(noreplace) %{_sysconfdir}/php.d/xcache.ini
%config %{_sysconfdir}/php.d/xcache.ini
%{php_extdir}/xcache.so
%{_var}/www/html/xcache/*

%changelog
* Wed Jan  7 2009 David Hrbáč <david@hrbac.cz> - 1.2.2-1
- initial rebuild
