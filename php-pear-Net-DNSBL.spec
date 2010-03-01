%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Net_DNSBL

Name:           php-pear-Net-DNSBL
Version:        1.3.3
Release:        2%{?dist}
Summary:        Checks if a given Host or URL is listed on an DNS-based Blackhole List (DNSBL, Real-time Blackhole List or RBL) or Spam URI Realtime Blocklist (SURBL)

Group:          Development/Libraries
License:        PHP License
URL:            http://pear.php.net/package/Net_DNSBL
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       php-pear(Cache_Lite) >= 1.4.1, php-pear(Net_DNS) >= 1.0.0, php-pear(Net_CheckIP) >= 1.1, php-pear(HTTP_Request) >= 1.2.3, php-pear(PEAR) >= 1.4.0b1

%description
Checks if a given Host or URL is listed on an DNS-based Blackhole List
(DNSBL, Real-time Blackhole List or RBL) or Spam URI Realtime Blocklist
(SURBL)

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
%{pear_phpdir}/Net/DNSBL/SURBL.php
%{pear_phpdir}/Net/DNSBL.php

%{pear_testdir}/Net_DNSBL


%changelog
* Mon Mar 01 2010 David Hrbáč <david@hrbac.cz> - 1.3.3-1
- added changelog :o)
