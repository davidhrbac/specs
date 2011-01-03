%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Text_CAPTCHA_Numeral

Name:           php-pear-Text-CAPTCHA-Numeral
Version:        1.3.0
Release:        4%{?dist}
Summary:        Generation of numeral maths captchas

Group:          Development/Libraries
License:        BSD License
URL:            http://pear.php.net/package/Text_CAPTCHA_Numeral
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
Patch0:         Text-CAPTCHA-Numeral-setOperation.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}


%description
Numeral captcha generates mathematical operations and answers in order to
prove that bots using it are human

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml
%patch0 -p0
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
%{pear_phpdir}/Text/CAPTCHA/Numeral.php
%{pear_phpdir}/Text/CAPTCHA/Numeral/NumeralInterface.php

%{pear_testdir}/Text_CAPTCHA_Numeral


%changelog
* Tue Dec 21 2010 David Hrbáč <david@hrbac.cz> - 1.3.0-4
- patch to get rid of zero results

* Thu Nov 18 2010 David Hrbáč <david@hrbac.cz> - 1.3.0-3
- patch to work setOperation, not getOperation

* Thu Nov 18 2010 David Hrbáč <david@hrbac.cz> - 1.3.0-2
- patch to work getOperation again

* Tue Nov 16 2010 David Hrbáč <david@hrbac.cz> - 1.3.0-1
- initial release

