# Minimal required versions
%define nspr_version 4.8
%define nss_version 3.12.3.99
%define cairo_version 1.6.0
%define freetype_version 2.1.9
%define sqlite_version 3.6.16
%define tarballdir mozilla-1.9.2

# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)

%define version_internal  1.9.2
%define mozappdir         %{_libdir}/%{name}-%{version_internal}

Summary:        XUL Runtime for Gecko Applications
Name:           xulrunner
Version:        1.9.2.1
Release:        4%{?pretag}%{?dist}
URL:            http://developer.mozilla.org/En/XULRunner
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
# You can get sources at ftp://ftp.mozilla.org/pub/firefox/releases/%{version}%{?pretag}/source
Source0:        %{name}-%{version}%{?pretag}.source.tar.bz2
Source10:       %{name}-mozconfig
Source12:       %{name}-redhat-default-prefs.js
Source21:       %{name}.sh.in
Source23:       %{name}.1

# build patches
Patch0:         xulrunner-version.patch
Patch1:         mozilla-build.patch
Patch3:         mozilla-jemalloc.patch
Patch4:         mozilla-about-firefox-version.patch
Patch5:         mozilla-jemalloc-526152.patch
Patch7:         xulrunner-1.9.2.1-build.patch
Patch8:         mozilla-plugin.patch
Patch9:         mozilla-build-sbrk.patch

# Fedora specific patches
Patch10:        mozilla-192-pkgconfig.patch

# Upstream patches
Patch100:       mozilla-ps-pdf-simplify-operators.patch
Patch101:       mozilla-462919.patch

# ---------------------------------------------------

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
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
BuildRequires:  libnotify-devel
BuildRequires:  autoconf213

Requires:       mozilla-filesystem
#Requires:       nspr >= %{nspr_version}
#Requires:       nss >= %{nss_version}
#Requires:       sqlite >= %{sqlite_build_version}
Provides:       gecko-libs = %{version}

%description
XULRunner provides the XUL Runtime environment for Gecko applications.

%package devel
Summary: Development files for Gecko
Group: Development/Libraries
Obsoletes: mozilla-devel < 1.9
Obsoletes: firefox-devel < 2.1
Obsoletes: xulrunner-devel-unstable
Provides: gecko-devel = %{version}
Provides: gecko-devel-unstable = %{version}

Requires: xulrunner = %{version}-%{release}
#Requires: nspr-devel >= %{nspr_version}
#Requires: nss-devel >= %{nss_version}
#Requires: cairo-devel >= %{cairo_version}
Requires: libjpeg-devel
Requires: zip
Requires: bzip2-devel
Requires: zlib-devel
Requires: libIDL-devel
Requires: gtk2-devel
Requires: gnome-vfs2-devel
Requires: libgnome-devel
Requires: libgnomeui-devel
Requires: krb5-devel
Requires: pango-devel
Requires: freetype-devel >= %{freetype_version}
Requires: libXt-devel
Requires: libXrender-devel
#Requires: hunspell-devel
#Requires: sqlite-devel
Requires: startup-notification-devel
Requires: alsa-lib-devel
Requires: libnotify-devel

%description devel
Gecko development files.

#---------------------------------------------------------------------

%prep
%setup -q -c
cd %{tarballdir}

sed -e 's/__RPM_VERSION_INTERNAL__/%{version_internal}/' %{P:%%PATCH0} \
    > version.patch
%{__patch} -p1 -b --suffix .version --fuzz=0 < version.patch

%patch1  -p1 -b .build
%patch3  -p1 -b .jemalloc
%patch4  -p1 -b .about-firefox-version
%patch5  -p1 -b .jemalloc-526152
%patch7  -p2 -b .del
%patch8  -p1 -b .plugin
%patch9  -p2 -b .sbrk

%patch10 -p1 -b .pk

%patch100 -p1 -b .ps-pdf-simplify-operators
%patch101 -p1 -b .462919


%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig

