Name:           trickle
Version:        1.07 
Release:        9%{?dist}
Summary:        Portable lightweight userspace bandwidth shaper

Group:          Applications/System
License:        BSD with advertising
URL:            http://monkey.org/~marius/pages/?page=trickle
Source0:        http://monkey.org/~marius/trickle/%{name}-%{version}.tar.gz
Source1:        %{name}d.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libevent-devel

Patch0:         %{name}-%{version}-include_netdb.patch
Patch1:         %{name}-%{version}-libdir.patch
Patch2:         %{name}-%{version}-CVE-2009-0415.patch

%description
trickle is a portable lightweight userspace bandwidth shaper.
It can run in collaborative mode or in stand alone mode.

trickle works by taking advantage of the unix loader preloading.
Essentially it provides, to the application, 
a new version of the functionality that is required 
to send and receive data through sockets.
It then limits traffic based on delaying the sending 
and receiving of data over a socket.
trickle runs entirely in userspace and does not require root privileges.

%prep
%setup -q
%patch0 -p1 -b .include_netdb
%patch1 -p1 -b .libdir
%patch2 -p1 -b .cve
touch -r configure aclocal.m4 Makefile.in stamp-h.in

iconv -f ISO88591 -t UTF8 < README > README.UTF8
mv README.UTF8 README

%build
%configure
# Parallel make is unsafe for this package, so %%{?_smp_mflags} is not used
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# for rpmlint warning : unstripped-binary-or-object
chmod +x $RPM_BUILD_ROOT%{_libdir}/%{name}/%{name}-overload.so
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE README TODO
%dir %{_libdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}d.conf
%{_bindir}/%{name}
%{_bindir}/%{name}ctl
%{_bindir}/%{name}d
%{_libdir}/%{name}/%{name}-overload.so
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man5/%{name}d.conf.5.gz
%{_mandir}/man8/%{name}d.8.gz


%changelog
* Fri Mar 12 2010 David Hrbáč <david@hrbac.cz> - 1.07-9
- initial rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Nicoleau Fabien <nicoleau.fabien@gmail.com> 1.07-7
- Replace sed with a patch for #484065 (CVE-2009-0415)
* Fri Feb  6 2009 Nicoleau Fabien <nicoleau.fabien@gmail.com> 1.07-6
- Add a fix for bug #484065 (CVE-2009-0415)
* Fri Aug 28 2008 Manuel Wolfshant <wolfy@fedoraproject.org> 1.07-5
- modify trickle-1.07-include_netdb.patch to adjust for building with fuzz=0
* Sun Jun 29 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> 1.07-4
- rebuild for new libevent
* Mon Jun 16 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> 1.07-3
- add configure.in
- add default configuration file for trickled
* Sun Jun 15 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> 1.07-2
- Licence changed
- ldconfig no more used
- dir macro used for libdir/name
- config.h file modified (/lib/ hardcoded)
* Sun Jun  8 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> 1.07-1
- Rebuild for version 1.07
- Removed smp_mflags flag for make
* Sat Jun  7 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> 1.06-1
- Initital build
