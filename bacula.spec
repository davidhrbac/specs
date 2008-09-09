# Bacula RPM spec file
# Copyright (C) 2000-2006 Kern Sibbald

# Platform Build Configuration

# basic defines for every build
%define _version 2.4.2
%define _release 2
%define depkgs_version 22Feb08
%define _rescuever 2.4.2
%define docs_version 2.4.2

# any patches for this release
# be sure to check the setup section for patch macros

#--------------------------------------------------------------------------
# it should not be necessary to change anything below here for a release
# except for patch macros in the setup section
#--------------------------------------------------------------------------

# third party packagers
%define _packager D. Scott Barninger <barninger@fairfieldcomputers.com>
%{?contrib_packager:%define _packager %{contrib_packager}}

Summary: Bacula - The Network Backup Solution
Name: bacula
Version: %{_version}
Release: %{_release}{?dist}
Group: System Environment/Daemons
License: GPL v2
Source0: http://www.prdownloads.sourceforge.net/bacula/%{name}-%{version}.tar.gz
Source1: http://www.prdownloads.sourceforge.net/bacula/depkgs-%{depkgs_version}.tar.gz
#Source2: Release_Notes-%{version}-%{release}.tar.gz
Source2: http://www.prdownloads.sourceforge.net/bacula/%{name}-docs-%{docs_version}.tar.gz
Source3: http://www.prdownloads.sourceforge.net/bacula/%{name}-rescue-%{_rescuever}.tar.gz
Source4: bacula-2.2.7-postgresql.patch
BuildRoot: %{_tmppath}/%{name}-root
URL: http://www.bacula.org/
Vendor: The Bacula Team
Packager: %{_packager}

# define the basic package description
%define blurb Bacula - It comes by night and sucks the vital essence from your computers.
%define blurb2 Bacula is a set of computer programs that permit you (or the system
%define blurb3 administrator) to manage backup, recovery, and verification of computer
%define blurb4 data across a network of computers of different kinds. In technical terms,
%define blurb5 it is a network client/server based backup program. Bacula is relatively
%define blurb6 easy to use and efficient, while offering many advanced storage management
%define blurb7 features that make it easy to find and recover lost or damaged files.
%define blurb8 Bacula source code has been released under the GPL version 2 license.

# directory locations
%define sqlite_bindir %_libdir/bacula/sqlite
%define _docsrc ../%{name}-docs-%{docs_version}
%define _rescuesrc ../%{name}-rescue-%{_rescuever}
%define depkgs ../depkgs
%define _mandir /usr/share/man

# directory locations for FHS-compatibility
%define sysconf_dir /etc/bacula
%define script_dir %_libdir/bacula
%define working_dir /var/lib/bacula
%define pid_dir /var/run

# NOTE these defines are used in some rather complex useradd and groupadd
# commands. If you change them examine the post scripts for consequences.
%define director_daemon_user bacula
%define storage_daemon_user bacula
%define file_daemon_user root
%define daemon_group bacula
# group that has write access to tape devices, usually disk on Linux
%define storage_daemon_group disk
%define user_file /etc/passwd
%define group_file /etc/group

# program locations
%define useradd /usr/sbin/useradd
%define groupadd /usr/sbin/groupadd
%define usermod /usr/sbin/usermod

# platform defines - set one below or define the build_xxx on the command line
# RedHat builds
%define rh7 0
%{?build_rh7:%define rh7 1}
%define rh8 0
%{?build_rh8:%define rh8 1}
%define rh9 0
%{?build_rh9:%define rh9 1}
# Fedora Core build
%define fc1 0
%{?build_fc1:%define fc1 1}
%define fc3 0
%{?build_fc3:%define fc3 1}
%define fc4 0
%{?build_fc4:%define fc4 1}
%define fc5 0
%{?build_fc5:%define fc5 1}
%define fc6 0
%{?build_fc6:%define fc6 1}
%define fc7 0
%{?build_fc7:%define fc7 1}
%define fc8 0
%{?build_fc8:%define fc8 1}
%define fc9 0
%{?build_fc9:%define fc9 1}
# Whitebox Enterprise build
%define wb3 0
%{?build_wb3:%define wb3 1}
# RedHat Enterprise builds
%define rhel3 0
%{?build_rhel3:%define rhel3 1}
%{?build_rhel3:%define wb3 1}
%define rhel4 0
%{?build_rhel4:%define rhel4 1}
%{?build_rhel4:%define fc3 1}
%define rhel5 0
%{?build_rhel5:%define rhel5 1}
%{?build_rhel5:%define fc6 1}
# CentOS build
%define centos3 0
%{?build_centos3:%define centos3 1}
%{?build_centos3:%define wb3 1}
%define centos4 0
%{?build_centos4:%define centos4 1}
%{?build_centos4:%define fc3 1}
%define centos5 0
%{?build_centos5:%define centos5 1}
%{?build_centos5:%define fc6 1}
# SL build
%define sl3 0
%{?build_sl3:%define sl3 1}
%{?build_sl3:%define wb3 1}
%define sl4 0
%{?build_sl4:%define sl4 1}
%{?build_sl4:%define fc3 1}
%define sl5 0
%{?build_sl5:%define sl5 1}
%{?build_sl5:%define fc6 1}
# SuSE build
%define su9 0
%{?build_su9:%define su9 1}
%define su10 0
%{?build_su10:%define su10 1}
%define su102 0
%{?build_su102:%define su102 1}
%define su103 0
%{?build_su103:%define su103 1}
%define su110 0
%{?build_su110:%define su110 1}
# Mandrake builds
%define mdk 0
%{?build_mdk:%define mdk 1}
%define mdv 0
%{?build_mdv:%define mdv 1}
%{?build_mdv:%define mdk 1}

# client only build
%define client_only 0
%{?build_client_only:%define client_only 1}

# test for a platform definition
%if !%{rh7} && !%{rh8} && !%{rh9} && !%{fc1} && !%{fc3} && !%{fc4} && !%{fc5} && !%{fc6} && !%{fc7} && !%{fc8} && !%{fc9} && !%{wb3} && !%{su9} && !%{su10} && !%{su102} && !%{su103} && !%{su110} && !%{mdk}
%{error: You must specify a platform. Please examine the spec file.}
exit 1
%endif

# database defines
# set for database support desired or define the build_xxx on the command line
%define mysql 0
%{?build_mysql:%define mysql 1}
# if using mysql 4.x define this and mysql above
# currently: Mandrake 10.1, SuSE 9.x & 10.0, RHEL4 and Fedora Core 4
%define mysql4 0
%{?build_mysql4:%define mysql4 1}
%{?build_mysql4:%define mysql 1}
# if using mysql 5.x define this and mysql above
# currently: SuSE 10.1 and Fedora Core 5
%define mysql5 0
%{?build_mysql5:%define mysql5 1}
%{?build_mysql5:%define mysql 1}
%define sqlite 0
%{?build_sqlite:%define sqlite 1}
%define postgresql 0
%{?build_postgresql:%define postgresql 1}

# test for a database definition
%if ! %{mysql} && ! %{sqlite} && ! %{postgresql} && ! %{client_only}
%{error: You must specify database support. Please examine the spec file.}
exit 1
%endif

%if %{mysql}
%define db_backend mysql
%endif
%if %{sqlite}
%define db_backend sqlite3
%endif
%if %{postgresql}
%define db_backend postgresql
%endif

# 64 bit support
%define x86_64 0
%{?build_x86_64:%define x86_64 1}

# check what distribution we are
%if %{rh7} || %{rh8} || %{rh9} || %{rhel3} || %{rhel4} || %{rhel5}
%define _dist %(grep Red /etc/redhat-release)
%endif
%if %{fc1} || %{fc4} || %{fc5} || %{fc7} || %{fc8} || %{fc9}
%define _dist %(grep Fedora /etc/redhat-release)
%endif
%if %{centos5} || %{centos4} || %{centos3}
%define _dist %(grep CentOS /etc/redhat-release)
%endif
%if %{sl5} ||%{sl4} || %{sl3}
%define _dist %(grep 'Scientific Linux' /etc/redhat-release)
%endif
%if %{fc3} && ! %{rhel4} && ! %{centos4} && ! %{sl4}
%define _dist %(grep Fedora /etc/redhat-release)
%endif
%if %{fc6} && ! %{rhel5} && ! %{centos5} && ! %{sl5}
%define _dist %(grep Fedora /etc/redhat-release)
%endif
%if %{wb3} && ! %{rhel3} && ! %{centos3} && ! %{sl3}
%define _dist %(grep White /etc/whitebox-release)
%endif
%if %{su9} || %{su10} || %{su102} || %{su103} || %{su110}
%define _dist %(grep -i SuSE /etc/SuSE-release)
%endif
%if %{mdk}
%define _dist %(grep Mand /etc/mandrake-release)
%endif
Distribution: %{_dist}

# Should we build gconsole, possible only if gtk= >= 2.4 available.
# leaving all the BuildRequires and Requires in place below for now.
# su10, fc3 and fc4 now nobuild, tray monitor fails to build as of 2.2.1 
# release as it needs 2.10

%define gconsole 1
%if %{rh7} || %{rh8} || %{rh9} || %{wb3} || %{fc1} || %{fc3} || %{fc4} || %{su9} || %{su10}
%define gconsole 0
%endif
%if %{mdk} && ! %{mdv}
%define gconsole 0
%endif

# specifically disallow gconsole if desired
%{?nobuild_gconsole:%define gconsole 0}

# Should we build wxconsole, only wxWidgets >=2.6 is supported
# SuSE 10 and FC4 and newer
%define wxconsole 0
%{?build_wxconsole:%define wxconsole 1}

# Should we build bat
# requires >= Qt-4.2
%define bat 0
%{?build_bat:%define bat 1}

# should we turn on python support
%define python 0
%{?build_python:%define python 1}

# specifically disallow build of mtx package if desired
%define mtx 1
%{?nobuild_mtx:%define mtx 0}

# do we need to patch for old postgresql version?
%define old_pgsql 0
%{?build_old_pgsql:%define old_pgsql 1}

# Mandriva somehow forces the manpage file extension to bz2 rather than gz
%if %{mdk}
%define manpage_ext bz2
%else
%define manpage_ext gz
%endif

# for client only build
%if %{client_only}
%define mysql 0
%define mysql4 0
%define mysql5 0
%define postgresql 0
%define sqlite 0
%define gconsole 0
%define wxconsole 0
%endif

%{expand: %%define gccver %(rpm -q --queryformat %%{version} gcc)}
%{expand: %%define gccrel %(rpm -q --queryformat %%{release} gcc)}

BuildRequires: gcc, gcc-c++, make, autoconf
BuildRequires: ncurses-devel, perl
BuildRequires: libstdc++-devel = %{gccver}-%{gccrel}, libxml2-devel, zlib-devel
BuildRequires: openssl-devel
%if %{python}
BuildRequires: python, python-devel
%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%endif
%if %{gconsole}
BuildRequires: pkgconfig, pango-devel, atk-devel
%endif

# Rh qt4 packages don't have a provide for, guess what, qt!
# still broken in fc8, ok in fc9
# so fix for broken rh
%define broken_rh 0
%if %{rhel5} || %{centos5} || %{sl5} || %{fc5} || %{fc6} || %{fc7} || %{fc8}
%define broken_rh 1
%endif
%if %{bat} && ! %{broken_rh}
BuildRequires: qt-devel >= 4.2
%endif
%if %{bat} && %{broken_rh}
BuildRequires: qt4-devel >= 4.2
%endif

