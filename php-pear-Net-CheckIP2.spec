%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Net_CheckIP2

Name:           php-pear-Net-CheckIP2
Version:        1.0.0
Release:        0.1.RC3%{?dist}
Summary:        A package to determine if an IP (v4) is valid

Group:          Development/Libraries
License:        MIT License
URL:            http://pear.php.net/package/Net_CheckIP2
Source0:        http://pear.php.net/get/%{pear_name}-%{version}RC3.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}


%description
Net_CheckIP2 allows you to validate an IPv4 address.

Additionally, using isReserved(), you may check if an IP is from a
reserved/private
IP space (according to RFC 1918). Using getClass(), you may retrieve the
IP's class
network (A, B, C currently supported).

Net_CheckIP2 is a PHP5 port of the Net_CheckIP package and is almost a
drop-in replacement.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}RC3/%{name}.xml
cd %{pear_name}-%{version}RC3


%build
cd %{pear_name}-%{version}RC3
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}RC3
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
%doc %{pear_name}-%{version}RC3/docdir/%{pear_name}/*


%{pear_xmldir}/%{name}.xml
# Expand this as needed to avoid owning dirs owned by our dependencies
# and to avoid unowned dirs
%{pear_phpdir}/Net/CheckIP2.php

%{pear_testdir}/Net_CheckIP2


%changelog
* Thu Jan 13 2011 David Hrbáč <david@hrbac.cz> - 1.0.0-0.1.RC3
- initial build

