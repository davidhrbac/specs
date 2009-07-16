%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")

Summary:      A zip management extension
Name:         php-pecl-zip
Version:      1.8.10
Release:      2%{?dist}
License:      PHP License
Group:        Development/Languages
URL:          http://pecl.php.net/package/zip

Source:       http://pecl.php.net/get/zip-%{version}.tgz
Source1:      PHP-LICENSE-3.01
Source2:      xml2changelog

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides:     php-pecl(zip) = %{version}-%{release}, php-zip = %{version}-%{release}
BuildRequires: php-devel, zlib-devel
%if %{?php_zend_api}0
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}
%else
Requires:     php-api = %{php_apiver}
%endif

%description
Zip is an extension to create and read zip files.

%prep 
%setup -c -q

%{_bindir}/php -n %{SOURCE2} package.xml >CHANGELOG

%{__install} -m 644 -c %{SOURCE1} LICENSE

%build
cd zip-%{version}
phpize
%configure
%{__make} %{?_smp_mflags}

%install
cd zip-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/zip.ini << 'EOF'
; Enable ZIP extension module
extension=zip.so
EOF

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc LICENSE CHANGELOG zip-%{version}/CREDITS zip-%{version}/examples
%config(noreplace) %{_sysconfdir}/php.d/zip.ini
%{php_extdir}/zip.so

%changelog
* Fri Jul 10 2009 David Hrbáč <david@hrbac.cz> - 1.8.10-2
- initial rebuild

* Thu Jun 07 2007 Remi Collet <Fedora@FamilleCollet.com> 1.8.10-1
- update to 1.8.10

* Sun Mar 25 2007 Remi Collet <Fedora@FamilleCollet.com> 1.8.8-1
- update to 1.8.8

* Mon Feb 26 2007 Remi Collet <Fedora@FamilleCollet.com> 1.8.6-1
- update to 1.8.6

* Sat Feb 24 2007 Remi Collet <Fedora@FamilleCollet.com> 1.8.5-1
- update to 1.8.5
- requires php(zend-abi) and php(api) when available

* Sat Dec 02 2006 Remi Collet <Fedora@FamilleCollet.com> 1.8.2-1
- update to 1.8.2

* Thu Nov 02 2006 Remi Collet <Fedora@FamilleCollet.com> 1.8.0-1
- update to 1.8.0

* Tue Oct 24 2006 Remi Collet <Fedora@FamilleCollet.com> 1.7.5-1
- update to 1.7.5

* Wed Sep 27 2006 Remi Collet <Fedora@FamilleCollet.com> 1.7.4-1
- update to 1.7.4

* Sun Sep 17 2006 Remi Collet <Fedora@FamilleCollet.com> 1.7.3-1
- update to 1.7.3
- remove PECL from sumnary
- change to %%setup -c -q
- add generated CHANGELOG to %%doc

* Mon Aug 28 2006 Remi Collet <Fedora@FamilleCollet.com> 1.7.2-2
- rebuild for FE6

* Sun Aug 27 2006 Remi Collet <Fedora@FamilleCollet.com> 1.7.2-1
- update to 1.7.2

* Sat Aug 26 2006 Remi Collet <Fedora@FamilleCollet.com> 1.7.1-2
- use php_zip.c version 1.73 from CVS 
- see http://pecl.php.net/bugs/bug.php?id=8564

* Fri Aug 25 2006 Remi Collet <Fedora@FamilleCollet.com> 1.7.1-1
- update to 1.7.1
- change macros to conform to PHP Guidelines

* Sun Aug 20 2006 Remi Collet <Fedora@FamilleCollet.com> 1.7.0-1
- update to 1.7.0

* Sun Jul 30 2006 Remi Collet <Fedora@FamilleCollet.com> 1.6.0-1
- update to 1.6.0 (Big change : Rename Class Zip to ZipArchive)

* Sun Jul 16 2006 Remi Collet <Fedora@FamilleCollet.com> 1.5.0-1
- update to 1.5.0
- Requires: php-api

* Thu Jun 29 2006 Remi Collet <Fedora@FamilleCollet.com> 1.4.1-1
- update to 1.4.1
- bundle the v3.01 PHP LICENSE file
- Suppr. Requires zip, Add Provides php-pecl(zip) and php-zip
- change defattr

* Fri Apr 28 2006 Remi Collet <Fedora@FamilleCollet.com> 1.3.1-2
- Add zlib(devel) to Requires

* Thu Apr 27 2006 Remi Collet <Fedora@FamilleCollet.com> 1.3.1-1
- update to 1.3.1

* Wed Apr 26 2006 Remi Collet <Fedora@FamilleCollet.com> 1.2.3-1
- initial RPM for extras
- add french summary & description
- add examples to doc.

* Tue Apr 11 2006 Remi Collet <RPMS@FamilleCollet.com> 1.2.3-1
- initial RPM