%if %{rh7}
BuildRequires: libtermcap-devel
BuildRequires: glibc-devel >= 2.2
%endif
%if %{su9}
BuildRequires: termcap
BuildRequires: glibc-devel >= 2.3
%endif
%if %{su9} && %{gconsole}
BuildRequires: libgnome >= 2.0
BuildRequires: gtk2-devel >= 2.0
BuildRequires: libgnomeui-devel >= 2.0
BuildRequires: ORBit2-devel
BuildRequires: libart_lgpl-devel >= 2.0
BuildRequires: libbonobo-devel >= 2.0
BuildRequires: libbonoboui-devel >= 2.0
BuildRequires: bonobo-activation-devel
BuildRequires: gconf2-devel
BuildRequires: linc-devel
BuildRequires: freetype2-devel
%endif
%if %{su10}
BuildRequires: termcap
BuildRequires: glibc-devel >= 2.3
%endif
%if %{su10} && %{gconsole}
BuildRequires: libgnome >= 2.12
BuildRequires: gtk2-devel >= 2.8
BuildRequires: libgnomeui-devel >= 2.12
BuildRequires: ORBit2-devel
BuildRequires: libart_lgpl-devel >= 2.3
BuildRequires: libbonobo-devel >= 2.10
BuildRequires: libbonoboui-devel >= 2.10
BuildRequires: bonobo-activation-devel
BuildRequires: gconf2-devel
BuildRequires: freetype2-devel
BuildRequires: cairo-devel
BuildRequires: fontconfig-devel >= 2.3
BuildRequires: gnome-vfs2-devel >= 2.12
BuildRequires: libpng-devel
%endif
%if %{su102}
BuildRequires: termcap
BuildRequires: glibc-devel >= 2.5
%endif
%if %{su102} && %{gconsole}
BuildRequires: libgnome >= 2.16
BuildRequires: gtk2-devel >= 2.10
BuildRequires: libgnomeui-devel >= 2.16
BuildRequires: ORBit2-devel
BuildRequires: libart_lgpl-devel >= 2.3
BuildRequires: libbonobo-devel >= 2.16
BuildRequires: libbonoboui-devel >= 2.16
BuildRequires: bonobo-activation-devel
BuildRequires: gconf2-devel
BuildRequires: freetype2-devel
BuildRequires: cairo-devel
BuildRequires: fontconfig-devel >= 2.4
BuildRequires: gnome-vfs2-devel >= 2.16
BuildRequires: libpng-devel
%endif
%if %{su103}
BuildRequires: termcap
BuildRequires: glibc-devel >= 2.6
%endif
%if %{su103} && %{gconsole}
BuildRequires: libgnome >= 2.20
BuildRequires: gtk2-devel >= 2.12
BuildRequires: libgnomeui-devel >= 2.20
BuildRequires: ORBit2-devel
BuildRequires: libart_lgpl-devel >= 2.3
BuildRequires: libbonobo-devel >= 2.20
BuildRequires: libbonoboui-devel >= 2.20
BuildRequires: bonobo-activation-devel
BuildRequires: gconf2-devel
BuildRequires: freetype2-devel
BuildRequires: cairo-devel
BuildRequires: fontconfig-devel >= 2.4
BuildRequires: gnome-vfs2-devel >= 2.20
BuildRequires: libpng-devel
%endif
%if %{su110}
BuildRequires: termcap
BuildRequires: glibc-devel >= 2.8
%endif
%if %{su110} && %{gconsole}
BuildRequires: libgnome >= 2.22
BuildRequires: gtk2-devel >= 2.12
BuildRequires: libgnomeui-devel >= 2.22
BuildRequires: ORBit2-devel
BuildRequires: libart_lgpl-devel >= 2.3
BuildRequires: libbonobo-devel >= 2.22
BuildRequires: libbonoboui-devel >= 2.22
BuildRequires: bonobo-activation-devel
BuildRequires: gconf2-devel
BuildRequires: freetype2-devel
BuildRequires: cairo-devel
BuildRequires: fontconfig-devel >= 2.4
BuildRequires: gnome-vfs2-devel >= 2.22
BuildRequires: libpng-devel
%endif
%if %{mdk}
BuildRequires: libtermcap-devel
BuildRequires: libstdc++-static-devel
BuildRequires: glibc-static-devel
BuildRequires: glibc-devel >= 2.3
%endif
%if %{mdk} && !%{mdv} && %{gconsole}
BuildRequires: gtk2-devel >= 2.0
BuildRequires: libgnomeui2-devel >= 2.0
BuildRequires: libORBit2-devel
BuildRequires: libart_lgpl-devel >= 2.0
BuildRequires: libbonobo2_0-devel
BuildRequires: libbonoboui2_0-devel
BuildRequires: libbonobo-activation-devel
BuildRequires: libGConf2-devel
BuildRequires: freetype2-devel
%endif
%if %{mdv} && %{gconsole}
BuildRequires: gtk2-devel >= 2.8
BuildRequires: libgnomeui2-devel >= 2.10
BuildRequires: libORBit2-devel
BuildRequires: libart_lgpl-devel >= 2.3
BuildRequires: libbonobo2_0-devel
BuildRequires: libbonoboui2_0-devel
BuildRequires: libbonobo-activation-devel
BuildRequires: libGConf2-devel
BuildRequires: freetype2-devel
%endif
%if %{fc3}
BuildRequires: libtermcap-devel
BuildRequires: glibc-devel >= 2.3
%endif
%if %{fc3} && %{gconsole}
BuildRequires: gtk2-devel >= 2.4
BuildRequires: libgnomeui-devel >= 2.8
BuildRequires: ORBit2-devel
BuildRequires: libart_lgpl-devel >= 2.3
BuildRequires: libbonobo-devel >= 2.8
BuildRequires: libbonoboui-devel >= 2.8
BuildRequires: bonobo-activation-devel
BuildRequires: GConf2-devel
BuildRequires: freetype-devel
%endif
%if %{fc4}
BuildRequires: libtermcap-devel
BuildRequires: glibc-devel >= 2.3
%endif
%if %{fc4} && %{gconsole}
BuildRequires: gtk2-devel >= 2.6
BuildRequires: libgnomeui-devel >= 2.10
BuildRequires: ORBit2-devel
BuildRequires: libart_lgpl-devel >= 2.3
BuildRequires: libbonobo-devel >= 2.8
BuildRequires: libbonoboui-devel >= 2.8
BuildRequires: bonobo-activation-devel
BuildRequires: GConf2-devel
BuildRequires: freetype-devel
%endif
%if %{fc5}
BuildRequires: libtermcap-devel
BuildRequires: glibc-devel >= 2.4
%endif
%if %{fc5} && %{gconsole}
BuildRequires: gtk2-devel >= 2.8
BuildRequires: libgnomeui-devel >= 2.14
BuildRequires: ORBit2-devel
BuildRequires: libart_lgpl-devel >= 2.3
BuildRequires: libbonobo-devel >= 2.14
BuildRequires: libbonoboui-devel >= 2.14
BuildRequires: GConf2-devel
BuildRequires: freetype-devel
%endif
%if %{fc6}
BuildRequires: libtermcap-devel
BuildRequires: glibc-devel >= 2.5
%endif
%if %{fc6} && %{gconsole}
BuildRequires: gtk2-devel >= 2.10
BuildRequires: libgnomeui-devel >= 2.16
BuildRequires: ORBit2-devel
BuildRequires: libart_lgpl-devel >= 2.3
BuildRequires: libbonobo-devel >= 2.16
BuildRequires: libbonoboui-devel >= 2.16
BuildRequires: GConf2-devel
BuildRequires: freetype-devel
%endif
%if %{fc7}
BuildRequires: libtermcap-devel
BuildRequires: glibc-devel >= 2.5
%endif
%if %{fc7} && %{gconsole}
BuildRequires: gtk2-devel >= 2.10
BuildRequires: libgnomeui-devel >= 2.18
BuildRequires: ORBit2-devel
BuildRequires: libart_lgpl-devel >= 2.3
BuildRequires: libbonobo-devel >= 2.18
BuildRequires: libbonoboui-devel >= 2.18
BuildRequires: GConf2-devel
BuildRequires: freetype-devel
%endif
%if %{fc8}
BuildRequires: libtermcap-devel
BuildRequires: glibc-devel >= 2.7
%endif
%if %{fc8} && %{gconsole}
BuildRequires: gtk2-devel >= 2.12
BuildRequires: libgnomeui-devel >= 2.20
BuildRequires: ORBit2-devel
BuildRequires: libart_lgpl-devel >= 2.3
BuildRequires: libbonobo-devel >= 2.20
BuildRequires: libbonoboui-devel >= 2.20
BuildRequires: GConf2-devel
BuildRequires: freetype-devel
%endif
%if %{fc9}
BuildRequires: libtermcap-devel
BuildRequires: glibc-devel >= 2.8
BuildRequires: zlib-static
%endif
%if %{fc9} && %{gconsole}
BuildRequires: gtk2-devel >= 2.12
BuildRequires: libgnomeui-devel >= 2.22
BuildRequires: ORBit2-devel
BuildRequires: libart_lgpl-devel >= 2.3
BuildRequires: libbonobo-devel >= 2.22
BuildRequires: libbonoboui-devel >= 2.22
BuildRequires: GConf2-devel
BuildRequires: freetype-devel
%endif
%if !%{rh7} && !%{su9} && !%{su10} && !%{su102} && !%{su103} && !%{su110} && !%{mdk} && !%{fc3} && !%{fc4} && !%{fc5} && !%{fc6} && !%{fc7} && !%{fc8} && !%{fc9}
BuildRequires: libtermcap-devel
BuildRequires: glibc-devel >= 2.3
%endif
%if !%{rh7} && !%{su9} && !%{su10} && !%{su102} && !%{su103} && !%{su110} && !%{mdk} && !%{fc3} && !%{fc4} && !%{fc5} && !%{fc6} && !%{fc7} && !%{fc8} && !%{fc9} && %{gconsole}
BuildRequires: gtk2-devel >= 2.0
BuildRequires: libgnomeui-devel >= 2.0
BuildRequires: ORBit2-devel
BuildRequires: libart_lgpl-devel >= 2.0
BuildRequires: libbonobo-devel >= 2.0
BuildRequires: libbonoboui-devel >= 2.0
BuildRequires: bonobo-activation-devel
BuildRequires: GConf2-devel
BuildRequires: linc-devel
BuildRequires: freetype-devel
%endif

%if %{mysql} && ! %{mysql4} && ! %{mysql5}
BuildRequires: mysql-devel >= 3.23
%endif

%if %{mysql} && %{mysql4}
BuildRequires: mysql-devel >= 4.0
%endif

%if %{mysql} && %{mysql5}
BuildRequires: mysql-devel >= 5.0
%endif

%if %{postgresql} && %{wb3}
BuildRequires: rh-postgresql-devel >= 7
%endif

%if %{postgresql} && ! %{wb3}
BuildRequires: postgresql-devel >= 7
%endif

%if %{wxconsole}
BuildRequires: wxGTK-devel >= 2.6
%endif

%description
%{blurb}

%{blurb2}
%{blurb3}
%{blurb4}
%{blurb5}
%{blurb6}
%{blurb7}
%{blurb8}

%if %{mysql}
%package mysql
%endif
%if %{sqlite}
%package sqlite
%endif
%if %{postgresql}
%package postgresql
%endif

Summary: Bacula - The Network Backup Solution
Group: System Environment/Daemons
Provides: bacula-dir, bacula-sd, bacula-fd, bacula-server
Conflicts: bacula-client
Obsoletes: bacula-rescue

%if %{su9} || %{su10} || %{su102} || %{su103} || %{su110}
Conflicts: bacula
%endif

Requires: ncurses, libstdc++, zlib, openssl, mtx

%if %{rh7}
Requires: glibc >= 2.2
Requires: libtermcap
%endif
%if %{su9} || %{su10}
Requires: glibc >= 2.3
Requires: termcap
%endif
%if %{su102}
Requires: glibc >= 2.5
Requires: termcap
%endif
%if %{su103}
Requires: glibc >= 2.6
Requires: termcap
%endif
%if %{su110}
Requires: glibc >= 2.8
Requires: termcap
%endif
%if ! %{rh7} && ! %{su9} && ! %{su10} && ! %{su102} && ! %{su103} && ! %{su110} && ! %{fc5} && ! %{fc6} && ! %{fc7} && ! %{fc8} && ! %{fc9}
Requires: glibc >= 2.3
Requires: libtermcap
%endif
%if %{fc5}
Requires: glibc >= 2.4
Requires: libtermcap
%endif
%if %{fc6} || %{fc7}
Requires: glibc >= 2.5
Requires: libtermcap
%endif
%if %{fc8}
Requires: glibc >= 2.7
Requires: libtermcap
%endif
%if %{fc9}
Requires: glibc >= 2.8
Requires: libtermcap
%endif

%if %{mysql} && ! %{su9} && ! %{mdk} && ! %{mysql4} && ! %{mysql5}
Requires: mysql >= 3.23
Requires: mysql-server >= 3.23
%endif
%if %{mysql} && ! %{su9} && ! %{su10} && ! %{mdk} && %{mysql4}
Requires: mysql >= 4.0
Requires: mysql-server >= 4.0
%endif
%if %{mysql} && ! %{su9} && ! %{su10} && ! %{su102} && ! %{su103} && ! %{su110} && ! %{mdk} && %{mysql5}
Requires: mysql >= 5.0
Requires: mysql-server >= 5.0
%endif

%if %{mysql} && %{su9} && ! %{mysql4}
Requires: mysql >= 3.23
Requires: mysql-client >= 3.23
%endif
%if %{mysql} && %{su9} && %{mysql4}
Requires: mysql >= 4.0
Requires: mysql-client >= 4.0
%endif
%if %{mysql} && %{su10} && %{mysql4}
Requires: mysql >= 4.0
Requires: mysql-client >= 4.0
%endif
%if %{mysql} && %{su10} && %{mysql5}
Requires: mysql >= 5.0
Requires: mysql-client >= 5.0
%endif
%if %{mysql} && %{su102} && %{mysql5}
Requires: mysql >= 5.0
Requires: mysql-client >= 5.0
%endif
%if %{mysql} && %{su103} && %{mysql5}
Requires: mysql >= 5.0
Requires: mysql-client >= 5.0
%endif
%if %{mysql} && %{su110} && %{mysql5}
Requires: mysql >= 5.0
Requires: mysql-client >= 5.0
%endif

%if %{mysql} && %{mdk} && ! %{mysql4}
Requires: mysql >= 3.23
Requires: mysql-client >= 3.23
%endif
%if %{mysql} && %{mdk} && %{mysql4}
Requires: mysql >= 4.0
Requires: mysql-client >= 4.0
%endif

%if %{postgresql} && %{wb3}
Requires: rh-postgresql >= 7
Requires: rh-postgresql-server >= 7
%endif
%if %{postgresql} && ! %{wb3}
Requires: postgresql >= 7
Requires: postgresql-server >= 7
%endif

%if %{mysql}
%description mysql
%endif
%if %{sqlite}
%description sqlite
%endif
%if %{postgresql}
%description postgresql
%endif

%if %{python}
Requires: python >= %{pyver}
%endif

%{blurb}

%{blurb2}
%{blurb3}
%{blurb4}
%{blurb5}
%{blurb6}
%{blurb7}
%{blurb8}

%if %{mysql}
This build requires MySQL to be installed separately as the catalog database.
%endif
%if %{postgresql}
This build requires PostgreSQL to be installed separately as the catalog database.
%endif
%if %{sqlite}
This build incorporates sqlite3 as the catalog database, statically compiled.
%endif
%if %{python}
This build includes python scripting support.
%endif

%if ! %{client_only} && %{mtx}
%package mtx
Summary: Bacula - The Network Backup Solution
Group: System Environment/Daemons
Provides: mtx

%description mtx
This is Bacula's version of mtx tape utilities for Linux distributions that
do not provide their own mtx package
%endif

%package client
Summary: Bacula - The Network Backup Solution
Group: System Environment/Daemons
Provides: bacula-fd
Conflicts: bacula-mysql
Conflicts: bacula-sqlite
Conflicts: bacula-postgresql
Obsoletes: bacula-rescue

%if %{su9} || %{su10} || %{su102} || %{su103} || %{su110}
Provides: bacula
%endif

