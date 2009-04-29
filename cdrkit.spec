Summary: A collection of CD/DVD utilities
Name: cdrkit
Version: 1.1.8
Release: 1%{?dist}
License: GPLv2
Group: Applications/System
URL: http://cdrkit.org/
Source: http://cdrkit.org/releases/cdrkit-%{version}.tar.gz

Patch1: cdrkit-1.1.8-werror.patch

BuildRequires: cmake libcap-devel zlib-devel perl file-devel bzip2-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
cdrkit is a collection of CD/DVD utilities.

%package -n wodim
Summary: A command line CD/DVD recording program
Group: Applications/Archiving
Obsoletes: dvdrecord <= 0:0.1.5
Provides: dvdrecord = 0:0.1.5.1
Obsoletes: cdrecord < 9:2.01-12
Provides: cdrecord = 9:2.01-12
Requires(preun): %{_sbindir}/alternatives chkconfig coreutils
Requires(post): %{_sbindir}/alternatives chkconfig coreutils

%description -n wodim
Wodim is an application for creating audio and data CDs. Wodim
works with many different brands of CD recorders, fully supports
multi-sessions and provides human-readable error messages.

%package -n genisoimage
Summary: Creates an image of an ISO9660 filesystem
Group: Applications/System
Obsoletes: mkisofs < 9:2.01-12
Provides: mkisofs = 9:2.01-12
Requires: perl >= 4:5.8.1
Requires(preun): %{_sbindir}/alternatives chkconfig coreutils
Requires(post): %{_sbindir}/alternatives chkconfig coreutils

%description -n genisoimage
The genisoimage program is used as a pre-mastering program; i.e., it
generates the ISO9660 filesystem. Genisoimage takes a snapshot of
a given directory tree and generates a binary image of the tree
which will correspond to an ISO9660 filesystem when written to
a block device. Genisoimage is used for writing CD-ROMs, and includes
support for creating bootable El Torito CD-ROMs.

Install the genisoimage package if you need a program for writing
CD-ROMs.

%package -n icedax
Group: Applications/Multimedia
Summary: A utility for sampling/copying .wav files from digital audio CDs
Obsoletes: cdda2wav < 9:2.01-12
Provides: cdda2wav = 9:2.01-12
Requires(preun): %{_sbindir}/alternatives chkconfig coreutils
Requires(post): %{_sbindir}/alternatives chkconfig coreutils

%description -n icedax
Icedax is a sampling utility for CD-ROM drives that are capable of
providing a CD's audio data in digital form to your host. Audio data
read from the CD can be saved as .wav or .sun format sound files.
Recording formats include stereo/mono, 8/12/16 bits and different
rates. Icedax can also be used as a CD player.

%prep
%setup -q 
%patch1 -p1 -b .werror

find . -type f -print0 | xargs -0 perl -pi -e 's#/usr/local/bin/perl#/usr/bin/perl#g'
find doc -type f -print0 | xargs -0 chmod a-x 


%build
mkdir fedora
cd fedora
export CFLAGS="$RPM_OPT_FLAGS -Wall -Werror -Wno-unused-function -Wno-unused-variable"
export CXXFLAGS="$CFLAGS"
export FFLAGS="$CFLAGS"
cmake .. \
        -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
        -DBUILD_SHARED_LIBS:BOOL=ON
make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
cd fedora
make install DESTDIR=$RPM_BUILD_ROOT
perl -pi -e 's#^require v5.8.1;##g' $RPM_BUILD_ROOT%{_bindir}/dirsplit
ln -s genisoimage $RPM_BUILD_ROOT%{_bindir}/mkisofs
ln -s genisoimage $RPM_BUILD_ROOT%{_bindir}/mkhybrid
ln -s icedax $RPM_BUILD_ROOT%{_bindir}/cdda2wav
ln -s wodim $RPM_BUILD_ROOT%{_bindir}/cdrecord
ln -s wodim $RPM_BUILD_ROOT%{_bindir}/dvdrecord

%clean
rm -rf $RPM_BUILD_ROOT

%post -n wodim
link=`readlink %{_bindir}/cdrecord`
if [ "$link" == "%{_bindir}/wodim" ]; then
        rm -f %{_bindir}/cdrecord
fi
link=`readlink %{_bindir}/dvdrecord`
if [ "$link" == "wodim" ]; then
        rm -f %{_bindir}/dvdrecord
fi

%{_sbindir}/alternatives --install %{_bindir}/cdrecord cdrecord \
		%{_bindir}/wodim 50 \
	--slave %{_mandir}/man1/cdrecord.1.gz cdrecord-cdrecordman \
		%{_mandir}/man1/wodim.1.gz \
	--slave %{_bindir}/dvdrecord cdrecord-dvdrecord %{_bindir}/wodim \
	--slave %{_mandir}/man1/dvdrecord.1.gz cdrecord-dvdrecordman \
		%{_mandir}/man1/wodim.1.gz \
	--slave %{_bindir}/readcd cdrecord-readcd %{_bindir}/readom \
	--slave %{_mandir}/man1/readcd.1.gz cdrecord-readcdman \
		%{_mandir}/man1/readom.1.gz 

%preun -n wodim
if [ $1 = 0 ]; then
        %{_sbindir}/alternatives --remove cdrecord %{_bindir}/wodim
fi

%post -n genisoimage
link=`readlink %{_bindir}/mkisofs`
if [ "$link" == "genisoimage" ]; then
	rm -f %{_bindir}/mkisofs
