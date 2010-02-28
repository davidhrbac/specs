%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Services_Akismet

Name:           php-pear-Services-Akismet
Version:        1.0.1
Release:        1%{?dist}
Summary:        PHP client for the Akismet REST API

Group:          Development/Libraries
License:        MIT
URL:            http://pear.php.net/package/Services_Akismet
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}


%description
This package provides an object-oriented interface to the Akismet REST API.
Akismet is used to detect and to filter spam comments posted on weblogs.
Though the use of Akismet is not specific to Wordpress, you will need a
Wordpress API key from http://wordpress.com/api-keys/ to use this package.

Akismet is free for personal use and a license may be purchased for
commercial or high-volume applications.

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
%{pear_phpdir}/Services/Akismet/HttpClient/Curl.php
%{pear_phpdir}/Services/Akismet/HttpClient/Socket.php
%{pear_phpdir}/Services/Akismet/HttpClient/Stream.php
%{pear_phpdir}/Services/Akismet/Comment.php
%{pear_phpdir}/Services/Akismet/CommunicationException.php
%{pear_phpdir}/Services/Akismet/HttpClient.php
%{pear_phpdir}/Services/Akismet/InvalidApiKeyException.php
%{pear_phpdir}/Services/Akismet/InvalidCommentException.php
%{pear_phpdir}/Services/Akismet.php

%{pear_testdir}/Services_Akismet


%changelog
* Sun Feb 28 2010 David Hrbáč <david@hrbac.cz> - 1.0.1-1
- initial release
