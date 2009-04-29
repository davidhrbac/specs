%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)                     
%define php_apiver %((echo %{default_apiver}; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)

Summary:       Extension for safely dealing with input parameters
Name:          php-pecl-filter
Version:       0.11.0
Release:       1%{?dist}
License:       PHP License
Group:         Development/Languages
URL:           http://pecl.php.net/package/filter
Source:        http://pecl.php.net/get/filter-%{version}.tgz
Patch0:        php-pecl-filter.patch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:      php-api = %{php_apiver}
Requires:      pcre
BuildRequires: php-devel httpd-devel pcre pcre-devel
Provides:      php-filter = %{version}-%{release}
Obsoletes:     php-filter
Provides:      php-pecl(filter)

%description
The Input Filter extension is meant to address
this issue by implementing a set of filters
and mechanisms that users can use to safely
access their input data.

%prep
%setup -q -n filter-%{version}
%patch0 -p1

%build
%{_bindir}/phpize
%configure  --with-libdir=%{_lib} 
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/filter.ini << 'EOF'
; Enable filter extension module
extension = filter.so
EOF

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
#%doc TECHNOTES.txt CHANGELOG LICENSE NOTICE TODO INSTALL filter.php
%config(noreplace) %{_sysconfdir}/php.d/filter.ini
%{php_extdir}/filter.so

%changelog
* Thu Apr  2 2009 David Hrbáč <david@hrbac.cz> - 0.11.0-1
- initial build
