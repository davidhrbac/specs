Summary: Create deltas between rpms
Name: deltarpm
Version: 3.4
Release: 11%{?dist}
License: BSD
Group: System Environment/Base
URL: http://www.novell.com/products/linuxpackages/professional/deltarpm.html

Source: ftp://ftp.suse.com/pub/projects/%{name}/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: bzip2-devel, rpm-devel, popt-devel

Patch0: deltarpm-3.4-multilib-workaround.patch
Patch1: deltarpm-3.4-multilib-include-colored.patch
Patch2: deltarpm-3.4-prelink-bugfix.patch
Patch3: deltarpm-3.4-skipmd5.patch

%description
A deltarpm contains the difference between an old
and a new version of a rpm, which makes it possible
to recreate the new rpm from the deltarpm and the old
one. You don't have to have a copy of the old rpm,
deltarpms can also work with installed rpms.

%prep
%setup -q
%patch0 -p0 -b .multilib
%patch1 -p1 -b .multicolor
%patch2 -p1 -b .prelink
%patch3 -p1 -b .skipmd5

%build
%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
    bindir=%{_bindir} mandir=%{_mandir} prefix=%{_prefix}

%install
%{__rm} -rf %{buildroot}
%makeinstall

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc LICENSE.BSD README
%doc %{_mandir}/man8/*
%{_bindir}/applydeltaiso
%{_bindir}/applydeltarpm
%{_bindir}/combinedeltarpm
%{_bindir}/drpmsync
%{_bindir}/fragiso
%{_bindir}/makedeltaiso
%{_bindir}/makedeltarpm
%{_bindir}/rpmdumpheader

%changelog
* Sun Jul 13 2008 Jonathan Dieter <jdieter@gmail.com> - 3.4-11
- Rebuild for rpm 4.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.4-10
- Autorebuild for GCC 4.3

* Mon Jan  7 2008 Jonathan Dieter <jdieter@gmail.com> - 3.4-9
- Add patch that allows deltarpm to rebuild rpms from deltarpms that have
  had the rpm signature added after their creation.  The code came from
  upstream.
- Drop nodoc patch added in 3.4-4 as most packages in repository have been
  updated since April-May 2007 and this patch was supposed to be temporary.

* Wed Aug 29 2007 Jonathan Dieter <jdieter@gmail.com> - 3.4-6
- Bring in popt-devel in BuildRequires to fix build in x86_64

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.4-5
- Rebuild for selinux ppc32 issue.

* Wed Jul 11 2007 Jonathan Dieter <jdieter@gmail.com> - 3.4-4
- Fix prelink bug
- Ignore verify bits on %doc files as they were set incorrectly in older
  versions of rpm.  Without this patch, deltarpm will not delta doc files
  in rpm created before April-May 2007

* Tue Jun  5 2007 Jeremy Katz <katzj@redhat.com> - 3.4-3
- include colored binaries from non-multilib-dirs so that deltas can work 
  on multilib platforms

* Wed May 09 2007 Adam Jackson <ajax@redhat.com> 3.4-2
- Add -a flag to work around multilib ignorance. (#238964)

* Tue Mar 06 2007 Adam Jackson <ajax@redhat.com> 3.4-1
- Update to 3.4 (#231154)

* Mon Feb 12 2007 Adam Jackson <ajax@redhat.com> 3.3-7
- Add RPM_OPT_FLAGS to make line. (#227380)

* Mon Feb 05 2007 Adam Jackson <ajax@redhat.com> 3.3-6
- Fix rpm db corruption in rpmdumpheader.  (#227326)

* Mon Sep 11 2006 Mihai Ibanescu <misa@redhat.com> - 3.3-5
- Rebuilding for new toolset

* Thu Aug 17 2006 Mihai Ibanescu <misa@redhat.com> - 3.3-4
- Removing BuildRequires: gcc

* Tue Aug 15 2006 Mihai Ibanescu <misa@redhat.com> - 3.3-3
- Fedora packaging guidelines build

* Tue Aug  8 2006 Mihai Ibanescu <misa@redhat.com> - 3.3-2
- Added BuildRequires: rpm-devel, gcc

* Sat Dec 03 2005 Dries Verachtert <dries@ulyssis.org> - 3.3-1 - 3768/dries
- Initial package.
