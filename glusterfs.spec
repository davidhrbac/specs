#define pre rc8
## NOTE: Lots of files in various subdirectories have the same name (such as
## "LICENSE") so this short macro allows us to distinguish them by using their
## directory names (from the source tree) as prefixes for the files.
## Usage: add_to_doc_files subdirname files
%define add_to_doc_files() \
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}-%{version}/%1 ||: ; \
%{__cp} -p %2 %{buildroot}%{_docdir}/%{name}-%{version}/%1 

# Possible rpmbuild options
%{?_without_ibverbs:%define _without_ibverbs --disable-ibverbs}
%{?_without_client:%define _without_client --disable-fuse-client}
%{?_without_python:%define _without_python --disable-python}

# Disable the python bindings if we have < 2.4, since 2.4+ is required
%if "%(%{__python} -c "import sys ; print sys.version[:3]")" < "2.4"
%define _without_python --disable-python
%endif

Summary: 	Cluster File System
Name: 		glusterfs
Version: 	2.0.9
Release: 	1%{?pre:.%{pre}}%{?dist}
License: 	GPLv3+
Group: 		System Environment/Base
URL: 		http://www.gluster.org/
Source0: 	http://ftp.gluster.com/pub/gluster/glusterfs/2.0/%{version}/glusterfs-%{version}%{?pre}.tar.gz
Source1: 	glusterfsd.init
Source2: 	glusterfsd.sysconfig
Source3: 	umount.glusterfs
Source4: 	glusterfs.logrotate
Source5: 	glusterfsd.logrotate
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service, /sbin/chkconfig
Requires(postun): /sbin/service
%{!?_without_ibverbs:BuildRequires: libibverbs-devel}
%{!?_without_client:BuildRequires: fuse-devel}
%{!?_without_python:BuildRequires: python-devel}
BuildRequires: 	flex, bison, byacc

%description
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file system in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in userspace and easily manageable.


%package common
Summary: 	GlusterFS common files for both the client and the server
Group: 		System Environment/Libraries
Obsoletes: 	glusterfs-libs < 2.0.0
Provides: 	glusterfs-libs = %{version}-%{release}

%description common
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file system in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in userspace and easily manageable.

This package includes the glusterfs binary, libglusterfs and glusterfs
translator modules common to both GlusterFS server and client framework.


%package client
Summary: 	GlusterFS Client
Group: 		Applications/File
Requires: 	fuse
Requires: 	%{name}-common = %{version}-%{release}

%description client
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file system in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in userspace and easily manageable.

This package provides the FUSE based GlusterFS client.


%package server
Summary: 	GlusterFS Server
Group: 		System Environment/Daemons
Requires: 	%{name}-common = %{version}-%{release}

%description server
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file system in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in userspace and easily manageable.

This package provides the glusterfs server daemon.

%package devel
Summary: 	GlusterFS Development Libraries
Group: 		Development/Libraries
Requires: 	%{name}-common = %{version}-%{release}

%description devel
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file system in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in userspace and easily manageable.

This package provides the development libraries.


