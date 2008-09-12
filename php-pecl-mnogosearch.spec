%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

%define php_pecl_name mnogosearch

Summary:      mnoGoSearch extension module for PHP
Name:         php-pecl-%{php_pecl_name}
Version:      1.96
Release:      1%{?dist}
License:      PHP License
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{php_pecl_name}

#Source:       http://pecl.php.net/get/%{php_pecl_name}-%{version}.tgz
Source:       http://www.mnogosearch.org/Download/php/mnogosearch-php-extension-%{version}.tar.gz
#Source1:      PHP-LICENSE-3.01
#Source2:      php-pecl-ssh2-0.10-README

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:     php-pecl(%{php_pecl_name}) = %{version}-%{release}, php-%{php_pecl_name} = %{version}-%{release}

Requires:     php-api >= %{php_apiver}
Requires:     mnogosearch

BuildRequires: php-devel, zlib-devel
BuildRequires: mnogosearch

%description
This extension is a complete PHP binding for the mnoGoSearch API.
For details please see to http://www.mnogosearch.org/ or the manual.

%prep 
%setup -c -q

#%{__install} -m 644 -c %{SOURCE1} LICENSE
#%{__install} -m 644 -c %{SOURCE2} README
%build
cd %{version}
phpize
%configure --with-mnogosearch=/usr
%{__make} %{?_smp_mflags}

%install
cd %{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{php_pecl_name}.ini << 'EOF'
; Enable %{php_pecl_name} extension module
extension=%{php_pecl_name}.so
EOF

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
#%doc LICENSE README
%config(noreplace) %{_sysconfdir}/php.d/%{php_pecl_name}.ini
%{php_extdir}/%{php_pecl_name}.so

%changelog
* Mon Feb  4 2008 David Hrbáč <david@hrbac.cz> 1.96-1
- update to 1.96
- dropped outdated http://pecl.php.net, taken from http://www.mnogosearch.org

* Fri Jul 27 2007 David Hrbáč <david@hrbac.cz> 1.0.0-2
- small changes

* Thu Jun 19 2007 David Hrbáč <david@hrbac.cz> 1.0.0-1
- initial spec created for CentOS-4
