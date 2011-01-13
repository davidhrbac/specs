%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Services_ProjectHoneyPot

Name:           php-pear-Services-ProjectHoneyPot
Version:        0.5.3
Release:        1%{?dist}
Summary:        A package to interface the http:bl API of ProjectHoneyPot.org

Group:          Development/Libraries
License:        The BSD License
URL:            http://pear.php.net/package/Services_ProjectHoneyPot
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       php-pear(Net_CheckIP2) >= 1.0.0, php-pear(Net_DNS) >= 1.0.0, php-pear(PEAR) >= 1.4.0b1

%description
This package is used to determine if an IP or hostname are a) a search
engine, b) suspicious, c) the ip of a harvester or/and d) of a comment
spammer.

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
%{pear_phpdir}/Services/ProjectHoneyPot/Response/Exception.php
%{pear_phpdir}/Services/ProjectHoneyPot/Response/Result.php
%{pear_phpdir}/Services/ProjectHoneyPot/Response/ResultSet.php
%{pear_phpdir}/Services/ProjectHoneyPot/Exception.php
%{pear_phpdir}/Services/ProjectHoneyPot/Response.php
%{pear_phpdir}/Services/ProjectHoneyPot.php

%{pear_testdir}/Services_ProjectHoneyPot


%changelog
* Thu Jan 13 2011 David Hrbáč <david@hrbac.cz> - 0.5.3-1
- initial build

