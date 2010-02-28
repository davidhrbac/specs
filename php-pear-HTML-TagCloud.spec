%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name HTML_TagCloud

Name:           php-pear-HTML-TagCloud
Version:        0.2.4
Release:        1%{?dist}
Summary:        Generate a "Tag Cloud" in HTML and visualize tags by their frequency. Additionally visualizes each tag's age.

Group:          Development/Libraries
License:        PHP License
URL:            http://pear.php.net/package/HTML_TagCloud
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}


%description
This package can be used to generate tag clouds. The output is HTML and
CSS.

A Tag Cloud is a visual representation of so-called "tags" or keywords,
that do
have a different font size depending on how often they occur on the
page/blog. A
less used synonym for a Tag Cloud that came up before Web 2.0 is the term
"weightet list". Popular examples of Tag Clouds and their use can be found
in
action at pages like Flickr, Del.icio.us and Technorati. A nice overview
on what
a Tag Cloud can actually do can be found at WikiPedia:
http://wikipedia.org/wiki/Tag_cloud

This package does not only visualize frequency, but also timeline
information.
The newer the tag is, the deeper its color will be; older tags will have a
lighter color.

The main goal of "HTML_TagCloud" is to provide an easy to implement and
configureable Tag Cloud solution that is suitable for any PHP-based
webapp.

Features:
 - set up each tag's name, URL, frequency, age
 - customizable colors
 - customizable font-sizes

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
%{pear_phpdir}/HTML/TagCloud.php

%{pear_testdir}/HTML_TagCloud

%changelog
* Sun Feb 28 2010 David Hrbáč <david@hrbac.cz> - 0.2.4-1
- initial release 
