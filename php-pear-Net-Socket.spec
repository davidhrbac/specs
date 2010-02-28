%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%define pear_name Net_Socket

Name:           php-pear-Net-Socket
Version:        1.0.9
Release:        3%{?dist}
Summary:        Network Socket Interface
Summary(fr):    Gestion des "sockets" réseaux

Group:          Development/Libraries
License:        PHP
URL:            http://pear.php.net/package/Net_Socket
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
Source2:        xml2changelog
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}


%description
  Net_Socket is a class interface to TCP sockets.  It provides blocking
  and non-blocking operation, with different reading and writing modes
  (byte-wise, block-wise, line-wise and special formats like network
  byte-order ip addresses).

%description -l fr
  Net_Socket est une classe d'interface sur les "sockets" TCP.
  Elle gère les opérations bloquantes et non bloquantes, avec plusieurs
  modes de lecture et d'écriture (par octet, par bloc, par ligne, et
  des formats spéciaux, comme les adresses IP dans l'ordre des
  octets du réseau).


%prep
%setup -q -c
%{_bindir}/php -n %{SOURCE2} package.xml >CHANGELOG

mv package.xml %{pear_name}-%{version}/%{pear_name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

cd Net_Socket-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{pear_name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_phpdir}/.??*

%{__mkdir_p} %{buildroot}%{pear_xmldir}
%{__install} -pm 644 %{pear_name}.xml %{buildroot}%{pear_xmldir}


%check
# Sanity check
lst=$(find %{buildroot}%{pear_phpdir} -exec grep -q %{buildroot} {} \; -print)
[ ! -z "$lst" ] && echo "Reference to BUILDROOT in $lst" && exit 1;


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{pear_name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc CHANGELOG
%{pear_phpdir}/Net
%{pear_xmldir}/Net_Socket.xml


%changelog
* Sun Feb 28 2010 David Hrbáč <david@hrbac.cz> - 1.0.9-3
- initial rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jul 12 2008 Remi Collet <Fedora@FamilleCollet.com> 1.0.9-1
- update to 1.0.9

* Fri Jun 13 2008 Jon Stanley <jonstanley@gmail.com> - 1.0.8-2
- Rebuild

* Tue May 08 2007 Remi Collet <Fedora@FamilleCollet.com> 1.0.8-1
- update to 1.0.8

* Sat Mar 31 2007 Remi Collet <Fedora@FamilleCollet.com> 1.0.7-1
- remove PEAR from sumnary
- update to 1.0.7
- spec cleanup
- add generated CHANGELOG

* Fri Sep 08 2006 Remi Collet <Fedora@FamilleCollet.com> 1.0.6-5
- last template.spec

* Sun Sep 03 2006 Remi Collet <Fedora@FamilleCollet.com> 1.0.6-4
- new and simpler %%prep and %%install

* Sat Sep 02 2006 Remi Collet <Fedora@FamilleCollet.com> 1.0.6-3
- install Licence in prep
- use new macros from /etc/rpm/macros.pear
- own /usr/share/pear/Net
- require php >= 4.3.0 (info from PHP_CompatInfo)

* Sat May 20 2006 Remi Collet <Fedora@FamilleCollet.com> 1.0.6-2
- Require pear >= 1.4.9
- bundle the v3.01 PHP LICENSE file
- use --packagingroot (instead of -R)
- check from install to check (as in php-pear)

* Sat May 06 2006 Remi Collet <Fedora@FamilleCollet.com> 1.0.6-1
- spec for extras
- use %%{_datadir}/pear/.pkgxml for XML (Bug #190252)

* Thu Apr 06 2006 Remi Collet <rpms@FamilleCollet.com> 1.0.6-2.fc{3,4,5}.remi
- change /var/lib/pear to %%{_libdir}/php/pear for XML (as in extras for FC5)
- spec cleanning

* Sat Jan  7 2006 Remi Collet <remi.collet@univ-reims.fr> 1.0.6-1.fc{3,4}.remi
- initial RPM
