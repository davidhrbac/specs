Name:           rpmlint
Version:        0.90
Release:        1%{?dist}
Summary:        Tool for checking common errors in RPM packages

Group:          Development/Tools
License:        GPLv2
URL:            http://rpmlint.zarb.org/
Source0:        http://rpmlint.zarb.org/download/%{name}-%{version}.tar.bz2
Source1:        %{name}.config
Source2:        %{name}-CHANGES.package.old
Source3:        %{name}-etc.config
# Fedora specific, not upstreamable
Patch0:         %{name}-0.85-compile.patch
# From upstream svn
Patch1:         %{name}-0.85-configs.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python >= 2.2
BuildRequires:  rpm-python
BuildRequires:  sed >= 3.95
Requires:       rpm-python
Requires:       python >= 2.2
Requires:       cpio
Requires:       binutils
Requires:       desktop-file-utils
Requires:       file

%description
rpmlint is a tool for checking common errors in RPM packages.  Binary
and source packages can be checked.


%prep
%setup -q
#%patch0 -p1
#%patch1 -p0
sed -i -e /MenuCheck/d Config.py
install -pm 644 %{SOURCE2} CHANGES.package.old
install -pm 644 %{SOURCE3} config


%build
make


%install
rm -rf $RPM_BUILD_ROOT
touch rpmlint.pyc rpmlint.pyo # just for the %%exclude to work everywhere
make install DESTDIR=$RPM_BUILD_ROOT ETCDIR=%{_sysconfdir} MANDIR=%{_mandir} \
  LIBDIR=%{_datadir}/rpmlint BINDIR=%{_bindir}
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/rpmlint/config


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
* Wed Jul 15 2009 David Hrbáč <david@hrbac.cz>  - 0.90-1
- new upstream version

* Wed Jul 15 2009 David Hrbáč <david@hrbac.cz>  - 0.85-3.1
- initial rebuild

* Thu Feb 05 2009 Manuel Wolfshant <wolfy at fedoraproject.org> - 0.85-3.1
- Bump release to express relationship with the rawhide version.
  No other changes.

* Sat Jan 24 2009 Manuel Wolfshant <wolfy at fedoraproject.org> - 0.85-1
- Sync with Fedora rawhide version 0.85-3, including:
-- Update to upstream version 0.85
-- Apply upstream patch to load all *config from /etc/rpmlint.
- Sync Fedora license list as Wiki revision 1.34
- Filter out "filename-too-long-for-joliet" and "symlink-should-be-*"
   warnings in default config.

* Sat Oct  18 2008 Manuel Wolfshant <wolfy at fedoraproject.org> - 0.84-3
- Sync Fedora license list with Wiki revision 1.09

* Wed Sep 10 2008 Manuel Wolfshant <wolfy at fedoraproject.org> - 0.84-2.1
- rebuild with proper changelog

* Sat Jul 26 2008 Manuel Wolfshant <wolfy at fedoraproject.org> - 0.84-2
- 0.84, fixes #355861, #456304.
- Sync Fedora license list with Wiki revision "16:08, 18 July 2008".
- Rediff patches.

* Tue May 27 2008 Manuel Wolfshant <wolfy at fedoraproject.org> - 0.83-1
- resync, bump release to match

* Tue May 27 2008 Manuel Wolfshant <wolfy at fedoraproject.org> - 0.83-0.1
- Sync with rawhide:
--Tue May 27 2008  Ville Skyttä
--- bump release to 0.83, fixes #237204, #428096, #430206, #433783, #434694, #444441.
--- Fedora licensing patch applied upstream.
--- Move pre-2007 changelog entries to CHANGES.package.old.
-- Tue May 20 2008 Todd Zullinger
--- Sync Fedora license list with Revision 0.83 (Wiki rev 131).

