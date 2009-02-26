%define	with_python_subpackage	1%{nil}
%define	with_python_version	2.3%{nil}
%define	with_bzip2		1%{nil}
%define	with_apidocs		1%{nil}

# XXX legacy requires './' payload prefix to be omitted from rpm packages.
%define	_noPayloadPrefix	1

%define	__prefix	%{?_prefix}%{!?_prefix:/usr}
%{?!_lib: %define _lib lib}
%{expand: %%define __share %(if [ -d %{__prefix}/share/man ]; then echo /share ; else echo %%{nil} ; fi)}

%define __bindir	%{__prefix}/bin
%define __includedir	%{__prefix}/include
%define __libdir	%{__prefix}/%{_lib}
%define __mandir	%{__prefix}%{__share}/man

Summary: The RPM package management system.
Name: rpm
%define version 4.4.2
Version: %{version}
%{expand: %%define rpm_version %{version}}
Release: 48%{?dist}
Group: System Environment/Base
Source0: rpm-%{rpm_version}.tar.gz
Source1: mono-find-provides
Source2: mono-find-requires
Patch0: rpm-4.4.1-hkp-disable.patch
Patch1: rpm-4.4.1-fileconflicts.patch 
Patch2: rpm-4.4.1-prereq.patch
Patch3: rpm-4.4.1-nonmerged.patch
Patch4: rpm-4.4.1-prepostun.patch
Patch5: rpm-4.4.1-ordererase.patch
Patch6: rpm-4.4.2-matchpathcon.patch
Patch7: rpm-4.4.2-perlreq.patch
Patch8: rpm-4.4.2-db3-param.patch
Patch9: rpm-4.4.2-contextverify.patch
Patch10: rpm-4.4.2-popt-charset.patch
Patch11: rpm-4.4.2-ghost-conflicts.patch
Patch12: rpm-4.4.2-exclude.patch
Patch13: rpm-4.4.2-excluded-size.patch
Patch14: rpm-4.4.2-cronpath.patch
Patch15: rpm-4.4.2-mono.patch
Patch16: rpm-4.4.2-file-softmagic.patch
Patch17: rpm-4.4.2-no-large-mmap.patch
Patch18: rpm-4.4.2-perlmainprov.patch
Patch19: rpm-4.4.2-rpmsq-deadlock.patch
Patch20: rpm-4.4.2-netsharedpath.patch
Patch21: rpm-4.4.2-userlock.patch
Patch22: rpm-4.4.2-vercmp.patch
Patch23: rpm-4.4.2-doxy.patch
Patch24: rpm-4.4.2-trust.patch
Patch25: rpm-4.4.2-devel-autodep.patch
Patch26: rpm-4.4.2-rpmfc-skip.patch
Patch27: rpm-4.4.2-noselinux-verify.patch
Patch28: rpm-4.4.2-python-aslist.patch
Patch29: rpm-4.4.2-rpmio-ipv6.patch
Patch30: rpm-4.4.2-gnuhash.patch
Patch31: rpm-4.4.2-debugedit-ppc-reloc.patch
Patch32: rpm-4.4.2-debugpaths.patch
Patch33: rpm-4.4.2-transaction-order.patch
Patch34: rpm-4.4.2-debugopt.patch
Patch35: rpm-4.4.2-query-flushbuffer.patch
Patch36: rpm-4.4.2-noneon.patch
Patch37: rpm-4.4.2-replaced-state.patch
Patch38: rpm-4.4.2-multiple-installs.patch
Patch39: rpm-4.4.2-order-multilib.patch
Patch40: rpm-4.4.2-prereqs-typo.patch
Patch41: rpm-4.4.2-ia32e-install.patch
Patch42: rpm-4.4.2-ldconfig.patch
Patch43: rpm-4.4.2-double-error.patch
Patch44: rpm-4.4.2-scriptnames.patch
License: GPL
Conflicts: patch < 2.5
%ifos linux
Prereq: fileutils shadow-utils
%endif
Requires: popt = 1.10.2
Obsoletes: rpm-perl < %{version}

BuildRequires: autoconf
BuildRequires: elfutils-devel 
#>= 0.112

BuildRequires: sed readline-devel zlib-devel

BuildRequires: beecrypt-devel 
#>= 4.1.2
Requires: beecrypt 
#>= 4.1.2

BuildConflicts: neon-devel
BuildRequires: sqlite-devel
BuildRequires: gettext-devel
BuildRequires: libselinux-devel
#XXX: lua fix this
BuildRequires: ncurses-devel

# XXX Red Hat 5.2 has not bzip2 or python
%if %{with_bzip2}
BuildRequires: bzip2-devel >= 0.9.0c-2
%endif
%if %{with_python_subpackage}
BuildRequires: python-devel >= %{with_python_version}
%endif

BuildRoot: %{_tmppath}/%{name}-root

%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages. Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%package libs
Summary:  Libraries for manipulating RPM packages.
Group: Development/Libraries
Requires: rpm = %{rpm_version}-%{release}

%description libs
This package contains the RPM shared libraries.

