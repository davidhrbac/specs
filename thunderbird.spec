%define nspr_version 4.8
%define nss_version 3.12.3.99
%define cairo_version 1.6.0
%define freetype_version 2.1.9
%define sqlite_version 3.6.14
%define build_langpacks 1
%define moz_objdir objdir-tb

# The tarball is pretty inconsistent with directory structure.
# Sometimes there is a top level directory.  That goes here.
#
# IMPORTANT: If there is no top level directory, this should be 
# set to the cwd, ie: '.'
#%define tarballdir .
%define tarballdir comm-1.9.1

%define official_branding 1
%define include_debuginfo 0

%define version_internal  3.0
%define mozappdir         %{_libdir}/%{name}-%{version_internal}

Summary:        Mozilla Thunderbird mail/newsgroup client
Name:           thunderbird
Version:        3.0.3
Release:        1%{?dist}
URL:            http://www.mozilla.org/projects/thunderbird/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
%if %{official_branding}
%define tarball thunderbird-%{version}.source.tar.bz2
%else
%define tarball thunderbird-3.0b2-source.tar.bz2
%endif
Source0:        http://releases.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/source/%{tarball}
%if %{build_langpacks}
Source1:        thunderbird-langpacks-%{version}-20100301.tar.bz2
%endif
Source10:       thunderbird-mozconfig
Source11:       thunderbird-mozconfig-branded
Source12:       thunderbird-redhat-default-prefs.js
Source13:       thunderbird-mozconfig-debuginfo
Source20:       thunderbird.desktop
Source21:       thunderbird.sh.in
Source30:       thunderbird-open-browser.sh
Source100:      find-external-requires

Patch0:         thunderbird-version.patch
Patch1:         mozilla-jemalloc.patch
Patch2:         thunderbird-shared-error.patch
Patch3:         thunderbird-debuginfo-fix-include.patch
Patch4:         thunderbird-clipboard-crash.patch
Patch99:         thunderbird-3.0.1-g_strcmp0.patch

%if %{official_branding}
# Required by Mozilla Corporation


%else
# Not yet approved by Mozillla Corporation


%endif


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildRequires:  nspr-devel >= %{nspr_version}
#BuildRequires:  nss-devel >= %{nss_version}
#BuildRequires:  cairo-devel >= %{cairo_version}
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  libIDL-devel
BuildRequires:  gtk2-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  libgnome-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= %{freetype_version}
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
#BuildRequires:  hunspell-devel
#BuildRequires:  sqlite-devel >= %{sqlite_version}
BuildRequires:  startup-notification-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  autoconf213
BuildRequires:  desktop-file-utils

Requires:       mozilla-filesystem
#Requires:       nspr >= %{nspr_version}
#Requires:       nss >= %{nss_version}
#Requires:       sqlite >= %{sqlite_version}

AutoProv: 0
%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE100}

%description
Mozilla Thunderbird is a standalone mail and newsgroup client.

#%package devel
#Summary: Development files for Thunderbird
#Group: Development/Libraries
#Provides: thunderbird-devel = %{version}
#
#Requires: thunderbird = %{version}-%{release}
#Requires: nspr-devel >= %{nspr_version}
#Requires: nss-devel >= %{nss_version}
#Requires: cairo-devel >= %{cairo_version}
#Requires: libjpeg-devel
#Requires: bzip2-devel
#Requires: zlib-devel
#Requires: libIDL-devel
#Requires: gtk2-devel
#Requires: gnome-vfs2-devel
#Requires: libgnome-devel
#Requires: libgnomeui-devel
#Requires: krb5-devel
#Requires: pango-devel
#Requires: freetype-devel >= %{freetype_version}
#Requires: libXt-devel
#Requires: libXrender-devel
#Requires: hunspell-devel
#Requires: sqlite-devel
#Requires: startup-notification-devel
#Requires: alsa-lib-devel
#Requires: libnotify-devel

#%description devel
#Thunderbird development files.
#
#===============================================================================

%prep
%setup -q -c
cd %{tarballdir}

sed -e 's/__RPM_VERSION_INTERNAL__/%{version_internal}/' %{P:%%PATCH0} \
    > version.patch
%{__patch} -p1 -b --suffix .version --fuzz=0 < version.patch

%patch1 -p0 -b .jemalloc
%patch2 -p1 -b .shared-error

%if %{include_debuginfo}
%patch3 -p1 -b .fix-include
%endif

%patch4 -p1 -b .clipboard-crash

%if %{official_branding}
# Required by Mozilla Corporation


%else
# Not yet approved by Mozillla Corporation


%endif


%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig
%if %{official_branding}
%{__cat} %{SOURCE11} >> .mozconfig
%endif
%if %{include_debuginfo}
%{__cat} %{SOURCE13} >> .mozconfig
%endif

