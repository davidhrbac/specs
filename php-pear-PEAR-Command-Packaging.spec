%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name PEAR_Command_Packaging

Name:           php-pear-PEAR-Command-Packaging
Version:        0.2.0
Release:        4%{?dist}
Summary:        Create RPM spec files from PEAR modules

Group:          Development/System
License:        PHP
URL:            http://pear.php.net/package/PEAR_Command_Packaging
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
Source1:        php-pear-PEAR-Command-Packaging-fedora-template-specfile
Patch0:         php-pear-PEAR-Command-Packaging-0.2.0-fedora-conventions.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires:       php-pear(PEAR) >= 1.4.3
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}

%description
This command is an improved implementation of the standard PEAR "makerpm" 
command, and contains several enhancements that make it far more flexible. 
Similar functions for other external packaging mechanisms may be added at
a later date.

%prep
%setup -q -c

# Patches for Fedora conventions
%patch0 -p0 -b .fedora

mv package.xml %{pear_name}-%{version}/%{name}.xml
cd %{pear_name}-%{version}


%build
# Empty build section, nothing required

%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{pear_phpdir}/data/%{pear_name}/template.spec

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Remove doc; will be installed later
rm -f $RPM_BUILD_ROOT%{pear_docdir}/%{pear_name}/LICENSE

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
%doc %{pear_name}-%{version}/LICENSE
%{pear_xmldir}/%{name}.xml
%{pear_datadir}/%{pear_name}
%{pear_phpdir}/PEAR/Command/Packaging.*


%changelog
* Sun Feb 28 2010 David Hrbáč <david@hrbac.cz> - 0.2.0-4
- initial rebuild

* Sat Feb 20 2010 Remi Collet <Fedora@FamilleCollet.com> 0.2.0-4
- fix missing pear in dep name (#536756)
- replace %%define by %%global in template
- requires php-common (rather than php) when needed (not used yet)
- apply patch in %%prep

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 19 2009 Remi Collet <Fedora@FamilleCollet.com> 0.2.0-2
- change %%{pear-name}.xml to %%{name}.xml

* Sat Jun 27 2009 Tim Jackson <rpm@timj.co.uk> 0.2.0-1
- Update to 0.2.0

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.1.2-6
- fix license tag

* Sat Sep 23 2006 Tim Jackson <rpm@timj.co.uk> 0.1.2-5
- Remove "PEAR:" from Summary in spec and template.spec

* Sun Sep 10 2006 Tim Jackson <rpm@timj.co.uk> 0.1.2-4
- Shorten summary
- Remove unnecessary dep on php
- Bundle LICENSE file
- Rename template specfile source to keep rpmlint happy

* Sat Sep 09 2006 Tim Jackson <rpm@timj.co.uk> 0.1.2-3
- Update to conform with latest conventions in bug #198706
- Update in-built spec (for generation of other package specs) to (nearly)
  conform with latest spec conventions

* Mon Jul 03 2006 Tim Jackson <rpm@timj.co.uk> 0.1.2-2
- BR php-pear 1.4.9; 1.4.8 is broken
- Update to conform to proposed Fedora PHP packaging standards

* Wed Jun 28 2006 Tim Jackson <rpm@timj.co.uk> 0.1.2-1
- Update to 0.1.2
- Update fedora-conventions patch to patch Packaging.xml
- Update fedora-conventions patch for peardir/tests -> peardir/test
- Backport upstream patch to make Fedora conventions work properly

* Fri Jun 9 2006 Tim Jackson <rpm@timj.co.uk> 0.1.1-2
- Add Epoch to php-pear BR

* Thu May 18 2006 Tim Jackson <rpm@timj.co.uk> 0.1.1-1
- Update to 0.1.1
- XML description now in datadir/pear/.pkgxml (see bug #190252)
- Stop buildroot path ending up in output files

* Wed Mar 15 2006 Tim Jackson <rpm@timj.co.uk> 0.1.0-2
- Own data/PEAR_Command_Packaging dir
- Remove empty doc line
- Remove empty build section
- Replace cp with install

* Tue Mar 14 2006 Tim Jackson <rpm@timj.co.uk> 0.1.0-1
- Initial RPM build