%package devel
Summary:  Development files for manipulating RPM packages.
Group: Development/Libraries
Requires: rpm = %{rpm_version}-%{release}
Requires: beecrypt 
#>= 4.1.2
Requires: sqlite-devel
Requires: libselinux-devel
Requires: elfutils-libelf-devel

%description devel
This package contains the RPM C library and header files. These
development files will simplify the process of writing programs that
manipulate RPM packages and databases. These files are intended to
simplify the process of creating graphical package managers or any
other tools that need an intimate knowledge of RPM packages in order
to function.

This package should be installed if you want to develop programs that
will manipulate RPM packages and databases.

%package build
Summary: Scripts and executable programs used to build packages.
Group: Development/Tools
Requires: rpm = %{rpm_version}-%{release}, patch >= 2.5, file, elfutils
Provides: rpmbuild(VendorConfig) = 4.1-1

%description build
The rpm-build package contains the scripts and executable programs
that are used to build packages using the RPM Package Manager.

%if %{with_python_subpackage}
%package python
Summary: Python bindings for apps which will manipulate RPM packages.
Group: Development/Libraries
Requires: rpm = %{rpm_version}-%{release}
Requires: python >= %{with_python_version}

%description python
The rpm-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python
programs that will manipulate RPM packages and databases.
%endif

%package -n popt
Summary: A C library for parsing command line parameters.
Group: Development/Libraries
Version: 1.10.2

%description -n popt
Popt is a C library for parsing command line parameters. Popt was
heavily influenced by the getopt() and getopt_long() functions, but it
improves on them by allowing more powerful argument expansion. Popt
can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments. Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

%prep
%setup -q
%patch0 -p1  -b .nohkp
%patch1 -p1  -b .fileconflicts
%patch2 -p1  -b .prereq
%patch3 -p1  -b .rpmal
%patch4 -p1  -b .prepostun
%patch5 -p1  -b .ordererase
# patch 6 moved
%patch7 -p1  -b .perlreq
%patch8 -p1  -b .param
%patch10 -p1  -b .charset
%patch11 -p1  -b .ghostconflicts
#patch12 -p1  -b .exclude
%patch13 -p1  -b .excludedsize
%patch14 -p1  -b .cronpath
%patch15 -p1  -b .mono
%patch16 -p1 -b .magic
%patch17 -p1 -b .no_large_mmap
%patch18 -p1 -b .perlmainprov
%patch19 -p1 -b .deadlock
%patch20 -p1 -b .netsharedpath
%patch21 -p1 -b .userlock
%patch22 -p1 -b .vercmp
%patch23 -p1 -b .doxy
%patch24 -p1 -b .trust
%patch25 -p1 -b .develdeps
%patch26 -p1 -b .fcskip
%patch27 -p0 -b .nosever
%patch6 -p1  -b .matchpathcon
%patch28 -p1 -b .aslist
%patch29 -p1 -b .ipv6
%patch30 -p1 -b .gnuhash
%patch31 -p0 -b .dbgppc
%patch32 -p1 -b .dbgpaths
%patch33 -p1 -b .order
%patch34 -p1 -b .dbgopt
%patch35 -p1 -b .flush
%patch36 -p1 -b .noneon
%patch37 -p1 -b .replaced
%patch38 -p1 -b .multinst
%patch39 -p1 -b .ordermulti
%patch40 -p1 -b .prereqfix
%patch41 -p1 -b .ia32e
%patch42 -p1 -b .ldconfig
%patch43 -p1 -b .double-error
%patch44 -p1 -b .scriptnames

# rebuild configure for ipv6
autoconf

%build

# XXX rpm needs functioning nptl for configure tests
unset LD_ASSUME_KERNEL || :

%if %{with_python_subpackage}
WITH_PYTHON="--with-python=%{with_python_version}"
%else
WITH_PYTHON="--without-python"
%endif

%ifos linux
CFLAGS="$RPM_OPT_FLAGS"; export CFLAGS
./configure --prefix=%{__prefix} --sysconfdir=/etc \
	--localstatedir=/var --infodir='${prefix}%{__share}/info' \
	--mandir='${prefix}%{__share}/man' \
	$WITH_PYTHON --enable-posixmutexes --without-javaglue
%else
export CPPFLAGS=-I%{__prefix}/include 
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{__prefix} $WITH_PYTHON \
	--without-javaglue
%endif

make -C zlib || :

make %{?_smp_mflags}

%install
# XXX rpm needs functioning nptl for configure tests
unset LD_ASSUME_KERNEL || :

rm -rf $RPM_BUILD_ROOT

make DESTDIR="$RPM_BUILD_ROOT" install

# Working around breakage from the -L$(RPM_BUILD_ROOT)... -L$(DESTDIR)...
# workaround to #132435,
# and from linking to included zlib
for i in librpm.la librpmbuild.la librpmdb.la librpmio.la ; do
	sed -i -e 's~-L'"$RPM_BUILD_ROOT"'[^ ]* ~~g' \
		-e 's~-L'"$RPM_BUILD_DIR"'[^ ]* ~~g' \
		"$RPM_BUILD_ROOT%{__libdir}/$i"