sed -i 's/ac_add_options --with-system-nss/#ac_add_options --with-system-nss/' .mozconfig
sed -i 's/ac_add_options --with-system-nspr/#ac_add_options --with-system-nspr/' .mozconfig
sed -i 's/ac_add_options --enable-system-hunspell/#ac_add_options --enable-system-hunspell/' .mozconfig
sed -i 's/ac_add_options --enable-system-sqlite/#ac_add_options --enable-system-sqlite/' .mozconfig
sed -i 's/ac_add_options --enable-system-cairo/#ac_add_options --enable-system-cairo/' .mozconfig

%patch99 -p2 
#./configure --disable-system-hunspell --disable-system-sqlite --disable-system-cairo

#===============================================================================

%build
cd %{tarballdir}

INTERNAL_GECKO=%{version_internal}
MOZ_APP_DIR=%{mozappdir}

# Build with -Os as it helps the browser; also, don't override mozilla's warning
# level; they use -Wall but disable a few warnings that show up _everywhere_
MOZ_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | %{__sed} -e 's/-O2/-Os/' -e 's/-Wall//')

export RPM_OPT_FLAGS=$MOZ_OPT_FLAGS
export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

%define moz_make_flags -j1
%ifarch ppc ppc64 s390 s390x
%define moz_make_flags -j1
%else
%define moz_make_flags %{?_smp_mflags}
%endif

export LDFLAGS="-Wl,-rpath,%{mozappdir}"
export MAKE="gmake %{moz_make_flags}"
make -f client.mk build

# create debuginfo for crash-stats.mozilla.com
%if %{include_debuginfo}
cd %{moz_objdir}
make buildsymbols
%endif

#===============================================================================

%install
%{__rm} -rf $RPM_BUILD_ROOT
cd %{tarballdir}

INTERNAL_GECKO=%{version_internal}

INTERNAL_APP_NAME=%{name}-${INTERNAL_GECKO}
MOZ_APP_DIR=%{_libdir}/${INTERNAL_APP_NAME}

cd %{moz_objdir}
DESTDIR=$RPM_BUILD_ROOT make install

# install icons
cd -
%{__cp} other-licenses/branding/%{name}/mailicon16.png \
        $RPM_BUILD_ROOT/%{mozappdir}/icons/
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps
%{__cp} other-licenses/branding/%{name}/mailicon16.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/thunderbird.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps
%{__cp} other-licenses/branding/%{name}/mailicon22.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/thunderbird.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/24x24/apps
%{__cp} other-licenses/branding/%{name}/mailicon24.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/24x24/apps/thunderbird.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
%{__cp} other-licenses/branding/%{name}/mailicon32.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/thunderbird.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
%{__cp} other-licenses/branding/%{name}/mailicon48.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/thunderbird.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps
%{__cp} other-licenses/branding/%{name}/mailicon256.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps/thunderbird.png


desktop-file-install --vendor mozilla \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category Network \
  --add-category Email \
  %{SOURCE20}


# set up the thunderbird start script
rm -f $RPM_BUILD_ROOT/%{_bindir}/thunderbird
%{__cat} %{SOURCE21} | %{__sed} -e 's,TBIRD_VERSION,%{version_internal},g' > \
  $RPM_BUILD_ROOT%{_bindir}/thunderbird
%{__chmod} 755 $RPM_BUILD_ROOT/%{_bindir}/thunderbird

install -Dm755 %{SOURCE30} $RPM_BUILD_ROOT/%{mozappdir}/open-browser.sh
%{__sed} -i -e 's|LIBDIR|%{_libdir}|g' $RPM_BUILD_ROOT/%{mozappdir}/open-browser.sh

# set up our default preferences
%{__cat} %{SOURCE12} | %{__sed} -e 's,THUNDERBIRD_RPM_VR,%{version}-%{release},g' \
                                -e 's,COMMAND,%{mozappdir}/open-browser.sh,g' > \
        $RPM_BUILD_ROOT/rh-default-prefs
%{__install} -D $RPM_BUILD_ROOT/rh-default-prefs $RPM_BUILD_ROOT/%{mozappdir}/greprefs/all-redhat.js
%{__install} -D $RPM_BUILD_ROOT/rh-default-prefs $RPM_BUILD_ROOT/%{mozappdir}/defaults/pref/all-redhat.js
%{__rm} $RPM_BUILD_ROOT/rh-default-prefs

%{__rm} -f $RPM_BUILD_ROOT%{_bindir}/thunderbird-config

# own mozilla plugin dir (#135050)
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins

