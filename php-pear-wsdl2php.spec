%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%define pear_name wsdl2php

Name:           php-pear-wsdl2php
Version:        0.2.1
Release:        1%{?dist}
Summary:        PHP coding standards enforcement tool

Group:          Development/Tools
License:        BSD
URL:            http://www.urdalen.no/wsdl2php/index.php
Source0:        http://downloads.sourceforge.net/project/wsdl2php/wsdl2php/wsdl2php-%{version}-pear/wsdl2php-%{version}-pear.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires:       php-pear(PEAR)
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}

%description
wsdl2php is a very simple tool for PHP 5 to generate client code
against a WSDL-file.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{pear_name}.xml


%build
# Empty build section, 


%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT docdir
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{pear_name}.xml

# Move documentation
mkdir -p docdir


# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{pear_name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{pear_name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
#%doc %{pear_name}-%{version}/wsdl2php-licence.txt 
#%doc %{pear_name}-%{version}/docdir/*
%{pear_xmldir}/%{pear_name}.xml
#%{pear_testdir}/%{pear_name}
#%dir %{pear_phpdir}/PHP
%{pear_phpdir}/*.php
#%dir %{pear_datadir}
%{_bindir}/%{pear_name}



%changelog
* Tue Sep 15 2009 David Hrbáč <david@hrbac.cz> - 0.2.1-1
- initial release