* Mon Mar  3 2008 Manuel Wolfshant <wolfy at fedoraproject.org> - 0.82-3
- Sync with rawhide:
-- Sync Fedora license list with Revision 0.69 (Wiki rev 110) (#434690).

* Mon Mar  3 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.82-3
- Sync Fedora license list with Revision 0.69 (Wiki rev 110) (#434690).

* Thu Dec  6 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.82-2
- Remove leftover "Affero GPL" from last license list sync (Todd Zullinger).

* Thu Dec  6 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.82-1
* Sun Jan 13 2008 Manuel Wolfshant <wolfy at fedoraproject.org> - 0.82-1
- Sync with current rawhide:
-- 0.82, fixes #362441, #388881, #399871, #409941.
-- Sync Fedora license list with Revision 0.61 (Wiki rev 98).
-- Remove leftover "Affero GPL" from last license list sync (Todd Zullinger).

* Sat Oct 06 2007 Todd Zullinger <tmz@pobox.com>
- Sync Fedora license list with Revision 0.55 (Wiki rev 92).

* Tue Sep 11 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.81-2
- Sync Fedora license list with Wiki rev 90.

* Mon Sep  3 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.81-1
- 0.81, fixes #239611, #240840, #241471, #244835.
- Improve Fedora license check (Todd Zullinger).
- Sync Fedora license list with Wiki rev 87.

* Wed Aug 29 2007 Ville Skyttä <ville.skytta at iki.fi>
- Sync Fedora license list with Wiki rev 84 (Todd Zullinger).

* Thu Aug 16 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.80-3
- Sync Fedora license list with Wiki rev 68.
- Move pre-2006 changelog entries to CHANGES.package.old.

* Tue Jul 31 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.80-2
- new fedora licensing scheme

* Thu May 31 2007 Ville Skyttä <ville.skytta at iki.fi>
- Filter hardcoded-library-path errors for /lib/udev.

* Thu Apr 12 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.80-1
- 0.80, fixes #227389, #228645, #233795.
- Accept "Redistributable, no modification permitted" as a valid license.
- Filter messages about doc file dependencies on /bin/sh.
- Add missing dependency on file.

* Fri Feb  2 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.79-1
- 0.79, fixes #211417, #212491, #214605, #218250, #219068, #220061, #221116,
  #222585, and #226879.
- Accept *.elX disttags in default config.

* Sun Oct 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.78-2
- Accumulated bugfixes since 0.78: #209876, #209889, #210110, 210261.
- Filter messages about gpg-pubkeys for now.

* Sun Sep 24 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.78-1
- 0.78, fixes #198605, #198616, #198705, #198707, #200032, #206383.
- /etc/profile.d/* filtering no longer needed.

* Sat Sep 16 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.77-2
- Filter false positives for /etc/profile.d/* file modes.
- Ship *.pyc and *.pyo as usual.

* Thu Jun 29 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.77-1
- 0.77, fixes #194466, #195962, #196008, #196985.
- Make "disttag" configurable using the DistRegex config file option.
- Sync standard users and groups with the FC setup package.
- Disable MenuCheck by default, it's currently Mandriva specific.
- Use upstream default valid License tag list, fixes #191078.
- Use upstream default valid Group tag list (dynamically retrieved from
  the GROUPS file shipped with rpm).
- Allow /usr/libexec, fixes #195992.

* Tue Apr 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.76-1
- 0.76.

* Mon Mar 27 2006 Ville Skyttä <ville.skytta at iki.fi>
- Don't pass -T to objdump for *.debug files (#185227).
- lib64 library path fixes (#185228).

* Wed Mar 15 2006 Ville Skyttä <ville.skytta at iki.fi>
- Accept zlib License (#185501).

* Tue Feb 28 2006 Ville Skyttä <ville.skytta at iki.fi>
- Accept Ruby License (#183384) and SIL Open Font License (#176405).

* Sat Feb 18 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.75-1
- 0.75 + -devel Epoch version check patch from CVS.

* Tue Jan 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.71-3
- Sync with upstream CVS as of 2006-01-15, includes improved versions of
  most of the earlier patches.
- Add dependency on binutils.
