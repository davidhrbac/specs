Name:           rpmlint
Version:        0.99
Release:        1%{?dist}
Summary:        Tool for checking common errors in RPM packages

Group:          Development/Tools
License:        GPLv2
URL:            http://rpmlint.zarb.org/
Source0:        http://rpmlint.zarb.org/download/%{name}-%{version}.tar.bz2
Source1:        %{name}.config
Source2:        %{name}-CHANGES.package.old
Source3:        %{name}-etc.config
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python >= 2.4
BuildRequires:  rpm-python >= 4.4
BuildRequires:  sed >= 3.95
Requires:       rpm-python >= 4.4
Requires:       python >= 2.4
# python-magic and python-enchant are actually optional dependencies, but
# they bring quite desirable features.
#Requires:       python-magic
#Requires:       python-enchant
Requires:       cpio
Requires:       binutils
Requires:       desktop-file-utils
Requires:       gzip
Requires:       bzip2
Requires:       xz

%description
rpmlint is a tool for checking common errors in RPM packages.  Binary
and source packages as well as spec files can be checked.


%prep
%setup -q
sed -i -e /MenuCheck/d Config.py
install -pm 644 %{SOURCE2} CHANGES.package.old
install -pm 644 %{SOURCE3} config


%build
make COMPILE_PYC=1


%install
rm -rf $RPM_BUILD_ROOT
touch rpmlint.pyc rpmlint.pyo # just for the %%exclude to work everywhere
make install DESTDIR=$RPM_BUILD_ROOT ETCDIR=%{_sysconfdir} MANDIR=%{_mandir} \
  LIBDIR=%{_datadir}/rpmlint BINDIR=%{_bindir}
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/rpmlint/config


#%check
#make check


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,0755)
%doc AUTHORS COPYING ChangeLog CHANGES.package.old README
%config(noreplace) %{_sysconfdir}/rpmlint/
%{_sysconfdir}/bash_completion.d/
%{_bindir}/rpmdiff
%{_bindir}/rpmlint
%{_datadir}/rpmlint/
%exclude %{_datadir}/rpmlint/rpmlint.py[co]
%{_mandir}/man1/rpmlint.1*


%changelog
* Fri Aug 27 2010 David Hrbáč <david@hrbac.cz> - 0.99-1
- new upstream version

* Sun Jun 20 2010 David Hrbáč <david@hrbac.cz> - 0.97-1
- new upstream version

* Tue Apr 27 2010 David Hrbáč <david@hrbac.cz> - 0.96-2
- fixed dependencies

* Fri Apr 23 2010 David Hrbáč <david@hrbac.cz> - 0.96-1
- new upstream version

* Mon Nov  2 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.92-1
- Update to 0.92; fixes #528535, and #531102 (partially).
- Python byte compile patch applied/superseded upstream.
- Add <lua> to list of valid scriptlet shells.
- Sync Fedora license list with Wiki revision 1.53.

* Mon Sep 14 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.91-1
- Update to 0.91; fixes #513811, #515185, #516492, #519694, and #521630.
- Add dependencies on gzip, bzip2, and xz.
- Sync Fedora license list with Wiki revision 1.49.
- Move pre-2008 %%changelog entries to CHANGES.package.old.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.90-1
- 0.90; fixes #508683.

* Sun Jun 21 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.89-1
- Update to 0.89; fixes #461610, #496735, #496737 (partially), #498107,
  #491188, and #506957.
- Sync Fedora license list with Wiki revision 1.44.
- Parse list of standard users and groups from the setup package's uidgid file.

* Thu Mar 19 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.87-1
- 0.87; fixes #480664, #483196, #483199, #486748, #488146, #488930, #489118.
- Sync Fedora license list with Wiki revision 1.38.
- Configs patch included upstream.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.85-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Ville Skyttä <ville.skytta@iki.fi>
- Sync Fedora license list with Wiki revision 1.34.
- Filter out filename-too-long-for-joliet and symlink-should-be-* warnings in
  default config.

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.85-3
- Rebuild for Python 2.6

* Thu Oct 30 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.85-2
- Apply upstream patch to load all *config from /etc/rpmlint.

* Thu Oct 23 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.85-1
- 0.85, fixes #355861, #450011, #455371, #456843, #461421, #461423, #461434.
- Mute some explicit-lib-dependency false positives (#458290).
- Sync Fedora license list with Wiki revision 1.19.
- Dist regex patch applied/superseded upstream.

* Fri Sep 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.84-3
- Sync Fedora license list with Wiki revision 1.09

* Sat Jul 26 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.84-2
- 0.84, fixes #355861, #456304.
- Sync Fedora license list with Wiki revision "16:08, 18 July 2008".
- Rediff patches.

* Tue May 27 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.83-1
- 0.83, fixes #237204, #428096, #430206, #433783, #434694, #444441.
- Fedora licensing patch applied upstream.
- Move pre-2007 changelog entries to CHANGES.package.old.
- Sync Fedora license list with Revision 0.88.

* Tue May 20 2008 Todd Zullinger <tmz@pobox.com> 
- Sync Fedora license list with Revision 0.83 (Wiki rev 131).

* Mon Mar  3 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.82-3
- Sync Fedora license list with Revision 0.69 (Wiki rev 110) (#434690).
