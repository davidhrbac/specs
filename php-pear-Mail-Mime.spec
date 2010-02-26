%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

Name:		php-pear-Mail-Mime
Version:	1.6.0
Release:	1%{?dist}
Summary:	Classes to create and decode mime messages

Group:		Development/Libraries
License:	BSD
URL:		http://pear.php.net/package/Mail_Mime
Source0:	http://pear.php.net/get/Mail_Mime-%{version}.tgz
Source1:	xml2changelog

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch
BuildRequires:	php-pear(PEAR)
Requires:	php-pear(PEAR)
Requires(post):	%{__pear}
Requires(postun): %{__pear}
Provides:	php-pear(Mail_Mime) = %{version}

%description
A Package to enable easy creation of complex multipart emails. If you look for
a simple API for creating such emails, then Mail_Mime class will probably
suffice. Else you can use Mail_mimePart, which gives you better control about
MIME creation


%prep
%setup -q -c 
# package.xml is v2
%{_bindir}/php -n %{SOURCE1} package.xml >CHANGELOG
mv package.xml Mail_Mime-%{version}/%{name}.xml


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot} docdir

cd Mail_Mime-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Move documentation
mkdir -p docdir
mv %{buildroot}%{pear_docdir}/Mail_Mime ../docdir

sed -i -e 's:@prefix@:%{_prefix}:' ../docdir/scripts/phail.php

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_phpdir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%check
# Sanity check
lst=$(find %{buildroot}%{pear_xmldir} -exec grep -q %{buildroot} {} \; -print)
[ ! -z "$lst" ] && echo "Reference to BUILDROOT in $lst" && exit 1;

# For documentation purpose only
# After install, as root :
# pear run-tests -p Mail_Mime
# Should return (1.6.0)
# 28 PASSED TESTS
# 1 SKIPPED TESTS


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only %{pear_xmldir}/%{name}.xml >/dev/null ||:


%postun
# if refcount = 0 then package has been removed (not upgraded)
if [ "$1" -eq "0" ]; then
	%{__pear} uninstall --nodeps --ignore-errors --register-only Mail_Mime >/dev/null ||:
fi


%files
%defattr(-,root,root,-)
%doc CHANGELOG docdir/*
%{pear_xmldir}/%{name}.xml
%{pear_testdir}/Mail_Mime
%{pear_datadir}/Mail_Mime
%{pear_phpdir}/Mail


%changelog
* Sat Jan 30 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.6.0-1
- update to new upstream version (Version 1.6.0 - API 1.4.0)
- generate CHANGELOG from package.xml

* Wed Dec 30 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.5.3-1
- update to new upstream version
- remove circular dependency on Mail_mimeDecode
- rename Mail_Mime.xml to php-pear-Mail-Mime.xml
- fix License (BSD, not PHP, since 1.4.0)
- fix missing URL

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.2-4
- fix license tag

* Thu Apr  3 2008 Brandon Holbrook <fedora at theholbrooks.org> 1.5.2-3
- Add Requirement for Mail_mimeDecode

* Wed May 16 2007 Brandon Holbrook <fedora at theholbrooks.org> 1.5.2-2
- Add Requirement for pear-1.6.0

* Wed May 16 2007 Brandon Holbrook <fedora at theholbrooks.org> 1.5.2-1
- Upgraded to 1.5.2

* Wed May 16 2007 Brandon Holbrook <fedora at theholbrooks.org> 1.4.0-1
- Upgraded to 1.4.0

* Wed Sep  6 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.3.1-8
- Remove quotes from 'install' in %%post section (rpmlint has been fixed)
- More specific BR: php-pear EVR

* Tue Sep  5 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.3.1-7
- New PEAR packaging standards

* Wed Jun 28 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.3.1-6
- Replaced version dependency for BuildRequires: php-pear :)

* Wed Jun 28 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.3.1-5
- Added Requires: php
- Removed version dependencies for php-pear(PEAR)
- Fixed incorrect URL line

* Tue Jun 27 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.3.1-4
- Added comment about 'install' in %%post

* Tue Jun 27 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.3.1-3
- Added php-pear version dependencies for (post) and (postun)
- Updated defattr
- Renamed from php-pear-Mail_Mime to php-pear-Mail-Mime
- Took ownership of /usr/share/pear/Mail/

* Mon Jun 26 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.3.1-2
- inserted newlines into description

* Mon Jun 26 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.3.1-1
- initial RPM borrowed HEAVILY from php-pear-Mail
