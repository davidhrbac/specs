# set to zero to avoid running test suite
%define make_check 1

%define with_java 0

# set JDK path to build javahl; default for JPackage
%define jdk_path /usr/lib/jvm/java

%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%{!?ruby_sitearch: %define ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"]')}

%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: A Modern Concurrent Version Control System
Name: subversion
Version: 1.6.3
Release: 1%{?dist}
License: ASL 1.1
Group: Development/Tools
URL: http://subversion.tigris.org/
Source0: http://subversion.tigris.org/tarballs/subversion-%{version}.tar.gz
Source1: subversion.conf
Source3: filter-requires.sh
Source4: http://www.xsteve.at/prg/emacs/psvn.el
Source5: psvn-init.el
Patch2: subversion-1.6.0-deplibs.patch
Patch3: subversion-1.6.1-rpath.patch
Patch6: subversion-1.6.0-pie.patch
Patch7: subversion-1.1.3-java.patch
Patch8: subversion-1.6.2-kwallet.patch
BuildRequires: autoconf, libtool, python, python-devel, texinfo, which
BuildRequires: db4-devel >= 4.1.25, swig >= 1.3.24, gettext
BuildRequires: apr-devel >= 1.3.0, apr-util-devel >= 1.3.0
BuildRequires: neon-devel >= 0:0.24.7-1, cyrus-sasl-devel
BuildRequires: sqlite-devel >= 3.4.0
BuildRequires: gnome-keyring-devel, dbus-devel, kdelibs-devel >= 4.0.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides: svn = %{version}-%{release}
Requires: apr >= 1.3.0

%define __perl_requires %{SOURCE3}

# Put Python bindings in site-packages
%define swigdirs swig_pydir=%{python_sitearch}/libsvn swig_pydir_extra=%{python_sitearch}/svn

%description
Subversion is a concurrent version control system which enables one
or more users to collaborate in developing and maintaining a
hierarchy of files and directories while keeping a history of all
changes.  Subversion only stores the differences between versions,
instead of every complete file.  Subversion is intended to be a
compelling replacement for CVS.

%package devel
Group: Development/Tools
Summary: Development package for the Subversion libraries
Requires: subversion = %{version}-%{release}, apr-devel, apr-util-devel

%description devel
The subversion-devel package includes the static libraries and
include files for developers interacting with the subversion
package.

%package gnome
Group: Development/Tools
Summary: GNOME Keyring support for Subversion
Requires: subversion = %{version}-%{release}

%description gnome
The subversion-gnome package adds support for storing Subversion
passwords in the GNOME Keyring.

%package kde
Group: Development/Tools
Summary: KDE Wallet support for Subversion
Requires: subversion = %{version}-%{release}

%description kde
The subversion-kde package adds support for storing Subversion
passwords in the KDE Wallet.

%package -n mod_dav_svn
Group: System Environment/Daemons
Summary: Apache httpd module for Subversion server
Requires: httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing)
Requires: subversion = %{version}-%{release}
BuildRequires: httpd-devel >= 2.0.45

%description -n mod_dav_svn
The mod_dav_svn package allows access to a Subversion repository
using HTTP, via the Apache httpd server.

%package perl
Group: Development/Libraries
Summary: Perl bindings to the Subversion libraries
BuildRequires: perl-devel >= 2:5.8.0, perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::More), perl(ExtUtils::Embed)
Requires: %(eval `perl -V:version`; echo "perl(:MODULE_COMPAT_$version)")
Requires: subversion = %{version}-%{release}

%description perl
This package includes the Perl bindings to the Subversion libraries.

%if %{with_java}
%package javahl
Group: Development/Libraries
Summary: JNI bindings to the Subversion libraries
Requires: subversion = %{version}-%{release}
BuildRequires: java-devel-openjdk

%description javahl
This package includes the JNI bindings to the Subversion libraries.
%endif

%package ruby
Group: Development/Libraries
Summary: Ruby bindings to the Subversion libraries
BuildRequires: ruby-devel >= 1.8.2, ruby >= 1.8.2
Requires: subversion = %{version}-%{release}, ruby-libs >= 1.8.2
Requires: ruby(abi) = 1.8