done

# Clean up dangling symlinks
# XXX Fix in rpm tree
for i in /usr/bin/rpme /usr/bin/rpmi /usr/bin/rpmu; do
    rm -f "$RPM_BUILD_ROOT"/"$i" 
done

# Clean up dangling symlinks
for i in /usr/lib/rpmpopt /usr/lib/rpmrc; do
    rm -f "$RPM_BUILD_ROOT"/"$i" 
done

%ifos linux

# Save list of packages through cron
mkdir -p ${RPM_BUILD_ROOT}/etc/cron.daily
install -m 755 scripts/rpm.daily ${RPM_BUILD_ROOT}/etc/cron.daily/rpm

mkdir -p ${RPM_BUILD_ROOT}/etc/logrotate.d
install -m 644 scripts/rpm.log ${RPM_BUILD_ROOT}/etc/logrotate.d/rpm

mkdir -p $RPM_BUILD_ROOT/etc/rpm

mkdir -p $RPM_BUILD_ROOT/var/spool/repackage
mkdir -p $RPM_BUILD_ROOT/var/lib/rpm
for dbi in \
	Basenames Conflictname Dirnames Group Installtid Name Packages \
	Providename Provideversion Requirename Requireversion Triggername \
	Filemd5s Pubkeys Sha1header Sigmd5 \
	__db.001 __db.002 __db.003 __db.004 __db.005 __db.006 __db.007 \
	__db.008 __db.009
do
    touch $RPM_BUILD_ROOT/var/lib/rpm/$dbi
done

%endif