sed -i 's/ac_add_options --with-system-nss/#ac_add_options --with-system-nss/' .mozconfig
sed -i 's/ac_add_options --with-system-nspr/#ac_add_options --with-system-nspr/' .mozconfig
sed -i 's/ac_add_options --enable-system-hunspell/#ac_add_options --enable-system-hunspell/' .mozconfig
sed -i 's/ac_add_options --enable-system-sqlite/#ac_add_options --enable-system-sqlite/' .mozconfig
sed -i 's/ac_add_options --enable-system-cairo/#ac_add_options --enable-system-cairo/' .mozconfig

./configure --disable-system-hunspell --disable-system-sqlite --disable-system-cairo
sed -i 's/ac_add_options --with-system-nss/#ac_add_options --with-system-nss/' .mozconfig
sed -i 's/ac_add_options --with-system-nspr/#ac_add_options --with-system-nspr/' .mozconfig

#---------------------------------------------------------------------

%build
## Do not proceed with build if the sqlite require would be broken:
## make sure the minimum requirement is non-empty, ...
#sqlite_version=$(expr "%{sqlite_version}" : '\([0-9]*\.\)[0-9]*\.') || exit 1
## ... and that major number of the computed build-time version matches:
#case "%{sqlite_build_version}" in
#  "$sqlite_version"*) ;;
#  *) exit 1 ;;
#esac

cd %{tarballdir}

INTERNAL_GECKO=%{version_internal}
MOZ_APP_DIR=%{_libdir}/%{name}-${INTERNAL_GECKO}

# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
MOZ_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | %{__sed} -e 's/-Wall//')
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
%ifnarch ppc ppc64 s390 s390x
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -gt 1 ] && MOZ_SMP_FLAGS=-j2
%endif

export LDFLAGS="-Wl,-rpath,${MOZ_APP_DIR}"
make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS"

#---------------------------------------------------------------------

%install
cd %{tarballdir}
%{__rm} -rf $RPM_BUILD_ROOT

INTERNAL_GECKO=%{version_internal}

INTERNAL_APP_NAME=%{name}-${INTERNAL_GECKO}
MOZ_APP_DIR=%{_libdir}/${INTERNAL_APP_NAME}

INTERNAL_APP_SDK_NAME=%{name}-sdk-${INTERNAL_GECKO}
MOZ_APP_SDK_DIR=%{_libdir}/${INTERNAL_APP_SDK_NAME}

DESTDIR=$RPM_BUILD_ROOT make install

%{__mkdir_p} $RPM_BUILD_ROOT/${MOZ_APP_DIR} \
             $RPM_BUILD_ROOT%{_datadir}/idl/${INTERNAL_APP_SDK_NAME} \
             $RPM_BUILD_ROOT%{_includedir}/${INTERNAL_APP_SDK_NAME}
%{__install} -p dist/sdk/bin/regxpcom $RPM_BUILD_ROOT/$MOZ_APP_DIR

%{__mkdir_p} $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_datadir}/applications}

# set up our default preferences
%{__cat} %{SOURCE12} | %{__sed} -e 's,RPM_VERREL,%{version}-%{release},g' > rh-default-prefs
%{__install} -p -D -m 644 rh-default-prefs $RPM_BUILD_ROOT/${MOZ_APP_DIR}/defaults/pref/all-redhat.js
%{__rm} rh-default-prefs

# Start script install
%{__rm} -rf $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__cat} %{SOURCE21} | %{__sed} -e 's,XULRUNNER_VERSION,%{version_internal},g' > \
  $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

%{__rm} -f $RPM_BUILD_ROOT${MOZ_APP_DIR}/%{name}-config

cd $RPM_BUILD_ROOT${MOZ_APP_DIR}/chrome
find . -name "*" -type d -maxdepth 1 -exec %{__rm} -rf {} \;
cd -

# Prepare our devel package
%{__mkdir_p} $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_SDK_NAME}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datadir}/idl/${INTERNAL_APP_SDK_NAME}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

