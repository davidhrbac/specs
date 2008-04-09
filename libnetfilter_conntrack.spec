Name:           libnetfilter_conntrack
Version:        0.0.89
Release: 1%{?dist}
Summary:        Netfilter conntrack userspace library
Group:          System Environment/Libraries
License:        GPL
URL:            http://netfilter.org
Source0:        http://netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
Patch0:         libnetfilter_conntrack-sysheader.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libnfnetlink-devel, pkgconfig, kernel-headers
BuildRequires:  autoconf, automake, libtool

%description
libnetfilter_conntrack is a userspace library providing a programming 
interface (API) to the in-kernel connection tracking state table.

%package        devel
Summary:        Netfilter conntrack userspace library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}, libnfnetlink-devel

%description    devel
libnetfilter_conntrack is a userspace library providing a programming
interface (API) to the in-kernel connection tracking state table.

%prep
%setup -q 
#%patch -p1

autoreconf -i --force

%build
%configure --disable-static --disable-rpath

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/libnetfilter_conntrack
%{_includedir}/libnetfilter_conntrack/*.h

%changelog
* Wed Apr  9 2008 David Hrbáč <david@hrbac.cz> - 0.0.89-1
- CentOS rebuild
- new upstream version

* Sun Jan 20 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.0.82-1
- new upstream version

* Thu Aug 30 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.81-1
- new upstream version

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.0.80-2
- Rebuild for selinux ppc32 issue.

* Thu Jul 19 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.80-1
- new upstream version

* Wed May 30 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.75-1
- new upstream version

* Sun Mar 25 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.50-4
- grab ownership of some directories

* Mon Mar 19 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.50-3
- include libnfnetlink-devel into -devel deps

* Sat Mar 17 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.50-2
- new way of handling rpaths (as in current packaging guidelines)

* Sun Feb 11 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.50-1
- upstream version 0.0.50

* Fri Sep 15 2006 Paul P. Komkoff Jr <i@stingr.net>
- rebuilt

* Wed Jul 12 2006 Felipe Kellermann <stdfk@terra.com.br> - 0.0.31-1
- Adds pkgconfig to devel files.
- Version 0.0.31.

* Mon May  8 2006 Paul P Komkoff Jr <i@stingr.net> - 0.0.30-2
- Include COPYING in %%doc

* Sun Mar 26 2006 Paul P Komkoff Jr <i@stingr.net> - 0.0.30-1
- Preparing for submission to fedora extras