%if %{with_apidocs}
gzip -9n apidocs/man/man*/* || :
%endif

# Get rid of unpackaged files
{ cd $RPM_BUILD_ROOT
  rm -f .%{_libdir}/lib*.la
  rm -f .%{__prefix}/lib/rpm/{Specfile.pm,cpanflute,cpanflute2,rpmdiff,rpmdiff.cgi,sql.prov,sql.req,tcl.req}
  rm -rf .%{__mandir}/{fr,ko}
%if %{with_python_subpackage}
  rm -f .%{__libdir}/python%{with_python_version}/site-packages/*.{a,la}
  rm -f .%{__libdir}/python%{with_python_version}/site-packages/rpm/*.{a,la}
  rm -f .%{__libdir}/python%{with_python_version}/site-packages/rpmdb/*.{a,la}
%endif
}

# Install mono find-provides/requires
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/usr/lib/rpm
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/usr/lib/rpm

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%ifos linux
if [ -f /var/lib/rpm/packages.rpm ]; then
    echo "
You have (unsupported)
	/var/lib/rpm/packages.rpm	db1 format installed package headers
Please install rpm-4.0.4 first, and do
	rpm --rebuilddb
to convert your database from db1 to db3 format.
"
    exit 1
fi
/usr/sbin/groupadd -g 37 rpm				> /dev/null 2>&1
/usr/sbin/useradd  -r -d /var/lib/rpm -u 37 -g 37 rpm -s /sbin/nologin	> /dev/null 2>&1
%endif
exit 0

%post
%ifos linux

# Establish correct rpmdb ownership.
/bin/chown rpm.rpm /var/lib/rpm/[A-Z]*

# XXX Detect (and remove) incompatible dbenv files during db-4.3.14 upgrade.
# XXX Removing dbenv files in %%post opens a lock race window, a tolerable
# XXX risk compared to the support issues involved with upgrading Berkeley DB.
[ -w /var/lib/rpm/__db.001 ] &&
/usr/lib/rpm/rpmdb_stat -CA -h /var/lib/rpm 2>&1 |
grep "db_stat: Program version 4.3 doesn't match environment version" 2>&1 > /dev/null &&
	rm -f /var/lib/rpm/__db*
                                                                                
%endif
exit 0

%ifos linux
%postun
if [ $1 = 0 ]; then
    /usr/sbin/userdel rpm
    /usr/sbin/groupdel rpm
fi
exit 0

%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post -n popt -p /sbin/ldconfig
%postun -n popt -p /sbin/ldconfig
%endif

%if %{with_python_subpackage}
%post python -p /sbin/ldconfig
%postun python -p /sbin/ldconfig
%endif

%define	rpmattr		%attr(0755, rpm, rpm)

%files
%defattr(-,root,root)
%doc RPM-PGP-KEY RPM-GPG-KEY BETA-GPG-KEY CHANGES GROUPS doc/manual/[a-z]*
# XXX comment these lines out if building with rpm that knows not %pubkey attr
%pubkey RPM-PGP-KEY
%pubkey RPM-GPG-KEY
%pubkey BETA-GPG-KEY
%attr(0755, rpm, rpm)	/bin/rpm

%ifos linux
%config(noreplace,missingok)	/etc/cron.daily/rpm
%config(noreplace,missingok)	/etc/logrotate.d/rpm
%dir				/etc/rpm
#%config(noreplace,missingok)	/etc/rpm/macros.*
%attr(0755, rpm, rpm)	%dir /var/lib/rpm
%attr(0755, rpm, rpm)	%dir /var/spool/repackage

%define	rpmdbattr %attr(0644, rpm, rpm) %verify(not md5 size mtime) %ghost %config(missingok,noreplace)
%rpmdbattr	/var/lib/rpm/*
%endif

%rpmattr	%{__bindir}/rpm2cpio
%rpmattr	%{__bindir}/gendiff
%rpmattr	%{__bindir}/rpmdb
#%rpmattr	%{__bindir}/rpm[eiu]
%rpmattr	%{__bindir}/rpmsign
%rpmattr	%{__bindir}/rpmquery
%rpmattr	%{__bindir}/rpmverify

%attr(0755, rpm, rpm)	%dir %{__prefix}/lib/rpm
%rpmattr	%{__prefix}/lib/rpm/config.guess
%rpmattr	%{__prefix}/lib/rpm/config.sub
%rpmattr	%{__prefix}/lib/rpm/convertrpmrc.sh
%rpmattr	%{__prefix}/lib/rpm/freshen.sh
%attr(0644, rpm, rpm)	%{__prefix}/lib/rpm/macros
%rpmattr	%{__prefix}/lib/rpm/mkinstalldirs
%rpmattr	%{__prefix}/lib/rpm/rpm.*
%rpmattr	%{__prefix}/lib/rpm/rpm2cpio.sh
%rpmattr	%{__prefix}/lib/rpm/rpm[deiukqv]
%rpmattr	%{__prefix}/lib/rpm/tgpg
%attr(0644, rpm, rpm)	%{__prefix}/lib/rpm/rpmpopt*
%attr(0644, rpm, rpm)	%{__prefix}/lib/rpm/rpmrc

%ifarch i386 i486 i586 i686 athlon pentium3 pentium4
%attr(-, rpm, rpm)		%{__prefix}/lib/rpm/i[3456]86*
%attr(-, rpm, rpm)		%{__prefix}/lib/rpm/athlon*
%attr(-, rpm, rpm)		%{__prefix}/lib/rpm/pentium*
%endif
%ifarch alpha alphaev5 alphaev56 alphapca56 alphaev6 alphaev67
%attr(-, rpm, rpm)		%{__prefix}/lib/rpm/alpha*
%endif
%ifarch sparc sparcv8 sparcv9 sparc64
%attr(-, rpm, rpm)		%{__prefix}/lib/rpm/sparc*
%endif
%ifarch ia64
%attr(-, rpm, rpm)		%{__prefix}/lib/rpm/ia64*
%endif
%ifarch powerpc ppc ppciseries ppcpseries ppcmac ppc64
%attr(-, rpm, rpm)		%{__prefix}/lib/rpm/ppc*
%endif
%ifarch s390 s390x
%attr(-, rpm, rpm)		%{__prefix}/lib/rpm/s390*
%endif
%ifarch armv3l armv4l
%attr(-, rpm, rpm)		%{__prefix}/lib/rpm/armv[34][lb]*
%endif
%ifarch mips mipsel
%attr(-, rpm, rpm)		%{__prefix}/lib/rpm/mips*
%endif
%ifarch x86_64
%attr(-, rpm, rpm)		%{__prefix}/lib/rpm/x86_64*
%attr(-, rpm, rpm)		%{__prefix}/lib/rpm/amd64*
%attr(-, rpm, rpm)		%{__prefix}/lib/rpm/ia32e*
%endif
%attr(-, rpm, rpm)		%{__prefix}/lib/rpm/noarch*

%rpmattr	%{__prefix}/lib/rpm/rpmdb_*
%rpmattr	%{__prefix}/lib/rpm/rpmfile

%lang(cs)	%{__prefix}/*/locale/cs/LC_MESSAGES/rpm.mo
%lang(da)	%{__prefix}/*/locale/da/LC_MESSAGES/rpm.mo
%lang(de)	%{__prefix}/*/locale/de/LC_MESSAGES/rpm.mo
%lang(fi)	%{__prefix}/*/locale/fi/LC_MESSAGES/rpm.mo
%lang(fr)	%{__prefix}/*/locale/fr/LC_MESSAGES/rpm.mo
%lang(gl)	%{__prefix}/*/locale/gl/LC_MESSAGES/rpm.mo
%lang(is)	%{__prefix}/*/locale/is/LC_MESSAGES/rpm.mo
%lang(ja)	%{__prefix}/*/locale/ja/LC_MESSAGES/rpm.mo
%lang(ko)	%{__prefix}/*/locale/ko/LC_MESSAGES/rpm.mo
%lang(no)	%{__prefix}/*/locale/no/LC_MESSAGES/rpm.mo
%lang(pl)	%{__prefix}/*/locale/pl/LC_MESSAGES/rpm.mo
%lang(pt)	%{__prefix}/*/locale/pt/LC_MESSAGES/rpm.mo
%lang(pt_BR)	%{__prefix}/*/locale/pt_BR/LC_MESSAGES/rpm.mo
%lang(ro)	%{__prefix}/*/locale/ro/LC_MESSAGES/rpm.mo
%lang(ru)	%{__prefix}/*/locale/ru/LC_MESSAGES/rpm.mo
%lang(sk)	%{__prefix}/*/locale/sk/LC_MESSAGES/rpm.mo
%lang(sl)	%{__prefix}/*/locale/sl/LC_MESSAGES/rpm.mo
%lang(sr)	%{__prefix}/*/locale/sr/LC_MESSAGES/rpm.mo
%lang(sv)	%{__prefix}/*/locale/sv/LC_MESSAGES/rpm.mo
%lang(tr)	%{__prefix}/*/locale/tr/LC_MESSAGES/rpm.mo

%{__mandir}/man1/gendiff.1*
%{__mandir}/man8/rpm.8*
%{__mandir}/man8/rpm2cpio.8*
%lang(ja)	%{__mandir}/ja/man[18]/*.[18]*
%lang(pl)	%{__mandir}/pl/man[18]/*.[18]*
%lang(ru)	%{__mandir}/ru/man[18]/*.[18]*
%lang(sk)	%{__mandir}/sk/man[18]/*.[18]*

%files libs
%defattr(-,root,root)
%{__libdir}/librpm-4.4.so
%{__libdir}/librpmdb-4.4.so
%{__libdir}/librpmio-4.4.so
%{__libdir}/librpmbuild-4.4.so

%files build
%defattr(-,root,root)
%dir %{__prefix}/src/redhat
%dir %{__prefix}/src/redhat/BUILD
%dir %{__prefix}/src/redhat/SPECS
%dir %{__prefix}/src/redhat/SOURCES
%dir %{__prefix}/src/redhat/SRPMS
%dir %{__prefix}/src/redhat/RPMS
%{__prefix}/src/redhat/RPMS/*
%rpmattr	%{__bindir}/rpmbuild
%rpmattr	%{__prefix}/lib/rpm/brp-*
%rpmattr	%{__prefix}/lib/rpm/check-files
%rpmattr	%{__prefix}/lib/rpm/check-prereqs
%rpmattr	%{__prefix}/lib/rpm/config.site
%rpmattr	%{__prefix}/lib/rpm/cross-build
%rpmattr	%{__prefix}/lib/rpm/debugedit
%rpmattr	%{__prefix}/lib/rpm/find-debuginfo.sh
%rpmattr	%{__prefix}/lib/rpm/find-lang.sh
%rpmattr	%{__prefix}/lib/rpm/find-prov.pl
%rpmattr	%{__prefix}/lib/rpm/find-provides
%rpmattr	%{__prefix}/lib/rpm/find-provides.perl
%rpmattr	%{__prefix}/lib/rpm/find-req.pl
%rpmattr	%{__prefix}/lib/rpm/find-requires
%rpmattr	%{__prefix}/lib/rpm/find-requires.perl
%rpmattr	%{__prefix}/lib/rpm/get_magic.pl
%rpmattr	%{__prefix}/lib/rpm/getpo.sh
%rpmattr	%{__prefix}/lib/rpm/http.req
%rpmattr	%{__prefix}/lib/rpm/javadeps
%rpmattr	%{__prefix}/lib/rpm/magic
%rpmattr	%{__prefix}/lib/rpm/magic.mgc
%rpmattr	%{__prefix}/lib/rpm/magic.mime
%rpmattr	%{__prefix}/lib/rpm/magic.mime.mgc
%rpmattr	%{__prefix}/lib/rpm/magic.prov
%rpmattr	%{__prefix}/lib/rpm/magic.req
%rpmattr	%{__prefix}/lib/rpm/mono-find-provides
%rpmattr	%{__prefix}/lib/rpm/mono-find-requires
%rpmattr	%{__prefix}/lib/rpm/perldeps.pl
%rpmattr	%{__prefix}/lib/rpm/perl.prov
%rpmattr	%{__prefix}/lib/rpm/perl.req
%rpmattr	%{__prefix}/lib/rpm/pythondeps.sh

%rpmattr	%{__prefix}/lib/rpm/rpm[bt]
%rpmattr	%{__prefix}/lib/rpm/rpmdeps
%rpmattr	%{__prefix}/lib/rpm/trpm
%rpmattr	%{__prefix}/lib/rpm/u_pkg.sh
%rpmattr	%{__prefix}/lib/rpm/vpkg-provides.sh
%rpmattr	%{__prefix}/lib/rpm/vpkg-provides2.sh

%{__mandir}/man8/rpmbuild.8*
%{__mandir}/man8/rpmdeps.8*

%if %{with_python_subpackage}
%files python
%defattr(-,root,root)
%{__libdir}/python%{with_python_version}/site-packages/rpm
%endif

%files devel
%defattr(-,root,root)
%if %{with_apidocs}
%doc apidocs
%endif
%{__includedir}/rpm
%{__libdir}/librpm.a
%{__libdir}/librpm.so
%{__libdir}/librpmdb.a
%{__libdir}/librpmdb.so
%{__libdir}/librpmio.a
%{__libdir}/librpmio.so
%{__libdir}/librpmbuild.a
%{__libdir}/librpmbuild.so
%{__mandir}/man8/rpmcache.8*
%{__mandir}/man8/rpmgraph.8*
%rpmattr	%{__prefix}/lib/rpm/rpmcache
%rpmattr	%{__bindir}/rpmgraph

%files -n popt
%defattr(-,root,root)
%{__libdir}/libpopt.so.*
%{__mandir}/man3/popt.3*
%lang(cs)	%{__prefix}/*/locale/cs/LC_MESSAGES/popt.mo
%lang(da)	%{__prefix}/*/locale/da/LC_MESSAGES/popt.mo
%lang(de)	%{__prefix}/*/locale/de/LC_MESSAGES/popt.mo
%lang(es)	%{__prefix}/*/locale/es/LC_MESSAGES/popt.mo
%lang(eu_ES)	%{__prefix}/*/locale/eu_ES/LC_MESSAGES/popt.mo
%lang(fi)	%{__prefix}/*/locale/fi/LC_MESSAGES/popt.mo
%lang(fr)	%{__prefix}/*/locale/fr/LC_MESSAGES/popt.mo
%lang(gl)	%{__prefix}/*/locale/gl/LC_MESSAGES/popt.mo
%lang(hu)	%{__prefix}/*/locale/hu/LC_MESSAGES/popt.mo
%lang(id)	%{__prefix}/*/locale/id/LC_MESSAGES/popt.mo
%lang(is)	%{__prefix}/*/locale/is/LC_MESSAGES/popt.mo
%lang(it)	%{__prefix}/*/locale/it/LC_MESSAGES/popt.mo
%lang(ja)	%{__prefix}/*/locale/ja/LC_MESSAGES/popt.mo
%lang(ko)	%{__prefix}/*/locale/ko/LC_MESSAGES/popt.mo
%lang(no)	%{__prefix}/*/locale/no/LC_MESSAGES/popt.mo
%lang(pl)	%{__prefix}/*/locale/pl/LC_MESSAGES/popt.mo
%lang(pt)	%{__prefix}/*/locale/pt/LC_MESSAGES/popt.mo
%lang(pt_BR)	%{__prefix}/*/locale/pt_BR/LC_MESSAGES/popt.mo
%lang(ro)	%{__prefix}/*/locale/ro/LC_MESSAGES/popt.mo
%lang(ru)	%{__prefix}/*/locale/ru/LC_MESSAGES/popt.mo
%lang(sk)	%{__prefix}/*/locale/sk/LC_MESSAGES/popt.mo
%lang(sl)	%{__prefix}/*/locale/sl/LC_MESSAGES/popt.mo
%lang(sr)	%{__prefix}/*/locale/sr/LC_MESSAGES/popt.mo
%lang(sv)	%{__prefix}/*/locale/sv/LC_MESSAGES/popt.mo
%lang(tr)	%{__prefix}/*/locale/tr/LC_MESSAGES/popt.mo
%lang(uk)	%{__prefix}/*/locale/uk/LC_MESSAGES/popt.mo
%lang(wa)	%{__prefix}/*/locale/wa/LC_MESSAGES/popt.mo
%lang(zh)	%{__prefix}/*/locale/zh/LC_MESSAGES/popt.mo
%lang(zh_CN)	%{__prefix}/*/locale/zh_CN/LC_MESSAGES/popt.mo
%lang(zh_TW)	%{__prefix}/*/locale/zh_TW/LC_MESSAGES/popt.mo

# XXX These may end up in popt-devel but it hardly seems worth the effort.
%{__libdir}/libpopt.a
%{__libdir}/libpopt.so
%{__includedir}/popt.h

%changelog
* Thu Sep 20 2007 Panu Matilainen <pmatilai@redhat.com> -  4.4.2-48
- Don't show errors twice on non-existent files (#215712)
- Update scriptlet names to match what's available (#248128)

* Fri Aug 24 2007 Panu Matilainen <pmatilai@redhat.com> -  4.4.2-47
- disable ldconfig optimizations (#253492)

* Mon Aug 20 2007 Panu Matilainen <pmatilai@redhat.com> -  4.4.2-46
- Rebuild due to apparent builroot temporary hickup to really fix #211119

* Mon Aug 06 2007 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-45
- Create x86_64 compat macros for ia32e and amd64 (#211119)

* Wed Jun 27 2007 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-44
- Fix typo in script 

* Wed Jun 27 2007 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-43
- Group multilb packages patch from jbj (#220348,#225074,#225077)

* Tue Jun 26 2007 Panu Matilainen <pmatilai@redhat.com> -  4.4.2-42
- actually apply the multiple installs patch (#213399)

* Tue Jun 26 2007 Panu Matilainen <pmatilai@redhat.com> -  4.4.2-41
- permit multiple versions of a package to be installed within a transaction
  with -i (#213399)

* Thu Jun 21 2007 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-40
- Update replaced state in transaction (#237478)

* Mon Jun 18 2007 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-39
- Preserve replaced state in transaction (#237478)

* Mon Jun 04 2007 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-38
- Update userlock patch for potential segfault (#231146)

* Thu Jan 04 2007 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-37
- Build without neon (#213055)

* Mon Nov 20 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-36
- Fix ordering issues (#214865)

* Tue Oct 31 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-35
- Flush query buffer patch from jbj (#212833)

* Tue Oct 31 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-34
- Debuginfo extraction with O0

* Wed Oct 25 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-33
- Fix for ordering (#202540, #202542, #202543, #202544)

* Thu Sep 07 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-32
- Various debuginfo fixes (#165434, #165418, #149113, #205339)

* Fri Jul 21 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-31
- Apply matchpathcon patch

* Wed Jul 19 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-30
- Fix debugedit for ppc relocations (#199473)

* Fri Jul 14 2006 David Cantrell <dcantrell@redhat.com> - 4.4.2-29
- Fixed null pointer problem in rpmfcELF() DT_GNU_HASH handling

* Tue Jul 11 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-28
- Detect and provide a requirement for DT_GNU_HASH 

* Wed Jul 05 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-27
- IPv4/6 and EPSV support by Arkadiusz Miskiewicz <misiek@pld.org.pl>

* Wed Jun 28 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-26
- Force CHANGELOGTIME to be a list in rpm-python

* Wed Jun 28 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-25
- Remove SELinux context verification (#193488)

* Thu May 04 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-24
- File classification with autoReq off (#190488)

* Thu May  4 2006 Jeremy Katz <katzj@redhat.com> - 4.4.2-23
- make rpm-libs requires on base package stronger

* Wed May  3 2006 Jeremy Katz <katzj@redhat.com> - 4.4.2-22
- put in simple workaround for per-file deps with autoreq off (#190488) 
  while pnasrat works on a real fix

* Fri Apr 28 2006 Jeremy Katz <katzj@redhat.com> - 4.4.2-21
- run ldconfig in -libs subpackage %%post, not main package
- add patch to generate shared lib deps by following symlinks so that 
  -devel packages sanely depend on main libs

* Thu Apr 27 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-20
- Update --trusted stubs for rpmk breakage

* Tue Apr 25 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-19
- Add --trusted stubs from upstream

* Wed Apr 12 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-18
- Resurrect doxygen (#187714)

* Tue Apr 11 2006 Jeremy Katz <katzj@redhat.com> - 4.4.2-17
- remove redundant elfutils-libelf buildrequires
- rpm-python doesn't require elfutils (related to #188495)

* Fri Mar 31 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-16
- Skipdirs on erase again (#187308)
- Make fcntl lock sensitive to --root (#151255)
- Fix netshared path comparison (#52725)
- Fix rpm vercmp (#178798)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.4.2-15.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.4.2-15.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-15
- Rebuild for newer neon
- Fix scriptlet deadlock (#146549)

* Wed Jan 18 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-14
- Don't emit perl(main) (#177960)

* Wed Jan 11 2006 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-13
- Don't mmap large files

* Mon Jan  9 2006 Alexander Larsson <alexl@redhat.com> - 4.4.2-12
- Add mono req/provides support

* Thu Dec 01 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-11
- Remove rpm .la files (#174261)
- Cron job use paths (#174211)

* Tue Nov 29 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-10
- Ignore excluded size (#89661)

* Tue Nov 29 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-9
- Don't skipDirs on erasures (#140055)

* Mon Nov 28 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-8
- Add elfutils Build Requires to rpmbuild (#155129)
- Don't do conflicts if both files %ghost(#155256)
- Fix popt charset for various languages (#172155)
- Don't include .la file (#174261)

* Tue Nov  8 2005 Tomas Mraz <tmraz@redhat.com> - 4.4.2-7
- rebuilt with new openssl

* Sun Oct 09 2005 Florian La Roche <laroche@redhat.com>
- rebuild for sqlite changes

* Thu Sep 22 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-5
- Actually fix context verification where matchpathcon fails (#162037)

* Fri Aug 26 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-4
- Fix build with CFLAGS having --param
- Fix for context verification in /tmp (#162037)

* Wed Jul 27 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-3
- popt minor version requires

* Tue Jul 26 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-2
- popt minor version bump
- revert to perl.req/perl.prov for now

* Thu Jul 21 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.2-1
- Upgrade to upstream release

* Tue May 24 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.1-21
- Update translations (#154623)

* Sat May 21 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.1-20
- Drop signature patch
- dangling unpackaged symlinks

* Tue May 17 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.1-19
- Check for symlinks in check-files (#108778)
- Move zh_CN (#154623)
- Test fix for signing old rpms (#127113)

* Wed May 04 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.1-18.1
- Fix typo
- Fix typo

* Wed May 04 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.1-18
- Add missing fsm.c from matchpathcon patches 

* Tue May 03 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.1-17
- Fix typo

* Tue May 03 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.1-16
- Yet more matchpathcon

* Tue May 03 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.1-15
- Some more matchpathcon work

* Mon May 02 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.1-14
- matchpathcon fixup

* Mon May 02 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.1-13
- Use matchpathcon (#151870)

* Sat Apr 30 2005 Miloslav Trmac <mitr@redhat.com> - 4.4.1-12
- Remove $RPM_BUILD_ROOT and $RPM_BUILD_DIR from distribued .la files (#116891)
- Don't ship static version of _rpmdb.so
- BuildRequires: readline-devel

* Wed Apr 27 2005 Paul Nasrat <pnasrat@redhat.com> - 4.4.1-11
- Fix for (pre,postun) (#155700)
- Erase ordering

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 4.4.1-10
- add patch to fix segfault with non-merged hdlists

* Thu Mar 31 2005 Thomas Woerner <twoerner@redhat.com> 4.4.1-9
- enabled prereqs again

* Mon Mar 21 2005 Paul Nasrat <pnasrat@redhat.com> 4.4.1-8
- Add devel requires libselinux-devel
- Fileconflicts as FC3 (#151609)

* Wed Mar  9 2005 Jeff Johnson <jbj@jbj.org> 4.4.1-7
- rebuild against renamed sqlite package (#149719).

* Mon Mar  7 2005 Jeremy Katz <katzj@redhat.com> - 4.4.1-6
- fix build with new glibc

* Mon Mar  7 2005 Jeremy Katz <katzj@redhat.com> - 4.4.1-5
- disable hkp by default

* Tue Mar  1 2005 Jeremy Katz <katzj@redhat.com> - 4.4.1-4
- fix build with gcc 4

* Mon Feb 28 2005 Jeremy Katz <katzj@redhat.com> - 4.4.1-3
- fix posttrans callback check being backwards (#149524)

* Sun Feb 13 2005 Jeff Johnson <jbj@jbj.org> 4.4.1-1
- don't classify files in /dev (#146623).
- don't build with sqlite3 if <sqlite3.h> is missing.

* Sat Feb 12 2005 Jeff Johnson <jbj@jbj.org> 4.4.1-0.24
- zlib: uniqify certain symbols to prevent name space pollution.
- macosx: include <sys/types.h> so that python sees the u_char typedef.
- macosx: change to --prefix=/usr rather than /opt/local.
- use waitpid rather than SIGCHLD reaper.
- rip out DB_PRIVATE revert if not NPTL, it's not the right thing to do.

* Fri Feb 11 2005 Jeff Johnson <jbj@jbj.org> 4.4.1-0.22
- permit build scriptlet interpreters to be individually overridden.

* Thu Feb 10 2005 Jeff Johnson <jbj@jbj.org> 4.4.1-0.20
- perform callbacks as always (#147537).

* Wed Feb  2 2005 Jeff Johnson <jbj@jbj.org> 4.4.1-0.16
- fix: length of gpg V4 hash seed was incorrect (#146896).
- add support for V4 rfc-2440 signatures.

* Mon Jan 31 2005 Jeff Johnson <jbj@jbj.org> 4.4.1-0.14
- add sqlite internal (build still expects external sqlite3-3.0.8).
- sqlite: revert to original narrow scoping of cOpen/cClose.

* Fri Jan 28 2005 Jeff Johnson <jbj@jbj.org> 4.4.1-0.12
- python: force dbMatch() h# key to be 32 bit integer (#146477).

* Tue Jan 25 2005 Jeff Johnson <jbj@jbj.org> 4.4.1-0.10
- more macosx fiddles.
- move global /var/lock/rpm/transaction to dbpath.
- permit fcntl path to be configured through rpmlock_path macro.
- add missing #if defined(ENABLE_NLS) (#146184).

* Mon Jan 17 2005 Jeff Johnson <jbj@jbj.org> 4.4.1-0.8
- changes to build on Mac OS X using darwinports neon/beecrypt.
- add https://svn.uhulinux.hu/packages/dev/zlib/patches/02-rsync.patch

* Sun Jan  9 2005 Jeff Johnson <jbj@jbj.org> 4.4.1-0.7
- build against external/internal neon.

* Tue Jan  4 2005 Jeff Johnson <jbj@jbj.org> 4.4.1-0.6
- mac os x patches (#131943,#131944,#132924,#132926).
- mac os x patches (#133611, #133612, #134637).

* Sun Jan  2 2005 Jeff Johnson <jbj@jbj.org> 4.4.1-0.5
- upgrade to db-4.3.27.
- revert MAGIC_COMPRESS, real fix is in libmagic (#143782).
- upgrade to file-4.12 internal.

* Tue Dec  7 2004 Jeff Johnson <jbj@jbj.org> 4.4.1-0.3
- use package color as Obsoletes: color.

* Mon Dec  6 2004 Jeff Johnson <jbj@jbj.org> 4.4.1-0.2
- automagically detect and emit "python(abi) = 2.4" dependencies.
- popt 1.10.1 to preserve newer.

* Sun Dec  5 2004 Jeff Johnson <jbj@jbj.org> 4.4.1-0.1
- force *.py->*.pyo byte code compilation with brp-python-bytecompile.