fi

%{_sbindir}/alternatives --install %{_bindir}/mkisofs mkisofs \
		%{_bindir}/genisoimage 50 \
	--slave %{_mandir}/man1/mkisofs.1.gz mkisofs-mkisofsman \
		%{_mandir}/man1/genisoimage.1.gz \
	--slave %{_bindir}/mkhybrid mkisofs-mkhybrid %{_bindir}/genisoimage

%preun -n genisoimage
if [ $1 = 0 ]; then
        %{_sbindir}/alternatives --remove mkisofs %{_bindir}/genisoimage
fi

%post -n icedax
link=`readlink %{_bindir}/cdda2wav`
if [ "$link" == "icedax" ]; then
        rm -f %{_bindir}/cdda2wav
fi
%{_sbindir}/alternatives --install %{_bindir}/cdda2wav cdda2wav \
		%{_bindir}/icedax 50 \
	--slave %{_mandir}/man1/cdda2wav.1.gz cdda2wav-cdda2wavman \
		%{_mandir}/man1/icedax.1.gz 

%preun -n icedax
if [ $1 = 0 ]; then
        %{_sbindir}/alternatives --remove cdda2wav %{_bindir}/icedax
fi

%files -n wodim
%defattr(-,root,root)
%doc Changelog COPYING FAQ FORK START
%doc doc/READMEs doc/wodim
%{_bindir}/devdump
%{_bindir}/wodim
%ghost %{_bindir}/cdrecord
%ghost %{_bindir}/dvdrecord
%{_bindir}/readom
%{_sbindir}/netscsid
%{_mandir}/man1/devdump.*
%{_mandir}/man1/wodim.*
%{_mandir}/man1/readom.*

%files -n icedax
%defattr(-,root,root)
%doc doc/icedax COPYING
%{_bindir}/icedax
%ghost %{_bindir}/cdda2wav
%{_bindir}/cdda2mp3
%{_bindir}/cdda2ogg
%{_mandir}/man1/icedax.*
%{_mandir}/man1/cdda2ogg.*
%{_mandir}/man1/list_audio_tracks.*

%files -n genisoimage
%defattr(-,root,root)
%doc doc/genisoimage COPYING
%{_bindir}/genisoimage
%ghost %{_bindir}/mkisofs
%ghost %{_bindir}/mkhybrid
%{_bindir}/isodebug
%{_bindir}/isodump
%{_bindir}/isoinfo
%{_bindir}/isovfy
%{_bindir}/dirsplit
%{_bindir}/pitchplay
%{_bindir}/readmult
%{_mandir}/man5/genisoimagerc.*
%{_mandir}/man1/genisoimage.*
%{_mandir}/man1/isodebug.*
%{_mandir}/man1/isodump.*
%{_mandir}/man1/isoinfo.*
%{_mandir}/man1/isovfy.*
%{_mandir}/man1/dirsplit.*
%{_mandir}/man1/pitchplay.*
%{_mandir}/man1/readmult.*

%changelog
* Fri Mar 13 2009 David Hrbáč <david@hrbac.cz> - 1.1.8-1
- Initial rebuild

* Tue May 27 2008 Roman Rakus <rrakus@redhat.cz> - 1.1.8-1
- Version 1.1.8 - old patches included
                - added bzip2-devel to build requirements
- fixed #171510 - preserve directory permissions

* Wed Feb 27 2008 Harald Hoyer <harald@redhat.com> 1.1.6-11
- refined -Werror patch

* Mon Feb 25 2008 Harald Hoyer <harald@redhat.com> 1.1.6-10
- patched to compile with -Werror (rhbz#429385)

* Thu Feb 21 2008 Harald Hoyer <harald@redhat.com> 1.1.6-9
- fixed loop on error message for old dev syntax (rhbz#429386)

* Thu Feb 21 2008 Harald Hoyer <harald@redhat.com> 1.1.6-8
- added file-devel to build requirements

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.6-7
- Autorebuild for GCC 4.3

* Tue Sep 25 2007 Harald Hoyer <harald@redhat.com> - 1.1.6-6
- fixed readcd man page symlink

* Fri Sep 21 2007 Harald Hoyer <harald@redhat.com> - 1.1.6-5
- fixed rhbz#255001 - icedax --devices segfaults
- fixed rhbz#249357 - Typo in wodim output

* Fri Sep 21 2007 Harald Hoyer <harald@redhat.com> - 1.1.6-4
- play stupid tricks, to let alternatives make the links and
  rpm not removing them afterwards
- removed bogus warning for "." and ".."

* Thu Sep 20 2007 Harald Hoyer <harald@redhat.com> - 1.1.6-3
- fixed rhbz#248262
- switched to alternatives

* Fri Aug 17 2007 Harald Hoyer <harald@redhat.com> - 1.1.6-2
- changed license to GPLv2

* Wed Jun 20 2007 Harald Hoyer <harald@redhat.com> - 1.1.6-1
- version 1.1.6
- added readcd symlink

* Mon Apr 23 2007 Harald Hoyer <harald@redhat.com> - 1.1.2-4
- bump obsoletes/provides

* Tue Feb 27 2007 Harald Hoyer <harald@redhat.com> - 1.1.2-3
- applied specfile changes as in bug #224365

* Wed Jan 24 2007 Harald Hoyer <harald@redhat.com> - 1.1.2-1
- version 1.1.2