%{__cp} -rL dist/include/* \
  $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_SDK_NAME}

# Copy pc files (for compatibility with 1.9.1)
%{__cp} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul.pc \
        $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-unstable.pc
%{__cp} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-embedding.pc \
        $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-embedding-unstable.pc

# Fix multilib devel conflicts...
%ifarch x86_64 ia64 s390x ppc64
%define mozbits 64
%else
%define mozbits 32
%endif

function install_file() {
genheader=$*
mv ${genheader}.h ${genheader}%{mozbits}.h
cat > ${genheader}.h << EOF
/* This file exists to fix multilib conflicts */
#if defined(__x86_64__) || defined(__ia64__) || defined(__s390x__) || defined(__powerpc64__)
#include "${genheader}64.h"
#else
#include "${genheader}32.h"
#endif
EOF
}

pushd $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_SDK_NAME}
install_file "mozilla-config"
popd

pushd $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_SDK_NAME}
install_file "jsautocfg"
popd

pushd $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_SDK_NAME}
install_file "js-config"

%{__install} -p -c -m 755 dist/bin/xpcshell \
  dist/bin/xpidl \
  dist/bin/xpt_dump \
  dist/bin/xpt_link \
  $RPM_BUILD_ROOT/${MOZ_APP_DIR}

%{__rm} -rf $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_NAME}
%{__rm} -rf $RPM_BUILD_ROOT/%{_datadir}/idl/${INTERNAL_APP_NAME}

%{__rm} -rf $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/include
ln -s  %{_includedir}/${INTERNAL_APP_SDK_NAME} \
       $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/include

%{__rm} -rf $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/idl
ln -s  %{_datadir}/idl/${INTERNAL_APP_SDK_NAME} \
       $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/idl

%{__rm} -rf $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/include
ln -s  %{_includedir}/${INTERNAL_APP_SDK_NAME} \
       $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/include

%{__rm} -rf $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/idl
ln -s  %{_datadir}/idl/${INTERNAL_APP_SDK_NAME} \
       $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/idl

find $RPM_BUILD_ROOT/%{_includedir} -type f -name "*.h" | xargs chmod 644
find $RPM_BUILD_ROOT/%{_datadir}/idl -type f -name "*.idl" | xargs chmod 644

