%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name XML_RSS

Name:           php-pear-XML-RSS
Version:        1.0.1
Release:        1%{?dist}
Summary:        RSS parser

Group:          Development/Libraries
License:        PHP License
URL:            http://pear.php.net/package/XML_RSS
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       php-pear(XML_Parser) >= 1.0.1, php-pear(PEAR) >= 1.4.0
Conflicts:      php-pear(XML_Parser) = 1.0.1

%description
Parser for Resource Description Framework (RDF)
  Site Summary (RSS) documents.

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
%{pear_phpdir}/XML/RSS.php

%{pear_testdir}/XML_RSS


%changelog
* Tue Jan 11 2011 David Hrbáč <david@hrbac.cz> - 1.0.1-1
- initial build