# Install langpacks
%{__rm} -f %{name}.lang # Delete for --short-circuit option
touch %{name}.lang
%if %{build_langpacks}
%{__mkdir_p} $RPM_BUILD_ROOT%{mozappdir}/langpacks
%{__tar} xjf %{SOURCE1}
for langpack in `ls thunderbird-langpacks/*.xpi`; do
  language=`basename $langpack .xpi`
  extensiondir=$RPM_BUILD_ROOT%{mozappdir}/extensions/langpack-$language@thunderbird.mozilla.org
  %{__mkdir_p} $extensiondir
  unzip $langpack -d $extensiondir
  find $extensiondir -type f | xargs chmod 644

  tmpdir=`mktemp -d %{name}.XXXXXXXX`
  langtmp=$tmpdir/%{name}/langpack-$language
  %{__mkdir_p} $langtmp
  jarfile=$extensiondir/chrome/$language.jar
  unzip $jarfile -d $langtmp

  find $langtmp -type f | xargs chmod 644
  %{__rm} -rf $jarfile
  cd $langtmp
  zip -r -D $jarfile locale
  %{__rm} -rf locale
  cd -
  %{__rm} -rf $tmpdir

  language=`echo $language | sed -e 's/-/_/g'`
  extensiondir=`echo $extensiondir | sed -e "s,^$RPM_BUILD_ROOT,,"`
  echo "%%lang($language) $extensiondir" >> %{name}.lang
done
%{__rm} -rf thunderbird-langpacks
%endif # build_langpacks

# Copy over the LICENSE
cd mozilla
install -c -m 644 LICENSE $RPM_BUILD_ROOT%{mozappdir}
cd -

# Use the system hunspell dictionaries
%{__rm} -rf $RPM_BUILD_ROOT/%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{mozappdir}/dictionaries

# ghost files
%{__mkdir_p} $RPM_BUILD_ROOT%{mozappdir}/components
touch $RPM_BUILD_ROOT%{mozappdir}/components/compreg.dat
touch $RPM_BUILD_ROOT%{mozappdir}/components/xpti.dat

# Devel package - sdk
#%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/idl/thunderbird-%{version_internal}
#%{__cp} %{moz_objdir}/mozilla/dist/sdk/idl/* $RPM_BUILD_ROOT%{_datadir}/idl/thunderbird-%{version_internal}

#%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/include/thunderbird-%{version_internal}
#%{__cp} %{moz_objdir}/mozilla/dist/sdk/include/* $RPM_BUILD_ROOT%{_datadir}/include/thunderbird-%{version_internal}

#%{__cp} %{moz_objdir}/mozilla/dist/sdk/bin/* $RPM_BUILD_ROOT%{mozappdir}/


