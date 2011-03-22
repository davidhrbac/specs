%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Cache_Lite

Name:           php-pear-Cache-Lite
Version:        1.7.9
Release:        1%{?dist}
Summary:        Fast and Safe little cache system

Group:          Development/Libraries
License:        lgpl
URL:            http://pear.php.net/package/Cache_Lite
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       php-pear(PEAR) >= 1.5.4

%description
This package is a little cache system optimized for file containers. It is
fast and safe (because it uses file locking and/or anti-corruption tests).

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
%{pear_phpdir}/Cache/Lite/File.php
%{pear_phpdir}/Cache/Lite/Function.php
%{pear_phpdir}/Cache/Lite/Output.php
%{pear_phpdir}/Cache/Lite.php

%{pear_testdir}/Cache_Lite


%changelog
* Mon Mar 14 2011 David Hrbáč <david@hrbac.cz> - 1.7.9-1
- new upstream release

* Sun Feb 28 2010 David Hrbáč <david@hrbac.cz> - 1.7.8-1
- initial release
