Name:           libnfnetlink
Version:        0.0.33
Release: 1%{?dist}
Summary:        Netfilter netlink userspace library
Group:          System Environment/Libraries
License:        GPL
URL:            http://netfilter.org
Source0:        http://netfilter.org/projects/libnfnetlink/files/%{name}-%{version}.tar.bz2
Source1:	http://www.gnu.org/licenses/gpl.txt
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  
#Requires:       

%description
libnfnetlink is a userspace library that provides some low-level
nfnetlink handling functions.  It is used as a foundation for other, netfilter
subsystem specific libraries such as libnfnetlink_conntrack, libnfnetlink_log
and libnfnetlink_queue.

%package        devel
Summary:        Netfilter netlink userspace library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
libnfnetlink is a userspace library that provides some low-level
nfnetlink handling functions.  It is used as a foundation for other, netfilter
subsystem specific libraries such as libnfnetlink_conntrack, libnfnetlink_log
and libnfnetlink_queue.

%prep
%setup -q
cp %{SOURCE1} LICENSE


%build
%configure --disable-static
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
%doc README LICENSE
%{_libdir}/*.so.*


%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/libnfnetlink
%{_includedir}/libnfnetlink/*.h

%changelog
* Wed Apr  9 2008 David Hrbáč <david@hrbac.cz> - 0.0.33-1
- CentOS rebuild
- new upstream version 

* Thu Aug 30 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.30-1
- new upstream version

* Sun Mar 25 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.25-2
- grab ownership of some directories

* Fri Feb  9 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.25-1
- upstream version 0.0.25

* Sun Sep 10 2006 Paul P. Komkoff Jr <i@stingr.net>
- rebuilt

* Wed Jul 12 2006 Felipe Kellermann <stdfk@terra.com.br> - 0.0.16-1
- Adds pkgconfig to devel files.
- Version 0.0.16.

* Mon May  8 2006 Paul P Komkoff Jr <i@stingr.net> - 0.0.14-3
- Include borrowed gpl.txt as LICENSE in %doc

* Sun Mar 26 2006 Paul P Komkoff Jr <i@stingr.net> - 0.0.14-1
- Preparing for submission to fedora extras

