%define git_date 20091007

Summary:	LZMA compression utilities
Name:		xz
Version:	4.999.9
#Release:	0.1.beta.%{git_date}git%{?dist}
Release:       0.1.beta%{?dist}
License:	LGPLv2+
Group:		Applications/File
# source created as "make dist" in checked out GIT tree
#Source0:	http://tukaani.org/%{name}/%{name}-%{version}beta.%{git_date}git.tar.xz
Source0:        http://tukaani.org/xz/xz-4.999.9beta.tar.gz
URL:		http://tukaani.org/%{name}/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	%{name}-libs = %{version}-%{release}

%description
XZ Utils are an attempt to make LZMA compression easy to use on free (as in
freedom) operating systems. This is achieved by providing tools and libraries
which are similar to use than the equivalents of the most popular existing
compression algorithms.

LZMA is a general purpose compression algorithm designed by Igor Pavlov as
part of 7-Zip. It provides high compression ratio while keeping the
decompression speed fast.

%package 	libs
Summary:	Libraries for decoding LZMA compression
Group:		System Environment/Libraries
License:	LGPLv2+

%description 	libs
Libraries for decoding files compressed with LZMA or XZ utils.

%package 	devel
Summary:	Devel libraries & headers for liblzma
Group:		Development/Libraries
License:	LGPLv2+
Requires:	%{name}-libs = %{version}-%{release}
Requires:	pkgconfig

%description  devel
Devel libraries and headers for liblzma.

%package 	lzma-compat
Summary:	Older LZMA format compatibility binaries
Group:		Development/Libraries
# lz{grep,diff,more} are GPLv2+. Other binaries are LGPLv2+
License:	GPLv2+ and LGPLv2+
Requires:	%{name} = %{version}-%{release}
Obsoletes:	lzma < 5
Provides:	lzma = 5

%description  lzma-compat
The lzma-compat package contains compatibility links for older
commands that deal with the older LZMA format.

%prep
%setup -q -n %{name}-%{version}beta

%build
CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64" \
CXXFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64" \
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"
rm -f %{buildroot}/%{_libdir}/*.a
rm -f %{buildroot}/%{_libdir}/*.la
rm -rf %{buildroot}/%{_docdir}/%{name}

%check
LD_LIBRARY_PATH=$PWD/src/liblzma/.libs make check

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS README THANKS COPYING.* ChangeLog 
%{_bindir}/*xz*

%files libs
%defattr(-,root,root,-)
%doc COPYING.*
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/lzma
%{_includedir}/lzma/*.h
%{_includedir}/lzma.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/liblzma.pc

%files lzma-compat
%defattr(-,root,root,-)
%{_bindir}/*lz*
%{_mandir}/man1/*

%changelog
* Wed Nov 18 2009 David Hrbáč <david@hrbac.cz> - 4.999.9-0.1.beta
- initial rebuild

* Fri Aug 28 2009 Jindrich Novy <jnovy@redhat.com> 4.999.9-0.1.beta
- update to 4.999.9beta

* Mon Aug 17 2009 Jindrich Novy <jnovy@redhat.com> 4.999.8-0.10.beta.20090817git
- sync with upstream because of #517806

* Tue Aug 04 2009 Jindrich Novy <jnovy@redhat.com> 4.999.8-0.9.beta.20090804git
- update to the latest GIT snapshot

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.999.8-0.8.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Bill Nottingham <notting@redhat.com> 4.999.8-0.7.beta
- tweak summary
- add %%check section (<tibbs@math.uh.edu>)
 
* Thu Jul 09 2009 Bill Nottingham <notting@redhat.com> 4.999.8-0.6.beta
- fix release versioning to match guidelines
- fix up lzma-compat summary/description
- tweak licensing

* Mon Jun 22 2009 Jindrich Novy <jnovy@redhat.com> 4.999.8beta-0.5
- introduce lzma-compat subpackage

* Fri Jun 19 2009 Jindrich Novy <jnovy@redhat.com> 4.999.8beta-0.4
- try to not to conflict with lzma

* Thu Jun 18 2009 Jindrich Novy <jnovy@redhat.com> 4.999.8beta-0.3
- obsolete but don't provide lzma, they are largely incompatible
- put beta to Release

* Wed Jun 17 2009 Jindrich Novy <jnovy@redhat.com> 4.999.8beta-0.2
- obsolete old lzma
- add Requires: pkgconfig

* Tue Jun 16 2009 Jindrich Novy <jnovy@redhat.com> 4.999.8beta-0.1
- package XZ Utils, based on LZMA Utils packaged by Per Patrice Bouchand
