%define tarball xf86-video-i810
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

%define legacy_version 1.6.5

Summary:   Xorg X11 i810 video driver(s)
Name:      xorg-x11-drv-i810
Version:   2.0.0
Release:   3%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:   ftp://ftp.x.org/pub/individual/driver/%{tarball}-%{legacy_version}.tar.bz2
Source1:   xf86-video-intel-%{version}.tar.bz2
Source2:   i810.xinf

# new school intel driver patches
Patch0: intel-2.0-vblank-power-savings.patch

# legacy i810 driver patches
Patch100: i810-1.6.5-to-git-20060911.patch
Patch101: i810-match-server-sync-ranges.patch
Patch1000: i965-xv-hang-fix.patch

ExclusiveArch: %{ix86} x86_64 ia64

BuildRequires: pkgconfig
BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-sdk 
BuildRequires: libXvMC-devel
BuildRequires: mesa-libGL-devel >= 6.5-9
BuildRequires: libdrm-devel >= 2.0-1

Requires:  xorg-x11-server-Xorg >= 1.1.0-1

Conflicts:  kudzu < 1.2.42-1

%description 
X.Org X11 i810 video driver.

%package devel
Summary:   Xorg X11 i810 video driver XvMC development package
Group:     Development/System
Requires:  %{name} = %{version}-%{release}
Provides:  xorg-x11-drv-intel = %{version}-%{release}

%description devel
X.Org X11 i810 video driver XvMC development package.

%prep
%setup -q -n %{tarball}-%{legacy_version}

%patch100 -p2 -b .i810-git-20060911
%patch101 -p2 -b .server-ranges
%patch1000 -p2 -b .965-xv

cd ..
rm -rf xf86-video-intel-%{version}
tar jxf %{SOURCE1}
cd xf86-video-intel-%{version}
%patch0 -p1 -b .vblank-interrupt

%build
OPTS="--disable-static --libdir=%{_libdir} --mandir=%{_mandir} --enable-dri"
./configure ${OPTS} && make || exit 1
cd ../xf86-video-intel-%{version} && ./configure ${OPTS} && make && cd - || exit 1

%install
rm -rf $RPM_BUILD_ROOT

cd ../xf86-video-intel-%{version} && make install DESTDIR=$RPM_BUILD_ROOT && cd - || exit 1
make install DESTDIR=$RPM_BUILD_ROOT || exit 1

mkdir -p $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases/

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

# Nuke until they're actually hooked up in the code
rm -f $RPM_BUILD_ROOT/%{driverdir}/{ch7017,ivch}.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/i810_drv.so
%{driverdir}/intel_drv.so
%{driverdir}/ch7xxx.so
%{driverdir}/sil164.so
#%{driverdir}/ch7017.so
#%{driverdir}/ivch.so
%{_datadir}/hwdata/videoaliases/i810.xinf
%{_libdir}/libI810XvMC.so.1
%{_libdir}/libI810XvMC.so.1.0.0
%{_mandir}/man4/i*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libI810XvMC.so

%changelog
* Mon May 14 2007 Adam Jackson <ajax@redhat.com> 2.0.0-3
- intel-2.0-vblank-power-savings.patch: Disable vblank interrupts when no
  DRI clients are active, for better battery life.

