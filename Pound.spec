%define pound_user   pound
%define pound_group  pound
%define pound_home   %{_localstatedir}/lib/pound

Name:        Pound
Version:     2.4.4
Release:     4%{?dist}
Summary:     Reverse proxy and load balancer

Group:       System Environment/Daemons
License:     GPLv3
URL:         http://www.apsis.ch/pound
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires: openssl-devel, pcre-devel

# tcmalloc doesn't exist on ppc yet (#238390)
# or sparc arches
#%ifnarch ppc ppc64 sparcv9 sparc64
#BuildRequires: google-perftools-devel
#%endif

Requires(pre):    %{_sbindir}/useradd
Requires(pre):    %{_sbindir}/groupadd
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service

Source0:  http://www.apsis.ch/pound/%{name}-%{version}.tgz
Source1:  pound.init
Source2:  pound.cfg
Patch0:   pound-remove-owner.patch
Patch1:   pound-2.4.4-openssl.patch

%description
The Pound program is a reverse proxy, load balancer and
HTTPS front-end for Web server(s). Pound was developed
to enable distributing the load among several Web-servers
and to allow for a convenient SSL wrapper for those Web
servers that do not offer it natively. Pound is distributed
under the GPL - no warranty, it's free to use, copy and
give away

%prep
%setup -q
%patch0 -p1 -b .remove-owner
%patch1 -p1 -b .openssl

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%{__install} -d %{buildroot}%{pound_home}
%{__install} -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/pound
%{__install} -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pound.cfg 

mkdir -p %{buildroot}%{_sysconfdir}/pki/tls/certs
touch %{buildroot}%{_sysconfdir}/pki/tls/certs/pound.pem

%clean
rm -rf %{buildroot}

%pre
%{_sbindir}/groupadd -f -r %{pound_group}
id %{pound_user} >/dev/null 2>&1 || \
    %{_sbindir}/useradd -r -g %{pound_group} -d %{pound_home} -s /sbin/nologin \
    -c "Pound user" %{pound_user}

%post
/sbin/chkconfig --add pound

# generate dummy certificate
exec > /dev/null 2> /dev/null
if [ ! -f %{_sysconfdir}/pki/tls/certs/pound.pem ] ; then
pushd %{_sysconfdir}/pki/tls/certs
umask 077
cat << EOF | make pound.pem
--
SomeState
SomeCity
Pound Example Certificate
SomeOrganizationalUnit
localhost.localdomain
root@localhost.localdomain
EOF
chown root:pound pound.pem
chmod 640 pound.pem
popd
fi
exit 0

%preun
if [ $1 = 0 ]; then
    /sbin/service pound stop >/dev/null 2>&1
    /sbin/chkconfig --del pound
fi

%postun
if [ $1 -ge 1 ] ; then
    /sbin/service pound condrestart > /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc CHANGELOG FAQ GPL.txt README
%{_mandir}/man8/pound.8*
%{_mandir}/man8/poundctl.8*
%{_sbindir}/pound
%{_sbindir}/poundctl
%{_initrddir}/pound
%config(noreplace) %{_sysconfdir}/pound.cfg
%ghost %config(noreplace) %{_sysconfdir}/pki/tls/certs/pound.pem
%attr(-,%{pound_user},%{pound_group}) %dir %{pound_home}

%changelog
* Fri Oct 30 2009 David Hrbáč <david@hrbac.cz> - 2.4.4-4
- initial rebuild

* Wed Aug 26 2009 Tomas Mraz <tmraz@redhat.com> - 2.4.4-4
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.4.4-1
- upstream released new version

* Mon Oct 13 2008 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.4.3-1
- Upstream released new version

* Fri Jun 27 2008 Dennis Gilmore <dennis@ausil.us> 2.4-2
- sparc arches dont have tcmalloc

* Sat Feb 16 2008 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.4-1
- New stable version

* Sat Feb 09 2008 Ruben Kerkhof <ruben@rubenkerkhof.com> - 2.4-0.2f
- Upstream released new version

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 2.4-0.2
- Rebuild for deps

* Sun Dec 01 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.4.0-1e
- Update to experimental version 2.4e
* Thu Aug 16 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.4.0-1d
- Update to experimental version 2.4d
- Upstream changed license to GPLv3
* Wed Jun 04 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.4.0-1c
- Upstream released new version
* Sat May 26 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.4.0-2b
- Disable linking with tcmalloc on ppc (#238390)
* Fri May 25 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.4-0.1b
- Update to experimental version 2.4b
- Better handling of user creation
- Build with tcmalloc for increased performance
* Wed Apr 11 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.3-1
- Update to 2.3
* Thu Apr 05 2007 <ruben@rubenkerkhof.com> 2.2.8-1
- Sync with upstream
* Mon Mar 12 2007 <ruben@rubenkerkhof.com> 2.2.7-1
- Sync with upstream
* Sun Mar 04 2007 <ruben@rubenkerkhof.com> 2.2.6-1
- Sync with upstream
* Wed Feb 21 2007 <ruben@rubenkerkhof.com> 2.2.5-1
- Sync with upstream
* Sat Feb 10 2007 <ruben@rubenkerkhof.com> 2.2.4-1
- Sync with upstream
* Sat Jan 20 2007 <ruben@rubenkerkhof.com> 2.2.3-1
- Fix problems in bad 2.2.2 release
* Mon Jan 15 2007 <ruben@rubenkerkhof.com> 2.2.2-1
- Sync with upstream
* Wed Jan 03 2007 <ruben@rubenkerkhof.com> 2.2.1-1
- Sync with new beta release from upstream
* Sun Dec 17 2006 <ruben@rubenkerkhof.com> 2.2-2
- Fixed empty debuginfo rpm (bz 219942)
* Sat Dec 16 2006 <ruben@rubenkerkhof.com> 2.2-1
- Sync with upstream
* Sat Dec 09 2006 <ruben@rubenkerkhof.com> 2.1.8-1
- Sync with upstream
* Thu Dec 07 2006 <ruben@rubenkerkhof.com> 2.1.7-1
- Sync with upstream
* Wed Nov 08 2006 <ruben@rubenkerkhof.com> 2.1.6-2
- Changed hardcoded paths into rpmmacros
* Mon Nov 06 2006 <ruben@rubenkerkhof.com> 2.1.6-1
- Synced with upstream version
- Changed Summary
- Added an init script
- Added pound.cfg with an example configuration
- Added pound user and group
- A self-signed ssl certificate is created in %%post
* Fri Nov 03 2006 <ruben@rubenkerkhof.com> 2.1.5-1
- initial version

