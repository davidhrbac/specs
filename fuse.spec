Name:           fuse
Version:        2.8.1
Release:        1%{?dist}
Summary:        File System in Userspace (FUSE) utilities

Group:          System Environment/Base
License:        GPL+
URL:            http://fuse.sf.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        fuse-udev.nodes
Source2:        fuse-makedev.d-fuse

Patch0:         fuse-udev_rules.patch
Patch1:         fuse-openfix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       kernel
Requires:       which
BuildRequires:  libselinux-devel

Requires(post):  MAKEDEV
Requires(preun): chkconfig
Requires(preun): initscripts

%description
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE userspace tools to
mount a FUSE filesystem.

%package libs
Summary:        File System in Userspace (FUSE) libraries
Group:          System Environment/Libraries
License:        LGPLv2+

%description libs
Devel With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE libraries.


%package devel
Summary:        File System in Userspace (FUSE) devel files
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig
License:        LGPLv2+

%description devel
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains development files (headers,
pgk-config) to develop FUSE based applications/filesystems.


%prep
%setup -q
#disable device creation during build/install
sed -i 's|mknod|echo Disabled: mknod |g' util/Makefile.in
%patch0 -p0 -b .patch0
%patch1 -p0 -b .patch1

%build
# Can't pass --disable-static here, or else the utils don't build
%configure \
 --libdir=/%{_lib} \
 --bindir=/bin \
 --exec-prefix=/
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
# FIXME change from 60 to 99
install -D -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/udev/makedev.d/99-fuse.nodes
install -D -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/makedev.d/z-fuse
# change from 4755 to 0755 to allow stripping -- fixed later in files
chmod 0755 $RPM_BUILD_ROOT/bin/fusermount
# Put pc file in correct place
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/%{_lib}/pkgconfig $RPM_BUILD_ROOT%{_libdir}