# Add debuginfo for crash-stats.mozilla.com 
%if %{include_debuginfo}
cp mozilla/dist/thunderbird-%{version}.en-US.linux-%{_target_cpu}-crashreporter-symbols.zip $RPM_BUILD_ROOT/%{_libdir}/debug%{mozappdir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/debug%{mozappdir}
cp %{moz_objdir}/mozilla/dist/thunderbird-%{version}.en-US.linux-i686.crashreporter-symbols.zip $RPM_BUILD_ROOT%{_libdir}/debug%{mozappdir}
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files -f %{tarballdir}/%{name}.lang
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/thunderbird
%attr(644,root,root) %{_datadir}/applications/mozilla-thunderbird.desktop
%dir %{mozappdir}
%doc %{mozappdir}/LICENSE
%{mozappdir}/chrome
%dir %{mozappdir}/components
%ghost %{mozappdir}/components/compreg.dat
%ghost %{mozappdir}/components/xpti.dat
%{mozappdir}/components/*.so
%{mozappdir}/components/*.xpt
%attr(644,root,root) %{mozappdir}/components/*.js
%{mozappdir}/defaults
%{mozappdir}/dictionaries
%dir %{mozappdir}/extensions
%{mozappdir}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}
%dir %{mozappdir}/langpacks
%{mozappdir}/greprefs
%{mozappdir}/icons
%{mozappdir}/isp
%{mozappdir}/mozilla-xremote-client
%{mozappdir}/open-browser.sh
%{mozappdir}/res
%{mozappdir}/run-mozilla.sh
%{mozappdir}/thunderbird-bin
%{mozappdir}/thunderbird
%{mozappdir}/updater
%{mozappdir}/*.so
%dir %{mozappdir}/modules
%{mozappdir}/modules/*.jsm
%{mozappdir}/modules/*.js
%dir %{mozappdir}/modules/gloda
%{mozappdir}/modules/gloda/*.js
%dir %{mozappdir}/modules/activity
%{mozappdir}/modules/activity/*.js
%{mozappdir}/README.txt
%{mozappdir}/platform.ini
%{mozappdir}/updater.ini
%{mozappdir}/application.ini
%exclude %{mozappdir}/dependentlibs.list
%exclude %{mozappdir}/removed-files
%{mozappdir}/update.locale
%{_datadir}/icons/hicolor/16x16/apps/thunderbird.png
%{_datadir}/icons/hicolor/22x22/apps/thunderbird.png
%{_datadir}/icons/hicolor/24x24/apps/thunderbird.png
%{_datadir}/icons/hicolor/256x256/apps/thunderbird.png
%{_datadir}/icons/hicolor/32x32/apps/thunderbird.png
%{_datadir}/icons/hicolor/48x48/apps/thunderbird.png
%if %{include_debuginfo}
%{mozappdir}/crashreporter
%{mozappdir}/crashreporter.ini
%{mozappdir}/Throbber-small.gif
%endif
%{_libdir}/%{name}*%{version_internal}/*

# TODO: devel package
#%files devel 
#%defattr(-,root,root,-) 
#%{_datadir}/idl/thunderbird-%{version_internal}
#%{_datadir}/include/thunderbird-%{version_internal}
#%{mozappdir}/xpidl
#%{mozappdir}/xpt_dump
#%{mozappdir}/xpt_link

#===============================================================================

%changelog
* Tue Mar 02 2010 David Hrbáč <david@hrbac.cz> - 3.0.3-1
- new upstream release

* Fri Feb 26 2010 David Hrbáč <david@hrbac.cz> - 3.0.2-1
- new upstream release

* Wed Feb 10 2010 David Hrbáč <david@hrbac.cz> - 3.0.1-1
- CentOS rebuild

* Wed Jan 20 2010 Martin Stransky <stransky@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Mon Jan 18 2010 Martin Stransky <stransky@redhat.com> - 3.0-5
- Added fix for #480603 - thunderbird takes 
  unacceptably long time to start

* Wed Dec  9 2009 Jan Horak <jhorak@redhat.com> - 3.0-4
- Update to 3.0

* Thu Dec  3 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.13.rc2
- Update to RC2

* Wed Nov 25 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.12.rc1
- Sync with Mozilla latest RC1 build

* Thu Nov 19 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.11.rc1
- Update to RC1

* Thu Sep 17 2009 Christopher Aillon <caillon@redhat.com> - 3.0-3.9.b4
- Update to 3.0 b4

* Thu Aug  6 2009 Martin Stransky <stransky@redhat.com> - 3.0-3.8.beta3
- Added fix for #437596
- Removed unused patches

* Thu Aug  6 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.7.beta3
- Removed unused build requirements

* Mon Aug  3 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.6.beta3
- Build with system hunspell

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-3.5.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 24 2009 Jan Horak <jhorak@redhat.com> - 3.0-2.5.beta3
- Use system hunspell

* Tue Jul 21 2009 Jan Horak <jhorak@redhat.com> - 3.0-2.4.beta3
- Update to 3.0 beta3

* Mon Mar 30 2009 Jan Horak <jhorak@redhat.com> - 3.0-2.2.beta2
- Fixed open-browser.sh to use xdg-open instead of gnome-open

* Mon Mar 23 2009 Christopher Aillon <caillon@redhat.com> - 3.0-2.1.beta2
- Disable the default app nag dialog

* Tue Mar 17 2009 Jan Horak <jhorak@redhat.com> - 3.0-2.beta2
- Fixed clicked link does not open in browser (#489120)
- Fixed missing help in thunderbird (#488885)

* Mon Mar  2 2009 Jan Horak <jhorak@redhat.com> - 3.0-1.beta2
- Update to 3.0 beta2
- Added Patch2 to build correctly when building with --enable-shared option 

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 07 2009 Christopher Aillon <caillon@redhat.com> - 2.0.0.18-2
- Disable the crash dialog

* Wed Nov 19 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.18-1
- Update to 2.0.0.18

* Thu Oct  9 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.17-1
- Update to 2.0.0.17

* Wed Jul 23 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.16-1
- Update to 2.0.0.16

* Thu May  1 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.14-1
- Update to 2.0.0.14
- Use the system dictionaries

* Fri Apr 18 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-6
- Icon belongs in _datadir/pixmaps

* Fri Apr 18 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-5
- rebuilt

* Mon Apr  7 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-4
- Add %%lang attributes to langpacks

* Sat Mar 15 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-3
- Avoid conflict between gecko debuginfos

* Mon Mar 03 2008 Martin Stransky <stransky@redhat.com> 2.0.0.12-2
- Updated starting script (#426331)

* Tue Feb 26 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-1
- Update to 2.0.0.12
- Fix up icon location and some scriptlets

* Sun Dec  9 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.9-2
- Fix some rpmlint warnings
- Drop some old patches and obsoletes

* Thu Nov 15 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.9-1
- Update to 2.0.0.9

* Wed Sep 26 2007 Martin Stransky <stransky@redhat.com> 2.0.0.6-6
- Fixed #242657 - firefox -g doesn't work

* Tue Sep 25 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.6-5
- Removed hardcoded MAX_PATH, PATH_MAX and MAXPATHLEN macros

* Tue Sep 11 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.6-4
- Fix crashes when using GTK+ themes containing a gtkrc which specify 
  GtkOptionMenu::indicator_size and GtkOptionMenu::indicator_spacing

* Mon Sep 10 2007 Martin Stransky <stransky@redhat.com> 2.0.0.6-3
- added fix for #246248 - firefox crashes when searching for word "do"

* Mon Aug 13 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.6-2
- Update the license tag

* Wed Aug  8 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.6-1
- Update to 2.0.0.6
- Own the application directory (#244901)

* Tue Jul 31 2007 Martin Stransky <stransky@redhat.com> 2.0.0.0-3
- added pango ligature fix

* Thu Apr 19 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-1
- Update to 2.0.0.0 Final

* Fri Apr 13 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.5.rc1
- Fix the desktop file
- Clean up the files list
- Remove the default client stuff from the pref window

* Thu Apr 12 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.4.rc1
- Rebuild into Fedora

* Wed Apr 11 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.3.rc1
- Update langpacks

* Thu Apr  5 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.2.rc1
- Build option tweaks
- Bring the install section to parity with Firefox's

* Thu Apr  5 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.1.rc1
- Update to 2.0.0.0 RC1

* Sun Mar 25 2007 Christopher Aillon <caillon@redhat.com> 1.5.0.11-1
- Update to 1.5.0.11

* Fri Mar 2 2007 Martin Stransky <stransky@redhat.com> 1.5.0.10-1
- Update to 1.5.0.10

* Mon Feb 12 2007 Martin Stransky <stransky@redhat.com> 1.5.0.9-8
- added fix for #227406: garbage characters on some websites
  (when pango is disabled)
  
* Tue Jan 30 2007 Christopher Aillon <caillon@redhat.com> 1.5.0.9-7
- Updated cursor position patch from tagoh to fix issue with "jumping"
  cursor when in a textfield with tabs.

* Tue Jan 30 2007 Christopher Aillon <caillon@redhat.com> 1.5.0.9-6
- Fix the DND implementation to not grab, so it works with new GTK+.

* Thu Dec 21 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.5.0.9-5
- Added firefox-1.5-pango-underline.patch

* Wed Dec 20 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.5.0.9-4
- Added firefox-1.5-pango-justified-range.patch

* Tue Dec 19 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.5.0.9-3
- Added firefox-1.5-pango-cursor-position-more.patch

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> 1.5.0.9-2
- Add a Requires: launchmail  (#219884)

* Tue Dec 19 2006 Christopher Aillon <caillon@redhat.com> 1.5.0.9-1
- Update to 1.5.0.9
- Take firefox's pango fixes
- Don't offer to import...nothing.

* Tue Nov  7 2006 Christopher Aillon <caillon@redhat.com> 1.5.0.8-1
- Update to 1.5.0.8
- Allow choosing of download directory
- Take the user to the correct directory from the Download Manager.
- Patch to add support for printing via pango from Behdad.

* Sun Oct  8 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.7-4
- Default to use of system colors

* Wed Oct  4 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.7-3
- Bring the invisible character to parity with GTK+

* Wed Sep 27 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.7-2
- Fix crash when changing gtk key theme
- Prevent UI freezes while changing GNOME theme
- Remove verbiage about pango; no longer required by upstream.

* Wed Sep 13 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.7-1
- Update to 1.5.0.7

* Thu Sep  7 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.5-8
- Shuffle order of the install phase around

* Thu Sep  7 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.5-7
- Let there be art for Alt+Tab again
- s/tbdir/mozappdir/g

* Wed Sep  6 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.5-6
- Fix for cursor position in editor widgets by tagoh and behdad (#198759)

* Tue Sep  5 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.5-5
- Update nopangoxft.patch
- Fix rendering of MathML thanks to Behdad Esfahbod.
- Update start page text to reflect the MathML fixes.
- Enable pango by default on all locales
- Build using -rpath
- Re-enable GCC visibility

* Thu Aug  3 2006 Kai Engert <kengert@redhat.com> - 1.5.0.5-4
- Fix a build failure in mailnews mime code.

* Tue Aug  1 2006 Matthias Clasen <mclasen@redhat.com> - 1.5.0.5-3
- Rebuild

* Thu Jul 27 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.5-2
- Update to 1.5.0.5

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.5.0.4-2.1
- rebuild

* Mon Jun 12 2006 Kai Engert <kengert@redhat.com> - 1.5.0.4-2
- Update to 1.5.0.4
- Fix desktop-file-utils requires

* Wed Apr 19 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.2-2
- Update to 1.5.0.2

* Thu Mar 16 2006 Christopher Aillon <caillon@redhat.com> - 1.5-7
- Bring the other arches back

* Mon Mar 13 2006 Christopher Aillon <caillon@redhat.com> - 1.5.6
- Temporarily disable other arches that we don't ship FC5 with, for time

* Mon Mar 13 2006 Christopher Aillon <caillon@redhat.com> - 1.5-5
- Add a notice to the mail start page denoting this is a pango enabled build.

* Fri Feb 10 2006 Christopher Aillon <caillon@redhat.com> - 1.5-3
- Add dumpstack.patch
- Improve the langpack install stuff

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.5-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 27 2006 Christopher Aillon <caillon@redhat.com> - 1.5-2
- Add some langpacks back in
- Stop providing MozillaThunderbird

* Thu Jan 12 2006 Christopher Aillon <caillon@redhat.com> - 1.5-1
- Official 1.5 release is out

* Wed Jan 11 2006 Christopher Aillon <caillon@redhat.com> - 1.5-0.5.6.rc1
- Fix crash when deleting highlighted text while composing mail within
  plaintext editor with spellcheck enabled.

* Tue Jan  3 2006 Christopher Aillon <caillon@redhat.com> - 1.5-0.5.5.rc1
- Looks like we can build on ppc64 again.

* Fri Dec 16 2005 Christopher Aillon <caillon@redhat.com> - 1.5-0.5.4.rc1
- Rebuild

* Fri Dec 16 2005 Christopher Aillon <caillon@redhat.com> - 1.5-0.5.3.rc1
- Once again, disable ppc64 because of a new issue.
  See https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=175944

- Use the system NSS libraries
- Build on ppc64

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 28 2005 Christopher Aillon <caillon@redhat.com> - 1.5-0.5.1.rc1
- Fix issue with popup dialogs and other actions causing lockups

* Sat Nov  5 2005 Christopher Aillon <caillon@redhat.com> 1.5-0.5.0.rc1
- Update to 1.5 rc1

* Sat Oct  8 2005 Christopher Aillon <caillon@redhat.com> 1.5-0.5.0.beta2
- Update to 1.5 beta2

* Wed Sep 28 2005 Christopher Aillon <caillon@redhat.com> 1.5-0.5.0.beta1
- Update to 1.5 beta1
- Bring the install phase of the spec file up to speed

* Sun Aug 14 2005 Christopher Aillon <caillon@redhat.com> 1.0.6-4
- Rebuild

* Sat Aug  6 2005 Christopher Aillon <caillon@redhat.com> 1.0.6-3
- Add patch to make file chooser dialog modal

* Fri Jul 22 2005 Christopher Aillon <caillon@redhat.com> 1.0.6-2
- Update to 1.0.6

* Mon Jul 18 2005 Christopher Aillon <caillon@redhat.com> 1.0.6-0.1.fc5
- 1.0.6 Release Candidate

* Fri Jul 15 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-8
- Use system NSPR
- Fix crash on 64bit platforms (#160330)

* Thu Jun 23 2005 Kristian Høgsberg <krh@redhat.com>  1.0.2-7
- Add firefox-1.0-pango-cairo.patch to get rid of the last few Xft
  references, fixing the "no fonts" problem.

* Fri May 13 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-6
- Change the Exec line in the desktop file to `thunderbird`

* Fri May 13 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-5
- Update pango patche, MOZ_DISABLE_PANGO now works as advertised.

* Mon May  9 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-4
- Add temporary workaround to not create files in the user's $HOME (#149664)

* Wed May  4 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-3
- Don't have downloads "disappear" when downloading to desktop (#139015)
- Fix for some more cursor issues in textareas (149991, 150002, 152089)
- Add upstream patch to fix bidi justification of pango
- Add patch to fix launching of helper applications
- Add patch to properly link against libgfxshared_s.a
- Fix multilib conflicts

* Wed Apr 27 2005 Warren Togami <wtogami@redhat.com>
- correct confusing PANGO vars in startup script

* Wed Mar 23 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-1
- Thunderbird 1.0.2

* Tue Mar  8 2005 Christopher Aillon <caillon@redhat.com> 1.0-5
- Add patch to compile against new fortified glibc macros

* Sat Mar  5 2005 Christopher Aillon <caillon@redhat.com> 1.0-4
- Rebuild against GCC 4.0
- Add execshield patches
- Minor specfile cleanup

* Mon Dec 20 2004 Christopher Aillon <caillon@redhat.com> 1.0-3
- Rebuild

* Thu Dec 16 2004 Christopher Aillon <caillon@redhat.com> 1.0-2
- Add RPM version to useragent

* Thu Dec 16 2004 Christopher Blizzard <blizzard@redhat.com>
- Port over pango patches from firefox

* Wed Dec  8 2004 Christopher Aillon <caillon@redhat.com> 1.0-1
- Thunderbird 1.0

* Mon Dec  6 2004 Christopher Aillon <caillon@redhat.com> 1.0-0.rc1.1
- Fix advanced prefs

* Fri Dec  3 2004 Christopher Aillon <caillon@redhat.com>
- Make this run on s390(x) now for real

* Wed Dec  1 2004 Christopher Aillon <caillon@redhat.com> 1.0-0.rc1.0
- Update to 1.0 rc1

* Fri Nov 19 2004 Christopher Aillon <caillon@redhat.com>
- Add patches to build and run on s390(x)

* Thu Nov 11 2004 Christopher Aillon <caillon@redhat.com> 0.9.0-2
- Rebuild to fix file chooser

* Fri Nov  5 2004 Christopher Aillon <caillon@redhat.com> 0.9.0-1
- Update to 0.9

* Fri Oct 22 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-10
- Prevent inlining of stack direction detection (#135255)

* Tue Oct 19 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-9
- More file chooser fixes (same as in firefox)
- Fix for upstream 28327.

* Mon Oct 18 2004 Christopher Blizzard <blizzard@redhat.com> 0.8.0-8
- Update the pango patch

* Mon Oct 18 2004 Christopher Blizzard <blizzard@redhat.com> 0.8.0-8
- Pull over patches from firefox build:
  - disable default application dialog
  - don't include software update since it doesn't work
  - make external app support work

* Thu Oct 14 2004 Christopher Blizzard <blizzard@redhat.com> 0.8.0-7
- Use pango for rendering

* Tue Oct 12 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-6
- Fix for 64 bit crash at startup (b.m.o #256603)

* Sat Oct  9 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-5
- Add patches to fix xremote (#135036)

* Fri Oct  8 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-4
- Add patch to fix button focus issues (#133507)
- Add patch for fix IMAP race issues (bmo #246439)

* Fri Oct  1 2004 Bill Nottingham <notting@redhat.com> 0.8.0-3
- filter out library Provides: and internal Requires:

* Tue Sep 28 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-2
- Backport the GTK+ File Chooser.
- Add fix for JS math on x86_64 systems
- Add pkgconfig patch

* Thu Sep 16 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-1
- Update to 0.8.0
- Remove enigmail
- Update BuildRequires
- Remove gcc34 and extension manager patches -- they are upstreamed.
- Fix for gnome-vfs2 error at component registration

* Fri Sep 03 2004 Christopher Aillon <caillon@redhat.com> 0.7.3-5
- Build with --disable-xprint

* Wed Sep 01 2004 David Hill <djh[at]ii.net> 0.7.3-4
- remove all Xvfb-related hacks

* Wed Sep 01 2004 Warren Togami <wtogami@redhat.com> 
- actually apply psfonts
- add mozilla gnome-uriloader patch to prevent build failure

* Tue Aug 31 2004 Warren Togami <wtogami@redhat.com> 0.7.3-3
- rawhide import
- apply NetBSD's freetype 2.1.8 patch
- apply psfonts patch
- remove BR on /usr/bin/ex, breaks beehive

* Tue Aug 31 2004 David Hill <djh[at]ii.net> 0.7.3-0.fdr.2
- oops, fix %%install

* Thu Aug 26 2004 David Hill <djh[at]ii.net> 0.7.3-0.fdr.1
- update to Thunderbird 0.7.3 and Enigmail 0.85.0
- remove XUL.mfasl on startup, add Debian enigmail patches
- add Xvfb hack for -install-global-extension

* Wed Jul 14 2004 David Hill <djh[at]ii.net> 0.7.2-0.fdr.0
- update to 0.7.2, just because it's there
- update gcc-3.4 patch (Kaj Niemi)
- add EM registration patch and remove instdir hack

* Sun Jul 04 2004 David Hill <djh[at]ii.net> 0.7.1-0.fdr.1
- re-add Enigmime 1.0.7, omit Enigmail until the Mozilla EM problems are fixed

* Wed Jun 30 2004 David Hill <djh[at]ii.net> 0.7.1-0.fdr.0
- update to 0.7.1
- remove Enigmail

* Mon Jun 28 2004 David Hill <djh[at]ii.net> 0.7-0.fdr.1
- re-enable Enigmail 0.84.1
- add gcc-3.4 patch (Kaj Niemi)
- use official branding (with permission)

* Fri Jun 18 2004 David Hill <djh[at]ii.net> 0.7-0.fdr.0
- update to 0.7
- temporarily disable Enigmail 0.84.1, make ftp links work (#1634)
- specify libdir, change BR for apt (V. Skyttä, #1617)

* Tue May 18 2004 Warren Togami <wtogami@redhat.com> 0.6-0.fdr.5
- temporary workaround for enigmail skin "modern" bug

* Mon May 10 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.4
- update to Enigmail 0.84.0 
- update launch script

* Mon May 10 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.3
- installation directory now versioned
- allow root to run the program (for installing extensions)
- remove unnecessary %%pre and %%post
- remove separators, update mozconfig and launch script (M. Schwendt, #1460)

* Wed May 05 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.2
- include Enigmail, re-add release notes
- delete %{_libdir}/thunderbird in %%pre

* Mon May 03 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.1
- update to Thunderbird 0.6

* Fri Apr 30 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.0.rc1
- update to Thunderbird 0.6 RC1
- add new icon, remove release notes

* Thu Apr 15 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.0.20040415
- update to latest CVS, update mozconfig and %%build accordingly
- update to Enigmail 0.83.6
- remove x-remote and x86_64 patches
- build with -Os

* Thu Apr 15 2004 David Hill <djh[at]ii.net> 0.5-0.fdr.12
- update x-remote patch
- more startup script fixes

* Tue Apr 06 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.11
- startup script fixes, and a minor cleanup

* Sun Apr 04 2004 Warren Togami <wtogami@redhat.com> 0:0.5-0.fdr.10
- Minor cleanups

* Sun Apr 04 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.8
- minor improvements to open-browser.sh and startup script
- update to latest version of Blizzard's x-remote patch

* Thu Mar 25 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.7
- update open-browser.sh, startup script, and BuildRequires

* Sun Mar 14 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.6
- update open-browser script, modify BuildRequires (Warren)
- add Blizzard's x-remote patch
- initial attempt at x-remote-enabled startup script

* Sun Mar 07 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.5
- refuse to run with excessive privileges

* Fri Feb 27 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.4
- add Mozilla x86_64 patch (Oliver Sontag)
- Enigmail source filenames now include the version
- modify BuildRoot

* Thu Feb 26 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.3
- use the updated official tarball

* Wed Feb 18 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.2
- fix %%prep script

* Mon Feb 16 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.1
- update Enigmail to 0.83.3
- use official source tarball (after removing the CRLFs)
- package renamed to thunderbird

* Mon Feb 09 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.0
- update to 0.5
- check for lockfile before launching

* Fri Feb 06 2004 David Hill <djh[at]ii.net>
- update to latest cvs
- update to Enigmail 0.83.2

* Thu Jan 29 2004 David Hill <djh[at]ii.net> 0:0.4-0.fdr.5
- update to Enigmail 0.83.1
- removed Mozilla/Firebird script patching

* Sat Jan 03 2004 David Hill <djh[at]ii.net> 0:0.4-0.fdr.4
- add startup notification to .desktop file

* Thu Dec 25 2003 Warren Togami <warren@togami.com> 0:0.4-0.fdr.3
- open-browser.sh release 3
- patch broken /usr/bin/mozilla script during install
- dir ownership
- XXX: Source fails build on x86_64... fix later

* Tue Dec 23 2003 David Hill <djh[at]ii.net> 0:0.4-0.fdr.2
- update to Enigmail 0.82.5
- add Warren's open-browser.sh (#1113)

* Tue Dec 09 2003 David Hill <djh[at]ii.net> 0:0.4-0.fdr.1
- use Thunderbird's mozilla-xremote-client to launch browser

* Sun Dec 07 2003 David Hill <djh[at]ii.net> 0:0.4-0.fdr.0
- update to 0.4
- make hyperlinks work (with recent versions of Firebird/Mozilla)

* Thu Dec 04 2003 David Hill <djh[at]ii.net>
- update to 0.4rc2

* Wed Dec 03 2003 David Hill <djh[at]ii.net>
- update to 0.4rc1 and Enigmail 0.82.4

* Thu Nov 27 2003 David Hill <djh[at]ii.net>
- update to latest CVS and Enigmail 0.82.3

* Sun Nov 16 2003 David Hill <djh[at]ii.net>
- update to latest CVS (0.4a)
- update Enigmail to 0.82.2
- alter mozconfig for new build requirements
- add missing BuildReq (#987)

* Thu Oct 16 2003 David Hill <djh[at]ii.net> 0:0.3-0.fdr.0
- update to 0.3

* Sun Oct 12 2003 David Hill <djh[at]ii.net> 0:0.3rc3-0.fdr.0
- update to 0.3rc3
- update Enigmail to 0.81.7

* Thu Oct 02 2003 David Hill <djh[at]ii.net> 0:0.3rc2-0.fdr.0
- update to 0.3rc2

* Wed Sep 17 2003 David Hill <djh[at]ii.net> 0:0.2-0.fdr.2
- simplify startup script

* Wed Sep 10 2003 David Hill <djh[at]ii.net> 0:0.2-0.fdr.1
- add GPG support (Enigmail 0.81.6)
- specfile fixes (#679)

* Thu Sep 04 2003 David Hill <djh[at]ii.net> 0:0.2-0.fdr.0
- update to 0.2

* Mon Sep 01 2003 David Hill <djh[at]ii.net>
- initial RPM
  (based on the fedora MozillaFirebird-0.6.1 specfile)