%prep
%setup -q -n %{name}-%{version}%{?pre}
# Remove file, it gets re-generated by bison (was causing koji build failures)
rm -f libglusterfs/src/y.tab.c
# Don't get executable sources in the debuginfo package (as of 2.0.0rc7)
chmod -x libglusterfsclient/src/*.{c,h}


%build
# Temp disable stack-protector until upstream fixes code
CFLAGS=`echo "%optflags"|sed 's/-D_FORTIFY_SOURCE=2/-D_FORTIFY_SOURCE=1/'`
%configure %{?_without_ibverbs} %{?_without_client} %{?_without_python}
# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot} examples
%{__make} install DESTDIR=%{buildroot}
%{__mkdir_p} %{buildroot}/var/log/glusterfs
%{__mkdir_p} %{buildroot}%{_includedir}/glusterfs
%{__install} -p -m 0644 libglusterfs/src/*.h \
    %{buildroot}%{_includedir}/glusterfs/

# Remove unwanted files from all of the shared libraries
find %{buildroot}%{_libdir}/glusterfs -name '*.a' -o -name '*.la' | xargs rm -f

# Remove installed docs, we include them ourselves as %%doc
%{__rm} -rf %{buildroot}%{_datadir}/doc/glusterfs/

# Rename the samples, so we can include them as %%config
for file in %{buildroot}%{_sysconfdir}/glusterfs/*.sample; do
  %{__mv} ${file} `dirname ${file}`/`basename ${file} .sample`
done

# Clean up the examples we want to include as %%doc
%{__cp} -a doc/examples examples
%{__rm} -f examples/Makefile*

# Install init script and sysconfig file
%{__install} -D -p -m 0755 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/init.d/glusterfsd
%{__install} -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/sysconfig/glusterfsd

%if 0%{!?_without_client:1}
# Install wrapper umount script
%{__install} -D -p -m 0755 %{SOURCE3} \
    %{buildroot}/sbin/umount.glusterfs
# Client logrotate entry
%{__install} -D -p -m 0644 %{SOURCE4} \
    %{buildroot}%{_sysconfdir}/logrotate.d/glusterfs
%endif

# Server logrotate entry
%{__install} -D -p -m 0644 %{SOURCE5} \
    %{buildroot}%{_sysconfdir}/logrotate.d/glusterfsd

# Install extra documentation
%add_to_doc_files benchmarking extras/benchmarking/{*.c,README,*.sh}


%clean
%{__rm} -rf %{buildroot}


%post common -p /sbin/ldconfig

%postun common -p /sbin/ldconfig


%post server
/sbin/chkconfig --add glusterfsd

%preun server
if [ $1 -eq 0 ]; then
    /sbin/service glusterfsd stop &>/dev/null || :
    /sbin/chkconfig --del glusterfsd
fi

%postun server
if [ $1 -ge 1 ]; then
    /sbin/service glusterfsd condrestart &>/dev/null || :
fi


%files common
%doc AUTHORS ChangeLog COPYING NEWS README extras/{glusterfs-mode.el,glusterfs.vim}
%{_docdir}/%{name}-%{version}/benchmarking
%{_libdir}/glusterfs/
%{_libdir}/*.so.*
%{_sbindir}/glusterfs
%{_sbindir}/glusterfsd
%{_mandir}/man8/glusterfs.8*
%dir /var/log/glusterfs/


%if 0%{!?_without_client:1}
%files client
%config(noreplace) %{_sysconfdir}/logrotate.d/glusterfs
/sbin/mount.glusterfs
/sbin/umount.glusterfs
%endif


%files server
%doc examples/ doc/glusterfs*.vol.sample
%dir %{_sysconfdir}/glusterfs/
%config(noreplace) %{_sysconfdir}/glusterfs/*.vol
%config(noreplace) %{_sysconfdir}/logrotate.d/glusterfsd
%config(noreplace) %{_sysconfdir}/sysconfig/glusterfsd
%{_sysconfdir}/init.d/glusterfsd


%files devel
%{_includedir}/glusterfs/
%{_includedir}/libglusterfsclient.h
%{_datadir}/glusterfs/*
%{_bindir}/glusterfs-volgen
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la
%{_libdir}/*.so


%changelog
* Fri Aug 27 2010 David Hrbáč <david@hrbac.cz> - 2.0.9-1
- new upstream release

* Thu Nov 19 2009 David Hrbáč <david@hrbac.cz> - 2.0.8-1
- initial release

* Sat Nov 8 2009 Jonathan Steffan <jsteffan@fedoraproject.org> - 2.0.8-1
- Update to 2.0.8
- Remove install of glusterfs-volgen, it's properly added to
  automake upstream now

* Sat Oct 31 2009 Jonathan Steffan <jsteffan@fedoraproject.org> - 2.0.7-1
- Update to 2.0.7
- Install glusterfs-volgen, until it's properly added to automake
  by upstream
- Add macro to be able to ship more docs

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> 2.0.6-2
- Rebuilt with new fuse

* Sat Sep 12 2009 Matthias Saou <http://freshrpms.net/> 2.0.6-1
- Update to 2.0.6.
- No longer default to disable the client on RHEL5 (#522192).
- Update spec file URLs.

* Mon Jul 27 2009 Matthias Saou <http://freshrpms.net/> 2.0.4-1
- Update to 2.0.4.

* Thu Jun 11 2009 Matthias Saou <http://freshrpms.net/> 2.0.1-2
- Remove libglusterfs/src/y.tab.c to fix koji F11/devel builds.

* Sat May 16 2009 Matthias Saou <http://freshrpms.net/> 2.0.1-1
- Update to 2.0.1.

* Thu May  7 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-1
- Update to 2.0.0 final.

* Wed Apr 29 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-0.3.rc8
- Move glusterfsd to common, since the client has a symlink to it.

* Fri Apr 24 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-0.2.rc8
- Update to 2.0.0rc8.

* Sun Apr 12 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-0.2.rc7
- Update glusterfsd init script to the new style init.
- Update files to match the new default vol file names.
- Include logrotate for glusterfsd, use a pid file by default.
- Include logrotate for glusterfs, using killall for lack of anything better.

* Sat Apr 11 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-0.1.rc7
- Update to 2.0.0rc7.
- Rename "libs" to "common" and move the binary, man page and log dir there.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-0.1.rc1
- Update to 2.0.0rc1.
- Include new libglusterfsclient.h.

* Mon Feb 16 2009 Matthias Saou <http://freshrpms.net/> 1.3.12-1
- Update to 1.3.12.
- Remove no longer needed ocreat patch.

* Thu Jul 17 2008 Matthias Saou <http://freshrpms.net/> 1.3.10-1
- Update to 1.3.10.
- Remove mount patch, it's been included upstream now.

* Fri May 16 2008 Matthias Saou <http://freshrpms.net/> 1.3.9-1
- Update to 1.3.9.

* Fri May  9 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-1
- Update to 1.3.8 final.

* Tue Apr 23 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.10
- Include short patch to include fixes from latest TLA 751.

* Mon Apr 22 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.9
- Update to 1.3.8pre6.
- Include glusterfs binary in both the client and server packages, now that
  glusterfsd is a symlink to it instead of a separate binary.

* Sun Feb  3 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.8
- Add python version check and disable bindings for version < 2.4.

* Sun Feb  3 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.7
- Add --without client rpmbuild option, make it the default for RHEL (no fuse).
  (I hope "rhel" is the proper default macro name, couldn't find it...)

* Wed Jan 30 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.6
- Add --without ibverbs rpmbuild option to the package.

* Mon Jan 14 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.5
- Update to current TLA again, patch-636 which fixes the known segfaults.

* Thu Jan 10 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.4
- Downgrade to glusterfs--mainline--2.5--patch-628 which is more stable.

* Tue Jan  8 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.3
- Update to current TLA snapshot.
- Include umount.glusterfs wrapper script (really needed? dunno).
- Include patch to mount wrapper to avoid multiple identical mounts.

* Sun Dec 30 2007 Matthias Saou <http://freshrpms.net/> 1.3.8-0.1
- Update to current TLA snapshot, which includes "volume-name=" fstab option.

* Mon Dec  3 2007 Matthias Saou <http://freshrpms.net/> 1.3.7-6
- Re-add the /var/log/glusterfs directory in the client sub-package (required).
- Include custom patch to support vol= in fstab for -n glusterfs client option.

* Mon Nov 26 2007 Matthias Saou <http://freshrpms.net/> 1.3.7-4
- Re-enable libibverbs.
- Check and update License field to GPLv3+.
- Add glusterfs-common obsoletes, to provide upgrade path from old packages.
- Include patch to add mode to O_CREATE opens.

* Thu Nov 22 2007 Matthias Saou <http://freshrpms.net/> 1.3.7-3
- Remove Makefile* files from examples.
- Include RHEL/Fedora type init script, since the included ones don't do.

* Wed Nov 21 2007 Matthias Saou <http://freshrpms.net/> 1.3.7-1
- Major spec file cleanup.
- Add misssing %%clean section.
- Fix ldconfig calls (weren't set for the proper sub-package).

* Sat Aug 4 2007 Matt Paine <matt@mattsoftware.com> - 1.3.pre7
- Added support to build rpm without ibverbs support (use --without ibverbs
  switch)

* Sun Jul 15 2007 Matt Paine <matt@mattsoftware.com> - 1.3.pre6
- Initial spec file

