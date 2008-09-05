Name:           conntrack-tools
Version:        0.9.7
Release: 1%{?dist}
Summary:        Tools to manipulate netfilter connection tracking table
Group:          System Environment/Base
License:        GPLv2
URL:            http://netfilter.org
Source0:        http://netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
#Patch0:         conntrack-tools-0.9.5-open.patch
Patch1:         conntrack-tools-rollup.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libnfnetlink-devel libnetfilter_conntrack-devel pkgconfig bison flex
Provides:       conntrack = 1.0-1
Obsoletes:      conntrack < 1.0-1

%description
The conntrack-tools package contains two programs:
- conntrack: the command line interface to interact with the connection
             tracking system.
- conntrackd: the connection tracking userspace daemon that can be used to
              deploy highly available GNU/Linux firewalls and collect
              statistics of the firewall use.

conntrack is used to search, list, inspect and maintain the netfilter
connection tracking subsystem of the Linux kernel.
Using conntrack, you can dump a list of all (or a filtered selection  of)
currently tracked connections, delete connections from the state table, 
and even add new ones.
In addition, you can also monitor connection tracking events, e.g. 
show an event message (one line) per newly established connection.

%prep
#%setup -q -n %{name}
%setup -q

#%patch0 -p1
%patch1 -p1
#autoreconf -i --force

%build
%configure --disable-static
%{__make} %{?_smp_mflags}
#find examples -type f | xargs chmod a-x

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING AUTHORS INSTALL TODO
%{_sbindir}/conntrack
%{_sbindir}/conntrackd
%{_mandir}/man8/*

%changelog
* Wed Sep  3 2008 David Hrbáč <david@hrbac.cz> - 0.9.7-1
- new upstream version

* Wed Apr  9 2008 David Hrbáč <david@hrbac.cz> - 0.9.6-1
- new upstream version

* Wed Apr  9 2008 David Hrbáč <david@hrbac.cz> - 0.9.5-3
- CentOS rebuild

* Tue Oct 23 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.9.5-3
- review fixes

* Sun Oct 21 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.9.5-2
- review fixes

* Fri Oct 19 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.9.5-1
- new upstream version

* Sun Jul 22 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.9.4-1
- replace conntrack with conntrack-tools
