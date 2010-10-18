%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Services_W3C_HTMLValidator

Name:           php-pear-Services-W3C-HTMLValidator
Version:        1.0.0
Release:        1%{?dist}
Summary:        An Object Oriented Interface to the W3C HTML Validator service

Group:          Development/Libraries
License:        BSD
URL:            http://pear.php.net/package/Services_W3C_HTMLValidator
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       php-pear(HTTP_Request2) >= 0.2.0, php-pear(PEAR) >= 1.5.4

%description
This package provides an object oriented interface to the API
of the W3 HTML Validator application (http://validator.w3.org/).
With this package you can connect to a running instance of the validator
and
retrieve the validation results (true|false) as well as the errors and
warnings
for a web page.

By using the SOAP 1.2 output format from the validator, you are returned
simple
objects containing all the information from the validator. With this
package it is
trivial to build a validation system for web publishing.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml
cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT docdir
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Move documentation
mkdir -p docdir
mv $RPM_BUILD_ROOT%{pear_docdir}/* docdir


# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.php.net/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_name}-%{version}/docdir/%{pear_name}/*


%{pear_xmldir}/%{name}.xml
# Expand this as needed to avoid owning dirs owned by our dependencies
# and to avoid unowned dirs
%{pear_phpdir}/Services/W3C/HTMLValidator/Error.php
%{pear_phpdir}/Services/W3C/HTMLValidator/Exception.php
%{pear_phpdir}/Services/W3C/HTMLValidator/Message.php
%{pear_phpdir}/Services/W3C/HTMLValidator/Response.php
%{pear_phpdir}/Services/W3C/HTMLValidator/Warning.php
%{pear_phpdir}/Services/W3C/HTMLValidator.php

%{pear_testdir}/Services_W3C_HTMLValidator


%changelog
* Mon Oct 18 2010 David Hrbáč <david@hrbac.cz> - 1.0.0-1
- initial release