%description ruby
This package includes the Ruby bindings to the Subversion libraries.

%prep
%setup -q
%patch2 -p1 -b .deplibs
%patch3 -p1 -b .rpath
#patch6 -p1 -b .pie
%if %{with_java}
%patch7 -p1 -b .java
%endif
%ifarch sparc64
sed -i -e 's|-fpie|-fPIE|g' Makefile.in
%endif
%patch8 -p1 -b .kwallet

%build
# Regenerate the buildsystem, so that:
#  1) patches applied to configure.in take effect
#  2) the swig bindings are regenerated using the system swig
./autogen.sh --release

# fix shebang lines, #111498
perl -pi -e 's|/usr/bin/env perl -w|/usr/bin/perl -w|' tools/hook-scripts/*.pl.in

# override weird -shrext from ruby
export svn_cv_ruby_link="%{__cc} -shared"
export svn_cv_ruby_sitedir_libsuffix=""
export svn_cv_ruby_sitedir_archsuffix=""

export CC=gcc CXX=g++ JAVA_HOME=%{jdk_path} CFLAGS="$RPM_OPT_FLAGS"
%configure --with-apr=%{_prefix} --with-apr-util=%{_prefix} \
        --with-swig --with-neon=%{_prefix} \
        --with-ruby-sitedir=%{ruby_sitearch} \
        --with-apxs=%{_sbindir}/apxs --disable-mod-activation \
        --disable-static --with-sasl=%{_prefix} \
        --disable-neon-version-check \
        --with-gnome-keyring \
        --with-kwallet
make %{?_smp_mflags} all
make swig-py swig-py-lib %{swigdirs}
make swig-pl swig-pl-lib swig-rb swig-rb-lib
%if %{with_java}
# javahl-javah does not parallel-make with javahl
make javahl-java javahl-javah
make javahl
%endif

%install
rm -rf ${RPM_BUILD_ROOT}
make install install-swig-py install-swig-pl-lib install-swig-rb \
        DESTDIR=$RPM_BUILD_ROOT %{swigdirs}
%if %{with_java}
make install-javahl-java install-javahl-lib javahl_javadir=%{_javadir} DESTDIR=$RPM_BUILD_ROOT
%endif

make pure_vendor_install -C subversion/bindings/swig/perl/native \
        PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
install -m 755 -d ${RPM_BUILD_ROOT}%{_sysconfdir}/subversion

# Add subversion.conf configuration file into httpd/conf.d directory.
install -m 755 -d ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d
install -m 644 $RPM_SOURCE_DIR/subversion.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d

# Remove unpackaged files
rm -rf ${RPM_BUILD_ROOT}%{_includedir}/subversion-*/*.txt \
       ${RPM_BUILD_ROOT}%{python_sitearch}/*/*.{a,la}

# remove stuff produced with Perl modules
find $RPM_BUILD_ROOT -type f \
    -a \( -name .packlist -o \( -name '*.bs' -a -empty \) \) \
    -print0 | xargs -0 rm -f

# make Perl modules writable so they get stripped
find $RPM_BUILD_ROOT%{_libdir}/perl5 -type f -perm 555 -print0 |
        xargs -0 chmod 755

# unnecessary libraries for swig bindings
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libsvn_swig_*.{so,la,a}

# Remove unnecessary ruby libraries
rm -f ${RPM_BUILD_ROOT}%{ruby_sitearch}/svn/ext/*.*a

# Trim what goes in docdir
rm -rf tools/*/*.in tools/test-scripts

# Install psvn for emacs and xemacs
for f in emacs/site-lisp xemacs/site-packages/lisp; do
  install -m 755 -d ${RPM_BUILD_ROOT}%{_datadir}/$f
  install -m 644 $RPM_SOURCE_DIR/psvn.el ${RPM_BUILD_ROOT}%{_datadir}/$f
done

install -m 644 $RPM_SOURCE_DIR/psvn-init.el \
        ${RPM_BUILD_ROOT}%{_datadir}/emacs/site-lisp

