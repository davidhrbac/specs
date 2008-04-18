%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

%define php_pecl_name oci8 

Summary:      OCI8 functions
Name:         php-pecl-%{php_pecl_name}
Version:      1.2.4
Release:      1%{?dist}
License:      PHP License
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{php_pecl_name}

Source:       http://pecl.php.net/get/%{php_pecl_name}-%{version}.tgz
#Source1:      PHP-LICENSE-3.01
#Source2:      php-pecl-ssh2-0.10-README

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides:     php-pecl(%{php_pecl_name}) = %{version}-%{release}, php-%{php_pecl_name} = %{version}-%{release}

Requires:     php-api >= %{php_apiver}
#Requires:     oracle-instantclient-basic
Requires:  oracle-instantclient-basic = %(rpm -q oracle-instantclient-basic --qf "%%{version}-%%{release}\n")


BuildRequires: php-devel, zlib-devel
BuildRequires: oracle-instantclient-devel

%description
These functions allow you to access Oracle database servers using the Oracle Call
Interface (OCI8).

%prep 
%setup -c -q

#%{__install} -m 644 -c %{SOURCE1} LICENSE
#%{__install} -m 644 -c %{SOURCE2} README
%build
export ORACLE_HOME=/usr/lib/oracle/10.2.0.3/client
cd %{php_pecl_name}-%{version}
phpize
%configure --with-oci8=shared,instantclient,/usr/lib/oracle/10.2.0.3/client/lib
%{__make} %{?_smp_mflags}

%install
cd %{php_pecl_name}-%{version}
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
* Sat Feb  2 2008 David Hrbáč <david@hrbac.cz> 1.2.4-1
- update to version 1.2.4

* Fri Jul 27 2007 David Hrbáč <david@hrbac.cz> 1.2.3-2
- small changes

* Thu Jun 19 2007 David Hrbáč <david@hrbac.cz> 1.2.3-1
- initial spec created for CentOS-4
