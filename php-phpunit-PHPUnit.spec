%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name PHPUnit
%global channel pear.phpunit.de

Name:           php-phpunit-PHPUnit
Version:        3.5.13
Release:        1%{?dist}
Summary:        Regression testing framework for unit tests

Group:          Development/Libraries
License:        BSD
URL:            http://www.phpunit.de
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz
Source1:	http://github.com/sebastianbergmann/phpunit/raw/3.4/README.markdown
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.8.1
BuildRequires:  php-channel(%{channel})

Requires:       php-xml >= 5.1.4
Requires:       php-pear(PEAR) >= 1.8.1
Requires:       php-channel(%{channel})
Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(pear.symfony-project.com/YAML) >= 1.0.2

# Optionnal dependencies
Requires:       php-pear(Image_GraphViz) >= 1.2.1
Requires:       php-pear(Log)
Requires:       php-json php-pdo php-soap
Requires:       php-pecl(Xdebug) >= 2.0.5

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}
Obsoletes:      php-pear-PHPUnit < %{version}
Provides:       php-pear-PHPUnit = %{version}-%{release}


%description
PHPUnit is a family of PEAR packages that supports the development of
object-oriented PHP applications using the concepts and methods of Agile
Software Development, Extreme Programming, Test-Driven Development and
Design-by-Contract Development by providing an elegant and robust framework
for the creation, execution and analysis of Unit Tests.


%prep
%setup -qc
# package.xml is V2
mv package.xml %{pear_name}-%{version}/%{name}.xml

cp %{SOURCE1} README.markdown

%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT docdir

# Install Package
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Move documentation
mkdir -p docdir
mv $RPM_BUILD_ROOT%{pear_docdir}/* docdir

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
install -d $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
#%{__pear} install --nodeps --soft --force --register-only \
#    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
#    %{__pear} uninstall --nodeps --ignore-errors --register-only \
#        %{channel}/%{pear_name} >/dev/null || :
fi

%triggerpostun -- php-pear-PHPUnit
# re-register extension unregistered during postun of obsoleted php-pear-PHPUnit
#%{__pear} install --nodeps --soft --force --register-only \
#    %{pear_xmldir}/%{name}.xml >/dev/null || :



%files
%defattr(-,root,root,-)
%doc %{pear_name}-%{version}/docdir/%{pear_name}/%{pear_name}/* README.markdown
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/%{pear_name}
%{_bindir}/phpunit
%{_bindir}/dbunit


%changelog
* Thu May 26 2011 David Hrbáč <david@hrbac.cz> - 3.5.13-1
- new upstream release

* Wed May 25 2011 David Hrbáč <david@hrbac.cz> - 3.4.16-1
- new upstream release

* Wed May 25 2011 David Hrbáč <david@hrbac.cz> - 3.4.15-1
- new upstream release

* Wed Jun 23 2010 David Hrbáč <david@hrbac.cz> - 3.4.14-1
- new upstream release

* Sat Feb 20 2010 David Hrbáč <david@hrbac.cz> - 3.4.11-1
- new upstream release

* Sun Jan 24 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.9-1
- Update to 3.4.9

* Sat Jan 16 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.7-1
- Update to 3.4.7
- rename from php-pear-PHPUnit to php-phpunit-PHPUnit
- update dependencies (PEAR 1.8.1, YAML, php-soap)

* Sat Sep 12 2009 Christopher Stone <chris.stone@gmail.com> 3.3.17-1
- Upstream sync

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 02 2009 Remi Collet <Fedora@famillecollet.com> - 3.3.16-1
- Upstream sync
- Fix requires (remove hint) and raise PEAR version to 1.7.1
- rename %%{pear_name}.xml to %%{name}.xml

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov  8 2008 Christopher Stone <chris.stone@gmail.com> 3.3.4-1
- Upstream sync

* Thu Oct 23 2008 Christopher Stone <chris.stone@gmail.com> 3.3.2-1
- Upstream sync
- Remove no longer needed Obsolete/Provides

* Thu Oct 09 2008 Christopher Stone <chris.stone@gmail.com> 3.3.1-1
- Upstream sync

* Thu Oct 09 2008 Christopher Stone <chris.stone@gmail.com> 3.2.21-1
- Upstream sync
- Add php-xml to Requires (bz #464758)

* Thu May 22 2008 Christopher Stone <chris.stone@gmail.com> 3.2.19-1
- Upstream sync

* Thu Feb 21 2008 Christopher Stone <chris.stone@gmail.com> 3.2.15-1
- Upstream sync

* Wed Feb 13 2008 Christopher Stone <chris.stone@gmail.com> 3.2.13-1
- Upstream sync

* Sun Nov 25 2007 Christopher Stone <chris.stone@gmail.com> 3.2.1-1
- Upstream sync

* Sat Sep 08 2007 Christopher Stone <chris.stone@gmail.com> 3.1.8-1
- Upstream sync

* Sun May 06 2007 Christopher Stone <chris.stone@gmail.com> 3.0.6-1
- Upstream sync

* Thu Mar 08 2007 Christopher Stone <chris.stone@gmail.com> 3.0.5-3
- Fix testdir
- Fix Provides version

* Wed Mar 07 2007 Christopher Stone <chris.stone@gmail.com> 3.0.5-2
- Add Obsoletes/Provides for php-pear(PHPUnit2)
- Requires php-pear(PEAR) >= 1.5.0
- Own %%{pear_testdir}/%%{pear_name}
- Remove no longer needed manual channel install
- Simplify %%doc
- Only unregister old phpunit on upgrade

* Mon Feb 26 2007 Christopher Stone <chris.stone@gmail.com> 3.0.5-1
- Upstream sync

* Wed Feb 21 2007 Christohper Stone <chris.stone@gmail.com> 3.0.4-1
- Upstream sync

* Mon Jan 29 2007 Christopher Stone <chris.stone@gmail.com> 3.0.3-1
- Upstream sync

* Sun Jan 14 2007 Christopher Stone <chris.stone@gmail.com> 3.0.2-1
- Upstream sync

* Fri Jan 05 2007 Christopher Stone <chris.stone@gmail.com> 3.0.1-1
- Upstream sync

* Wed Dec 27 2006 Christopher Stone <chris.stone@gmail.com> 3.0.0-1
- Initial Release
