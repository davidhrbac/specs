%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Net_DNS

Name:           php-pear-Net-DNS
Version:        1.0.7
Release:        1%{?dist}
Summary:        Resolver library used to communicate with a DNS server

Group:          Development/Libraries
License:        LGPL
URL:            http://pear.php.net/package/Net_DNS
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}


%description
A resolver library used to communicate with a name server to perform DNS
queries, zone transfers, dynamic DNS updates, etc.
Creates an object hierarchy from a DNS server response, which allows you
to view all of the information given by the DNS server. It bypasses the
system resolver library and communicates directly with the server.

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
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/tests

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
%{pear_phpdir}/Net/DNS.php
%{pear_phpdir}/Net/DNS/Header.php
%{pear_phpdir}/Net/DNS/Packet.php
%{pear_phpdir}/Net/DNS/Question.php
%{pear_phpdir}/Net/DNS/RR.php
%{pear_phpdir}/Net/DNS/RR/A.php
%{pear_phpdir}/Net/DNS/RR/AAAA.php
%{pear_phpdir}/Net/DNS/RR/CNAME.php
%{pear_phpdir}/Net/DNS/RR/HINFO.php
%{pear_phpdir}/Net/DNS/RR/LOC.php
%{pear_phpdir}/Net/DNS/RR/MX.php
%{pear_phpdir}/Net/DNS/RR/NAPTR.php
%{pear_phpdir}/Net/DNS/RR/NS.php
%{pear_phpdir}/Net/DNS/RR/PTR.php
%{pear_phpdir}/Net/DNS/RR/RP.php
%{pear_phpdir}/Net/DNS/RR/SOA.php
%{pear_phpdir}/Net/DNS/RR/SPF.php
%{pear_phpdir}/Net/DNS/RR/SRV.php
%{pear_phpdir}/Net/DNS/RR/TSIG.php
%{pear_phpdir}/Net/DNS/RR/TXT.php
%{pear_phpdir}/Net/DNS/Resolver.php
##{pear_phpdir}/Net/generate_package_xml.php
%{pear_testdir}/%{pear_name}


%changelog
* Mon Jan 03 2011 David Hrbáč <david@hrbac.cz> - 1.0.7-1
- new upstream release

* Mon Oct 18 2010 David Hrbáč <david@hrbac.cz> - 1.0.5-1
- new upstream release

* Sun Feb 28 2010 David Hrbáč <david@hrbac.cz> - 1.0.1-1 
- initial release