Requires: libstdc++, zlib, openssl

%if %{rh7}
Requires: glibc >= 2.2
Requires: libtermcap
%endif
%if %{su9} || %{su10}
Requires: glibc >= 2.3
Requires: termcap
%endif
%if %{su102}
Requires: glibc >= 2.5
Requires: termcap
%endif
%if %{su103}
Requires: glibc >= 2.6
Requires: termcap
%endif
%if %{su110}
Requires: glibc >= 2.8
Requires: termcap
%endif
%if ! %{rh7} && ! %{su9} && ! %{su10} && ! %{su102} && ! %{su103} && ! %{su110} && ! %{fc5} && ! %{fc6} && ! %{fc7} && ! %{fc8} && ! %{fc9}
Requires: glibc >= 2.3
Requires: libtermcap
%endif
%if %{fc5}
Requires: glibc >= 2.4
Requires: libtermcap
%endif
%if %{fc6} || %{fc7}
Requires: glibc >= 2.5
Requires: libtermcap
%endif
%if %{fc8}
Requires: glibc >= 2.7
Requires: libtermcap
%endif
%if %{fc9}
Requires: glibc >= 2.8
Requires: libtermcap
%endif

%if %{python}
Requires: python >= %{pyver}
%endif

%description client
%{blurb}

%{blurb2}
%{blurb3}
%{blurb4}
%{blurb5}
%{blurb6}
%{blurb7}
%{blurb8}

This is the File daemon (Client) only package. It includes the command line 
console program.
%if %{python}
This build includes python scripting support.
%endif

%if ! %{client_only}
%package updatedb

Summary: Bacula - The Network Backup Solution
Group: System Environment/Daemons

%description updatedb
%{blurb}

%{blurb2}
%{blurb3}
%{blurb4}
%{blurb5}
%{blurb6}
%{blurb7}
%{blurb8}

This package installs scripts for updating older versions of the bacula
database.
%endif

%if %{gconsole}
%package gconsole
Summary: Bacula - The Network Backup Solution
Group: System Environment/Daemons
Requires: atk, libstdc++, zlib, pango, libxml2, bacula-fd, openssl
%endif

%if %{gconsole} && %{su9}
Requires: gtk2 >= 2.0
Requires: libgnome >= 2.0
Requires: libgnomeui >= 2.0
Requires: glibc >= 2.3
Requires: ORBit2
Requires: libart_lgpl >= 2.0
Requires: libbonobo >= 2.0
Requires: libbonoboui >= 2.0
Requires: bonobo-activation
Requires: gconf2
Requires: linc
Requires: freetype2
%endif
%if %{gconsole} && %{su10}
Requires: gtk2 >= 2.8
Requires: libgnome >= 2.12
Requires: libgnomeui >= 2.12
Requires: glibc >= 2.3
Requires: ORBit2
Requires: libart_lgpl >= 2.3
Requires: libbonobo >= 2.10
Requires: libbonoboui >= 2.10
Requires: bonobo-activation
Requires: gconf2
Requires: freetype2
Requires: cairo
Requires: fontconfig >= 2.3
Requires: gnome-vfs2 >= 2.12
Requires: libpng
%endif
%if %{gconsole} && %{su102}
Requires: gtk2 >= 2.10
Requires: libgnome >= 2.16
Requires: libgnomeui >= 2.16
Requires: glibc >= 2.5
Requires: ORBit2
Requires: libart_lgpl >= 2.3
Requires: libbonobo >= 2.16
Requires: libbonoboui >= 2.16
Requires: bonobo-activation
Requires: gconf2
Requires: freetype2
Requires: cairo
Requires: fontconfig >= 2.4
Requires: gnome-vfs2 >= 2.16
Requires: libpng
%endif
%if %{gconsole} && %{su103}
Requires: gtk2 >= 2.12
Requires: libgnome >= 2.20
Requires: libgnomeui >= 2.20
Requires: glibc >= 2.6
Requires: ORBit2
Requires: libart_lgpl >= 2.3
Requires: libbonobo >= 2.20
Requires: libbonoboui >= 2.20
Requires: bonobo-activation
Requires: gconf2
Requires: freetype2
Requires: cairo
Requires: fontconfig >= 2.4
Requires: gnome-vfs2 >= 2.20
Requires: libpng
%endif
%if %{gconsole} && %{su110}
Requires: gtk2 >= 2.12
Requires: libgnome >= 2.22
Requires: libgnomeui >= 2.22
Requires: glibc >= 2.8
Requires: ORBit2
Requires: libart_lgpl >= 2.3
Requires: libbonobo >= 2.22
Requires: libbonoboui >= 2.22
Requires: bonobo-activation
Requires: gconf2
Requires: freetype2
Requires: cairo
Requires: fontconfig >= 2.4
Requires: gnome-vfs2 >= 2.22
Requires: libpng
%endif
%if %{gconsole} && %{mdk} && !%{mdv}
Requires: gtk2 >= 2.0
Requires: libgnomeui2
Requires: glibc >= 2.3
Requires: ORBit2
Requires: libart_lgpl >= 2.0
Requires: libbonobo >= 2.0
Requires: libbonoboui >= 2.0
Requires: GConf2
Requires: freetype2
%endif
%if %{gconsole} && %{mdv}
Requires: gtk2 >= 2.8
Requires: libgnomeui2
Requires: glibc >= 2.3
Requires: ORBit2
Requires: libart_lgpl >= 2.3
Requires: libbonobo >= 2.10
Requires: libbonoboui >= 2.10
Requires: GConf2
Requires: freetype2
%endif
%if %{gconsole} && %{fc3}  
Requires: gtk2 >= 2.4
Requires: libgnomeui >= 2.8
Requires: glibc >= 2.3
Requires: ORBit2
Requires: libart_lgpl >= 2.3
Requires: libbonobo >= 2.8
Requires: libbonoboui >= 2.8
Requires: bonobo-activation
Requires: GConf2
Requires: freetype
%endif
%if %{gconsole} && %{fc4}  
Requires: gtk2 >= 2.6
Requires: libgnomeui >= 2.10
Requires: glibc >= 2.3
Requires: ORBit2
Requires: libart_lgpl >= 2.3
Requires: libbonobo >= 2.8
Requires: libbonoboui >= 2.8
Requires: bonobo-activation
Requires: GConf2
Requires: freetype
%endif
%if %{gconsole} && %{fc5}  
Requires: gtk2 >= 2.8
Requires: libgnomeui >= 2.14
Requires: glibc >= 2.4
Requires: ORBit2
Requires: libart_lgpl >= 2.3
Requires: libbonobo >= 2.14
Requires: libbonoboui >= 2.14
Requires: GConf2
Requires: freetype
%endif
%if %{gconsole} && %{fc6}  
Requires: gtk2 >= 2.10
Requires: libgnomeui >= 2.16
Requires: glibc >= 2.5
Requires: ORBit2
Requires: libart_lgpl >= 2.3
Requires: libbonobo >= 2.16
Requires: libbonoboui >= 2.16
Requires: GConf2
Requires: freetype
%endif
%if %{gconsole} && %{fc7}  
Requires: gtk2 >= 2.10
Requires: libgnomeui >= 2.18
Requires: glibc >= 2.5
Requires: ORBit2
Requires: libart_lgpl >= 2.3
Requires: libbonobo >= 2.18
Requires: libbonoboui >= 2.18
Requires: GConf2
Requires: freetype
%endif
%if %{gconsole} && %{fc8}  
Requires: gtk2 >= 2.12
Requires: libgnomeui >= 2.20
Requires: glibc >= 2.7
Requires: ORBit2
Requires: libart_lgpl >= 2.3
Requires: libbonobo >= 2.20
Requires: libbonoboui >= 2.20
Requires: GConf2
Requires: freetype
%endif
%if %{gconsole} && %{fc9}  
Requires: gtk2 >= 2.12
Requires: libgnomeui >= 2.22
Requires: glibc >= 2.8
Requires: ORBit2
Requires: libart_lgpl >= 2.3
Requires: libbonobo >= 2.22
Requires: libbonoboui >= 2.22
Requires: GConf2
Requires: freetype
%endif
%if %{gconsole} && !%{su9} && !%{su10} && !%{su102} && !%{su103} && !%{su110} && !%{mdk} && !%{fc3} && !%{fc4} && !%{fc5} && !%{fc6} && !%{fc7} && !%{fc8} && !%{fc9}
Requires: gtk2 >= 2.0
Requires: libgnomeui >= 2.0
Requires: glibc >= 2.3
Requires: ORBit2
Requires: libart_lgpl >= 2.0
Requires: libbonobo >= 2.0
Requires: libbonoboui >= 2.0
Requires: bonobo-activation
Requires: GConf2
Requires: linc
Requires: freetype
%endif
%if %{gconsole} && %{su9}
Requires: xsu
%endif
%if %{gconsole} && %{su10}
Requires: xsu
%endif
%if %{gconsole} && %{su102}
Requires: xsu
%endif
%if %{gconsole} && %{su103}
Requires: xsu
%endif
%if %{gconsole} && %{su110}
Requires: xsu
%endif
%if %{gconsole} && ! %{su9} && ! %{su10} && ! %{su102} && ! %{su103} && ! %{su110}
Requires: usermode
%endif

%if %{gconsole}
%description gconsole
%{blurb}

%{blurb2}
%{blurb3}
%{blurb4}
%{blurb5}
%{blurb6}
%{blurb7}
%{blurb8}

This is the Gnome Console package. It is an add-on to the client or
server packages.
%endif

%if %{wxconsole}
%package wxconsole
Summary: Bacula - The Network Backup Solution
Group: System Environment/Daemons
Requires: wxGTK >= 2.6, libstdc++, openssl
%endif

%if %{wxconsole} && %{su10}
Requires: gtk2 >= 2.8
%endif

%if %{wxconsole} && %{su102}
Requires: gtk2 >= 2.10
%endif

%if %{wxconsole} && %{su103}
Requires: gtk2 >= 2.12
%endif

%if %{wxconsole} && %{su110}
Requires: gtk2 >= 2.12
%endif

%if %{wxconsole} && %{fc3}  
Requires: gtk2 >= 2.4
%endif

%if %{wxconsole} && %{fc4}  
Requires: gtk2 >= 2.6
%endif

%if %{wxconsole} && %{fc5}  
Requires: gtk2 >= 2.8
%endif

%if %{wxconsole} && %{fc6}  
Requires: gtk2 >= 2.10
%endif

%if %{wxconsole} && %{fc7}  
Requires: gtk2 >= 2.10
%endif

%if %{wxconsole} && %{fc8}  
Requires: gtk2 >= 2.12
%endif

%if %{wxconsole} && %{fc9}  
Requires: gtk2 >= 2.12
%endif

%if %{wxconsole}
%description wxconsole
%{blurb}

%{blurb2}
%{blurb3}
%{blurb4}
%{blurb5}
%{blurb6}
%{blurb7}
%{blurb8}

This is the WXWindows Console package. It is an add-on to the client or
server packages.
%endif

%if %{bat}
%package bat
Summary: Bacula - The Network Backup Solution
Group: System Environment/Daemons
%endif

%if %{bat} && %{su10}
Requires: openssl
Requires: glibc >= 2.4
Requires: fontconfig
Requires: freetype2
Requires: libgcc
Requires: libpng
Requires: qt >= 4.2
Requires: libstdc++
Requires: zlib
%endif

%if %{bat} && %{su102}
Requires: openssl
Requires: glibc >= 2.5
Requires: fontconfig
Requires: freetype2
Requires: libgcc
Requires: libpng
Requires: qt >= 4.2
Requires: libstdc++
Requires: zlib
%endif

%if %{bat} && %{su103}
Requires: openssl
Requires: glibc >= 2.6
Requires: fontconfig
Requires: freetype2
Requires: libgcc
Requires: libpng
Requires: qt >= 4.2
Requires: libstdc++
Requires: zlib
%endif

%if %{bat} && %{su110}
Requires: openssl
Requires: glibc >= 2.8
Requires: fontconfig
Requires: freetype2
Requires: libgcc
Requires: libpng
Requires: qt >= 4.2
Requires: libstdc++
Requires: zlib
%endif

%if %{bat} && %{fc5}
Requires: openssl
Requires: glibc >= 2.4
Requires: fontconfig
Requires: freetype
Requires: libgcc
Requires: libpng
Requires: qt4 >= 4.2
Requires: libstdc++
Requires: zlib
%endif

%if %{bat} && %{fc6}
Requires: openssl
Requires: glibc >= 2.5
Requires: fontconfig
Requires: freetype
Requires: libgcc
Requires: libpng
Requires: qt4 >= 4.2
Requires: libstdc++
Requires: zlib
%endif

%if %{bat} && %{fc7}
Requires: openssl
Requires: glibc >= 2.5
Requires: fontconfig
Requires: freetype
Requires: libgcc
Requires: libpng
Requires: qt4 >= 4.2
Requires: libstdc++
Requires: zlib
%endif

%if %{bat} && %{fc8}
Requires: openssl
Requires: glibc >= 2.7
Requires: fontconfig
Requires: freetype
Requires: libgcc
Requires: libpng
Requires: qt4 >= 4.2
Requires: libstdc++
Requires: zlib
%endif

%if %{bat} && %{fc9}
Requires: openssl
Requires: glibc >= 2.8
Requires: fontconfig
Requires: freetype
Requires: libgcc
Requires: libpng
Requires: qt4 >= 4.3
Requires: libstdc++
Requires: zlib
%endif

%if %{bat}
%description bat
%{blurb}

%{blurb2}
%{blurb3}
%{blurb4}
%{blurb5}
%{blurb6}
%{blurb7}
%{blurb8}

This is the Bacula Administration Tool package. It is an add-on to 
the client or server packages.
%endif

