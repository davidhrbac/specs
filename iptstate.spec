Name: iptstate
Summary: A top-like display of IP Tables state table entries
Version: 2.2.1
Release: 3%{?dist}
Source: iptstate-%{version}.tar.bz2
Patch0: iptstate-2.1-man8.patch
Patch1: iptstate-2.2.1-strerror.patch
Group: System Environment/Base
URL: http://www.phildev.net/iptstate/
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
License: zlib
Requires: iptables
BuildRequires: ncurses-devel
BuildRequires: libnetfilter_conntrack-devel

%description
IP Tables State (iptstate) was originally written to implement
the "state top" feature of IP Filter (see "The Idea" below) in
IP Tables. "State top" displays the states held by your stateful
firewall in a top-like manner.

Since IP Tables doesn't have a built in way to easily display 
this information even once, an option was added to just have it 
display the state table once.
 
  Features include:
        - Top-like realtime state table information
        - Sorting by any field
        - Reversible sorting
        - Single display of state table
        - Customizable refresh rate
        - Display filtering
        - Color-coding
        - Open Source
        - much more...

%prep
%setup -q
%patch0 -p1 -b .man8
%patch1 -p1 -b .strerror

%build
make CXXFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}
%makeinstall PREFIX=%{buildroot}%{_prefix}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc LICENSE README
%{_sbindir}/iptstate
%{_mandir}/man8/iptstate.*

%changelog
* Wed Apr  9 2008 David Hrbáč <david@hrbac.cz> - 2.2.1-3
- CentOS rebuild

* Mon Feb 25 2008 Thomas Woerner <twoerner@redhat.com> 2.2.1-3
- fixed compile problem because of strerror undefined in scope
  Fixes (rhbz#434482)
- fixed description (rhbz#140516)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.2.1-2
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Thomas Woerner <twoerner@redhat.com> 2.2.1-1
- added dist tag

* Tue Aug 21 2007 Thomas Woerner <twoerner@redhat.com> 2.2.1-1
- new version 2.2.1
- spec file fixes

* Wed Oct 25 2006 Thomas Woerner <twoerner@redhat.com> 2.1-1
- new version 2.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.4-1.1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.4-1.1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.4-1.1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Apr 18 2005 Thomas Woerner <twoerner@redhat.com> 1.4-1.1
- fixed man page: install as man8 instead of man1, fixed reference for
  iptables(8)

* Sun Apr 17 2005 Warren Togami <wtogami@redhat.com> 1.4-1
- 1.4

* Wed Feb  9 2005 Thomas Woerner <twoerner@redhat.com> 1.3-5
- rebuild

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb  2 2004 Thomas Woerner <twoerner@redhat.com> 1.3-2
- added BuildRequires for ncurses-devel

* Mon Jan 26 2004 Thomas Woerner <twoerner@redhat.com> 1.3-1
- initial package