# Get rid of static libs
rm -f $RPM_BUILD_ROOT/%{_lib}/*.a
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/init.d/fuse

# Compatibility symlinks
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cd $RPM_BUILD_ROOT%{_bindir}
ln -s /bin/fusermount fusermount
ln -s /bin/ulockmgr_server ulockmgr_server

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/MAKEDEV fuse

%preun
if [ -f /etc/init.d/fuse ] ; then
    /sbin/service fuse stop >/dev/null 2>&1
    /sbin/chkconfig --del fuse
fi


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ Filesystems NEWS README README.NFS
/sbin/mount.fuse
%attr(4755,root,root) /bin/fusermount
/bin/ulockmgr_server
%{_sysconfdir}/makedev.d/z-fuse
# Compat symlinks
%{_bindir}/fusermount
%{_bindir}/ulockmgr_server
%config %{_sysconfdir}/udev/rules.d/99-fuse.rules
%config %{_sysconfdir}/udev/makedev.d/99-fuse.nodes

%files libs
%defattr(-,root,root,-)
%doc COPYING.LIB
/%{_lib}/libfuse.so.*
/%{_lib}/libulockmgr.so.*

%files devel
%defattr(-,root,root,-)
/%{_lib}/libfuse.so
/%{_lib}/libulockmgr.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/fuse.h
%{_includedir}/ulockmgr.h
%{_includedir}/fuse

%changelog
* Wed Nov 11 2009 David Hrbáč <david@hrbac.cz> - 2.8.1-1
- initial rebuild

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> 2.8.1-1
- Ver. 2.8.1

* Wed Aug 19 2009 Peter Lemenkov <lemenkov@gmail.com> 2.8.0-1
- Ver. 2.8.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Peter Lemenkov <lemenkov@gmail.com> 2.7.4-2
- Fixed BZ#479581

* Sat Aug 23 2008 Peter Lemenkov <lemenkov@gmail.com> 2.7.4-1
- Ver. 2.7.4

* Sat Jul 12 2008 Peter Lemenkov <lemenkov@gmail.com> 2.7.3-3
- Fixed initscripts (BZ#441284)

* Thu Feb 28 2008 Peter Lemenkov <lemenkov@gmail.com> 2.7.3-2
- Fixed BZ#434881

* Wed Feb 20 2008 Peter Lemenkov <lemenkov@gmail.com> 2.7.3-1
- Ver. 2.7.3
- Removed usergroup fuse
- Added chkconfig support (BZ#228088)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.7.2-2
- Autorebuild for GCC 4.3

* Mon Jan 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.2-1
- bump to 2.7.2
- fix license tag

* Sun Nov  4 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-9
- fix initscript to work with chkconfig

* Mon Oct  1 2007 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-8
- Added Require: which (BZ#312511)

* Fri Sep 21 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-7
- revert udev rules change

* Thu Sep 20 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-6
- change udev rules so that /dev/fuse is chmod 666 (bz 298651)

* Wed Aug 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-5
- fix open issue (bz 265321)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.7.0-4
- Rebuild for selinux ppc32 issue.

* Sun Jul 22 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-3
- put pkgconfig file in correct place
- enable compat symlinks for files in /bin

* Sat Jul 21 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-2
- redefine exec_prefix to /
- redefine bindir to /bin
- redefine libdir to %%{_lib}
- don't pass --disable-static to configure
- manually rm generated static libs

* Wed Jul 18 2007 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-1
- Version 2.7.0
- Redefined exec_prefix due to demands from NTFS-3G

* Wed Jun  6 2007 Peter Lemenkov <lemenkov@gmail.com> 2.6.5-2
- Add BR libselinux-devel (bug #235145)
- Config files properly marked as config (bug #211122)

* Sat May 12 2007 Peter Lemenkov <lemenkov@gmail.com> 2.6.5-1
- Version 2.6.5

* Thu Feb 22 2007 Peter Lemenkov <lemenkov@gmail.com> 2.6.3-2
- Fixed bug #229642

* Wed Feb  7 2007 Peter Lemenkov <lemenkov@gmail.com> 2.6.3-1
* Ver. 2.6.3

* Tue Dec 26 2006 Peter Lemenkov <lemenkov@gmail.com> 2.6.1-1
- Ver. 2.6.1

* Sat Nov 25 2006 Peter Lemenkov <lemenkov@gmail.com> 2.6.0-2
- fixed nasty typo (see bug #217075)

* Fri Nov  3 2006 Peter Lemenkov <lemenkov@gmail.com> 2.6.0-1
- Ver. 2.6.0

* Sun Oct 29 2006 Peter Lemenkov <lemenkov@gmail.com> 2.5.3-5
- Fixed udev-rule again

* Sat Oct  7 2006 Peter Lemenkov <lemenkov@gmail.com> 2.5.3-4
- Fixed udev-rule

* Tue Sep 12 2006 Peter Lemenkov <lemenkov@gmail.com> 2.5.3-3%{?dist}
- Rebuild for FC6

* Wed May 03 2006 Peter Lemenkov <lemenkov@newmail.ru> 2.5.3-1%{?dist}
- Update to 2.5.3

* Thu Mar 30 2006 Peter Lemenkov <lemenkov@newmail.ru> 2.5.2-4%{?dist}
- rebuild

* Mon Feb 13 2006 Peter Lemenkov <lemenkov@newmail.ru> - 2.5.2-3
- Proper udev rule

* Mon Feb 13 2006 Peter Lemenkov <lemenkov@newmail.ru> - 2.5.2-2
- Added missing requires

* Tue Feb 07 2006 Peter Lemenkov <lemenkov@newmail.ru> - 2.5.2-1
- Update to 2.5.2
- Dropped fuse-mount.fuse.patch

* Wed Nov 23 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.4.2-1
- Use dist

* Wed Nov 23 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.4.2-1
- Update to 2.4.2 (solves CVE-2005-3531)
- Update README.fedora

* Sat Nov 12 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.4.1-3
- Add README.fedora
- Add hint to README.fedora and that you have to be member of the group "fuse"
  in the description
- Use groupadd instead of fedora-groupadd

* Fri Nov 04 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.4.1-2
- Rename packages a bit
- use makedev.d/40-fuse.nodes
- fix /sbin/mount.fuse
- Use a fuse group to restict access to fuse-filesystems

* Fri Oct 28 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.4.1-1
- Initial RPM release.
