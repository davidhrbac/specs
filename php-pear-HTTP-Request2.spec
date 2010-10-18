%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name HTTP_Request2

Name:           php-pear-HTTP-Request2
Version:        0.5.2
Release:        1%{?dist}
Summary:        Provides an easy way to perform HTTP requests

Group:          Development/Libraries
License:        BSD License
URL:            http://pear.php.net/package/HTTP_Request2
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       php-pear(Net_URL2) >= 0.2.0, php-pear(PEAR) >= 1.5.4

%description
PHP5 rewrite of HTTP_Request package. Provides cleaner API and pluggable
Adapters. Currently available are:
  * Socket adapter, based on old HTTP_Request code,
  * Curl adapter, wraps around PHP's cURL extension,
  * Mock adapter, to use for testing packages dependent on HTTP_Request2.
Supports POST requests with data and file uploads, basic and digest 
authentication, cookies, proxies, gzip and deflate encodings, redirects,
monitoring the request progress with Observers...

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
%{pear_phpdir}/HTTP/Request2/Adapter/Curl.php
%{pear_phpdir}/HTTP/Request2/Adapter/Mock.php
%{pear_phpdir}/HTTP/Request2/Adapter/Socket.php
%{pear_phpdir}/HTTP/Request2/Observer/Log.php
%{pear_phpdir}/HTTP/Request2/Adapter.php
%{pear_phpdir}/HTTP/Request2/Exception.php
%{pear_phpdir}/HTTP/Request2/MultipartBody.php
%{pear_phpdir}/HTTP/Request2/Response.php
%{pear_phpdir}/HTTP/Request2.php

%{pear_testdir}/HTTP_Request2


%changelog
* Sun Feb 28 2010 David Hrbáč <david@hrbac.cz> - 0.5.1-1
- initial release
