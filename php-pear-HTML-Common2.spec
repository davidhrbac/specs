%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name HTML_Common2

Name:           php-pear-HTML-Common2
Version:        2.0.0RC1
Release:        1%{?dist}
Summary:        Abstract base class for HTML classes (PHP5 port of HTML_Common package)

Group:          Development/Libraries
License:        BSD License
URL:            http://pear.php.net/package/HTML_Common2
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}


%description
HTML_Common2 package provides methods for HTML code display and attributes
handling.
* Provides methods to set, remove, merge HTML attributes.
* Handles global document options (charset, linebreak and indentation
characters).
* Provides methods to handle indentation and HTML comments (useful in
subclasses).

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
%{pear_phpdir}/HTML/Common2.php

%{pear_testdir}/HTML_Common2


%changelog
* Mon Oct 18 2010 David Hrbáč <david@hrbac.cz> - 2.0.0RC1-1
- initial release

