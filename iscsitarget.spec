%define snapshotrev 1266

# Generate version information for kernel module
%{!?kernel:	%define kernel %(uname -r)}

%define kver  %(echo %{kernel} | sed -e 's/smp//' -e 's/bigmem//' -e 's/enterprise//')
%define ktype %(echo kernel-%{kernel}|sed -e 's/%{kver}//' -e 's/-$//')
%define krel  %(echo %{kver} | sed -e 's/-/_/g')

Summary: iSCSI Enterprise Target 
Name: iscsitarget
Version: 0.4.13
Release: %{?snapshotrev: 0.%{snapshotrev}.}1
License: GPL
Group: System Environment/Daemons
URL: http://sourceforge.net/projects/iscsitarget/
Packager: Bastiaan Bakker <bastiaan.bakker@lifeline.nl>
%if %{snapshotrev}
Source0: http://www.zaal.org/iscsi/iet/%{version}/r%{snapshotrev}.tar.gz
%else
Source0: %{name}-%{version}.tar.gz
%endif
Patch1: %{name}-r1266-condrestart.patch
# kernel compatibility patches
# unlocked_ioctl API change
Patch2610: %{name}-0.4.12-kernel-compat-2.6.10.patch
# __nlmsg_put API change
Patch2612: %{name}-r1257-kernel-compat-2.6.12.patch
BuildRequires: %{ktype}-devel = %{kver}, gcc, /usr/bin/install, openssl-devel
Requires: %{name}-kernel-module = %{version}

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%define servicename iscsi-target

%description
iSCSI Enterprise Target

%package %{ktype}
Summary: iSCSI Enterprise Target kernel module
Group: System Environment/Kernel
Release: %{release}_%{krel}
Requires: %{ktype} = %{kver}
Provides: %{name}-kernel-module

%description %{ktype}
iSCSI Enterprise Target kernel module

%prep
%setup %{?snapshotrev: -n r%{snapshotrev}}
%patch1 -p0
%patch2610 -p0
%patch2612 -p0

%build
make KERNELSRC=/lib/modules/%{kernel}/build

%install
%{__rm} -rf %{buildroot}

install -d %{buildroot}/etc/rc.d/init.d
ln -s rc.d/init.d %{buildroot}/etc/init.d
make install KERNELSRC=/lib/modules/%{kernel}/build DISTDIR=%{buildroot}
rm %{buildroot}/etc/init.d
install -m 644 -D etc/ietd.conf %{buildroot}/etc/ietd.conf
install -m 644 -D etc/initiators.allow %{buildroot}/etc/initiators.allow
install -m 644 -D etc/initiators.deny %{buildroot}/etc/initiators.deny
install -m 644 -D doc/manpages/ietd.8 %{buildroot}%{_mandir}/man8/ietd.8
install -m 644 -D doc/manpages/ietd.conf.5 %{buildroot}%{_mandir}/man5/ietd.conf.5

%clean
%{__rm} -rf %{buildroot}

%post
umask 022

/sbin/chkconfig --add %{servicename}
exit 0

%preun
umask 022
if [ "$1" = 0 ]; then
    /sbin/service %{servicename} stop &>/dev/null
    /sbin/chkconfig --del %{servicename}
fi
exit 0

%postun
if [ "$1" != 0 ]; then
    /sbin/service %{servicename} condrestart 2>&1 > /dev/null
fi
exit 0

%post %{ktype}
/sbin/depmod %{kernel} -A

%preun %{ktype}
modprobe -r -q --set-version %{kernel} iscsi_trgt
/sbin/depmod %{kernel} -A

%files
%defattr(-, root, root, 0755)
/usr/sbin/ietd
/usr/sbin/ietadm
/etc/rc.d/init.d/iscsi-target
%defattr(-, root, root, 0644)
%config(noreplace) /etc/ietd.conf
%config(noreplace) /etc/initiators.allow
%config(noreplace) /etc/initiators.deny
%doc COPYING README
%{_mandir}/man?/*

%files %{ktype}
%defattr(-, root, root, 0744)
/lib/modules/%{kernel}/kernel/iscsi/iscsi_trgt.ko

%changelog
* Mon Nov 21 2005 Bastiaan Bakker <bastiaan.bakker@lifeline.nl> - 0.4.13-0.1266.1
- upstream snapshot 1266
- added condrestart patch
- stop and start service on update or removal

* Sun Nov 13 2005 Bastiaan Bakker <bastiaan.bakker@lifeline.nl> - 0.4.13-0.1264.2
- run %post and %preun for kernel package, not main package

* Sun Nov 13 2005 Bastiaan Bakker <bastiaan.bakker@lifeline.nl> - 0.4.13-0.1264.1
- updated to snapshot 1264

* Thu Nov 03 2005 Bastiaan Bakker <bastiaan.bakker@lifeline.nl> - 0.4.12-6
- added openssl-devel build requirement
- removed '.ko' extension in modprobe command

* Wed Nov 02 2005 Bastiaan Bakker <bastiaan.bakker@lifeline.nl> - 0.4.12-5
- fixed kernel-devel BuildRequires

* Fri Sep 23 2005 Bastiaan Bakker <bastiaan.bakker@lifeline.nl> - 0.4.12-4
- fixed modprobe -r 'FATAL' message
- run depmod with correct kernel version

* Fri Sep 23 2005 Bastiaan Bakker <bastiaan.bakker@lifeline.nl> - 0.4.12-3
- added config files
- set kernel module file permissions to 744
- fixed provides/requires of kernel module
- removed BuildArch restriction

* Thu Sep 22 2005 Bastiaan Bakker <bastiaan.bakker@lifeline.nl> - 0.4.12-2
- create separate subpackage for kernel module
- include man pages
- added kernel compatibility patch for kernels < 2.6.11

* Wed Aug 03 2005 Bastiaan Bakker <bastiaan.bakker@lifeline.nl>
- First version.


