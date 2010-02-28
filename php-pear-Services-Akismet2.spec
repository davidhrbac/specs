%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Services_Akismet2

Name:           php-pear-Services-Akismet2
Version:        0.3.0
Release:        1%{?dist}
Summary:        PHP client for the Akismet REST API

Group:          Development/Libraries
License:        MIT
URL:            http://pear.php.net/package/Services_Akismet2
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       php-pear(HTTP_Request2) >= 0.1.0, php-pear(PEAR) >= 1.4.0

%description
This package provides an object-oriented interface to the Akismet REST API.
The Akismet API is used to detect and to filter spam comments posted on
weblogs.

There are several anti-spam service providers that use the Akismet API. To
use the API, you will need an API key from such a provider. Example
providers include Wordpress (http://wordpress.com) and TypePad
(http://antispam.typepad.com).

Most services are free for personal or low-volume use, and offer licensing
for commercial or high-volume applications.

This package is derived from the miPHP Akismet class written by Bret Kuhns
for use in PHP 4. This package requires PHP 5.2.1.

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



%{pear_xmldir}/%{name}.xml
# Expand this as needed to avoid owning dirs owned by our dependencies
# and to avoid unowned dirs
%{pear_phpdir}/Services/Akismet2/Comment.php
%{pear_phpdir}/Services/Akismet2/HttpException.php
%{pear_phpdir}/Services/Akismet2/InvalidApiKeyException.php
%{pear_phpdir}/Services/Akismet2/InvalidCommentException.php
%{pear_phpdir}/Services/Akismet2.php

%{pear_testdir}/Services_Akismet2


%changelog
* Sun Feb 28 2010 David Hrbáč <david@hrbac.cz> - 0.3.0-1
- initial release