# SuSE turns off stripping of binaries by default. In order to get
# stripped packages we must generate debug package. RedHat and Mandriva
# turn debug packages on by default but strip binaries regardless.
%if %{su9} || %{su10} || %{su102} || %{su103} || %{su110}
%debug_package
%endif

%prep

%setup
%setup -T -D -b 1
%setup -T -D -b 2
%setup -T -D -b 3
%setup -T -D -b 4

%build

%if %{su9} || %{su10} || %{su102} || %{su103} || %{su110}
export LDFLAGS="${LDFLAGS} -L/usr/lib/termcap"
%endif

cwd=${PWD}
cd %{depkgs}
%if %{sqlite}
make sqlite3
%endif
%if ! %{client_only} && %{mtx}
make mtx
%endif
%if %{bat}
make qwt
%endif
cd ${cwd}

%if %{wb3} || %{old_pgsql}
patch -p3 src/cats/postgresql.c < %SOURCE5
%endif

# patches for the bundled sqlite scripts

# patch the make_sqlite_tables script for installation bindir
#patch src/cats/make_sqlite_tables.in src/cats/make_sqlite_tables.in.patch
patch src/cats/make_sqlite3_tables.in src/cats/make_sqlite3_tables.in.patch

# patch the create_sqlite_database script for installation bindir
#patch src/cats/create_sqlite_database.in src/cats/create_sqlite_database.in.patch
patch src/cats/create_sqlite3_database.in src/cats/create_sqlite3_database.in.patch

# patch the make_catalog_backup script for installation bindir
patch src/cats/make_catalog_backup.in src/cats/make_catalog_backup.in.patch

# patch the update_sqlite_tables script for installation bindir
#patch src/cats/update_sqlite_tables.in src/cats/update_sqlite_tables.in.patch
patch src/cats/update_sqlite3_tables.in src/cats/update_sqlite3_tables.in.patch

# patch the bacula-dir init script to remove sqlite service
%if %{sqlite} && %{su9}
patch platforms/suse/bacula-dir.in platforms/suse/bacula-dir-suse-sqlite.patch
%endif
%if %{sqlite} && %{su10}
patch platforms/suse/bacula-dir.in platforms/suse/bacula-dir-suse-sqlite.patch
%endif
%if %{sqlite} && %{su102}
patch platforms/suse/bacula-dir.in platforms/suse/bacula-dir-suse-sqlite.patch
%endif
%if %{sqlite} && %{su103}
patch platforms/suse/bacula-dir.in platforms/suse/bacula-dir-suse-sqlite.patch
%endif
%if %{sqlite} && %{su110}
patch platforms/suse/bacula-dir.in platforms/suse/bacula-dir-suse-sqlite.patch
%endif

# 64 bit lib location hacks
# as of 1.39.18 it should not be necessary to enable x86_64 as configure is
# reported to be fixed to properly detect lib locations.
%if %{x86_64}
export LDFLAGS="${LDFLAGS} -L/usr/lib64"
%endif
%if %{mysql} && %{x86_64}
export LDFLAGS="${LDFLAGS} -L/usr/lib64/mysql"
%endif
%if %{python} && %{x86_64}
export LDFLAGS="${LDFLAGS} -L/usr/lib64/python%{pyver}"
%endif

# Red Hat's 64 bit installation of QT4 appears to be broken so:
%define qt_path 0
%if %{rhel5} || %{centos5} || %{sl5}
%define qt_path 1
%endif
%if %{bat} && %{qt_path} && %{x86_64}
export PATH=/usr/lib64/qt4/bin/:$PATH
export QTDIR=/usr/lib64/qt4/
export QTINC=/usr/lib64/qt4/include/
export QTLIB=/usr/lib64/qt4/
%endif

%configure \
        --prefix=/usr \
        --sbindir=/usr/sbin \
	--sysconfdir=%{sysconf_dir} \
	--with-scriptdir=%{script_dir} \
	--with-working-dir=%{working_dir} \
	--with-pid-dir=%{pid_dir} \
        --enable-smartalloc \
        --enable-client-only \
	%if %{mdk}
	--disable-nls \
	%endif
        --enable-static-fd

make

%configure \
        --prefix=/usr \
        --sbindir=/usr/sbin \
	--sysconfdir=%{sysconf_dir} \
	--with-scriptdir=%{script_dir} \
	--with-working-dir=%{working_dir} \
	--with-pid-dir=%{pid_dir} \
        --enable-smartalloc \
%if %{gconsole}
        --enable-gnome \
%endif
%if %{gconsole} && ! %{rh8}
        --enable-tray-monitor \
%endif
%if %{mysql}
        --with-mysql \
%endif
%if %{sqlite}
        --with-sqlite3=${cwd}/%{depkgs}/sqlite3 \
%endif
%if %{postgresql}
        --with-postgresql \
%endif
%if %{wxconsole}
	--enable-bwx-console \
%endif
%if %{bat}
	--enable-bat \
	--with-qwt=${cwd}/%{depkgs}/qwt \
%endif
%if %{python}
	--with-python \
%endif
%if %{client_only}
	--enable-client-only \
%endif
%if %{rh7} || %{rh8} || %{rh9} || %{fc1} || %{fc3} || %{wb3} 
	--disable-batch-insert \
%endif
	--mandir=%{_mandir} \
        --with-subsys-dir=/var/lock/subsys \
        --with-dir-user=%{director_daemon_user} \
        --with-dir-group=%{daemon_group} \
        --with-sd-user=%{storage_daemon_user} \
        --with-sd-group=%{storage_daemon_group} \
        --with-fd-user=%{file_daemon_user} \
        --with-fd-group=%{daemon_group} \
        --with-dir-password="XXX_REPLACE_WITH_DIRECTOR_PASSWORD_XXX" \
        --with-fd-password="XXX_REPLACE_WITH_CLIENT_PASSWORD_XXX" \
        --with-sd-password="XXX_REPLACE_WITH_STORAGE_PASSWORD_XXX" \
        --with-mon-dir-password="XXX_REPLACE_WITH_DIRECTOR_MONITOR_PASSWORD_XXX" \
        --with-mon-fd-password="XXX_REPLACE_WITH_CLIENT_MONITOR_PASSWORD_XXX" \
        --with-mon-sd-password="XXX_REPLACE_WITH_STORAGE_MONITOR_PASSWORD_XXX" \
        --with-openssl

make

%install
 
cwd=${PWD}
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
mkdir -p $RPM_BUILD_ROOT/etc/init.d
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
mkdir -p $RPM_BUILD_ROOT/etc/log.d/conf/logfiles
mkdir -p $RPM_BUILD_ROOT/etc/log.d/conf/services
mkdir -p $RPM_BUILD_ROOT/etc/log.d/scripts/services
mkdir -p $RPM_BUILD_ROOT%{script_dir}/updatedb

%if %{gconsole} || %{wxconsole} || %{bat}
mkdir -p $RPM_BUILD_ROOT/usr/share/applications
mkdir -p $RPM_BUILD_ROOT/usr/share/pixmaps
%endif

%if %{gconsole} || %{wxconsole} || %{bat}
%define usermode_iftrick 1
%else
%define usermode_iftrick 0
%endif

%if %{usermode_iftrick} && ! %{su9} && ! %{su10} && ! %{su102} && ! %{su103} && ! %{su110}
mkdir -p $RPM_BUILD_ROOT/etc/pam.d
mkdir -p $RPM_BUILD_ROOT/etc/security/console.apps
mkdir -p $RPM_BUILD_ROOT/usr/bin
%endif

%if %{sqlite}
mkdir -p $RPM_BUILD_ROOT%{sqlite_bindir}
%endif

