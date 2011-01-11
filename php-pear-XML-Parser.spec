%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name XML_Parser

Name:           php-pear-XML-Parser
Version:        1.3.4
Release:        1%{?dist}
Summary:        XML parsing class based on PHP's bundled expat

Group:          Development/Libraries
License:        BSD License
URL:            http://pear.php.net/package/XML_Parser
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       php-pear(PEAR) >= 1.4.0b1

%description
This is an XML parser based on PHPs built-in xml extension.
It supports two basic modes of operation: "func" and "event".  In "func"
mode, it will look for a function named after each element (xmltag_ELEMENT
for start tags and xmltag_ELEMENT_ for end tags), and in "event" mode it
uses a set of generic callbacks.

Since version 1.2.0 there's a new XML_Parser_Simple class that makes
parsing of most XML documents easier, by automatically providing a stack
for the elements.
Furthermore its now possible to split the parser from the handler object,
so you do not have to extend XML_Parser anymore in order to parse a
document with it.

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
%{pear_phpdir}/XML/Parser/Simple.php
%{pear_phpdir}/XML/Parser.php

%{pear_testdir}/XML_Parser


%changelog
* Tue Jan 11 2011 David Hrbáč <david@hrbac.cz> - 1.3.4-1
- initial build
