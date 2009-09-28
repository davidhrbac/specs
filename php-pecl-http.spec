%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)
%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

%define pecl_name pecl_http

Name:           php-pecl-http
Version:        1.6.5
Release:        1%{?dist}
Summary:        The PHP PECL HTTP library

License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  php-devel libevent-devel curl-devel zlib-devel php-pear
Requires: curl libevent zlib
Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Provides:       php-pecl(http) = %{version}

%if %{?php_zend_api}0
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
%else
# for EL-5
Requires:       php-api = %{php_apiver}
%endif


%description
This HTTP extension aims to provide a convenient and powerful
set of functionality for one of PHPs major applications.

It eases handling of HTTP urls, dates, redirects, headers and
messages, provides means for negotiation of clients preferred
language and charset, as well as a convenient way to send any
arbitrary data with caching and resuming capabilities.

%package devel
Requires: php-pecl-http = %{version}
Summary: Development files for php-pecl-http
Group: Development/Languages
%description devel
Devel files for php-pecl-http.

%prep
%setup -c -q 

%{__rm} package.xml
%{__mv} package2.xml %{pecl_name}-%{version}/%{pecl_name}.xml

%build
cd %{pecl_name}-%{version}
phpize
%configure
%{__make} %{?_smp_mflags}

%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 %{pecl_name}.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
%{__install} -d %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable http extension module
extension=http.so
EOF


%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
#%doc LICENSE README
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/http.so
%{pecl_xmldir}/%{name}.xml

%files devel
%{_includedir}/php/ext/http/


%changelog
* Mon Sep 28 2009 David Hrbáč <david@hrbac.cz> - 1.6.5-1
- initial build
