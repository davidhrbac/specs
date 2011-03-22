%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%define pear_name Net_SMTP

Name:           php-pear-Net-SMTP
Version:        1.5.1
Release:        1%{?dist}
Summary:        Provides an implementation of the SMTP protocol
Summary(fr):    Fournit une mise en oeuvre du protocol SMTP

Group:          Development/Libraries
License:        PHP
URL:            http://pear.php.net/package/Net_SMTP
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

Source2:        xml2changelog
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       php-pear(PEAR) >= 1.4.9
Requires:       php-pear(Net_Socket) >= 1.0.7
Requires:       php-pear(Auth_SASL)


%description
Provides an implementation of the SMTP protocol using PEAR's Net_Socket class.

php-pear-Net-SMTP can optionally use package "php-pear-Auth-SASL".

%description -l fr
Fournit une mise en oeuvre du protocol SMTP utilisant la classe Net_Socket.

php-pear-Net-SMTP peut optionellement utiliser
l'extension "php-pear-Auth-SASL".


%prep
%setup -q -c
# Package.xml is V2
%{_bindir}/php -n %{SOURCE2} package.xml >CHANGELOG

mv package.xml %{pear_name}-%{version}/%{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot} docdir

pushd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_phpdir}/.??*

# Install XML package description
%{__mkdir_p} %{buildroot}%{pear_xmldir}
%{__install} -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

popd
# Sort out documentation
%{__mkdir} docdir
mv %{buildroot}%{pear_docdir}/* docdir


%check
# Sanity check
lst=$(find %{buildroot}%{pear_phpdir} -exec grep -q %{buildroot} {} \; -print)
[ ! -z "$lst" ] && echo "Reference to BUILDROOT in $lst" && exit 1;

# For documentation purpose only
# After install, as root :
# cd /usr/share/pear/test/Net_SMTP/tests
# cp config.php.dist config.php
# vi config.php # you should use a working mail account
# pear run-tests -p Net_SMTP
# Should return 
# 3 PASSED TESTS
# 0 SKIPPED TESTS


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc CHANGELOG docdir/%{pear_name}/docs/* docdir/%{pear_name}/examples
%{pear_phpdir}/Net/*
%{pear_testdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml


%changelog
* Mon Mar 14 2011 David Hrbáč <david@hrbac.cz> - 1.5.1-1
- new upstream release

* Mon Feb 07 2011 David Hrbáč <david@hrbac.cz> - 1.5.0-1
- new upstream release

* Mon Mar 08 2010 David Hrbáč <david@hrbac.cz> - 1.4.2-1
- new upstream release

* Sun Feb 28 2010 David Hrbáč <david@hrbac.cz> - 1.4.1-1
- initial rebuild

* Mon Jan 25 2010 Remi Collet <Fedora@FamilleCollet.com> 1.4.1-1
- update to 1.4.1

* Sun Jan 24 2010 Remi Collet <Fedora@FamilleCollet.com> 1.4.0-1
- update to 1.4.0
- add examples to %%doc

* Sun Nov 29 2009 Remi Collet <Fedora@FamilleCollet.com> 1.3.4-1
- update to 1.3.4

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Remi Collet <Fedora@FamilleCollet.com> 1.3.3-1
- update to 1.3.3
- rename Net_SMTP.xml to php-pear-Net-SMTP.xml

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 21 2008 Remi Collet <Fedora@FamilleCollet.com> 1.3.2-1
- update to 1.3.2

* Tue Jun 10 2008 Remi Collet <Fedora@FamilleCollet.com> 1.3.1-1
- update to 1.3.1
- add Comment on howto to run test suite

* Sun Apr 27 2008 Remi Collet <Fedora@FamilleCollet.com> 1.3.0-1
- update to 1.3.0

* Fri Feb 15 2008 Remi Collet <Fedora@FamilleCollet.com> 1.2.11-1
- update to 1.2.11
- fix License

* Sat Mar 31 2007 Remi Collet <Fedora@FamilleCollet.com> 1.2.10-1
- remove PEAR from sumnary
- update to 1.2.10 
- requires Net_Socket >= 1.0.7
- spec cleanup
- add generated CHANGELOG
- don't own /usr/share/pear/Net (already own by Net_Socket)

* Fri Sep 08 2006 Remi Collet <Fedora@FamilleCollet.com> 1.2.8-5
- last template.spec

* Sun Sep 03 2006 Remi Collet <Fedora@FamilleCollet.com> 1.2.8-4
- new and simpler %%prep and %%install

* Sat Sep 02 2006 Remi Collet <Fedora@FamilleCollet.com> 1.2.8-3
- install Licence in prep
- use new macros from /etc/rpm/macros.pear
- own /usr/share/pear/Net
- require php >= 4.0.5

* Sat May 20 2006 Remi Collet <Fedora@FamilleCollet.com> 1.2.8-2
- Require pear >= 1.4.9
- bundle the v3.01 PHP LICENSE file
- use --packagingroot (instead of -R)
- check from install to check (as in php-pear)
- Remove Auth_SASL from Requires (optional)

* Sat May 06 2006 Remi Collet <Fedora@FamilleCollet.com> 1.2.8-1
- spec for extras
- workaround for buggy pear 1.4.6 installer
- use %%{_datadir}/pear/.pkgxml for XML (Bug #190252)

* Thu Apr 06 2006 Remi Collet <rpms@FamilleCollet.com> 1.2.8-3.fc{3,4,5}.remi
- change /var/lib/pear to %%{_libdir}/php/pear for XML (as in extras for FC5)
- spec cleanning

* Sat Mar 04 2006 Remi Collet <RPMS@FamilleCollet.com> 1.2.8-2.fc{3,4}.remi
- add Requires: php-pear(Auth_SASL)

* Sat Feb 25 2006 Remi Collet <RPMS@FamilleCollet.com> 1.2.8-1.fc{3,4}.remi
- update to 1.2.8

* Sat Jan  7 2006 Remi Collet <remi.collet@univ-reims.fr> 1.2.7-1.fc{3,4}.remi
- initial RPM