%{__rm} -rf $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/lib/*.so
pushd $RPM_BUILD_ROOT${MOZ_APP_DIR}
for i in *.so; do
    ln -s ${MOZ_APP_DIR}/$i $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/lib/$i
done
popd

# GRE stuff
%ifarch x86_64 ia64 ppc64 s390x
%define gre_conf_file gre64.conf
%else
%define gre_conf_file gre.conf
%endif

MOZILLA_GECKO_VERSION=`./config/milestone.pl --topsrcdir=.`
%{__mv} $RPM_BUILD_ROOT/etc/gre.d/$MOZILLA_GECKO_VERSION".system.conf" \
        $RPM_BUILD_ROOT/etc/gre.d/%{gre_conf_file}
chmod 644 $RPM_BUILD_ROOT/etc/gre.d/%{gre_conf_file}

# Library path
%ifarch x86_64 ia64 ppc64 s390x
%define ld_conf_file xulrunner-64.conf
%else
%define ld_conf_file xulrunner-32.conf
%endif

%{__mkdir_p} $RPM_BUILD_ROOT/etc/ld.so.conf.d
%{__cat} > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{ld_conf_file} << EOF
${MOZ_APP_DIR}
EOF
                        
# Copy over the LICENSE
%{__install} -p -c -m 644 LICENSE $RPM_BUILD_ROOT${MOZ_APP_DIR}

# Use the system hunspell dictionaries
#%{__rm} -rf ${RPM_BUILD_ROOT}${MOZ_APP_DIR}/dictionaries
#ln -s %{_datadir}/myspell ${RPM_BUILD_ROOT}${MOZ_APP_DIR}/dictionaries

# ghost files
%{__mkdir_p} $RPM_BUILD_ROOT${MOZ_APP_DIR}/components
touch $RPM_BUILD_ROOT${MOZ_APP_DIR}/components/compreg.dat
touch $RPM_BUILD_ROOT${MOZ_APP_DIR}/components/xpti.dat

#---------------------------------------------------------------------

%clean
%{__rm} -rf $RPM_BUILD_ROOT

#---------------------------------------------------------------------

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  %{__rm} -rf ${MOZ_APP_DIR}/components
fi

%files
%defattr(-,root,root,-)
%{_bindir}/xulrunner
%dir /etc/gre.d
/etc/gre.d/%{gre_conf_file}
%dir %{mozappdir}
%doc %attr(644, root, root) %{mozappdir}/LICENSE
%doc %attr(644, root, root) %{mozappdir}/README.txt
%{mozappdir}/chrome
%{mozappdir}/dictionaries
%dir %{mozappdir}/components
%ghost %{mozappdir}/components/compreg.dat
%ghost %{mozappdir}/components/xpti.dat
%{mozappdir}/components/*.so
%{mozappdir}/components/*.xpt
%attr(644, root, root) %{mozappdir}/components/*.js
%{mozappdir}/defaults
%{mozappdir}/greprefs
%dir %{mozappdir}/icons
%attr(644, root, root) %{mozappdir}/icons/*
%{mozappdir}/modules
%{mozappdir}/plugins
%{mozappdir}/res
%{mozappdir}/*.so
%{mozappdir}/mozilla-xremote-client
%{mozappdir}/run-mozilla.sh
%{mozappdir}/regxpcom
%{mozappdir}/xulrunner
%{mozappdir}/xulrunner-bin
%{mozappdir}/xulrunner-stub
%{mozappdir}/platform.ini
%{mozappdir}/dependentlibs.list
%{_sysconfdir}/ld.so.conf.d/xulrunner*.conf
%{_libdir}/%{name}*%{version_internal}/*

# XXX See if these are needed still
%{mozappdir}/updater*
%exclude %{mozappdir}/update.locale
%exclude %{mozappdir}/components/components.list

%files devel
%defattr(-,root,root,-)
%dir %{_libdir}/%{name}-sdk-*
%dir %{_libdir}/%{name}-sdk-*/sdk
%dir %{_datadir}/idl/%{name}*%{version_internal}
%{_datadir}/idl/%{name}*%{version_internal}
%{_includedir}/%{name}*%{version_internal}
%{_libdir}/%{name}-sdk-*/*
%{_libdir}/%{name}-sdk-*/sdk/*
%{_libdir}/pkgconfig/*.pc
%{mozappdir}/xpcshell
%{mozappdir}/xpidl
%{mozappdir}/xpt_dump
%{mozappdir}/xpt_link

#---------------------------------------------------------------------

%changelog
* Wed Mar 17 2010 David Hrbáč <david@hrbac.cz> - 1.9.2.1-4
- stick with Fedora 1.9.2.1-4
- Enable startup notification, closes #445543
- Added fix for mozbz#462919 - Override NSS database path 
  for xulrunner application
- Added fix for #564184 - xulrunner-devel multilib conflict

* Wed Feb 10 2010 David Hrbáč <david@hrbac.cz> - 1.9.2.1-1
- CentOS rebuild

* Fri Jan 22 2010 Martin Stransky <stransky@redhat.com> 1.9.2.1-1
- Update to 1.9.2.1

* Wed Jan 18 2010 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.10.rc1
- Update to 1.9.2.1 RC2

* Wed Jan 13 2010 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.9.rc1
- Update to 1.9.2.1 RC1

* Mon Dec 21 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.8.b5
- Update to 1.9.2.1 Beta 5

* Thu Dec 17 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.7.b4
- Added fix for mozbz#543585 - jemalloc alignment assertion 
  and abort on Linux

* Thu Dec 3 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.6.b4
- Added fix for #543585 - mozilla-plugin.pc contains incorrect CFLAGS

* Fri Nov 27 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.5.b4
- Update to 1.9.2.1 Beta 4

* Mon Nov 23 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.4.b3
- added -unstable.pc files for compatibility with 1.9.1

* Fri Nov 20 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.3.b3
- Necko wifi monitor disabled
- fixed a dependency (#539261)
- added source URL (#521704)

* Wed Nov 18 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.2.b3
- Rebase to 1.9.2.1 Beta 3

* Fri Nov 13 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.1.beta2
- Rebase to 1.9.2.1 Beta 2
- fix the sqlite runtime requires again (#480989), add a check 
  that the sqlite requires is sane (by Stepan Kasal)

* Thu Nov  5 2009 Jan Horak <jhorak@redhat.com> - 1.9.1.5-1
- Update to 1.9.1.5

* Mon Oct 26 2009 Jan Horak <jhorak@redhat.com> - 1.9.1.4-1
- Update to 1.9.1.4

* Mon Sep  7 2009 Jan Horak <jhorak@redhat.com> - 1.9.1.3-1
- Update to 1.9.1.3

* Fri Aug 21 2009 Jan Horak <jhorak@redhat.com> - 1.9.1.2-4
- Added libnotify support

* Wed Aug 12 2009 Martin Stransky <stransky@redhat.com> 1.9.1.2-3
- Added fix from #516118 - Headers not C89

* Mon Aug 6 2009 Martin Stransky <stransky@redhat.com> 1.9.1.2-2
- Rebuilt

* Mon Aug 3 2009 Martin Stransky <stransky@redhat.com> 1.9.1.2-1
- Update to 1.9.1.2

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Christopher Aillon <caillon@redhat.com> - 1.9.1.1-1
- Update to 1.9.1.1

* Mon Jul 13 2009 Jan Horak <jhorak@redhat.com> - 1.9.1-3
- Fixed wrong version of Firefox when loading 'about:' as location
- Added patch to compile against latest GTK

* Tue Jun 30 2009 Yanko Kaneti <yaneti@declera.com> - 1.9.1-2
- Build using system hunspell

* Tue Jun 30 2009 Christopher Aillon <caillon@redhat.com> 1.9.1-1
- Update to 1.9.1 final release

* Wed Jun 24 2009 Martin Stransky <stransky@redhat.com> 1.9.1-0.23
- Rebuilt because of gcc update (#506952)

* Thu Jun 18 2009 Martin Stransky <stransky@redhat.com> 1.9.1-0.22
- Backed out last change, it does not work inside mock (koji)

* Tue Jun 16 2009 Stepan Kasal <skasal@redhat.com> 1.9.1-0.21
- require sqlite of version >= what was used at buildtime (#480989)
- in devel subpackage, drop version from sqlite-devel require; that's
  handled indirectly through the versioned require in main package

* Mon Apr 27 2009 Christopher Aillon <caillon@redhat.com> 1.9.1-0.20
- 1.9.1 beta 4

* Fri Mar 27 2009 Christopher Aillon <caillon@redhat.com> 1.9.1-0.11
- Add patches for MFSA-2009-12, MFSA-2009-13

* Fri Mar 13 2009 Christopher Aillon <caillon@redhat.com> 1.9.1-0.10
- 1.9.1 beta 3

* Fri Feb 27 2009 Martin Stransky <stransky@redhat.com> 1.9.1-0.9
- Build fix for pango 1.23
- Misc. build fixes

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-0.8.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Christopher Aillon <caillon@redhat.com> 1.9.1-0.7
- Re-enable NM by default

* Wed Jan  7 2009 Martin Stransky <stransky@redhat.com> 1.9.1-0.6
- Copied mozilla-config.h to stable include dir (#478445)

* Mon Dec 22 2008 Christopher Aillon <caillon@redhat.com> 1.9.1-0.5
- Typo fix

* Sat Dec 20 2008 Christopher Aillon <caillon@redhat.com> 1.9.1-0.4
- 1.9.1 beta 2

* Tue Dec  9 2008 Christopher Aillon <caillon@redhat.com> 1.9.1-0.3
- Mark this as a pre-release

* Tue Dec  9 2008 Christopher Aillon <caillon@redhat.com> 1.9.1-0.2
- Add needed -devel requires to the -devel package

* Thu Dec  4 2008 Christopher Aillon <caillon@redhat.com> 1.9.1-0.1
- 1.9.1 beta 1

* Wed Nov 12 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.4-1
- Update to 1.9.0.4

* Mon Oct 27 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.2-5
- Password manager fixes from upstream

* Tue Oct  7 2008 Marco Pesenti Gritti <mpg@redhat.com> 1.9.0.2-4
- Add missing dependency on python-devel

* Sun Oct  5 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.2-3
- Enable PyXPCOM

* Thu Sep 25 2008 Martin Stransky <stransky@redhat.com> 1.9.0.2-2 
- Build with system cairo (#463341)

* Tue Sep 23 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.2-1
- Update to 1.9.0.2

* Wed Jul 23 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.1-2
- Disable system hunspell for now as it's causing some crashes (447444)

* Wed Jul 16 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.1-1
- Update to 1.9.0.1

* Tue Jun 17 2008 Christopher Aillon <caillon@redhat.com> 1.9-1
- Update to 1.9 final

* Thu May 29 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.63
- Simplify PS/PDF operators

* Thu May 22 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.62
- Upstream patch to fsync() less

* Thu May 08 2008 Colin Walters <walters@redhat.com> 1.9-0.61
- Ensure we enable startup notification; add BR and modify config
  (bug #445543)

* Wed Apr 30 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.60
- Some files moved to mozilla-filesystem; kill them and add the Req

* Mon Apr 28 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.59
- Clean up the %%files list and get rid of the executable bit on some files

* Sat Apr 26 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.58
- Fix font scaling

* Fri Apr 25 2008 Martin Stransky <stransky@redhat.com> 1.9-0.57
- Enabled phishing protection (#443403)

* Wed Apr 23 2008 Martin Stransky <stransky@redhat.com> 1.9-0.56
- Changed "__ppc64__" to "__powerpc64__", 
  "__ppc64__" doesn't work anymore
- Added fix for #443725 - Critical hanging bug with fix 
  available upstream (mozbz#429903)

* Fri Apr 18 2008 Martin Stransky <stransky@redhat.com> 1.9-0.55
- Fixed multilib issues, added starting script instead of a symlink
  to binary (#436393)

* Sat Apr 12 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.54
- Add upstream patches for dpi, toolbar buttons, and invalid keys
- Re-enable system cairo

* Mon Apr  7 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.53
- Spec cleanups

* Wed Apr  2 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.52
- Beta 5

* Mon Mar 31 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.51
- Beta 5 RC2

* Thu Mar 27 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.50
- Update to latest trunk (2008-03-27)

* Wed Mar 26 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.49
- Update to latest trunk (2008-03-26)

* Tue Mar 25 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.48
- Update to latest trunk (2008-03-25)

* Mon Mar 24 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.47
- Update to latest trunk (2008-03-24)

* Thu Mar 20 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.46
- Update to latest trunk (2008-03-20)

* Mon Mar 17 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.45
- Update to latest trunk (2008-03-17)

* Mon Mar 17 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.44
- Revert to trunk from the 15th to fix crashes on HTTPS sites

* Sun Mar 16 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.43
- Update to latest trunk (2008-03-16)
- Add patch to negate a11y slowdown on some pages (#431162)

* Sat Mar 15 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.42
- Update to latest trunk (2008-03-15)

* Sat Mar 15 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.41
- Avoid conflicts between gecko debuginfo packages

* Wed Mar 12 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.40
- Update to latest trunk (2008-03-12)

* Tue Mar 11 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.39
- Update to latest trunk (2008-03-11)

* Mon Mar 10 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.38
- Update to latest trunk (2008-03-10)

* Sun Mar  9 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.37
- Update to latest trunk (2008-03-09)

* Fri Mar  7 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta4.36
- Update to latest trunk (2008-03-07)

* Thu Mar  6 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta4.35
- Update to latest trunk (2008-03-06)

* Tue Mar  4 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta4.34
- Update to latest trunk (2008-03-04)

* Sun Mar  2 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.33
- Update to latest trunk (2008-03-02)

* Sat Mar  1 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.32
- Update to latest trunk (2008-03-01)

* Fri Feb 29 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.31
- Update to latest trunk (2008-02-29)

* Thu Feb 28 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.30
- Update to latest trunk (2008-02-28)

* Wed Feb 27 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.29
- Update to latest trunk (2008-02-27)

* Tue Feb 26 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.28
- Update to latest trunk (2008-02-26)

* Sat Feb 23 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.27
- Update to latest trunk (2008-02-23)

* Fri Feb 22 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.26
- Update to latest trunk (2008-02-22)

* Thu Feb 21 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.25
- Update to latest trunk (2008-02-21)

* Wed Feb 20 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.24
- Update to latest trunk (2008-02-20)

* Sun Feb 17 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.23
- Update to latest trunk (2008-02-17)

* Fri Feb 15 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.22
- Update to latest trunk (2008-02-15)

* Thu Feb 14 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.21
- Update to latest trunk (2008-02-14)
- Use system hunspell

* Mon Feb 11 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.19
- Update to latest trunk (2008-02-11)

* Mon Feb 11 2008 Adam Jackson <ajax@redhat.com> 1.9-0.beta2.19
- STRIP="/bin/true" on the %%make line so xulrunner-debuginfo contains,
  you know, debuginfo.

* Sun Feb 10 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.18
- Update to latest trunk (2008-02-10)

* Sat Feb  9 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.17
- Update to latest trunk (2008-02-09)

* Wed Feb  6 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.16
- Update to latest trunk (2008-02-06)

* Tue Jan 29 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.15
- Update to latest trunk (2008-01-30)

* Wed Jan 25 2008 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.14
- rebuild agains new nss
- enabled gnome vfs

* Wed Jan 23 2008 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.13
- fixed stable pkg-config files (#429654)
- removed sqlite patch

* Mon Jan 21 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.12
- Update to latest trunk (2008-01-21)

* Tue Jan 15 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.11
- Update to latest trunk (2008-01-15)
- Now with system extensions directory support

* Sat Jan 13 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.10
- Update to latest trunk (2008-01-13)
- Use CFLAGS instead of configure arguments
- Random cleanups: BuildRequires, scriptlets, prefs, etc.

* Sat Jan 12 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.9
- Provide gecko-devel-unstable as well

* Wed Jan 9 2008 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.8
- divided devel package to devel and devel-unstable

* Mon Jan 7 2008 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.7
- removed fedora specific pkg-config files
- updated to the latest trunk (2008-01-07)
- removed unnecessary patches
- fixed idl dir (#427965)

* Thu Jan 3 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.6
- Re-enable camellia256 support now that NSS supports it

* Thu Jan 3 2008 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.5
- updated to the latest trunk (2008-01-03)

* Mon Dec 24 2007 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.4
- Don't Provide webclient (xulrunner is not itself a webclient)
- Don't Obsolete old firefox, only firefox-devel
- Kill legacy obsoletes (phoenix, etc) that were never in rawhide

* Thu Dec 21 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.3
- added java and plugin subdirs to plugin includes

* Thu Dec 20 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.2
- dependency fixes, obsoletes firefox < 3 and firefox-devel now

* Wed Dec 12 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.1
- updated to Beta 2.
- moved SDK to xulrunner-sdk

* Thu Dec 06 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta1.4
- fixed mozilla-plugin.pc (#412971)

* Tue Nov 27 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta1.3
- export /etc/gre.d/gre.conf (it's used by python gecko applications)

* Mon Nov 26 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta1.2
- added xulrunner/js include dir to xulrunner-js

* Tue Nov 20 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta1.1
- update to beta 1

* Mon Nov 19 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.6
- packed all gecko libraries (#389391)

* Thu Nov 15 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.5
- registered xulrunner libs system-wide
- added xulrunner-gtkmozembed.pc

* Wed Nov 14 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.4
- added proper nss/nspr dependencies

* Wed Nov 14 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.3
- more build fixes, use system nss libraries

* Tue Nov 6 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.2
- build fixes

* Tue Oct 30 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.1
- updated to the latest trunk

* Thu Sep 20 2007 David Woodhouse <dwmw2@infradead.org> 1.9-0.alpha7.4
- build fixes for ppc/ppc64

* Tue Sep 20 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha7.3
- removed conflicts with the current gecko-based apps
- added updated ppc64 patch

* Tue Sep 18 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha7.2
- build fixes

* Wed Sep  5 2007 Christopher Aillon <caillon@redhat.com> 1.9-0.alpha7.1
- Initial cut at XULRunner 1.9 Alpha 7
- Temporarily revert camellia 256 support since our nss doesn't support it yet