# Rename authz_svn INSTALL doc for docdir
ln -f subversion/mod_authz_svn/INSTALL mod_authz_svn-INSTALL

# Trim exported dependencies to SVN and APR libraries only:
sed -i "/^dependency_libs/{
     s, -l[^ ']*, ,g;
     s,%{_libdir}/lib[^sa][^vp][^nr].*.la, ,g;
     }"  $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name}

%if %{make_check}
%check
export LANG=C LC_ALL=C
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}
make check check-swig-pl check-swig-py CLEANUP=yes
# check-swig-rb omitted: it runs svnserve
%endif

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post perl -p /sbin/ldconfig

%postun perl -p /sbin/ldconfig

%post ruby -p /sbin/ldconfig

%postun ruby -p /sbin/ldconfig

%if %{with_java}
%post javahl -p /sbin/ldconfig

%postun javahl -p /sbin/ldconfig
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc BUGS COMMITTERS COPYING HACKING INSTALL README CHANGES
%doc tools subversion/LICENSE mod_authz_svn-INSTALL
%doc contrib/client-side/svn_load_dirs/{*.pl,*.example,*.README}
%doc contrib/client-side/svnmerge/*.{README,py}
%doc contrib/client-side/wcgrep
%{_bindir}/*
%{_libdir}/libsvn_*.so.*
%{_mandir}/man*/*
%{python_sitearch}/svn
%{python_sitearch}/libsvn
%{_datadir}/emacs/site-lisp/*.el
%{_datadir}/xemacs/site-packages/lisp/*.el
%dir %{_sysconfdir}/subversion
%exclude %{_libdir}/libsvn_swig_perl*
%exclude %{_libdir}/libsvn_swig_ruby*
%exclude %{_libdir}/libsvn_auth_kwallet*
%exclude %{_libdir}/libsvn_auth_gnome*
%exclude %{_mandir}/man*/*::*

%files gnome
%{_libdir}/libsvn_auth_gnome_keyring-*.so.*

%files kde
%{_libdir}/libsvn_auth_kwallet-*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/subversion-1
%{_libdir}/libsvn*.*a
%{_libdir}/libsvn*.so
%exclude %{_libdir}/libsvn_swig_perl*
%if %{with_java}
%exclude %{_libdir}/libsvnjavahl-1.*
%endif

%files -n mod_dav_svn
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/subversion.conf
%{_libdir}/httpd/modules/mod_dav_svn.so
%{_libdir}/httpd/modules/mod_authz_svn.so

