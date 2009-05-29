# $Id: php-pecl-ssh2.spec,v 1.1 2008-05-19 11:38:25 dhrbac Exp $
# Authority: stefan
%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)
%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

%define pecl_name bbcode

Summary: %{pecl_name} - A Bzip2 management extension
Name: php-pecl-%{pecl_name}
Version: 1.0.2
Release: 1%{?dist}
License: PHP / BSD
Group: Development/Languages
URL: http://pecl.php.net/package/%{release}

Source: http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: php
BuildRequires: php, php-devel
BuildRequires: bzip2-devel 

%description
Bz2 is an extension to create and parse bzip2 compressed data.

%prep
%setup -n %{pecl_name}-%{version}


%build
# Workaround for broken phpize on 64 bits
%{_bindir}/phpize
%configure
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so


%changelog
* Fri May 29 2009 David Hrbáč <david@hrbac.cz> - 1.0.2-1
- initial build