make \
        prefix=$RPM_BUILD_ROOT/usr \
        sbindir=$RPM_BUILD_ROOT/usr/sbin \
	sysconfdir=$RPM_BUILD_ROOT%{sysconf_dir} \
	scriptdir=$RPM_BUILD_ROOT%{script_dir} \
        working_dir=$RPM_BUILD_ROOT%{working_dir} \
	piddir=$RPM_BUILD_ROOT%{pid_dir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
        install

%if ! %{client_only} && %{mtx}
cd %{depkgs}
make \
        prefix=$RPM_BUILD_ROOT/usr \
        sbindir=$RPM_BUILD_ROOT/usr/sbin \
	sysconfdir=$RPM_BUILD_ROOT%{sysconf_dir} \
	scriptdir=$RPM_BUILD_ROOT%{script_dir} \
        working_dir=$RPM_BUILD_ROOT%{working_dir} \
	piddir=$RPM_BUILD_ROOT%{pid_dir} \
        mandir=$RPM_BUILD_ROOT%{_mandir} \
        mtx-install
cd ${cwd}
%endif

# make install in manpages installs _everything_ shotgun style
# so now delete what we will not be packaging
%if ! %{wxconsole}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/bacula-bwxconsole.1.%{manpage_ext}
%endif
%if ! %{bat}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/bat.1.%{manpage_ext}
%endif
%if ! %{gconsole}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/bacula-bgnome-console.1.%{manpage_ext}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/bacula-tray-monitor.1.%{manpage_ext}
%endif
%if %{client_only}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/bsmtp.1.%{manpage_ext}
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/bacula-dir.8.%{manpage_ext}
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/bacula-sd.8.%{manpage_ext}
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/bcopy.8.%{manpage_ext}
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/bextract.8.%{manpage_ext}
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/bls.8.%{manpage_ext}
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/bscan.8.%{manpage_ext}
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/btape.8.%{manpage_ext}
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/dbcheck.8.%{manpage_ext}
%endif

# fixme - make installs the mysql scripts for sqlite build
%if %{sqlite}
rm -f $RPM_BUILD_ROOT%{script_dir}/startmysql
rm -f $RPM_BUILD_ROOT%{script_dir}/stopmysql
rm -f $RPM_BUILD_ROOT%{script_dir}/grant_mysql_privileges
%endif

# fixme - make installs the mysql scripts for postgresql build
%if %{postgresql}
rm -f $RPM_BUILD_ROOT%{script_dir}/startmysql
rm -f $RPM_BUILD_ROOT%{script_dir}/stopmysql
%endif

# fixme - make installs gconsole script for build without gconsole
%if ! %{gconsole}
rm -f $RPM_BUILD_ROOT%{script_dir}/gconsole
%endif

rm -f $RPM_BUILD_ROOT/usr/sbin/static-bacula-fd

# install the init scripts
%if %{su9} || %{su10} || %{su102} || %{su103} || %{su110}
cp -p platforms/suse/bacula-dir $RPM_BUILD_ROOT/etc/init.d/bacula-dir
cp -p platforms/suse/bacula-fd $RPM_BUILD_ROOT/etc/init.d/bacula-fd
cp -p platforms/suse/bacula-sd $RPM_BUILD_ROOT/etc/init.d/bacula-sd
%endif
%if %{mdk}
cp -p platforms/mandrake/bacula-dir $RPM_BUILD_ROOT/etc/init.d/bacula-dir
cp -p platforms/mandrake/bacula-fd $RPM_BUILD_ROOT/etc/init.d/bacula-fd
cp -p platforms/mandrake/bacula-sd $RPM_BUILD_ROOT/etc/init.d/bacula-sd
%endif
%if ! %{su9} && ! %{su10} && ! %{su102} && ! %{su103} && ! %{su110} && ! %{mdk}
cp -p platforms/redhat/bacula-dir $RPM_BUILD_ROOT/etc/init.d/bacula-dir
cp -p platforms/redhat/bacula-fd $RPM_BUILD_ROOT/etc/init.d/bacula-fd
cp -p platforms/redhat/bacula-sd $RPM_BUILD_ROOT/etc/init.d/bacula-sd
%endif
chmod 0754 $RPM_BUILD_ROOT/etc/init.d/*
%if %{client_only}
rm -f $RPM_BUILD_ROOT/etc/init.d/bacula-dir
rm -f $RPM_BUILD_ROOT/etc/init.d/bacula-sd
%endif

# install the menu stuff
%if %{gconsole} && %{su9}
cp -p scripts/bacula.png $RPM_BUILD_ROOT/usr/share/pixmaps/bacula.png
cp -p scripts/bacula.desktop.gnome2.xsu $RPM_BUILD_ROOT/usr/share/applications/bacula.desktop
cp -p src/tray-monitor/generic.xpm $RPM_BUILD_ROOT/usr/share/pixmaps/bacula-tray-monitor.xpm
cp -p scripts/bacula-tray-monitor.desktop $RPM_BUILD_ROOT/usr/share/applications/bacula-tray-monitor.desktop
%endif
%if %{gconsole} && %{su10}
cp -p scripts/bacula.png $RPM_BUILD_ROOT/usr/share/pixmaps/bacula.png
cp -p scripts/bacula.desktop.gnome2.xsu $RPM_BUILD_ROOT/usr/share/applications/bacula.desktop
cp -p src/tray-monitor/generic.xpm $RPM_BUILD_ROOT/usr/share/pixmaps/bacula-tray-monitor.xpm
cp -p scripts/bacula-tray-monitor.desktop $RPM_BUILD_ROOT/usr/share/applications/bacula-tray-monitor.desktop
%endif
%if %{gconsole} && %{su102}
cp -p scripts/bacula.png $RPM_BUILD_ROOT/usr/share/pixmaps/bacula.png
cp -p scripts/bacula.desktop.gnome2.xsu $RPM_BUILD_ROOT/usr/share/applications/bacula.desktop
cp -p src/tray-monitor/generic.xpm $RPM_BUILD_ROOT/usr/share/pixmaps/bacula-tray-monitor.xpm
cp -p scripts/bacula-tray-monitor.desktop $RPM_BUILD_ROOT/usr/share/applications/bacula-tray-monitor.desktop
%endif
%if %{gconsole} && %{su103}
cp -p scripts/bacula.png $RPM_BUILD_ROOT/usr/share/pixmaps/bacula.png
cp -p scripts/bacula.desktop.gnome2.xsu $RPM_BUILD_ROOT/usr/share/applications/bacula.desktop
cp -p src/tray-monitor/generic.xpm $RPM_BUILD_ROOT/usr/share/pixmaps/bacula-tray-monitor.xpm
cp -p scripts/bacula-tray-monitor.desktop $RPM_BUILD_ROOT/usr/share/applications/bacula-tray-monitor.desktop
%endif
%if %{gconsole} && %{su110}
cp -p scripts/bacula.png $RPM_BUILD_ROOT/usr/share/pixmaps/bacula.png
cp -p scripts/bacula.desktop.gnome2.xsu $RPM_BUILD_ROOT/usr/share/applications/bacula.desktop
cp -p src/tray-monitor/generic.xpm $RPM_BUILD_ROOT/usr/share/pixmaps/bacula-tray-monitor.xpm
cp -p scripts/bacula-tray-monitor.desktop $RPM_BUILD_ROOT/usr/share/applications/bacula-tray-monitor.desktop
%endif
%if %{wxconsole} && %{su10}
cp -p src/wx-console/wxwin16x16.xpm $RPM_BUILD_ROOT/usr/share/pixmaps/wxwin16x16.xpm
cp -p scripts/wxconsole.desktop.xsu $RPM_BUILD_ROOT/usr/share/applications/wxconsole.desktop
%endif
%if %{wxconsole} && %{su102}
cp -p src/wx-console/wxwin16x16.xpm $RPM_BUILD_ROOT/usr/share/pixmaps/wxwin16x16.xpm
cp -p scripts/wxconsole.desktop.xsu $RPM_BUILD_ROOT/usr/share/applications/wxconsole.desktop
%endif
%if %{wxconsole} && %{su103}
cp -p src/wx-console/wxwin16x16.xpm $RPM_BUILD_ROOT/usr/share/pixmaps/wxwin16x16.xpm
cp -p scripts/wxconsole.desktop.xsu $RPM_BUILD_ROOT/usr/share/applications/wxconsole.desktop
%endif
%if %{wxconsole} && %{su110}
cp -p src/wx-console/wxwin16x16.xpm $RPM_BUILD_ROOT/usr/share/pixmaps/wxwin16x16.xpm
cp -p scripts/wxconsole.desktop.xsu $RPM_BUILD_ROOT/usr/share/applications/wxconsole.desktop
%endif
%if %{bat} && %{su102}
cp -p src/qt-console/images/bat_icon.png $RPM_BUILD_ROOT/usr/share/pixmaps/bat_icon.png
cp -p scripts/bat.desktop.xsu $RPM_BUILD_ROOT/usr/share/applications/bat.desktop
%endif
%if %{bat} && %{su103}
cp -p src/qt-console/images/bat_icon.png $RPM_BUILD_ROOT/usr/share/pixmaps/bat_icon.png
cp -p scripts/bat.desktop.xsu $RPM_BUILD_ROOT/usr/share/applications/bat.desktop
%endif
%if %{bat} && %{su110}
cp -p src/qt-console/images/bat_icon.png $RPM_BUILD_ROOT/usr/share/pixmaps/bat_icon.png
cp -p scripts/bat.desktop.xsu $RPM_BUILD_ROOT/usr/share/applications/bat.desktop
%endif
%if %{rh8} || %{rh9} || %{wb3} || %{fc1} || %{fc3} || %{fc4} || %{fc5} || %{fc6} || %{fc7} || %{fc8} || %{fc9} || %{mdk}
%define iftrick 1
%else
%define iftrick 0
%endif
%if %{gconsole} && %{iftrick}
cp -p scripts/bacula.png $RPM_BUILD_ROOT/usr/share/pixmaps/bacula.png
cp -p scripts/bacula.desktop.gnome2.consolehelper $RPM_BUILD_ROOT/usr/share/applications/bacula.desktop
cp -p scripts/bgnome-console.console_apps $RPM_BUILD_ROOT/etc/security/console.apps/bgnome-console
cp -p scripts/bgnome-console.pamd $RPM_BUILD_ROOT/etc/pam.d/bgnome-console
ln -sf consolehelper $RPM_BUILD_ROOT/usr/bin/bgnome-console
%endif
%if %{gconsole} && ! %{rh8}
cp -p src/tray-monitor/generic.xpm $RPM_BUILD_ROOT/usr/share/pixmaps/bacula-tray-monitor.xpm
cp -p scripts/bacula-tray-monitor.desktop $RPM_BUILD_ROOT/usr/share/applications/bacula-tray-monitor.desktop
%endif
%if %{wxconsole} && %{iftrick}
cp -p src/wx-console/wxwin16x16.xpm $RPM_BUILD_ROOT/usr/share/pixmaps/wxwin16x16.xpm
cp -p scripts/wxconsole.desktop.consolehelper $RPM_BUILD_ROOT/usr/share/applications/wxconsole.desktop
cp -p scripts/wxconsole.console_apps $RPM_BUILD_ROOT/etc/security/console.apps/bwx-console
cp -p scripts/wxconsole.pamd $RPM_BUILD_ROOT/etc/pam.d/bwx-console
ln -sf consolehelper $RPM_BUILD_ROOT/usr/bin/bwx-console
%endif
%if %{bat} && %{iftrick}
cp -p src/qt-console/images/bat_icon.png $RPM_BUILD_ROOT/usr/share/pixmaps/bat_icon.png
cp -p scripts/bat.desktop.consolehelper $RPM_BUILD_ROOT/usr/share/applications/bat.desktop
cp -p scripts/bat.console_apps $RPM_BUILD_ROOT/etc/security/console.apps/bat
cp -p scripts/bat.pamd $RPM_BUILD_ROOT/etc/pam.d/bat
ln -sf consolehelper $RPM_BUILD_ROOT/usr/bin/bat
%endif

# install sqlite
%if %{sqlite}
cp -p %{depkgs}/sqlite3/sqlite3 $RPM_BUILD_ROOT%{sqlite_bindir}/sqlite3
cp -p %{depkgs}/sqlite3/sqlite3.h $RPM_BUILD_ROOT%{sqlite_bindir}/sqlite3.h
cp -p %{depkgs}/sqlite3/libsqlite3.a $RPM_BUILD_ROOT%{sqlite_bindir}/libsqlite3.a
%endif

# install the logrotate file
cp -p scripts/logrotate $RPM_BUILD_ROOT/etc/logrotate.d/bacula

# install the updatedb scripts
cp -p updatedb/* $RPM_BUILD_ROOT%{script_dir}/updatedb/

# install the logwatch scripts
%if ! %{client_only}
cp -p scripts/logwatch/bacula $RPM_BUILD_ROOT/etc/log.d/scripts/services/bacula
cp -p scripts/logwatch/logfile.bacula.conf $RPM_BUILD_ROOT/etc/log.d/conf/logfiles/bacula.conf
cp -p scripts/logwatch/services.bacula.conf $RPM_BUILD_ROOT/etc/log.d/conf/services/bacula.conf
chmod 755 $RPM_BUILD_ROOT/etc/log.d/scripts/services/bacula
chmod 644 $RPM_BUILD_ROOT/etc/log.d/conf/logfiles/bacula.conf
chmod 644 $RPM_BUILD_ROOT/etc/log.d/conf/services/bacula.conf
%endif

# install the rescue files
mkdir $RPM_BUILD_ROOT%{script_dir}/rescue
mkdir $RPM_BUILD_ROOT%{script_dir}/rescue/freebsd
mkdir $RPM_BUILD_ROOT%{script_dir}/rescue/solaris
cp -p %{_rescuesrc}/Makefile* $RPM_BUILD_ROOT%{script_dir}/rescue/
cp -p %{_rescuesrc}/freebsd/Makefile* $RPM_BUILD_ROOT%{script_dir}/rescue/freebsd/
cp -p %{_rescuesrc}/solaris/Makefile* $RPM_BUILD_ROOT%{script_dir}/rescue/solaris/
cp -p %{_rescuesrc}/README $RPM_BUILD_ROOT%{script_dir}/rescue/
cp -p %{_rescuesrc}/configure $RPM_BUILD_ROOT%{script_dir}/rescue/
cp -p %{_rescuesrc}/version.h $RPM_BUILD_ROOT%{script_dir}/rescue/
cp -pr %{_rescuesrc}/linux $RPM_BUILD_ROOT%{script_dir}/rescue/
cp -pr %{_rescuesrc}/autoconf $RPM_BUILD_ROOT%{script_dir}/rescue/
cp -pr %{_rescuesrc}/knoppix $RPM_BUILD_ROOT%{script_dir}/rescue/
touch $RPM_BUILD_ROOT%{script_dir}/rescue/linux/cdrom/rpm_release
cp -p src/filed/static-bacula-fd $RPM_BUILD_ROOT%{script_dir}/rescue/linux/cdrom/bacula/bin/bacula-fd
rm -f src/filed/static-bacula-fd

# install bat since make doesn't at the moment
%if %{bat}
cp -p src/qt-console/bat $RPM_BUILD_ROOT/usr/sbin/bat
cp -p src/qt-console/bat.conf $RPM_BUILD_ROOT%{sysconf_dir}/bat.conf
%endif

# now clean up permissions that are left broken by the install
chmod o-rwx $RPM_BUILD_ROOT%{working_dir}
%if %{gconsole} && ! %{rh8}
chmod 755 $RPM_BUILD_ROOT/usr/sbin/bacula-tray-monitor
chmod 644 $RPM_BUILD_ROOT%{sysconf_dir}/tray-monitor.conf
%endif

# fix me - building enable-client-only installs files not included in bacula-client package
%if %{client_only}
rm -f $RPM_BUILD_ROOT%{script_dir}/bacula
rm -f $RPM_BUILD_ROOT%{script_dir}/bacula-ctl-dir
rm -f $RPM_BUILD_ROOT%{script_dir}/bacula-ctl-sd
rm -f $RPM_BUILD_ROOT%{script_dir}/disk-changer
rm -f $RPM_BUILD_ROOT%{script_dir}/dvd-handler
rm -f $RPM_BUILD_ROOT%{script_dir}/mtx-changer
rm -f $RPM_BUILD_ROOT%{script_dir}/startmysql
rm -f $RPM_BUILD_ROOT%{script_dir}/stopmysql
rm -rf $RPM_BUILD_ROOT%{script_dir}/updatedb
%endif

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
rm -rf $RPM_BUILD_DIR/%{name}-docs-%{docs_version}
rm -rf $RPM_BUILD_DIR/%{name}-rescue-%{_rescuever}
rm -rf $RPM_BUILD_DIR/depkgs
rm -f $RPM_BUILD_DIR/Release_Notes-%{version}-%{release}.txt

%if %{mysql}
# MySQL specific files
%files mysql
%defattr(-, root, root)
%attr(-, root, %{daemon_group}) %{script_dir}/create_mysql_database
%attr(-, root, %{daemon_group}) %{script_dir}/drop_mysql_database
%attr(-, root, %{daemon_group}) %{script_dir}/make_mysql_tables
%attr(-, root, %{daemon_group}) %{script_dir}/drop_mysql_tables
%attr(-, root, %{daemon_group}) %{script_dir}/update_mysql_tables
%attr(-, root, %{daemon_group}) %{script_dir}/grant_mysql_privileges
%attr(-, root, %{daemon_group}) %{script_dir}/startmysql
%attr(-, root, %{daemon_group}) %{script_dir}/stopmysql
%endif

%if %{sqlite}
%files sqlite
%defattr(-,root,root)
%attr(-, root, %{daemon_group}) %{script_dir}/create_sqlite3_database
%attr(-, root, %{daemon_group}) %{script_dir}/drop_sqlite3_database
%attr(-, root, %{daemon_group}) %{script_dir}/grant_sqlite3_privileges
%attr(-, root, %{daemon_group}) %{script_dir}/make_sqlite3_tables
%attr(-, root, %{daemon_group}) %{script_dir}/drop_sqlite3_tables
%attr(-, root, %{daemon_group}) %{script_dir}/update_sqlite3_tables
%{sqlite_bindir}/libsqlite3.a
%{sqlite_bindir}/sqlite3.h
%{sqlite_bindir}/sqlite3
%endif

%if %{postgresql}
%files postgresql
%defattr(-,root,root)
%attr(-, root, %{daemon_group}) %{script_dir}/create_postgresql_database
%attr(-, root, %{daemon_group}) %{script_dir}/drop_postgresql_database
%attr(-, root, %{daemon_group}) %{script_dir}/make_postgresql_tables
%attr(-, root, %{daemon_group}) %{script_dir}/drop_postgresql_tables
%attr(-, root, %{daemon_group}) %{script_dir}/update_postgresql_tables
%attr(-, root, %{daemon_group}) %{script_dir}/grant_postgresql_privileges
%endif

# The rest is DB backend independent
%if ! %{client_only}
%attr(-, root, %{daemon_group}) %dir %{script_dir}
%attr(-, root, %{daemon_group}) %{script_dir}/bacula
%attr(-, root, %{daemon_group}) %{script_dir}/bconsole
%attr(-, root, %{daemon_group}) %{script_dir}/create_bacula_database
%attr(-, root, %{daemon_group}) %{script_dir}/drop_bacula_database
%attr(-, root, %{daemon_group}) %{script_dir}/grant_bacula_privileges
%attr(-, root, %{daemon_group}) %{script_dir}/make_bacula_tables
%attr(-, root, %{daemon_group}) %{script_dir}/drop_bacula_tables
%attr(-, root, %{daemon_group}) %{script_dir}/update_bacula_tables
%attr(-, root, %{daemon_group}) %{script_dir}/make_catalog_backup
%attr(-, root, %{daemon_group}) %{script_dir}/delete_catalog_backup
%attr(-, root, %{daemon_group}) %{script_dir}/btraceback.dbx
%attr(-, root, %{daemon_group}) %{script_dir}/btraceback.gdb
%attr(-, root, %{daemon_group}) %{script_dir}/rescue
%attr(-, root, %{daemon_group}) %{script_dir}/disk-changer
%attr(-, root, %{daemon_group}) %{script_dir}/bacula-ctl-dir
%attr(-, root, %{daemon_group}) %{script_dir}/bacula-ctl-fd
%attr(-, root, %{daemon_group}) %{script_dir}/bacula-ctl-sd
%attr(-, root, %{daemon_group}) /etc/init.d/bacula-dir
%attr(-, root, %{daemon_group}) /etc/init.d/bacula-fd
%attr(-, root, %{storage_daemon_group}) %{script_dir}/dvd-handler
%attr(-, root, %{storage_daemon_group}) /etc/init.d/bacula-sd
%attr(-, root, %{storage_daemon_group}) %{script_dir}/mtx-changer

%doc COPYING ChangeLog ReleaseNotes VERIFYING kernstodo 
%doc %{_docsrc}/manual/bacula.pdf %{_docsrc}/developers/developers.pdf %{_docsrc}/manual/bacula ../Release_Notes-%{version}-%{release}.txt

/etc/logrotate.d/bacula
/etc/log.d/scripts/services/bacula
%attr(-, root, %{daemon_group}) %config(noreplace) %{sysconf_dir}/bacula-dir.conf
%attr(-, root, %{daemon_group}) %config(noreplace) %{sysconf_dir}/bacula-fd.conf
%attr(-, root, %{storage_daemon_group}) %config(noreplace) %{sysconf_dir}/bacula-sd.conf
%attr(-, root, %{daemon_group}) %config(noreplace) %{sysconf_dir}/bconsole.conf
%attr(-, root, %{daemon_group}) %config(noreplace) /etc/log.d/conf/logfiles/bacula.conf
%attr(-, root, %{daemon_group}) %config(noreplace) /etc/log.d/conf/services/bacula.conf
%attr(-, root, %{daemon_group}) %config(noreplace) %{script_dir}/query.sql

%attr(-, %{storage_daemon_user}, %{daemon_group}) %dir %{working_dir}

/usr/sbin/bacula-dir
/usr/sbin/bacula-fd
/usr/sbin/bacula-sd
/usr/sbin/bcopy
/usr/sbin/bextract
/usr/sbin/bls
/usr/sbin/bscan
/usr/sbin/btape
/usr/sbin/btraceback
/usr/sbin/bconsole
/usr/sbin/dbcheck
/usr/sbin/bsmtp
/usr/sbin/bregex
/usr/sbin/bwild
%{_mandir}/man8/bacula-fd.8.%{manpage_ext}
%{_mandir}/man8/bacula-dir.8.%{manpage_ext}
%{_mandir}/man8/bacula-sd.8.%{manpage_ext}
%{_mandir}/man8/bacula.8.%{manpage_ext}
%{_mandir}/man8/bconsole.8.%{manpage_ext}
%{_mandir}/man8/bcopy.8.%{manpage_ext}
%{_mandir}/man8/bextract.8.%{manpage_ext}
%{_mandir}/man8/bls.8.%{manpage_ext}
%{_mandir}/man8/bscan.8.%{manpage_ext}
%{_mandir}/man8/btape.8.%{manpage_ext}
%{_mandir}/man8/btraceback.8.%{manpage_ext}
%{_mandir}/man8/dbcheck.8.%{manpage_ext}
%{_mandir}/man1/bsmtp.1.%{manpage_ext}
%endif

%if %{mysql}
%pre mysql
# test for bacula database older than version 9
# note: this ASSUMES no password has been set for bacula database
DB_VER=`mysql 2>/dev/null bacula -e 'select * from Version;'|tail -n 1`
%endif

%if %{sqlite}
%pre sqlite
# are we upgrading from sqlite to sqlite3?
if [ -s %{working_dir}/bacula.db ] && [ -s %{sqlite_bindir}/sqlite ];then
        echo "This version of bacula-sqlite involves an upgrade to sqlite3."
	echo "Your catalog database file is not compatible with sqlite3, thus"
	echo "you will need to dump the data, delete the old file, and re-run"
	echo "this rpm upgrade."
	echo ""
	echo "Backing up your current database..."
        echo ".dump" | %{sqlite_bindir}/sqlite %{working_dir}/bacula.db > %{working_dir}/bacula_backup.sql
	mv %{working_dir}/bacula.db %{working_dir}/bacula.db.old
	echo "Your catalog data has been saved in %{working_dir}/bacula_backup.sql and your"
	echo "catalog file has been renamed %{working_dir}/bacula.db.old."
	echo ""
	echo "Please re-run this rpm package upgrade."
	echo "After the upgrade is complete, restore your catalog"
	echo "with the following commands:"
	echo "%{script_dir}/drop_sqlite3_tables"
	echo "cd %{working_dir}"
	echo "%{sqlite_bindir}/sqlite3 $* bacula.db < bacula_backup.sql"
	echo "chown bacula.bacula bacula.db"
	exit 1
fi
# test for bacula database older than version 9 and sqlite3
if [ -s %{working_dir}/bacula.db ] && [ -s %{sqlite_bindir}/sqlite3 ];then
        DB_VER=`echo "select * from Version;" | %{sqlite_bindir}/sqlite3 2>/dev/null %{working_dir}/bacula.db | tail -n 1`
%endif

%if %{postgresql}
%pre postgresql
DB_VER=`echo 'select * from Version;' | psql bacula 2>/dev/null | tail -3 | head -1`
%endif

%if ! %{client_only}
if [ -n "$DB_VER" ] && [ "$DB_VER" -lt "9" ]; then
        echo "This bacula upgrade will update a bacula database from version 9 to 10."
        echo "You appear to be running database version $DB_VER. You must first update"
        echo "your database to version 9 and then install this upgrade. The alternative"
	echo "is to use %{script_dir}/drop_%{db_backend}_tables to delete all your your current"
        echo "catalog information, then do the upgrade. Information on updating a"
        echo "database older than version 9 can be found in the release notes."
        exit 1
fi
%endif

%if %{sqlite}
fi
%endif

%if ! %{client_only}
# check for and copy %{sysconf_dir}/console.conf to bconsole.conf
if [ -s %{sysconf_dir}/console.conf ];then
	cp -p %{sysconf_dir}/console.conf %{sysconf_dir}/bconsole.conf
fi

# create the daemon users and groups
# first create the groups if they don't exist
HAVE_BACULA=`grep %{daemon_group} %{group_file} 2>/dev/null`
if [ -z "$HAVE_BACULA" ]; then
        %{groupadd} -r %{daemon_group} > /dev/null 2>&1
        echo "The group %{daemon_group} has been added to %{group_file}."
        echo "See the manual chapter \"Running Bacula\" for details."
fi
HAVE_BACULA=`grep %{storage_daemon_group} %{group_file} 2>/dev/null`
if [ -z "$HAVE_BACULA" ]; then
        %{groupadd} -r %{storage_daemon_group} > /dev/null 2>&1
        echo "The group %{storage_daemon_group} has been added to %{group_file}."
        echo "See the manual chapter \"Running Bacula\" for details."
fi
# now create the users if they do not exist
# we do not use the -g option allowing the primary group to be set to system default
# this will be a unique group on redhat type systems or the group users on some systems
HAVE_BACULA=`grep %{storage_daemon_user} %{user_file} 2>/dev/null`
if [ -z "$HAVE_BACULA" ]; then
        %{useradd} -r -c "Bacula" -d %{working_dir} -g %{storage_daemon_group} -M -s /sbin/nologin %{storage_daemon_user} > /dev/null 2>&1
        echo "The user %{storage_daemon_user} has been added to %{user_file}."
        echo "See the manual chapter \"Running Bacula\" for details."
fi
HAVE_BACULA=`grep %{director_daemon_user} %{user_file} 2>/dev/null`
if [ -z "$HAVE_BACULA" ]; then
        %{useradd} -r -c "Bacula" -d %{working_dir} -g %{daemon_group} -M -s /sbin/nologin %{director_daemon_user} > /dev/null 2>&1
        echo "The user %{director_daemon_user} has been added to %{user_file}."
        echo "See the manual chapter \"Running Bacula\" for details."
fi
HAVE_BACULA=`grep %{file_daemon_user} %{user_file} 2>/dev/null`
if [ -z "$HAVE_BACULA" ]; then
        %{useradd} -r -c "Bacula" -d %{working_dir} -g %{daemon_group} -M -s /sbin/nologin %{file_daemon_user} > /dev/null 2>&1
        echo "The user %{file_daemon_user} has been added to %{user_file}."
        echo "See the manual chapter \"Running Bacula\" for details."
fi
# now we add the supplementary groups, this is ok to call even if the users already exist
# we only do this if the user is NOT root
IS_ROOT=%{director_daemon_user}
if [ "$IS_ROOT" != "root" ]; then
%{usermod} -G %{daemon_group} %{director_daemon_user}
fi
IS_ROOT=%{storage_daemon_user}
if [ "$IS_ROOT" != "root" ]; then
%{usermod} -G %{daemon_group},%{storage_daemon_group} %{storage_daemon_user}
fi
IS_ROOT=%{file_daemon_user}
if [ "$IS_ROOT" != "root" ]; then
%{usermod} -G %{daemon_group} %{file_daemon_user}
fi
%endif

%if %{mysql}
%post mysql
%endif
%if %{sqlite}
%post sqlite
%endif
%if %{postgresql}
%post postgresql
%endif

%if ! %{client_only}
# add our links
if [ "$1" -ge 1 ] ; then
/sbin/chkconfig --add bacula-dir
/sbin/chkconfig --add bacula-fd
/sbin/chkconfig --add bacula-sd
fi
%endif

%if %{mysql}
# test for an existing database
# note: this ASSUMES no password has been set for bacula database
DB_VER=`mysql 2>/dev/null bacula -e 'select * from Version;'|tail -n 1`

# grant privileges and create tables if they do not exist
if [ -z "$DB_VER" ]; then
        echo "Hmm, doesn't look like you have an existing database."
        echo "Granting privileges for MySQL user bacula..."
	%{script_dir}/grant_mysql_privileges
        echo "Creating MySQL bacula database..."
	%{script_dir}/create_mysql_database
        echo "Creating bacula tables..."
	%{script_dir}/make_mysql_tables

# check to see if we need to upgrade a 1.38 or lower database
elif [ "$DB_VER" -lt "10" ]; then
        echo "This release requires an upgrade to your bacula database."
        echo "Backing up your current database..."
        mysqldump -f --opt bacula | bzip2 > %{working_dir}/bacula_backup.sql.bz2
        echo "Upgrading bacula database ..."
	%{script_dir}/update_mysql_tables
        echo "If bacula works correctly you can remove the backup file %{working_dir}/bacula_backup.sql.bz2"

fi
%endif

%if %{sqlite}
# test for an existing database
if [ -s %{working_dir}/bacula.db ]; then
        DB_VER=`echo "select * from Version;" | %{sqlite_bindir}/sqlite3 2>/dev/null %{working_dir}/bacula.db | tail -n 1`
        # check to see if we need to upgrade a 1.38 or lower database
        if [ "$DB_VER" -lt "10" ] && [ "$DB_VER" -ge "9" ]; then
                echo "This release requires an upgrade to your bacula database."
                echo "Backing up your current database..."
                echo ".dump" | %{sqlite_bindir}/sqlite3 %{working_dir}/bacula.db | bzip2 > %{working_dir}/bacula_backup.sql.bz2
                echo "Upgrading bacula database ..."
		%{script_dir}/update_sqlite3_tables
                echo "If bacula works correctly you can remove the backup file %{working_dir}/bacula_backup.sql.bz2"
        fi
else
        # create the database and tables
        echo "Hmm, doesn't look like you have an existing database."
        echo "Creating SQLite database..."
	%{script_dir}/create_sqlite3_database
	chown %{director_daemon_user}.%{daemon_group} %{working_dir}/bacula.db
        echo "Creating the SQLite tables..."
	%{script_dir}/make_sqlite3_tables
fi
%endif

%if %{postgresql}
# test for an existing database
# note: this ASSUMES no password has been set for bacula database
DB_VER=`echo 'select * from Version;' | psql bacula 2>/dev/null | tail -3 | head -1`

# grant privileges and create tables if they do not exist
if [ -z "$DB_VER" ]; then
        echo "Hmm, doesn't look like you have an existing database."
        echo "Creating PostgreSQL bacula database..."
	%{script_dir}/create_postgresql_database
        echo "Creating bacula tables..."
	%{script_dir}/make_postgresql_tables
        echo "Granting privileges for PostgreSQL user bacula..."
	%{script_dir}/grant_postgresql_privileges

# check to see if we need to upgrade a 1.38 or lower database
elif [ "$DB_VER" -lt "10" ]; then
        echo "This release requires an upgrade to your bacula database."
        echo "Backing up your current database..."
        pg_dump bacula | bzip2 > %{working_dir}/bacula_backup.sql.bz2
        echo "Upgrading bacula database ..."
	%{script_dir}/update_postgresql_tables
        echo "If bacula works correctly you can remove the backup file %{working_dir}/bacula_backup.sql.bz2"
        
fi
%endif

%if ! %{client_only}
# generate passwords if needed
if [ -d %{sysconf_dir} ]; then
	cd %{sysconf_dir}
        for file in *.conf; do
                for string in XXX_REPLACE_WITH_DIRECTOR_PASSWORD_XXX XXX_REPLACE_WITH_CLIENT_PASSWORD_XXX XXX_REPLACE_WITH_STORAGE_PASSWORD_XXX XXX_REPLACE_WITH_DIRECTOR_MONITOR_PASSWORD_XXX XXX_REPLACE_WITH_CLIENT_MONITOR_PASSWORD_XXX XXX_REPLACE_WITH_STORAGE_MONITOR_PASSWORD_XXX; do
                        need_password=`grep $string $file 2>/dev/null`
                        if [ -n "$need_password" ]; then
                                pass=`openssl rand -base64 33`
                                sed "s-$string-$pass-g" $file > $file.new
                                cp -f $file.new $file; rm -f $file.new
                        fi
                done
        done
fi
%endif

%if %{mysql}
%preun mysql
%endif
%if %{sqlite}
%preun sqlite
%endif
%if %{postgresql}
%preun postgresql
%endif

%if ! %{client_only}
# delete our links
if [ $1 = 0 ]; then
/sbin/chkconfig --del bacula-dir
/sbin/chkconfig --del bacula-fd
/sbin/chkconfig --del bacula-sd
fi
%endif


%if ! %{client_only} && %{mtx}
%files mtx
%defattr(-,root,root)
%attr(-, root, %{storage_daemon_group}) /usr/sbin/loaderinfo
%attr(-, root, %{storage_daemon_group}) /usr/sbin/mtx
%attr(-, root, %{storage_daemon_group}) /usr/sbin/scsitape
%attr(-, root, %{storage_daemon_group}) /usr/sbin/tapeinfo
%attr(-, root, %{storage_daemon_group}) /usr/sbin/nsmhack
%attr(-, root, %{storage_daemon_group}) /usr/sbin/scsieject
%{_mandir}/man1/loaderinfo.1.%{manpage_ext}
%{_mandir}/man1/mtx.1.%{manpage_ext}
%{_mandir}/man1/scsitape.1.%{manpage_ext}
%{_mandir}/man1/tapeinfo.1.%{manpage_ext}
%{_mandir}/man1/scsieject.1.%{manpage_ext}
%endif

%files client
%defattr(-,root,root)
%attr(-, root, %{daemon_group}) %dir %{script_dir}
%attr(-, root, %{daemon_group}) %{script_dir}/bconsole
%{script_dir}/bacula-ctl-fd
/etc/init.d/bacula-fd
%attr(-, root, %{daemon_group}) %{script_dir}/rescue

%doc COPYING ChangeLog ReleaseNotes VERIFYING kernstodo 
%doc %{_docsrc}/manual/bacula.pdf %{_docsrc}/developers/developers.pdf %{_docsrc}/manual/bacula ../Release_Notes-%{version}-%{release}.txt

/etc/logrotate.d/bacula

%attr(-, root, %{daemon_group}) %config(noreplace) %{sysconf_dir}/bacula-fd.conf
%attr(-, root, %{daemon_group}) %config(noreplace) %{sysconf_dir}/bconsole.conf

%attr(-, root, %{daemon_group}) %dir %{working_dir}

/usr/sbin/bacula-fd
/usr/sbin/btraceback
%attr(-, root, %{daemon_group}) %{script_dir}/btraceback.gdb
%attr(-, root, %{daemon_group}) %{script_dir}/btraceback.dbx
/usr/sbin/bconsole
%{_mandir}/man8/bacula-fd.8.%{manpage_ext}
%{_mandir}/man8/bacula.8.%{manpage_ext}
%{_mandir}/man8/bconsole.8.%{manpage_ext}
%{_mandir}/man8/btraceback.8.%{manpage_ext}


%pre client
# create the daemon group and user
HAVE_BACULA=`grep %{daemon_group} %{group_file} 2>/dev/null`
if [ -z "$HAVE_BACULA" ]; then
        %{groupadd} -r %{daemon_group} > /dev/null 2>&1
        echo "The group %{daemon_group} has been added to %{group_file}."
        echo "See the manual chapter \"Running Bacula\" for details."
fi
# we do not use the -g option allowing the primary group to be set to system default
# this will be a unique group on redhat type systems or the group users on some systems
HAVE_BACULA=`grep %{file_daemon_user} %{user_file} 2>/dev/null`
if [ -z "$HAVE_BACULA" ]; then
        %{useradd} -r -c "Bacula" -d %{working_dir} -g %{daemon_group} -M -s /sbin/nologin %{file_daemon_user} > /dev/null 2>&1
        echo "The user %{file_daemon_user} has been added to %{user_file}."
        echo "See the manual chapter \"Running Bacula\" for details."
fi
# now we add the supplementary group, this is ok to call even if the user already exists
# we only do this if the user is NOT root
IS_ROOT=%{file_daemon_user}
if [ "$IS_ROOT" != "root" ]; then
%{usermod} -G %{daemon_group} %{file_daemon_user}
fi

%post client
# add our link
if [ "$1" -ge 1 ] ; then
/sbin/chkconfig --add bacula-fd
fi

# generate passwords if needed
if [ -d %{sysconf_dir} ]; then
	cd %{sysconf_dir}
        for file in *.conf; do
                for string in XXX_REPLACE_WITH_DIRECTOR_PASSWORD_XXX XXX_REPLACE_WITH_CLIENT_PASSWORD_XXX XXX_REPLACE_WITH_STORAGE_PASSWORD_XXX XXX_REPLACE_WITH_DIRECTOR_MONITOR_PASSWORD_XXX XXX_REPLACE_WITH_CLIENT_MONITOR_PASSWORD_XXX XXX_REPLACE_WITH_STORAGE_MONITOR_PASSWORD_XXX; do
                        need_password=`grep $string $file 2>/dev/null`
                        if [ -n "$need_password" ]; then
                                pass=`openssl rand -base64 33`
                                sed "s-$string-$pass-g" $file > $file.new
                                cp -f $file.new $file; rm -f $file.new
                        fi
                done
        done
fi

%preun client
# delete our link
if [ $1 = 0 ]; then
/sbin/chkconfig --del bacula-fd
fi

%if ! %{client_only}
%files updatedb
%defattr(-,root,%{daemon_group})
%{script_dir}/updatedb/*

%pre updatedb
# create the daemon group
HAVE_BACULA=`grep %{daemon_group} %{group_file} 2>/dev/null`
if [ -z "$HAVE_BACULA" ]; then
        %{groupadd} -r %{daemon_group} > /dev/null 2>&1
        echo "The group %{daemon_group} has been added to %{group_file}."
        echo "See the manual chapter \"Running Bacula\" for details."
fi

%post updatedb
echo "The database update scripts were installed to %{script_dir}/updatedb"
%endif

%if %{gconsole}
%files gconsole
%defattr(-,root,root)
/usr/sbin/bgnome-console
%attr(-, root, %{daemon_group}) %dir %{script_dir}
%attr(-, root, %{daemon_group}) %{script_dir}/gconsole
%attr(-, root, %{daemon_group}) %config(noreplace) %{sysconf_dir}/bgnome-console.conf
/usr/share/pixmaps/bacula.png
/usr/share/applications/bacula.desktop
%{_mandir}/man1/bacula-bgnome-console.1.%{manpage_ext}
%endif

%if %{gconsole} && ! %{rh8}
/usr/sbin/bacula-tray-monitor
%config(noreplace) %{sysconf_dir}/tray-monitor.conf
/usr/share/pixmaps/bacula-tray-monitor.xpm
/usr/share/applications/bacula-tray-monitor.desktop
%{_mandir}/man1/bacula-tray-monitor.1.%{manpage_ext}
%endif

%if %{gconsole} && ! %{su9} && ! %{su10} && ! %{su102} && ! %{su103} && ! %{su110}
# add the console helper files
%config(noreplace,missingok) /etc/pam.d/bgnome-console
%config(noreplace,missingok) /etc/security/console.apps/bgnome-console
/usr/bin/bgnome-console
%endif

%if %{gconsole}
%pre gconsole
# create the daemon group
HAVE_BACULA=`grep %{daemon_group} %{group_file} 2>/dev/null`
if [ -z "$HAVE_BACULA" ]; then
        %{groupadd} -r %{daemon_group} > /dev/null 2>&1
        echo "The group %{daemon_group} has been added to %{group_file}."
        echo "See the manual chapter \"Running Bacula\" for details."
fi

%post gconsole
# generate passwords if needed
if [ -d %{sysconf_dir} ]; then
	cd %{sysconf_dir}
        for file in *.conf; do
                for string in XXX_REPLACE_WITH_DIRECTOR_PASSWORD_XXX XXX_REPLACE_WITH_CLIENT_PASSWORD_XXX XXX_REPLACE_WITH_STORAGE_PASSWORD_XXX XXX_REPLACE_WITH_DIRECTOR_MONITOR_PASSWORD_XXX XXX_REPLACE_WITH_CLIENT_MONITOR_PASSWORD_XXX XXX_REPLACE_WITH_STORAGE_MONITOR_PASSWORD_XXX; do
                        need_password=`grep $string $file 2>/dev/null`
                        if [ -n "$need_password" ]; then
                                pass=`openssl rand -base64 33`
                                sed "s-$string-$pass-g" $file > $file.new
                                cp -f $file.new $file; rm -f $file.new
                        fi
                done
        done
fi
%endif

%if %{wxconsole}
%files wxconsole
%defattr(-,root,root)
/usr/sbin/bwx-console
%attr(-, root, %{daemon_group}) %dir %{sysconf_dir}
%attr(-, root, %{daemon_group}) %config(noreplace) %{sysconf_dir}/bwx-console.conf
/usr/share/pixmaps/wxwin16x16.xpm
/usr/share/applications/wxconsole.desktop
%{_mandir}/man1/bacula-bwxconsole.1.%{manpage_ext}
%endif

%if %{wxconsole} && ! %{su9} && ! %{su10} && ! %{su102} && ! %{su103} && ! %{su110}
# add the console helper files
%config(noreplace,missingok) /etc/pam.d/bwx-console
%config(noreplace,missingok) /etc/security/console.apps/bwx-console
/usr/bin/bwx-console
%endif

%if %{wxconsole}
%pre wxconsole
# create the daemon group
HAVE_BACULA=`grep %{daemon_group} %{group_file} 2>/dev/null`
if [ -z "$HAVE_BACULA" ]; then
        %{groupadd} -r %{daemon_group} > /dev/null 2>&1
        echo "The group %{daemon_group} has been added to %{group_file}."
        echo "See the manual chapter \"Running Bacula\" for details."
fi

%post wxconsole
# generate passwords if needed
if [ -d %{sysconf_dir} ]; then
	cd %{sysconf_dir}
        for file in *.conf; do
                for string in XXX_REPLACE_WITH_DIRECTOR_PASSWORD_XXX XXX_REPLACE_WITH_CLIENT_PASSWORD_XXX XXX_REPLACE_WITH_STORAGE_PASSWORD_XXX XXX_REPLACE_WITH_DIRECTOR_MONITOR_PASSWORD_XXX XXX_REPLACE_WITH_CLIENT_MONITOR_PASSWORD_XXX XXX_REPLACE_WITH_STORAGE_MONITOR_PASSWORD_XXX; do
                        need_password=`grep $string $file 2>/dev/null`
                        if [ -n "$need_password" ]; then
                                pass=`openssl rand -base64 33`
                                sed "s-$string-$pass-g" $file > $file.new
                                cp -f $file.new $file; rm -f $file.new
                        fi
                done
        done
fi
%endif

%if %{bat}
%files bat
%defattr(-,root,root)
/usr/sbin/bat
%attr(-, root, %{daemon_group}) %dir %{sysconf_dir}
%attr(-, root, %{daemon_group}) %config(noreplace) %{sysconf_dir}/bat.conf
/usr/share/pixmaps/bat_icon.png
/usr/share/applications/bat.desktop
%{_mandir}/man1/bat.1.%{manpage_ext}
%endif

%if %{bat} && ! %{su9} && ! %{su10} && ! %{su102} && ! %{su103} && ! %{su110}
# add the console helper files
%config(noreplace,missingok) /etc/pam.d/bat
%config(noreplace,missingok) /etc/security/console.apps/bat
/usr/bin/bat
%endif

%if %{bat}
%pre bat
# create the daemon group
HAVE_BACULA=`grep %{daemon_group} %{group_file} 2>/dev/null`
if [ -z "$HAVE_BACULA" ]; then
        %{groupadd} -r %{daemon_group} > /dev/null 2>&1
        echo "The group %{daemon_group} has been added to %{group_file}."
        echo "See the manual chapter \"Running Bacula\" for details."
fi

%post bat
# generate passwords if needed
if [ -d %{sysconf_dir} ]; then
	cd %{sysconf_dir}
        for file in *.conf; do
                for string in XXX_REPLACE_WITH_DIRECTOR_PASSWORD_XXX XXX_REPLACE_WITH_CLIENT_PASSWORD_XXX XXX_REPLACE_WITH_STORAGE_PASSWORD_XXX XXX_REPLACE_WITH_DIRECTOR_MONITOR_PASSWORD_XXX XXX_REPLACE_WITH_CLIENT_MONITOR_PASSWORD_XXX XXX_REPLACE_WITH_STORAGE_MONITOR_PASSWORD_XXX; do
                        need_password=`grep $string $file 2>/dev/null`
                        if [ -n "$need_password" ]; then
                                pass=`openssl rand -base64 33`
                                sed "s-$string-$pass-g" $file > $file.new
                                cp -f $file.new $file; rm -f $file.new
                        fi
                done
        done
fi
%endif

%changelog
* Mon Aug 04 2008 D. Scott Barninger <barninger@fairfieldcomputers.com>
- fix bat dependencies
* Sat Jun 28 2008 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add su110 target
* Sat May 24 2008 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add fc9 target
* Sun Mar 30 2008 D. Scott Barninger <barninger@fairfieldcomputers.com>
- FHS compatibility changes
* Sat Feb 16 2008 D. Scott Barninger <barninger@fairfieldcomputers.com>
- remove fix for false buffer overflow detection with glibc >= 2.7
* Sat Feb 09 2008 D. Scott Barninger <barninger@fairfieldcomputers.com>
- fix for false buffer overflow detection with glibc >= 2.7
* Sun Jan 27 2008 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 2.2.8 release
- add debug package for SuSE
* Sat Jan 12 2008 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 2.2.8 beta release  
- fix bug 1037
- add fc8 target
* Sun Dec 30 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- fix typo on su103 client package requirements
* Fri Dec 28 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add nobuild_mtx switch
- add patch for postgresql.c for old postgresql versions
* Sat Nov 17 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- switch to sqlite3
* Sun Nov 11 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add new files required by rescue makefile
* Sat Nov 10 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add su103 build target
* Sun Nov 04 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- fix dist defines for rhel5 and clones
- fix rhel broken 64 bit QT4 paths
- rh qt4 packages don't provide qt so fix that too
* Mon Oct 29 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- correct ownership when creating sqlite db file in post script
* Sun Sep 16 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- fix disable-batch-insert
* Fri Sep 14 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 2.2.4 release
- turn off gconsole build for fc3, tray monitor fails to build
- add new files for mtx package (09Sep07 depkgs update)
* Sat Sep 08 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add --disable-batch-insert for older platforms
- add build targets for rhel5 and clones
* Mon Sep 03 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 2.2.1 release
- turn off gconsole build for su10 & fc4, tray monitor fails to build
* Sat Jul 14 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 2.1.26 add make of qwt in depkgs for bat
* Sat Jun 02 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- upgrade Qt requirement for bat to 4.2
* Sun May 06 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add fc7 build target
* Sun Apr 29 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 2.1.8
- gnome-console now bgnome-console
- wxconsole now bwx-console
- add build option for bat
* Sat Apr 08 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- merge Otto Mueller's patch but keep script dir set to /etc/bacula
- add build tag for Scientific Linux per Jon Peatfield <J.S.Peatfield@damtp.cam.ac.uk>
* Tue Mar 27 2007 Otto Mueller <otto.mueller@bundestag.de>
- adjust directory locations for FHS-compatibility
  sysconf_dir (/etc/bacula), script_dir (/usr/lib/bacula),
  working_dir (/var/lib/bacula) and pid_dir (/var/run)
* Mon Feb 26 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add SuSE 10.2 target
* Sat Jan 20 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- correct bug 752
- set query.sql as config file
- correct bug 754
* Sun Jan 14 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 2.0.1 release
- change determination of gcc version per patch from Marc Hennes
- move BuildRequire for atk-devel to gnome only builds
- add fc6 build tag
* Sat Jan 06 2007 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 2.0.0 release
* Sun Oct 15 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 1.39.26 remove create_sqlite_database.in.patch
* Sun Sep 24 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- change ownership of working_dir on server packages to bacula.bacula so that
- bacula-sd can create bootstrap files
* Sat Sep 02 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 1.39.22 remove separate cd and make of manpages the main Makefile does it now
* Sun Aug 06 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- fix manpages file extension for mdk
* Sat Aug 05 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- bug 648 re-enable and update sqlite patches
- 1.39.18 changes
- updatedb 9 to 10
- install man pages
- lock out gconsole build for gtk+ < 2.4
* Mon Jul 17 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- move pango-devel BuildRequires into gconsole only build
* Sat Jul 15 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add provides and conflicts for standard suse packages
- add third party packager tag support
- add build_client_only tag
- remove bsmtp from client package
- add bacula-ctl-fd to client package
* Thu Jul 13 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- fix directory creation when wxconsole and not gconsole
* Tue Jul 04 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add check to buildrequires to make sure libstdc++ version matches gcc
* Mon Jul 03 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add python build support
- fix LDFLAGS declarations
* Sun Jul 02 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add requires for standard compiler toolchain
- move version and release tags up
- move patches up
- add docs_version tag
* Sat Jul 01 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- update rescuever to 1.8.6
* Sun Jun 25 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- update depkgs to 25Jun06
- add mysql5 build tag
* Mon Jun 12 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 1.38.10 bump rescue version
* Sun Jun 03 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- fix usermod statements
- add fc5 target
* Thu Apr 27 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add -g param back to useradd statements Bug 605
* Mon Apr 17 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- redundant code cleanup
* Sun Apr 16 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add wxconsole package
* Fri Apr 14 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 1.38.8 release
- dependency update for Mandriva
* Sun Apr 08 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 1.38.7 release
- remove -n option from useradd scripts
* Sun Apr 02 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 1.38.6 release
- fix problem specifying more than one primary group for user bacula
- add build switch to not build gconsole regardless of platform
* Sun Jan 29 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add centos3 build tag
- fix link error of static-fd on Mandrake with --disable-nls
* Fri Jan 27 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add fc4 dependencies
* Mon Jan 23 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add SuSE 10.0 build
- remove specific permission in attrib macros
* Sat Jan 21 2006 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 1.38.5 release
- fix usermode required on suse, suse doesn't have usermode (xsu instead)
- refix compat for _dist on SLES9 which seems to have been removed
- added note regarding Aleksandar's use of specific permissions in attrib macros
- need to review and add specific fc4 build currently using fc3 Requires
* Wed Dec 14 2005 Aleksandar Milivojevic <alex@milivojevic.org>
- 1.38.2 release
- Reorganize files and pre/post sections to remove repetitions
- Always build separate mtx package
- Fix file ownerships for /etc/bacula and Bacula's working dir
* Wed Nov 23 2005 Aleksandar Milivojevic <alex@milivojevic.org>
- Disable GNOME on RH7
* Fri Nov 18 2005 Aleksandar Milivojevic <alex@milivojevic.org>
- Red Hat and look alikes have mtx RPM, do not build/package our version
* Sun Nov 13 2005 D. Scott Barninger <barninger@fairfieldcomputers.com>
- minor edit to _dist for SLES9 compatibility
* Sat Nov 05 2005 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 1.38.0 release
- kern changed location of pdf files and html manual in docs package
* Sun Oct 30 2005 D. Scott Barninger <barninger@fairfieldcomputers.com>
- 1.38.0 release
- add docs (from prebuilt tarball) and rescue packages back in
- remove dvd-freespace and dvd-writepart files, add dvd-handler
- remove 3 of 4 sqlite script patches as not needed
* Sun Jul 24 2005 D. Scott Barninger <barninger@fairfieldcomputers.com>
- changes for 1.38
- remove docs and rescue sections (remove static fd)
- add dvd-freespace and dvd-writepart files
- update depkgs to 22Jun05
- change database update to 8 to 9
* Sun Jul 24 2005 D. Scott Barninger <barninger@fairfieldcomputers.com>
- minor cleanups before 1.38 changes
- add popt and popt-devel build dependencies
- add tetex and tetex-dvips dependencies for doc build
- replace deprecated Copyright tag with License
* Sat May 07 2005 D. Scott Barninger <barninger@fairfieldcomputers.com>
- move sqlite installation bindir to /usr/lib/bacula/sqlite and remove
- conflict with sqlite packages. remove readline dependency.
* Sun Apr 17 2005 D. Scott Barninger <barninger@fairfieldcomputers.com>
- release 1.36.3 update docs
* Tue Apr 05 2005 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add centos4 build tag
- add x86_64 build tag
* Sun Apr 03 2005 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add rhel4 build tag
- clean up for mysql4 which is now mdk-10.1, suse-9.2 and rhel4
* Sun Mar 06 2005 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add rhel3 build tag
* Tue Mar 01 2005 D. Scott Barninger <barninger@fairfieldcomputers.com>
- fix tray-monitor.conf for noreplace
* Mon Feb 28 2005 D. Scott Barninger <barninger@fairfieldcomputers.com>
- fix distribution check for Fedora and Whitebox
* Sun Feb 06 2005 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add logwatch script
- add dvd scripts
* Sat Jan 15 2005 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add build for Fedora Core 3 (linc now included in ORDit2)
- add mysql4 define for Mandrake 10.1
* Fri Jan 14 2005 D. Scott Barninger <barninger@fairfieldcomputers.com>
- fix {group_file} variable in post scripts
* Thu Dec 30 2004 D. Scott Barninger <barninger@fairfieldcomputers.com>
- add distribution checking and custom Distribution tag
* Thu Dec 09 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- ASSIGNMENT OF COPYRIGHT
- FOR VALUE RECEIVED, D. Scott Barninger hereby sells, transfers and 
- assigns unto Kern Sibbald, his successors, assigns and personal representatives, 
- all right, title and interest in and to the copyright in this software RPM
- spec file. D. Scott Barninger warrants good title to said copyright, that it is 
- free of all liens, encumbrances or any known claims against said copyright.
* Sat Dec 04 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- bug 183 fixes
- thanks to Daniel Widyono
- update description for rescue package to describe cdrom creation
* Thu Nov 18 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- update depkgs to 29Oct04
* Fri Nov 12 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- add cdrom rescue to bacula-rescue package
* Sun Oct 31 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- misc fixes from 1.36.0 suse feedback
- fix situation where sqlite database exists but sqlite has been removed.
* Fri Oct 22 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- remove tray-monitor from RH8 build
- fix permissions on tray-monitor files
* Wed Oct 13 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- add Mandrake support and tray-monitor, misc changes for 1.35.8/1.36.0,
- change database update to 7 to 8 upgrade,
- revert depkgs to 08Mar04 as there seems to be a bug in the sqlite
- build in 30Jul04, add freetype dependancy to gnome package.
* Sun Sep 12 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- add documentation to console for groupadd
* Sat Sep 04 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- add support for running daemons as root.bacula
- correct for change in location of floppy rescue files in 1.35.2
- removed /etc/bacula/fd script from all packages as it has disappeared from 1.35.2
- updated depgkgs to 30Jul04
* Thu Jun 24 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- really, really fix symlink creation for gconsole
* Thu Jun 17 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- fix symlink creation in gconsole post install
* Sat Jun 12 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- fixed error in gconsole post script
* Fri Apr 30 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- add check for gconsole symlink before trying to create it
* Sun Apr 11 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- fix some minor permissions issues on doc files that CVS won't let us fix
* Sun Apr 04 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- add pkgconfig to BuildRequires
- clean up gnome1/2 menu entries for appropriate packages
* Fri Apr 02 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- tightened up doc distribution
* Tue Mar 30 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- added usermode (Redhat) and xsu (SuSE) support for gnome-console;
- rpm's horrible bug that prevents nested conditional macros prevents me
- from implementing these 2 separate approaches within the conditionals which
- create the separate server packages.
- the solution adopted is to remove the gnome-console files from the server packages
- so bacula-gconsole is now an add on for both client and server packages.
- this also now allows the server packages to be install on machines without
- an X-server and we can still maintain a single spec file.
- added tests to make sure we have defined platform and database macros.
* Sat Mar 13 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- corrected mysql prerequisites for suse
* Mon Mar 1 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- replaced all cp commands with cp -p
- removed addition of a+x permissions on gnome-console
- corrected permissions on init scripts
* Sat Feb 28 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- corrected creation of sqlite_bindir in install from !mysql to sqlite
-
- various cleanup patches from Michael K. Johnson:
- corrected post install routines for nicer chkconfig
- removed chmod changes in post routines and moved to install section
- removed interactive nature of post routine for rescue package
- added description of building rescue disks to the description of rescue package
- added clean of build root to beginning of install
- removed specifying attr in all file lists
* Fri Feb 20 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- added bconsole to client package
- added gconsole package as add-on to client
- removed spurious dependancies on updatedb package (!cut/paste)
* Thu Feb 19 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- added updatedb package
* Thu Feb 12 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- added postgresql package
* Wed Feb 11 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- corrected the if else logic in the dependancy sections
- changes for 1.34 release
- /etc/bacula/console is now /etc/bacula/bconsole
- /etc/bacula/console.conf is now /etc/bacula/bconsole.conf
- /usr/sbin/btraceback.gdb is now /etc/bacula/btraceback.gdb
- /usr/sbin/smtp is now /usr/sbin/bsmtp
- added new /etc/bacula/drop_mysql_database
- added new /etc/bacula/drop_sqlite_database
- added new /etc/bacula/grant_sqlite_privileges
- added new generic bacula database scripts in /etc/bacula
- added pre-install sections to check for database versions older than 6
- added check for /etc/bacula/console.conf and copy to bconsole.conf
* Sun Feb 08 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- added /etc/bacula/update_sqlite_tables and /etc/bacula/update_mysql_tables for 1.34 release
- added testing for existing databases before executing any of the database creation scripts
- added defines working_dir and sqlite_bindir in place of hard coded paths
* Sat Jan 31 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- added build configuration for SuSE.
- Thanks to Matt Vollmar <matt at panamschool.edu.sv> for his input
* Sat Jan 24 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- added patch for create_sqlite_database to fix the installed bindir
- added execute of create_sqlite_database to post of sqlite package
* Sat Jan 10 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- added virtual package Provides bacula-dir, bacula-sd, bacula-fd
- added bacula-fd as Requires for rescue package
- added build tag for Fedora Core 1
- cleaned up dependancies for all builds
* Thu Jan 1 2004 D. Scott Barninger <barninger at fairfieldcomputers.com>
- removed rh_version from package names
- added platform build configuration section to beginning of file
* Tue Nov 25 2003 D. Scott Barninger <barninger at fairfieldcomputers.com>
- removed make_static_bacula script from rescue package install
* Sun Nov 23 2003 D. Scott Barninger <barninger at fairfieldcomputers.com>
- Added define at top of file for depkgs version
- Added rescue sub-package
- Moved requires statements into proper sub-package locations
* Mon Oct 27 2003 D. Scott Barninger <barninger at fairfieldcomputers.com>
- Corrected Requires for Gnome 1.4/2.0 builds
* Fri Oct 24 2003 D. Scott Barninger <barninger at fairfieldcomputers.com>
- Added separate source declaration for depkgs
- added patch for make_catalog_backup script
* Mon May 11 2003 D. Scott Barninger <barninger at fairfieldcomputers.com>
- Misc changes to mysql/sqlite build and rh7/8 menu differences
- Added rh_version to sub-package names
- Added installed but missing file /etc/bacula/gconsole
- rm'd /etc/bacula/grant_mysql_privileges on sqlite builds
* Thu May 08 2003 Kern Sibbald <kern at sibbald.com>
- Update spec for version 1.31 and combine client
* Sun Mar 30 2003 D. Scott Barninger <barninger at fairfieldcomputers.com>
- Initial spec file
