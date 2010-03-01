%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%define pear_name Mail

Name:           php-pear-Mail
Version:        1.2.0
Release:        1%{?dist}
Summary:        Class that provides multiple interfaces for sending emails
Summary(fr):    Une Classe fournissant des interfaces pour envoyer des emails

Group:          Development/Libraries
License:        PHP
URL:            http://pear.php.net/package/Mail
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
Source2:        xml2changelog

## See http://www.debian.org/security/2009/dsa-1938
#Patch0:         %{name}-security.patch 

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires:       php-pear(PEAR) >= 1.4.9 php-pear(Net_SMTP) >= 1.4.1
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}


%description
PEAR's Mail package defines an interface for implementing mailers under the
PEAR hierarchy.  It also provides supporting functions useful to multiple
mailer backends.  Currently supported backends include: PHP's native
mail() function, sendmail, and SMTP.  This package also provides a RFC822
email address list validation utility class.
 
%description -l fr
L'extension Mail définie une interfance permettant de construire des
gestionnaires de courrier dans l'arborescence PEAR. Elle fournie aussi
des fonctions utiles à l'utilisation de ces gestionnaires. Actuellement 
elle supporte la fonction PHP standard mail(), sendmail et SMTP.
Cette extension contient aussi une classe permettant de vérifer la 
conformité à la RFC822 des liste d'adresses de courrier.


%prep
%setup -q -c

#%patch0 -p0

# Package is still an old V1 one
#%{__pear} convert package.xml package2.xml 
%{_bindir}/php -n %{SOURCE2} package.xml >CHANGELOG
mv package.xml %{pear_name}-%{version}/%{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf $RPM_BUILD_ROOT
cd %{pear_name}-%{version}
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
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc CHANGELOG
%{pear_phpdir}/Mail.php
%{pear_phpdir}/Mail
%{pear_testdir}/Mail
%{pear_xmldir}/%{name}.xml


%changelog
* Mon Mar 01 2010 David Hrbáč <david@hrbac.cz> - 1.2.0-1
- new upstream release
- change dependecy php-pear(Net_SMTP) >= 1.4.1

* Sun Feb 28 2010 David Hrbáč <david@hrbac.cz> - 1.1.14-5
- initial rebuild

* Fri Nov 27 2009 Remi Collet <Fedora@FamilleCollet.com> 1.1.14-5
- Fix CVE-2009-4023 (#540842)
- rename Mail.xml to php-pear-Mail.xml

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 24 2007 Remi Collet <Fedora@FamilleCollet.com> 1.1.14-2
- Fix License

* Thu Oct 12 2006 Remi Collet <Fedora@FamilleCollet.com> 1.1.14-1
- update to 1.1.14

* Sat Sep 16 2006 Remi Collet <Fedora@FamilleCollet.com> 1.1.13-1
- regenerate SPEC with pear make-rpm-spec
- remove PEAR from sumnary
- update to 1.1.13
- add generated CHANGELOG %%doc

* Fri Sep 08 2006 Remi Collet <Fedora@FamilleCollet.com> 1.1.10-8
- last template.spec

* Mon Sep 04 2006 Remi Collet <Fedora@FamilleCollet.com> 1.1.10-7
- new and simpler %%prep and %%install

* Mon Aug 28 2006 Remi Collet <Fedora@FamilleCollet.com> 1.1.10-6
- FE6 rebuild

* Sat Jul 22 2006 Remi Collet <Fedora@FamilleCollet.com> 1.1.10-5
- remove "rm pearrc"
- secure scriplet with || :
- install Licence in prep
- use new macros from /etc/rpm/macros.pear

* Mon May 15 2006 Remi Collet <Fedora@FamilleCollet.com> 1.1.10-4
- Require pear >= 1:1.4.9
- Requires(hint): php-pear(Net_SMTP) >= 1.1.0 (only comment actually)
- bundle the v3.01 PHP LICENSE file
- use --packagingroot (instead of -R)
- check from install to check (as in php-pear)

* Sun May 14 2006 Remi Collet <Fedora@FamilleCollet.com> 1.1.10-3
- License : PHP -> PHP License

* Sat May 06 2006 Remi Collet <Fedora@FamilleCollet.com> 1.1.10-2
- new spec for extras
- use %%{_datadir}/pear/.pkgxml for XML (Bug #190252)

* Thu Apr 27 2006 Remi Collet <Fedora@FamilleCollet.com> 1.1.10-1
- spec for extras

* Wed Apr 26 2006 Remi Collet <rpms@FamilleCollet.com> 1.1.10-1.fc{3,4,5}.remi
- update to 1.1.10

* Thu Apr 06 2006 Remi Collet <rpms@FamilleCollet.com> 1.1.9-2.fc{3,4,5}.remi
- change /var/lib/pear to %%{_libdir}/php/pear for XML (as in extras for FC5)
- spec cleanning

* Sat Jan  7 2006 Remi Collet <remi.collet@univ-reims.fr> 1.1.9-1.fc{3,4}.remi
- initial RPM
