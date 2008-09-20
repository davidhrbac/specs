Summary:	Library for reading and writing sound files
Name:		libsndfile
Version:	1.0.17
Release:	3%{?dist}
License:	LGPL
Group:		System Environment/Libraries
URL:		http://www.mega-nerd.com/libsndfile/
Source0:	http://www.mega-nerd.com/libsndfile/libsndfile-%{version}.tar.gz
Patch0:         libsndfile-1.0.17+flac-1.1.3.patch
Patch1:         libsndfile-1.0.17-flac-buffer-overflow.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

BuildRequires:	alsa-lib-devel
Provides:	%{name}-octave = %{version}-%{release}

%package devel
Summary:	Development files for libsndfile
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release} pkgconfig

%description
libsndfile is a C library for reading and writing sound files such as
AIFF, AU, WAV, and others through one standard interface. It can
currently read/write 8, 16, 24 and 32-bit PCM files as well as 32 and
64-bit floating point WAV files and a number of compressed formats. It
compiles and runs on *nix, MacOS, and Win32.

%description devel
libsndfile is a C library for reading and writing sound files such as
AIFF, AU, WAV, and others through one standard interface.
This package contains files needed to develop with libsndfile.


%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure --disable-dependency-tracking
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT __docs
make install DESTDIR=$RPM_BUILD_ROOT
cp -pR $RPM_BUILD_ROOT%{_docdir}/libsndfile1-dev/html __docs
rm -rf $RPM_BUILD_ROOT%{_docdir}/libsndfile1-dev


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS TODO README NEWS ChangeLog
%{_bindir}/sndfile-info
%{_bindir}/sndfile-play
%{_bindir}/sndfile-convert
%{_bindir}/sndfile-regtest
%{_mandir}/man1/sndfile-info.1*
%{_mandir}/man1/sndfile-play.1*
%{_mandir}/man1/sndfile-convert.1*
%{_libdir}/%{name}.so.*
%{_datadir}/octave

%files devel
%defattr(-,root,root,-)
%doc __docs/*
%exclude %{_libdir}/%{name}.la
%{_includedir}/sndfile.h
%{_includedir}/sndfile.hh
%{_libdir}/%{name}.so
%{_libdir}/%{name}.a
%{_libdir}/pkgconfig/sndfile.pc


%changelog
* Sat Sep 20 2008 David Hrbáč <david@hrbac.cz> - 1.0.17-3
- initial rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.17-3
- Autorebuild for GCC 4.3

* Thu Sep 20 2007 Andreas Thienemann <andreas@bawue.net> - 1.0.17-2
- Adding FLAC support to libsndfile courtesy of gentoo, #237575
- Fixing CVE-2007-4974. Thanks to the gentoo people for the patch, #296221

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 1.0.17-1
- Updated to 1.0.17

* Sun Apr 30 2006 Andreas Thienemann <andreas@bawue.net> - 1.0.16-1
- Updated to 1.0.16

* Thu Mar 30 2006 Andreas Thienemann <andreas@bawue.net> - 1.0.15-1
- Updated to 1.0.15

* Thu Mar 16 2006 Dams <anvil[AT]livna.org> - 1.0.14-1.fc5
- Updated to 1.0.14
- Dropped patch0

* Thu May 12 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0.11-3
- rebuilt

* Sat Mar  5 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0.11-2
- Fix format string bug (#149863).
- Drop explicit Epoch 0.

* Sat Dec  4 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.11-0.fdr.1
- Update to 1.0.11.

* Wed Oct 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.10-0.fdr.1
- Update to 1.0.10, update URLs, include ALSA support.
- Disable dependency tracking to speed up the build.
- Add missing ldconfig invocations.
- Make -devel require pkgconfig.
- Include developer docs in -devel.
- Provide -octave in main package, own more related dirs.
- Bring specfile up to date with current spec templates.

* Sat Apr 12 2003 Dams <anvil[AT]livna.org>
- Initial build.
