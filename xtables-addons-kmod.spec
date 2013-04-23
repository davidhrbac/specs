# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
#define buildforkernels newest

Name:       xtables-addons-kmod
Summary:    Kernel module (kmod) for xtables-addons
Version:    1.46
Release:    1%{?dist}.3
License:    GPLv2
Group:      System Environment/Kernel
URL:        http://xtables-addons.sourceforge.net
Source0:    http://downloads.sourceforge.net/xtables-addons/xtables-addons-%{version}.tar.xz
#Source11:  xtables-addons-kmodtool-excludekernel-filterfile
# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Xtables-addons provides extra modules for iptables not present in the kernel, 
and is the successor of patch-o-matic. Extensions includes new targets like 
TEE, TARPIT, CHAOS, or modules like geoip, ipset, and account.

This package provides the xtables-addons kernel modules. You must also install 
the xtables-addons package in order to make use of these modules.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0
for kernel_version in %{?kernel_versions} ; do
    cp -a xtables-addons-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
    if ! grep -q 'XT_TARGET_TEE=m' %{_usrsrc}/kernels/${kernel_version%%___*}/.config; then
        sed -i 's/build_TEE=/build_TEE=m/' _kmod_build_${kernel_version%%___*}/mconfig
    fi
    if ! grep -q 'XT_TARGET_CHECKSUM=m' %{_usrsrc}/kernels/${kernel_version%%___*}/.config; then
        sed -i 's/build_CHECKSUM=/build_CHECKSUM=m/' _kmod_build_${kernel_version%%___*}/mconfig
    fi
    export XA_ABSTOPSRCDIR=${PWD}/_kmod_build_${kernel_version%%___*}
    make %{?_smp_mflags} V=1 -C "${kernel_version##*___}" M=${PWD}/_kmod_build_${kernel_version%%___*}/extensions modules
done


%install
for kernel_version  in %{?kernel_versions} ; do
    export XA_ABSTOPSRCDIR=${PWD}/_kmod_build_${kernel_version%%___*}
    make %{?_smp_mflags} V=1 -C "${kernel_version##*___}" M=${PWD}/_kmod_build_${kernel_version%%___*}/extensions _emodinst_ INSTALL_MOD_PATH=%{buildroot} ext-mod-dir=%{kmodinstdir_postfix}
done
chmod u+x %{buildroot}/lib/modules/*/extra/*/*
%{?akmod_install}

%clean
rm -rf %{buildroot}

%changelog
* Thu Oct 18 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.46-1.3
- Rebuilt for updated kernel

* Thu Oct 11 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.46-1.2
- Rebuilt for updated kernel

* Mon Oct 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.46-1.1
- Rebuilt for updated kernel

* Wed Oct 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.46-1
- Update to 1.46

* Tue Jul 31 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.45-1
- Update to 1.45

* Thu May 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.42-2
- Fix build

* Wed May 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.42-1.4
- rebuild for updated kernel

* Sat Apr 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.42-1.3
- rebuild for updated kernel

* Sun Apr 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.42-1.2
- rebuild for updated kernel

* Mon Apr 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.42-1.1
- rebuild for updated kernel

* Thu Apr 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.42-1
- Update to 1.42

* Thu Apr 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.41-2
- rebuild for beta kernel

* Tue Feb 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.41-1.1
- Rebuild for UsrMove

* Tue Jan 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.41-1
- Update to 1.41

* Thu Nov 17 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.39-1
- Update to 1.39

* Wed Oct 27 2010 Chen Lei <supercyper@163.com> - 1.30-1
- update to 1.30

* Sun Jul 25 2010 Chen Lei <supercyper@163.com> - 1.28-1
- update to 1.28

* Mon Jun 28 2010 Chen Lei <supercyper@163.com> - 1.27-2
- rebuild for kernel 2.6.35

* Mon May 31 2010 Chen Lei <supercyper@163.com> - 1.27-1
- update to 1.27

* Thu May 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.26-1.4
- rebuild for new kernel

* Mon May 17 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.26-1.3
- rebuild for new kernel

* Fri May 07 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.26-1.2
- rebuild for new kernel

* Tue May 04 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.26-1.1
- rebuild for new kernel

* Sun May 02 2010 Chen Lei <supercyper@163.com> - 1.26-1
- update to 1.26

* Thu Apr 29 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.25-1.1
- rebuild for new kernel

* Mon Apr 26 2010 Chen Lei <supercyper@163.com> - 1.25-1
- update to 1.25

* Sun Apr 25 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.24-1.1
- rebuild for new kernel

* Thu Mar 18 2010 Chen Lei <supercyper@163.com> - 1.24-1
- initial rpm build
