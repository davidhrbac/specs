%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Services_W3C_CSSValidator

Name:           php-pear-Services-W3C-CSSValidator
Version:        0.2.2
Release:        1%{?dist}
Summary:        An Object Oriented Interface to the W3C CSS Validator service

Group:          Development/Libraries
License:        BSD
URL:            http://pear.php.net/package/Services_W3C_CSSValidator
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
of the W3 CSS Validator application (http://jigsaw.w3.org/css-validator/).
With this package you can connect to a running instance of the validator
and
retrieve the validation results (true|false) as well as the errors and
warnings
for a a style sheet.

By using the SOAP 1.2 output format from the validator, you are returned
simple
objects containing all the information from the validator.

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
%{pear_phpdir}/Services/W3C/CSSValidator.php
%{pear_phpdir}/Services/W3C/CSSValidator/Error.php
%{pear_phpdir}/Services/W3C/CSSValidator/Message.php
%{pear_phpdir}/Services/W3C/CSSValidator/Response.php
%{pear_phpdir}/Services/W3C/CSSValidator/Warning.php

%{pear_testdir}/Services_W3C_CSSValidator


%changelog
* Tue Feb 01 2011 David Hrbáč <david@hrbac.cz> - 0.2.2-1
- initial rebuild
