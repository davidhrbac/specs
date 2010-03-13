%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

%global prerelease RC

Name:           umit
Version:        1.0
Release:        0.2.%{prerelease}%{?dist}
Summary:        Nmap frontend

Group:          Applications/Internet
License:        GPLv2+ and LGPLv2+
URL:            http://umit.sourceforge.net/
Source0:        http://downloads.sourceforge.net/umit/umit-%{version}%{prerelease}.tar.gz
# http://trac.umitproject.org/ticket/378
Source1:        umit_48x48.png
# http://trac.umitproject.org/ticket/378
Source2:        umit.desktop
# Fedora-specific: Fix check-buildroot issues
Patch0:         umit-1.0RC-setup.py.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  python2-devel
BuildRequires:  python-sphinx

Requires:       nmap
Requires:       pygtk2


%description
With Umit, you have all the power provided by Nmap through its regular 
command line interface, and a lot more in a highly usable and portable 
Graphical Interface. Some of its main features include:
    * Easily create powerful Nmap commands and save them as profiles to use 
      whenever you need it
    * Edit your Profiles using the Interface Editor
    * Create Profiles with the assistance of a Wizard
    * Group and order you scan results
    * Filter hosts list by services
    * Filter services list by hosts
    * Compare two scan results in one of our three compare modes: text diff, 
      graphical comparison and HTML diff
    * Search scan results
    * Use Umit interface through the Web


%prep
%setup -q -n %{name}-%{version}%{prerelease}
%patch0 -p1


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install --root %{buildroot}

# Remove useless files
rm %{buildroot}%{_bindir}/uninstall_umit

# Fix permissions
find %{buildroot} -type f -exec chmod 644 {} \;
chmod 755 %{buildroot}%{_bindir}/*

# Remove a interpreter from the site-packages
find %{buildroot}%{python_sitelib} -type f -iname "*py" -exec \
    sed -i 's/#!\/usr\/bin\/env python//' {} \;

# Fix the file end-of-line encoding
sed -i 's/\r//' %{buildroot}%{_docdir}/%{name}/html/_sources/plugins.txt

# Install the icons
install -pm 0644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/%{name}
install -d %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
ln -s ../../../../pixmaps/%{name}/%{name}_48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png

# Install the desktop file
install -d %{buildroot}%{_datadir}/applications
desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    %{SOURCE2}

%find_lang %{name}


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING COPYING_HIGWIDGETS README
%doc %{_docdir}/%{name}
%{_bindir}/%{name}
%{_bindir}/umit_scheduler.py
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/%{name}*
%{_datadir}/icons/%{name}
%{_datadir}/pixmaps/%{name}
%{_datadir}/%{name}
%{python_sitelib}/higwidgets
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-*.egg-info


%changelog
* Sat Mar 13 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 1.0-0.2.RC
- Add the pygtk2 to the Requires
- Fix the license
- Fix the Source0
- Remove the unused macro python_sitearch
- Remove the -doc subpackage
- Replace generally useful macros by regular commands

* Fri Feb 05 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 1.0-0.1.RC
- Initial package build

