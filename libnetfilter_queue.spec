Name:           libnetfilter_queue
Version:        0.0.15
Release:        1%{?dist}
Summary:        Netfilter queue userspace library
Group:          System Environment/Libraries
License:        GPL
URL:            http://netfilter.org
Source0:        http://netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libnfnetlink-devel, pkgconfig

%description
libnetfilter_queue is a userspace library providing an API to packets that have
been queued by the kernel packet filter. It is is part of a system that
deprecates the old ip_queue / libipq mechanism.

libnetfilter_queue has been previously known as libnfnetlink_queue. 

%package        devel
Summary:        Netfilter queue userspace library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}, pkgconfig

%description    devel
libnetfilter_queue is a userspace library providing an API to packets that have
been queued by the kernel packet filter. It is is part of a system that
deprecates the old ip_queue / libipq mechanism.

libnetfilter_queue has been previously known as libnfnetlink_queue.

%prep
%setup -q

%build
%configure --disable-static --disable-rpath

# kill the rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

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
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Apr  9 2008 David Hrbáč <david@hrbac.cz> - 0.0.15-1
- CentOS rebuild

* Tue Sep 18 2007 Paul P Komkoff Jr <i@stingr.net> - 0.0.15-1
- new upstream version

* Mon Mar 26 2007 Paul P Komkoff Jr <i@stingr.net> - 0.0.13-3
- own some directories

* Mon Mar 19 2007 Paul P Komkoff Jr <i@stingr.net> - 0.0.13-2
- fix source url
- add pkgconfig to -devel Requires

* Sat Mar 17 2007 Paul P Komkoff Jr <i@stingr.net> - 0.0.13-1
- Preparing for submission to fedora extras
