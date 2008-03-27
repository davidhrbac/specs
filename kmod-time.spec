# build with --target=i686
#            --define "kernel <version>"

%define _libmoddir /lib/modules

%{!?kernel:%define kernel %(rpm -q kernel-devel --qf '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}\\n' | tail -1)}

%define _with_smp %(test -d %{_libmoddir}/%{kernel}smp/build && echo 1 || echo 0)

%define kversion %(echo "%{kernel}" | sed -e 's|-.*||')
%define krelease %(echo "%{kernel}" | sed -e 's|.*-||')

%define pversion 20051006
%define real_name ipt_time
%define builddir  BUILD-time
%define moduledir /kernel/net/ipv4/netfilter
%define includedir /build/include/linux/netfilter_ipv4

Summary: Linux module for time.
Name:    kmod-time
Version: %(echo %{kernel} | sed 's@-@_@g')
Release: 0.%{pversion}.%{mysig}
License: GPL
Group:   System Environment/Kernel
URL:     http://www.netfilter.org/patch-o-matic/
Source0: http://ftp.netfilter.org/pub/patch-o-matic-ng/snapshot/patch-o-matic-ng-%{pversion}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: kernel-devel
ExclusiveArch: i686 x86_64
Requires: kernel = %{kernel}
Packager: David Hrbáč <david@hrbac.cz>
Obsoletes: kmod-time-2.6.9-11.EL

%description
Module time for Linux 2.6.x kernel.

%package -n kmod-time-smp
Summary:  Linux SMP time for Linux 2.6.x kernel.
Group:    System Environment/Kernel
Requires: kernel-smp = %{kernel}
Obsoletes: kmod-time-2.6.9-11.EL

%description -n kmod-time-smp
Module time for Linux 2.6.x SMP kernel.

%prep
%setup -q -n patch-o-matic-ng-%{pversion}
cat <<EOF

Package version: %{version}
Package release: %{release}
For kernel: %{kernel}
For target: %{_target_cpu}

EOF

preparemodule() {
	# lets move source off the tree
	mkdir $1
	pushd $1
	cp -a ../patchlets/time/linux/include/linux/netfilter_ipv4/%{real_name}.h .
	cp -a ../patchlets/time/linux/net/ipv4/netfilter/%{real_name}.c .
	# ipt_time.h is in the current directory
	perl -pi -e 's@<linux/netfilter_ipv4/(%{real_name}.h)>@"$1"@' %{real_name}.c
	# because RH changes in 2.6.9, we need a sligtly newer version of ipt_time.c
	# Makefile from http://www.redhat.com/docs/manuals/enterprise/RHEL-4-Manual/release-notes/as-x86/
	cat > Makefile <<EOF
obj-m := %{real_name}.o

KDIR  := /lib/modules/$2/build
PWD   := \$(shell pwd)

default:
	%{__make} -C \$(KDIR) SUBDIRS=\$(PWD) modules
	#%{__make} -C \$(KDIR) SUBDIRS=\$(PWD) ARCH="$(echo %{_target_cpu} | sed -e 's/\(i.86\|athlon\)/i386/')" modules
EOF
	popd
}

preparemodule %{builddir} %{kernel}
%if %{_with_smp}
  preparemodule %{builddir}-smp %{kernel}smp
%endif

%build
pushd %{builddir}
make
popd
%if %{_with_smp}
  pushd %{builddir}-smp
  make
  popd
%endif

%install
installmodule() {
	pushd $1
	DIR=$RPM_BUILD_ROOT%{_libmoddir}/$2/%{moduledir}
	mkdir -p $DIR
	install -m744 %{real_name}.ko $DIR
	DIR=$RPM_BUILD_ROOT%{_libmoddir}/$2/%{includedir}
	mkdir -p $DIR
	install -m644 %{real_name}.h $DIR
	popd
}

installmodule %{builddir} %{kernel}
%if %{_with_smp}
  installmodule %{builddir}-smp %{kernel}smp
%endif

%post -n kmod-time
/sbin/depmod -ae %{kernel} || :

%postun -n kmod-time
/sbin/depmod -ae %{kernel} || :

%post -n kmod-time-smp
/sbin/depmod -ae %{kernel}smp || :

%postun -n kmod-time-smp
/sbin/depmod -ae %{kernel}smp || :

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%attr(0744,root,root) %{_libmoddir}/%{kernel}/%{moduledir}/%{real_name}.ko
%attr(0644,root,root) %{_libmoddir}/%{kernel}/%{includedir}/%{real_name}.h

%if %{_with_smp}
%files -n kmod-time-smp
%defattr(-, root, root)
%attr(0744,root,root) %{_libmoddir}/%{kernel}smp/%{moduledir}/%{real_name}.ko
%attr(0644,root,root) %{_libmoddir}/%{kernel}smp/%{includedir}/%{real_name}.h
%endif

%changelog
* Fri Oct 05 2007 David Hrbáč <david@hrbac.cz> - 2.6.9_55.0.9.EL-2.20051006
- Kernel 2.6.9_55.0.9 rebuild

* Fri Sep 21 2007 David Hrbáč <david@hrbac.cz> - 2.6.9_55.0.6.EL-0.20051006
- Rebuild for 2.6.9_55.0.6.EL

* Sun Sep 03 2006 David Hrbáč <david@hrbac.cz> 
- Initial package
