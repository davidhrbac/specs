Summary:        C library for portable packet creation and injection
Name:           libnet
Version:        1.1.2.1
Release:        12%{?dist}
License:        BSD
Group:          System Environment/Libraries
URL:            http://www.packetfactory.net/libnet/
Source0:        http://www.packetfactory.net/libnet/dist/libnet-%{version}.tar.gz
# excerpted from debian patcheset
Patch0:         libnet-1.1.2.1-odd_chksum.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Libnet is an API to help with the construction and handling of network packets.
It provides a portable framework for low-level network packet writing and
handling (use libnet in conjunction with libpcap and you can write some really
cool stuff).  Libnet includes packet creation at the IP layer and at the link
layer as well as a host of supplementary and complementary functionality.
Libnet is very handy with which to write network tools and network test code.
See the manpage and sample test code for more detailed information.

%package devel
Summary:        Development files for libnet
Group:          Development/Libraries
Provides:       %{name} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}

%description devel
Libnet is an API to help with the construction and handling of network packets.
It provides a portable framework for low-level network packet writing and
handling (use libnet in conjunction with libpcap and you can write some really
cool stuff).  Libnet includes packet creation at the IP layer and at the link
layer as well as a host of supplementary and complementary functionality.
Libnet is very handy with which to write network tools and network test code.
See the manpage and sample test code for more detailed information.


%prep
%setup -q -n libnet
%patch0 -p1 -b odd_chksum
sed -i -e 's/\r$//' doc/CHANGELOG doc/CONTRIB
find . -depth -type d -name CVS -exec rm -rf {} ';'
rm -f sample/.\#* sample/.*.swp


%build
# keep the sample directory untouched by make
rm -rf __fedora_sample
mkdir __fedora_sample 
cp -a sample __fedora_sample

export CFLAGS="%{optflags} -fPIC"
%configure --disable-dependency-tracking
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install INSTALL='install -c -p'

mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_mandir}/man3
install -p -m0755 libnet-config %{buildroot}%{_bindir}/libnet-config
install -p -m0644 doc/man/man3/libnet*.3 %{buildroot}%{_mandir}/man3/

# prepare samples directory
rm -rf __fedora_sample/sample/win32
rm __fedora_sample/sample/Makefile.in
sed -i -e 's:#include "../include/libnet.h":#include <libnet.h>:' __fedora_sample/sample/libnet_test.h

%clean
rm -rf %{buildroot}


%files devel
%defattr(-,root,root,-)
%doc README VERSION
%doc doc/BUGS doc/CHANGELOG doc/CONTRIB doc/COPYING doc/DESIGN_NOTES
%doc doc/MIGRATION doc/PACKET_BUILDING doc/PORTED doc/RAWSOCKET_NON_SEQUITUR
%doc doc/TODO doc/html/ __fedora_sample/sample/

%{_bindir}/libnet-config
%{_includedir}/libnet/
%{_includedir}/libnet.h
%{_libdir}/libnet.a
%{_mandir}/man3/libnet*


%changelog
* Sat Apr 12 2008 David Hrbáč <david@hrbac.cz> - 1.1.2.1-12
- CentOS rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.2.1-12
- Autorebuild for GCC 4.3

* Wed Aug  1 2007 Patrice Dumas <pertusus@free.fr> 1.1.2.1-11
- build with -fPIC (#250296)

* Fri Jan 12 2007 Patrice Dumas <pertusus@free.fr> 1.1.2.1-10
- add debian patch to correct bad checksums

* Tue Aug 29 2006 Patrice Dumas <pertusus@free.fr> 1.1.2.1-9
- rebuild for FC6

* Fri Feb 17 2006 Patrice Dumas <pertusus@free.fr> 1.1.2.1-8
- rebuild for fc5

* Thu Dec 22 2005 Patrice Dumas <pertusus@free.fr> 1.1.2.1-7
- rebuild

* Mon Sep 12 2005 Patrice Dumas <pertusus@free.fr> 1.1.2.1-6
- bump release and add dist tag

* Tue Aug 30 2005 Paul Howarth <paul@city-fan.org> 1.1.2.1-5
- spec file cleanup

* Fri Aug 26 2005 Patrice Dumas <pertusus@free.fr> 1.1.2.1-4
- use pushd and popd (from Oliver Falk) 

* Mon Aug 22 2005 Patrice Dumas <pertusus@free.fr> 1.1.2.1-3
- Correct dos end of lines
- add in devel: Provides: %%{name} = %%{version}-%%{release} 

* Fri Aug 12 2005 Patrice Dumas <pertusus@free.fr> 1.1.2.1-2
- put everything in a devel subpackage
- add smpflags
- clean in sample

* Fri Aug 12 2005 Patrice Dumas <pertusus@free.fr> 1.1.2.1-1
- rebuild changing only name

* Wed Jun 02 2004 Marcin Garski <garski@poczta.onet.pl> 1.1.2.1-2.fc2
- Rebuild for Fedora Core 2

* Sat May 08 2004 Marcin Garski <garski@poczta.onet.pl> 1.1.2.1-1
- Initial specfile