* Tue May 01 2007 Adam Jackson <ajax@redhat.com> 2.0.0-2
- Rebuild for final RANDR 1.2 ABI.  Fixes segfault at startup. (#238575)

* Mon Apr 23 2007 Adam Jackson <ajax@redhat.com> 2.0.0-1
- xf86-video-intel 2.0.0.  Change the version number to match, why not.
- Add a Virtual provides for xorg-x11-drv-intel, since we should probably
  rename this at some point.

* Tue Apr 10 2007 Adam Jackson <ajax@redhat.com> 1.6.5-19
- i810.xinf: Move all 965 and 945 chips onto the new driver, as well as
  915GM.

* Thu Apr 05 2007 Adam Jackson <ajax@redhat.com> 1.6.5-18
- i810.xinf: More intel whitelisting (#214011, #234877)

* Wed Apr 04 2007 Adam Jackson <ajax@redhat.com> 1.6.5-17
- xf86-video-intel-1.9.94 (RC4).  Adds support for 965GM.
- i810.xinf: Point 965GM support at the intel driver since it's not present
  in old i810.

* Fri Mar 30 2007 Adam Jackson <ajax@redhat.com> 1.6.5-16
- xf86-video-intel-1.9.93 (RC3).

* Tue Mar 27 2007 Jeremy Katz <katzj@redhat.com> - 1.6.5-15
- fix typo with 945GM pci id from my laptop

* Thu Mar 22 2007 Adam Jackson <ajax@redhat.com> 1.6.5-14
- xf86-video-intel 1.9.92 (RC2).

* Mon Mar 05 2007 Adam Jackson <ajax@redhat.com> 1.6.5-13
- Updated modesetting driver to one that will actually work with a 1.3 server.

* Tue Feb 27 2007 Adam Jackson <ajax@redhat.com> 1.6.5-12
- Nuke %%with_dri, since the arch list exactly matched the ExclusiveArch list
- Remove ivch and ch7017 from the install since they aren't hooked up to the
  code anywhere
- Disown the module

* Tue Jan 30 2007 Jeremy Katz <katzj@redhat.com> - 1.6.5-11
- update modesetting driver to git snapshot from today

* Tue Nov 7 2006 Adam Jackson <ajackson@redhat.com> 1.6.5-10
- i965-xv-hang-fix.patch: Backport Xv hang fix for G965.

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.6.5-9
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Adam Jackson <ajackson@redhat.com> 1.6.5-8.fc6
- Change 'Requires: kudzu >= foo' to 'Conflicts: kudzu < foo' since we don't
  actually require kudzu to run.

* Fri Sep 15 2006 Adam Jackson <ajackson@redhat.com> 1.6.5-7.fc6
- i810.xinf: Whitelist Apple 945GM machines and Aopen Mini PC onto intel(4)

* Tue Sep 12 2006 Adam Jackson <ajackson@redhat.com> 1.6.5-6.fc6
- i810-1.6.5-to-git-20060911.patch: Backport post-1.6.5 fixes from git.
- i810-match-server-sync-ranges.patch: Make a terrible heuristic in the
  driver match the corresponding terrible heuristic in the server.

* Mon Aug 28 2006 Adam Jackson <ajackson@redhat.com> 1.6.5-5.fc6
- intel-945gm-lfp-blacklist.patch: Tweak the Apple blacklist to (hopefully)
  correctly distinguish between Mac Mini and Macbook Pro.

* Mon Aug 21 2006 Adam Jackson <ajackson@redhat.com> 1.6.5-4.fc6
- i810.xinf: PCI IDs for i965.

* Thu Aug 17 2006 Adam Jackson <ajackson@redhat.com> 1.6.5-3.fc6
- i810.xinf: Uppercase PCI IDs.

* Fri Aug 10 2006 Adam Jackson <ajackson@redhat.com> 1.6.5-2.fc6
- Update i810 to 1.6.5, should fix DRI.
- Add kuzdu requires.
- i810.xinf: Start whitelisting devices over to intel.

* Wed Aug  9 2006 Adam Jackson <ajackson@redhat.com> 1.6.4-3.fc6
- intel-driver-rename.patch: Fix the driver name in more places so it'll,
  you know, load.

* Wed Aug  9 2006 Adam Jackson <ajackson@redhat.com> 1.6.4-2.fc6
- intel-945gm-lfp-blacklist.patch: At anholt's suggestion, remove the other
  LFP special casing in favor of the blacklist.

* Wed Aug  9 2006 Adam Jackson <ajackson@redhat.com> 1.6.4-1.fc6
- Admit defeat, kinda.  Package both i810 stable and modesetting drivers.
  The modesetting driver is installed as intel_drv.so instead of i810_drv.so,
  and is selected with Driver "intel" in xorg.conf.  Individual devices will
  whitelist over to "intel" until that branch gets merged into head.
- Update the stable branch driver to 1.6.4 from upstream, adds i965 support.
- intel-945gm-lfp-blacklist.patch: Blacklist LFP detection on machines where
  the BIOS is known to lie.

* Tue Aug  8 2006 Adam Jackson <ajackson@redhat.com> 1.6.0-14.20060808modeset.fc6
- Today's snapshot: I2C bus creation fix.

* Wed Aug  2 2006 Adam Jackson <ajackson@redhat.com> 1.6.0-13.20060717modeset.fc6
- intel-prune-by-edid-pixclock.patch: Honor the EDID-reported maximum pixel
  clock when computing the modes list.
- intel-virtual-sizing-bogon.patch: Don't interpret the size of the display
  in centimeters as the size of the display in pixels.

* Mon Jul 24 2006 Adam Jackson <ajackson@redhat.com> 1.6.0-12.20060717modeset.fc6
- Disable spread-spectrum LVDS, various crash and hang fixes, saner output
  probing.

* Thu Jul 13 2006 Adam Jackson <ajackson@redhat.com> 1.6.0-11.20060713modeset.fc6
- Update again for a mode comparison bugfix.

* Thu Jul 13 2006 Adam Jackson <ajackson@redhat.com> 1.6.0-10.20060713modeset.fc6
- Update to today's git; crash fixes, better pre-915 support, slightly better
  autoconfigurability.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.6.0-9.20060707modeset.1.fc6
- rebuild

* Tue Jul 11 2006 Adam Jackson <ajackson@redhat.com> 1.6.0-9.20060707modeset
- Fix Revision number to match naming policy.

* Tue Jul 11 2006 Kristian Høgsberg <krh@redhat.com> 1.6.0-8.modeset20060707
- Add back modesetting changes.

* Mon Jul 10 2006 Kristian Høgsberg <krh@redhat.com> 1.6.0-7
- Roll back modesetting changes and build for fc5 aiglx repo.

* Fri Jul  7 2006 Adam Jackson <ajackson@redhat.com> 1.6.0-6.modeset20060707
- Snapshot of the git modesetting branch.

* Fri Jul  7 2006 Adam Jackson <ajackson@redhat.com> 1.6.0-6
- Update i810.xinf to include entries for E7221 and 945GM.

* Fri Jun 23 2006 Mike A. Harris <mharris@redhat.com> 1.6.0-5
- Add with_dri macro to spec file, and conditionalize build time DRI support

* Fri May 26 2006 Mike A. Harris <mharris@redhat.com> 1.6.0-4
- Added "BuildRequires: libdrm >= 2.0-1" for (#192334), and updated sdk dep
  to pick up proto-devel as well.

* Tue May 23 2006 Adam Jackson <ajackson@redhat.com> 1.6.0-3
- Rebuild for 7.1 ABI fix.

* Tue Apr 11 2006 Kristian Høgsberg <krh@redhat.com> 1.6.0-2
- Bump for fc5-bling build.

* Sun Apr 09 2006 Adam Jackson <ajackson@redhat.com> 1.6.0-1
- Update to 1.6.0 from 7.1RC1.

* Tue Apr 04 2006 Kristian Høgsberg <krh@redhat.com> 1.4.1.3-4.cvs20060322.1
- Add patch to add missing #include's, specifically assert.h.

* Wed Mar 22 2006 Kristian Høgsberg <krh@redhat.com> 1.4.1.3-4.cvs20060322
- Update to CVS snapshot of 20060322.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.4.1.3-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sat Feb 04 2006 Mike A. Harris <mharris@redhat.com> 1.4.1.3-3
- Added 8086:2772 mapping to i810.xinf for bug (#178451)

* Fri Feb 03 2006 Mike A. Harris <mharris@redhat.com> 1.4.1.3-2
- Added 8086:2592 mapping to i810.xinf for bug (#172884)

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.4.1.3-1
- Updated xorg-x11-drv-i810 to version 1.4.1.3 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.4.1.2-1
- Updated xorg-x11-drv-i810 to version 1.4.1.2 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.4.1-1
- Updated xorg-x11-drv-i810 to version 1.4.1 from X11R7 RC2

* Fri Nov 04 2005 Mike A. Harris <mharris@redhat.com> 1.4.0.1-1
- Updated xorg-x11-drv-i810 to version 1.4.0.1 from X11R7 RC1
- Fix *.la file removal.
- Added 'devel' subpackage for XvMC .so
- Added 'BuildRequires: libXvMC-devel' for XvMC drivers.

* Mon Oct 03 2005 Mike A. Harris <mharris@redhat.com> 1.4.0-1
- Update BuildRoot to use Fedora Packaging Guidelines.
- Deglob file manifest.
- Limit "ExclusiveArch" to x86, x86_64, ia64

* Fri Sep 02 2005 Mike A. Harris <mharris@redhat.com> 1.4.0-0
- Initial spec file for i810 video driver generated automatically
  by my xorg-driverspecgen script.
