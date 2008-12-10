%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)                     
%define php_apiver %((echo %{default_apiver}; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)

Summary:       APC caches and optimizes PHP intermediate code
Name:          php-pecl-apc
Version:       3.0.19
Release:       1%{?dist}
License:       PHP License
Group:         Development/Languages
URL:           http://pecl.php.net/package/APC
Source:        http://pecl.php.net/get/APC-%{version}.tgz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:      php-api = %{php_apiver}
Conflicts:     php-mmcache php-eaccelerator
BuildRequires: php-devel httpd-devel
Provides:      php-apc = %{version}-%{release}
Obsoletes:     php-apc
Provides:      php-pecl(apc)

%description
APC is a free, open, and robust framework for 
caching and optimizing PHP intermediate code.

%prep
%setup -q -n APC-%{version}

%build
%{_bindir}/phpize
%configure --enable-apc-mmap --with-apxs=%{_sbindir}/apxs --with-php-config=%{_bindir}/php-config
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/apc.ini << 'EOF'
; Enable apc extension module
extension = apc.so
; Options for the apc module
apc.enabled=1
apc.shm_segments=1
apc.optimization=0
apc.shm_size=32
apc.ttl=7200
apc.user_ttl=7200
apc.num_files_hint=1024
apc.mmap_file_mask=/tmp/apc.XXXXXX
apc.enable_cli=1
apc.cache_by_default=1
EOF

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc TECHNOTES.txt CHANGELOG LICENSE NOTICE TODO INSTALL apc.php
%config(noreplace) %{_sysconfdir}/php.d/apc.ini
%{php_extdir}/apc.so

%changelog
* Wed Dec 10 2008 David Hrbáč <david@hrbac.cz> - 3.0.19-1
- new upstream version

* Fri Sep 15 2006 Chris Chabot <chabotc@xs4all.nl> - 3.0.12-5
- Updated to new upstream version

* Mon Sep 11 2006 Chris Chabot <chabotc@xs4all.nl> - 3.0.10-5
- FC6 rebuild 

* Sun Aug 13 2006 Chris Chabot <chabotc@xs4all.nl> - 3.0.10-4
- FC6T2 rebuild

* Mon Jun 19 2006 - Chris Chabot <chabotc@xs4all.nl> - 3.0.10-3
- Renamed to php-pecl-apc and added provides php-apc
- Removed php version string from the package version

* Mon Jun 19 2006 - Chris Chabot <chabotc@xs4all.nl> - 3.0.10-2
- Trimmed down BuildRequires
- Added Provices php-pecl(apc)

* Sun Jun 18 2006 - Chris Chabot <chabotc@xs4all.nl> - 3.0.10-1
- Initial package, templated on already existing php-json 
  and php-eaccelerator packages