%files perl
%defattr(-,root,root,-)
%{perl_vendorarch}/auto/SVN
%{perl_vendorarch}/SVN
%{_libdir}/libsvn_swig_perl*
%{_mandir}/man*/*::*

%files ruby
%defattr(-,root,root,-)
%{_libdir}/libsvn_swig_ruby*
%{ruby_sitearch}/svn

%if %{with_java}
%files javahl
%defattr(-,root,root,-)
%{_libdir}/libsvnjavahl-1.*
%{_javadir}/svn-javahl.jar
%endif

%changelog
* Tue Jun 23 2009 Joe Orton <jorton@redhat.com> 1.6.3-1
- update to 1.6.3

* Sun Jun 14 2009 Joe Orton <jorton@redhat.com> 1.6.2-3
- add -gnome, -kde subpackages

* Mon Jun  1 2009 Joe Orton <jorton@redhat.com> 1.6.2-2
- enable KWallet, gnome-keyring support

* Fri May 15 2009 Joe Orton <jorton@redhat.com> 1.6.2-1
- update to 1.6.2

* Wed Apr 15 2009 Joe Orton <jorton@redhat.com> 1.6.1-4
- really disable PIE

* Tue Apr 14 2009 Joe Orton <jorton@redhat.com> 1.6.1-3
- update to 1.6.1; disable PIE patch for the time being

* Tue Mar 31 2009 Joe Orton <jorton@redhat.com> 1.6.0-3
- BR sqlite-devel

* Tue Mar 31 2009 Joe Orton <jorton@redhat.com> 1.6.0-1
- update to 1.6.0

* Thu Mar 12 2009 Dennis Gilmore <dennis@ausil.us> - 1.5.6-4
- use -fPIE on sparc64

* Mon Mar  9 2009 Joe Orton <jorton@redhat.com> 1.5.6-3
- update to 1.5.6
- autoload psvn (#238491, Tom Tromey)
- regenerate swig bindings (#480503)
- fix build with libtool 2.2 (#469524)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Joe Orton <jorton@redhat.com> 1.5.5-5
- update to 1.5.5

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.5.4-4
- Rebuild for Python 2.6

* Mon Oct 27 2008 Joe Orton <jorton@redhat.com> 1.5.4-3
- update to 1.5.4

* Mon Oct 13 2008 Joe Orton <jorton@redhat.com> 1.5.3-3
- fix build

* Mon Oct 13 2008 Joe Orton <jorton@redhat.com> 1.5.3-2
- update to 1.5.3 (#466674)
- update psvn.el to r33557

* Tue Sep 30 2008 Joe Orton <jorton@redhat.com> 1.5.2-3
- enable SASL support (#464267)

* Fri Sep 12 2008 Joe Orton <jorton@redhat.com> 1.5.2-2
- update to 1.5.2

* Mon Jul 28 2008 Joe Orton <jorton@redhat.com> 1.5.1-2
- update to 1.5.1
- require suitable APR

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.0-8
- rebuild against new db4-4.7

* Thu Jul  3 2008 Joe Orton <jorton@redhat.com> 1.5.0-7
- add svnmerge and wcgrep to docdir (Edward Rudd, #451932)
- drop neon version overrides

* Wed Jul  2 2008 Joe Orton <jorton@redhat.com> 1.5.0-6
- build with OpenJDK

* Wed Jul  2 2008 Joe Orton <jorton@redhat.com> 1.5.0-5
- fix files list

* Wed Jul  2 2008 Joe Orton <jorton@redhat.com> 1.5.0-4
- swig-perl test suite fix for Perl 5.10 (upstream r31546)

* Tue Jul  1 2008 Joe Orton <jorton@redhat.com> 1.5.0-3
- attempt build without java bits

* Thu Jun 26 2008 Joe Orton <jorton@redhat.com> 1.5.0-2
- update to 1.5.0

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.6-7
- tests are randomly failing, unrelated to new perl, disabled tests

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.6-6
- rebuild for new perl (again)

* Thu Feb 21 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.4.6-5
- Correct install location of java stuff (#433295)

* Wed Feb  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.6-4
- BR perl(ExtUtils::Embed)

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.6-3
- rebuild for new perl

* Fri Dec 21 2007 Joe Orton <jorton@redhat.com> 1.4.6-2
- update to 1.4.6

* Mon Dec 10 2007 Warren Togami <wtogami@redhat.com> 1.4.4-11
- temporarily disable test suite

* Thu Dec  6 2007 Joe Orton <jorton@redhat.com> 1.4.4-10
- fix build with swig 1.3.33 (patch by Torsten Landschoff)

* Wed Dec  5 2007 Joe Orton <jorton@redhat.com> 1.4.4-9
- rebuild for OpenLDAP soname bump

* Tue Sep  4 2007 Joe Orton <jorton@redhat.com> 1.4.4-8
- update to psvn.el r26383 from upstream

* Sun Sep  2 2007 Joe Orton <jorton@redhat.com> 1.4.4-7
- rebuild for fixed 32-bit APR 

* Thu Aug 30 2007 Joe Orton <jorton@redhat.com> 1.4.4-6
- clarify License tag; re-enable test suite

* Thu Aug 23 2007 Joe Orton <jorton@redhat.com> 1.4.4-5
- rebuild for neon 0.27

* Wed Aug 22 2007 Joe Orton <jorton@redhat.com> 1.4.4-4
- trim dependencies from .la files
- detabify spec file
- test suite disabled to ease stress on builders

* Wed Aug  8 2007 Joe Orton <jorton@redhat.com> 1.4.4-3
- fix build with new glibc open()-as-macro
- build all swig code in %%build, not %%install
- BuildRequire perl(Test::More), perl(ExtUtils::MakeMaker)

* Tue Jul  3 2007 Joe Orton <jorton@redhat.com> 1.4.4-2
- update to 1.4.4
- add Provides: svn (#245087)
- fix without-java build (Lennert Buytenhek, #245467)

* Wed Apr 11 2007 Joe Orton <jorton@redhat.com> 1.4.3-5
- fix version of apr/apr-util in BR (#216181)

* Thu Mar 29 2007 Joe Orton <jorton@redhat.com> 1.4.3-4
- fix javahl compile failure

* Mon Jan 29 2007 Joe Orton <jorton@redhat.com> 1.4.3-3
- update to 1.4.3 (#228691)
- remove trailing dot from Summary
- use current preferred standard BuildRoot
- add post/postun ldconfig scriptlets for -ruby and -javahl

* Fri Dec  8 2006 Joe Orton <jorton@redhat.com> 1.4.2-5
- fix use of python_sitearch

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.4.2-4
- rebuild against python 2.5
- follow python packaging guidelines

* Wed Nov  8 2006 Joe Orton <jorton@redhat.com> 1.4.2-3
- update to 1.4.2

* Mon Sep 11 2006 Joe Orton <jorton@redhat.com> 1.4.0-2
- update to 1.4.0

* Thu Jul 13 2006 Joe Orton <jorton@redhat.com> 1.3.2-6
- fix ruby packaging (#191611)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.3.2-5.1
- rebuild

* Wed Jun  7 2006 Joe Orton <jorton@redhat.com> 1.3.2-5
- disable test suite

* Wed Jun  7 2006 Joe Orton <jorton@redhat.com> 1.3.2-4
- BR gettext

* Fri Jun  2 2006 Joe Orton <jorton@redhat.com> 1.3.2-3
- re-enable test suite

* Fri Jun  2 2006 Joe Orton <jorton@redhat.com> 1.3.2-2
- update to 1.3.2
- fix Ruby sitelibdir (Garrick Staples, #191611)
- own /etc/subversion (#189071)
- update to psvn.el r19857

* Thu Apr  6 2006 Joe Orton <jorton@redhat.com> 1.3.1-4
- move libsvn_swig_ruby* back to subversion-ruby

* Tue Apr  4 2006 Joe Orton <jorton@redhat.com> 1.3.1-3
- update to 1.3.1
- update to psvn.el r19138 (Stefan Reichoer)
- build -java on s390 again

* Thu Feb 16 2006 Florian La Roche <laroche@redhat.com> - 1.3.0-5
- do not package libs within subversion-ruby, these are already
  available via the main package

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3.0-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3.0-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Joe Orton <jorton@redhat.com> 1.3.0-4
- run check-swig-py in %%check (#178448)
- relax JDK requirement (Kenneth Porter, #177367)

* Tue Jan 31 2006 Joe Orton <jorton@redhat.com> 1.3.0-3
- rebuild for neon 0.25

* Wed Jan  4 2006 Joe Orton <jorton@redhat.com> 1.3.0-2
- update to 1.3.0 (#176833)
- update to psvn.el r17921 Stefan Reichoer

* Mon Dec 12 2005 Joe Orton <jorton@redhat.com> 1.2.3-6
- fix ownership of libsvnjavahl.* (#175289)
- try building javahl on ia64/ppc64 again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Joe Orton <jorton@redhat.com> 1.2.3-5
- rebuild for httpd-2.2/apr-1.2/apr-util-1.2

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 1.2.3-4
- rebuilt against new openssl

* Thu Sep  8 2005 Joe Orton <jorton@redhat.com> 1.2.3-3
- update to 1.2.3
- update to psvn.el r16070 from Stefan Reichoer
- merge subversion.conf changes from RHEL4
- merge filter-requires.sh changes from FC4 updates

* Mon Aug  8 2005 Joe Orton <jorton@redhat.com> 1.2.1-4
- add BR for which (#161015)

* Fri Jul 22 2005 Joe Orton <jorton@redhat.com> 1.2.0-3
- update to 1.2.1
- fix BuildRequires for ruby and apr-util (#163126)
- drop static library archives

* Wed May 25 2005 Joe Orton <jorton@redhat.com> 1.2.0-2
- disable java on all but x86, x86_64, ppc (#158719)

* Tue May 24 2005 Joe Orton <jorton@redhat.com> 1.2.0-1
- update to 1.2.0; add ruby subpackage

* Wed Apr 13 2005 Joe Orton <jorton@redhat.com> 1.1.4-3
- enable java subpackage again
- tweak subversion.conf comments

* Sun Apr  3 2005 Joe Orton <jorton@redhat.com> 1.1.4-2
- update to 1.1.4

* Tue Mar 22 2005 Joe Orton <jorton@redhat.com> 1.1.3-8
- further swig bindings fix (upstream via Max Bowsher, #151798)
- fix perl File::Path dependency in filter-requires.sh

* Tue Mar 22 2005 Joe Orton <jorton@redhat.com> 1.1.3-7
- restore swig bindings support (from upstream via Max Bowsher, #141343)
- tweak SELinux commentary in default subversion.conf

* Wed Mar  9 2005 Joe Orton <jorton@redhat.com> 1.1.3-6
- fix svn_load_dirs File::Path version requirement

* Tue Mar  8 2005 Joe Orton <jorton@redhat.com> 1.1.3-5
- add -java subpackage for javahl libraries (Anthony Green, #116202)

* Fri Mar  4 2005 Joe Orton <jorton@redhat.com> 1.1.3-4
- rebuild

* Tue Feb 15 2005 Joe Orton <jorton@redhat.com> 1.1.3-3
- run test suite in C locale (#146125)
- adjust -pie patch for build.conf naming upstream

* Wed Jan 19 2005 Joe Orton <jorton@redhat.com> 1.1.3-2
- rebuild to pick up db-4.3 properly; don't ignore test failures

* Sun Jan 16 2005 Joe Orton <jorton@redhat.com> 1.1.3-1
- update to 1.1.3 (#145236)
- fix python bindings location on x86_64 (#143522)

* Mon Jan 10 2005 Joe Orton <jorton@redhat.com> 1.1.2-3
- update to 1.1.2
- disable swig bindings due to incompatible swig version

* Wed Nov 24 2004 Joe Orton <jorton@redhat.com> 1.1.1-5
- update subversion.conf examples to be SELinux-friendly

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 1.1.1-4
- rebuild against db-4.3.21.
- x86_64: don't fail "make check" while diagnosing db-4.3.21 upgrade.

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 1.1.1-3
- rebuild against python 2.4

* Mon Oct 25 2004 Joe Orton <jorton@redhat.com> 1.1.1-2
- update to 1.1.1
- update -pie patch to address #134786

* Mon Oct  4 2004 Joe Orton <jorton@redhat.com> 1.1.0-5
- use pure_vendor_install to fix Perl modules
- use %%find_lang to package translations (Axel Thimm)

* Thu Sep 30 2004 Joe Orton <jorton@redhat.com> 1.1.0-4
- don't use parallel make for swig-py

* Thu Sep 30 2004 Joe Orton <jorton@redhat.com> 1.1.0-3
- BuildRequire newest swig for "swig -ldflags" fix

* Thu Sep 30 2004 Joe Orton <jorton@redhat.com> 1.1.0-2
- fix swig bindings build on x86_64

* Thu Sep 30 2004 Joe Orton <jorton@redhat.com> 1.1.0-1
- update to 1.1.0

* Thu Sep 23 2004 Joe Orton <jorton@redhat.com> 1.0.8-2
- update to 1.0.8
- remove -neonver patch
- update psvn.el to 11062

* Mon Aug 23 2004 Joe Orton <jorton@redhat.com> 1.0.6-3
- add svn_load_dirs.pl to docdir (#128338)
- add psvn.el (#128356)

* Thu Jul 22 2004 Joe Orton <jorton@redhat.com> 1.0.6-2
- rebuild

* Tue Jul 20 2004 Joe Orton <jorton@redhat.com> 1.0.6-1
- update to 1.0.6
- allow build against neon 0.24.*

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun 10 2004 Joe Orton <jorton@redhat.com> 1.0.5-1
- update to 1.0.5

* Mon Jun  7 2004 Joe Orton <jorton@redhat.com> 1.0.4-2
- add ra_svn security fix for CVE CAN-2004-0413 (Ben Reser)

* Fri May 28 2004 Joe Orton <jorton@redhat.com> 1.0.4-1.1
- rebuild for new swig

* Sat May 22 2004 Joe Orton <jorton@redhat.com> 1.0.4-1
- update to 1.0.4

* Fri May 21 2004 Joe Orton <jorton@redhat.com> 1.0.3-2
- build /usr/bin/* as PIEs
- add fix for libsvn_client symbol namespace violation (r9608)

* Wed May 19 2004 Joe Orton <jorton@redhat.com> 1.0.3-1
- update to 1.0.3

* Sun May 16 2004 Joe Orton <jorton@redhat.com> 1.0.2-3
- add ldconfig invocations for -perl post/postun (Ville Skyttä)

* Tue May  4 2004 Joe Orton <jorton@redhat.com> 1.0.2-2
- add perl MODULE_COMPAT requirement for -perl subpackage
- move perl man pages into -perl subpackage
- clean up -perl installation and dependencies (Ville Skyttä, #123045)

* Mon Apr 19 2004 Joe Orton <jorton@redhat.com> 1.0.2-1
- update to 1.0.2

* Fri Mar 12 2004 Joe Orton <jorton@redhat.com> 1.0.1-1
- update to 1.0.1; cvs2svn no longer included

* Fri Mar 12 2004 Joe Orton <jorton@redhat.com> 1.0.0-3
- add -perl subpackage for Perl bindings (steve@silug.org)
- include mod_authz_svn INSTALL file

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 1.0.0-2.1
- rebuilt

* Wed Feb 25 2004 Joe Orton <jorton@redhat.com> 1.0.0-2
- add fix for lack of apr_dir_read ordering guarantee (Philip Martin)
- enable compression in ra_dav by default (Tobias Ringström)

* Mon Feb 23 2004 Joe Orton <jorton@redhat.com> 1.0.0-1
- update to one-dot-oh

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 0.37.0-2
- rebuilt

* Sat Jan 24 2004 Joe Orton <jorton@redhat.com> 0.37.0-1
- update to 0.37.0

* Tue Jan 13 2004 Joe Orton <jorton@redhat.com> 0.36.0-1
- update to 0.36.0

* Thu Jan  8 2004 Joe Orton <jorton@redhat.com> 0.35.1-1
- update to 0.35.1
- fix shebang lines in hook scripts (#111498)

* Sat Dec 13 2003 Jeff Johnson <jbj@jbj.org> 0.34.0-3
- rebuild against db-4.2.52.

* Thu Dec  4 2003 Joe Orton <jorton@redhat.com> 0.34.0-2
- package all man pages

* Thu Dec 04 2003 Joe Orton <jorton@redhat.com> 0.34.0-1
- update to 0.34.0

* Thu Nov 13 2003 Joe Orton <jorton@redhat.com> 0.32.1-3
- remove workarounds for #109268 and #109267

* Thu Nov  6 2003 Joe Orton <jorton@redhat.com> 0.32.1-2
- rebuild for Python 2.3.2
- remove libtool workaround
- add workarounds for #109268 and #109267

* Fri Oct 24 2003 Joe Orton <jorton@redhat.com> 0.32.1-1
- update to 0.31.2
- work around libtool/ppc64/db4 confusion

* Mon Oct 13 2003 Jeff Johnson <jbj@jbj.org> 0.31.0-2.1
- rebuild against db-4.2.42.

* Fri Oct 10 2003 Joe Orton <jorton@redhat.com> 0.31.0-2
- include The Book
- don't add an RPATH for libdir to executables

* Thu Oct  9 2003 Joe Orton <jorton@redhat.com> 0.31.0-1
- update to 0.31.0

* Wed Sep 24 2003 Joe Orton <jorton@redhat.com> 0.30.0-1
- update to 0.30.0

* Sun Sep  7 2003 Joe Orton <jorton@redhat.com> 0.29.0-1
- update to 0.29.0

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 0.25-2
- rebuild

* Tue Jul 15 2003 Joe Orton <jorton@redhat.com> 0.25-1
- update to 0.25

* Mon Jul 14 2003 Joe Orton <jorton@redhat.com> 0.24.2-4
- rebuild

* Tue Jun 24 2003 Joe Orton <jorton@redhat.com> 0.24.2-3
- rebuild

* Tue Jun 24 2003 Joe Orton <jorton@redhat.com> 0.24.2-2
- don't use any LDFLAGS when building swig, fix for libdir=lib64

* Tue Jun 24 2003 Joe Orton <jorton@redhat.com> 0.24.2-1
- update to 0.24.2; fix Python bindings

* Tue Jun 17 2003 Joe Orton <jorton@redhat.com> 0.24.1-1
- update to 0.24.1; include mod_authz_svn
- force use of CC=gcc CXX=g++

* Mon Jun  9 2003 Joe Orton <jorton@redhat.com> 0.23.0-2
- add cvs2svn man page

* Mon Jun  9 2003 Joe Orton <jorton@redhat.com> 0.23.0-1
- update to 0.23.0

* Sun Jun  8 2003 Joe Orton <jorton@redhat.com> 0.22.2-7
- package cvs2svn to be usable outside docdir
- remove unnecessary files

* Thu Jun  5 2003 Joe Orton <jorton@redhat.com> 0.22.2-6
- add fix for unhandled deadlock errors in libsvn_fs
- don't package the out-of-date info pages

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> 0.22.2-5
- rebuilt

* Tue Jun  3 2003 Joe Orton <jorton@redhat.com> 0.22.2-4
- cleanups

* Mon Jun  2 2003 Elliot Lee <sopwith@redhat.com> 0.22.2-3
- Add back in s390x, excludearch bad.

* Tue May 20 2003 Jeff Johnson <jbj@redhat.com> 0.22.2-2
- use external neon-0.23.9-2 (i.e. with neon-config), drop internal neon.
- use db-4.1.25, not db-4.0.14.
- do "make check" (but ignore failure for now).
- s390x knows not of httpd >= 2.0.45.

* Thu May  8 2003 Joe Orton <jorton@redhat.com> 0.22.2-1
- update to 0.22.2; add mod_dav_svn subpackage
- include Python bindings
- neon: force use of expat, enable SSL
- drop check for specific apr version added in -3

* Thu May  1 2003 Joe Orton <jorton@redhat.com> 0.20.1-6
- filter out perl(Config::IniFiles) requirement

* Thu May  1 2003 Joe Orton <jorton@redhat.com> 0.20.1-5
- fail early if apr-config is not 0.9.3

* Wed Apr 30 2003 Joe Orton <jorton@redhat.com> 0.20.1-4
- fix workaround for non-lib64 platforms

* Wed Apr 30 2003 Joe Orton <jorton@redhat.com> 0.20.1-3
- add workaround for libtool problem

* Tue Apr 29 2003 Joe Orton <jorton@redhat.com> 0.20.1-2
- require and use system apr, apr-util libraries
- use License not Copyright

* Fri Apr 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 0.20.1

* Wed Jan 22 2003 Jeff Johnson <jbj@redhat.com> 0.17.1-4503.0
- upgrade to 0.17.1.

* Wed Dec 11 2002 Jeff Johnson <jbj@redhat.com> 0.16-3987.1
- upgrade to 0.16.

* Wed Nov 13 2002 Jeff Johnson <jbj@redhat.com> 0.15-3687.2
- don't mess with the info handbook install yet.

* Sun Nov 10 2002 Jeff Johnson <jbj@redhat.com> 0.15-3687.1
- use libdir, build on x86_64 too.
- avoid "perl(Config::IniFiles) >= 2.27" dependency.

* Sat Nov  9 2002 Jeff Johnson <jbj@redhat.com> 0.15-3687.0
- first build from adapted spec file, only client and libraries for now.
- internal apr/apr-utils/neon until incompatibilities sort themselves out.
- avoid libdir issues on x86_64 for the moment.
