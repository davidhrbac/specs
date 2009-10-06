Name: mod_mono
Version: 2.4.2
Release: 2%{?dist}
License: MIT
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: http://mono.ximian.com/monobuild/preview/sources-preview/
Source0: %{name}-%{version}.tar.bz2
BuildRequires: mono-devel >= 2.4.2, xsp-devel >= 2.4.2, pkgconfig, httpd-devel apr-devel
Patch0: mod_mono-2.0-varrun.patch
Requires: httpd >= 2.2, mono-core, xsp
Summary: A module to deploy an ASP.NET application on Apache with Mono
Group: System Environment/Daemons

ExclusiveArch: %ix86 x86_64 ia64 armv4l sparc alpha ppc ppc64

%description

mod_mono allows Apache to serve ASP.NET pages by proxying the requests 
to a slightly modified version of the XSP server, called mod-mono-server, 
that is installed along with XSP
 
%prep
%setup -q 
%patch0 -p1 -b .varrun

%build
%configure --disable-static
make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
mv %{buildroot}%{_sysconfdir}/httpd/conf/mod_mono* %{buildroot}%{_sysconfdir}/httpd/conf.d/
rm -rf %{buildroot}%{_sysconfdir}/httpd/conf

mkdir -p %{buildroot}/var/run/mod_mono

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING NEWS README INSTALL
%{_libdir}/httpd/modules/mod_mono.so*
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_mono.conf
%attr(0755,apache,apache) /var/run/mod_mono
%{_mandir}/man8/mod_mono.8*

%changelog
* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 09 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4.2-1
- Bump to 2.4.2 preview
- Reenable ppc
- Add in ppc64 support

* Mon Apr 06 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-4.1
- Remove ppc support

* Thu Mar 26 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-4
- Full 2.4 release

* Wed Mar 18 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-3.RC3
- Bump to RC3

* Tue Mar 10 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-3.RC2
- Bump to RC2

* Fri Feb 27 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-2.RC1
- Bump to RC1

* Sat Jan 28 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-1.pre1.20090124svn124159
- Update to 2.4
- altered BRs to use mono-2.4
- retagged as pre-1

* Fri Jan 09 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-4.RC2.20090901svn122806
- Bump to RC2
- Big update from svn

* Wed Dec 17 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-3.pre3.20081217svn117989
- Bump to preview 3
- Move to svn for bug fixes

* Sat Dec 06 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-2.pre2
- Bump to preview 2

* Tue Nov 25 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-1.pre1
- Bump to 2.2 preview 1
- incorporate fix to the var-run patch (thanks to Dario Lesca)

* Sat Oct 11 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-6
- use var run instead of tmp
- added additional Requires

* Fri Oct 10 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-5
- fix URLs

* Fri Oct 03 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-4
- bump to RC4

* Mon Sep 29 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-3
- bump to RC3

* Tue Sep 09 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-2
- bump to 2.0 RC 1

* Sun Aug 03 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-1
- bump to 2.0 preview 1
- licence changed and other spec file alterations

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.6-2.1
- Autorebuild for GCC 4.3

* Thu Dec 20 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.6-1.1
- remove arch ppc64

* Thu Nov 22 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.6-1
- bump 
- url fix

* Sun Nov 18 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.5-1
- bump

* Sat Apr 22 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.4-1
- bump

* Sat Nov 25 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.1-1
- bump

* Fri Nov 03 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2-1
- bump

* Sat Oct 14 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.18-1
- bump

* Fri Sep 08 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.17-3
- Spec file fixes
- Modified SOURCE0 and URL tags

* Thu Aug 31 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.17-1
- bump to new version
- Altered BR xsp to BR xsp-devel

* Sun Apr 23 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.14-3
- removed static libdir
- included archs mono is currently on

* Tue Apr 18 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.14-2
- libdir now usr-lib irrespective of the architecture built on
- minor change to spec file

* Mon Apr 17 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.14-1
- Initial import for FE
- Spec file based on the Novell version (though quite hacked)

