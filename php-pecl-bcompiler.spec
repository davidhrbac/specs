%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

%define php_pecl_name bcompiler 

Summary:      A bytecode compiler
Name:         php-pecl-%{php_pecl_name}
Version:      0.9.1
Release:      1%{?dist}
License:      PHP License
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{php_pecl_name}

Source:       http://pecl.php.net/get/%{php_pecl_name}-%{version}.tgz
#Source1:      PHP-LICENSE-3.01

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides:     php-pecl(%{php_pecl_name}) = %{version}-%{release}, php-%{php_pecl_name} = %{version}-%{release}

Requires:     php-api >= %{php_apiver}
Requires:     bzip2

BuildRequires: php-devel
BuildRequires: bzip2-devel

%description
bcompiler enables you to encode your scripts in phpbytecode, enabling you to protect the source code.
bcompiler could be used in the following situations

- to create a exe file of a PHP-GTK application (in conjunction with other software)
- to create closed source libraries
- to provide clients with time expired software (prior to payment)
- to deliver close source applications
- for use on embedded systems, where disk space is a priority.

For install instructions see the manual at pear.php.net

%prep 
%setup -c -q

#%{__install} -m 644 -c %{SOURCE1} LICENSE
%build
cd %{php_pecl_name}-%{version}
phpize
%configure
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
#%doc README
%config(noreplace) %{_sysconfdir}/php.d/%{php_pecl_name}.ini
%{php_extdir}/%{php_pecl_name}.so

%changelog
* Sun Nov 29 2009 David Hrbáč <david@hrbac.cz> - 0.9.1-1
- new upstream release

* Mon Dec  8 2008 David Hrbáč <david@hrbac.cz> 0.8-2
- initial spec created for CentOS
