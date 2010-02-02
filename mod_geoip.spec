Summary: GeoIP module for the Apache HTTP Server
Name: mod_geoip
Version: 1.2.5
Release: 2%{?dist}
License: Apache Software License
Group: System Environment/Daemons
URL: http://www.maxmind.com/app/mod_geoip
Source: http://www.maxmind.com/download/geoip/api/mod_geoip2/mod_geoip2_%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: GeoIP httpd httpd-mmn = %([ -a %{_includedir}/httpd/.mmn ] && cat %{_includedir}/httpd/.mmn || echo missing)
BuildRequires: httpd-devel GeoIP-devel
Patch0: mod_geoip-ipv6.patch

%description
mod_geoip is an Apache module for finding the country that a web request
originated from.  It uses the GeoIP library and database to perform
the lookup.  It is free software, licensed under the Apache license.

%prep

%setup -n mod_geoip2_%{version}
%patch0 -p0

%build
/usr/sbin/apxs -Wc,"%{optflags}" -Wl,"-lGeoIP" -c mod_geoip.c

%install
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -Dp .libs/mod_geoip.so %{buildroot}%{_libdir}/httpd/modules/mod_geoip.so

cat << EOF > %{buildroot}%{_sysconfdir}/httpd/conf.d/mod_geoip.conf
LoadModule geoip_module modules/mod_geoip.so

<IfModule mod_geoip.c>
  GeoIPEnable On
  GeoIPEnableUTF8 On
  GeoIPDBFile /var/lib/GeoIP/GeoIP.dat
  GeoIPDBFile /var/lib/GeoIP/GeoIPv6.dat
</IfModule>

EOF

%clean
rm -rf %{buildroot}

%files
%defattr (-,root,root)
%doc INSTALL README* Changes
%{_libdir}/httpd/modules/mod_geoip.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_geoip.conf

%changelog
* Fri Jan 29 2010 David Hrbáč <david@hrbac.cz> - 1.2.5-2
- better mod_geoip.conf
- experimental support for GEOIP_COUNTRY_EDITION_V6
- experimental support for GeoIPUseLastXForwardedForIP

* Wed Sep 17 2008 David Hrbáč <david@hrbac.cz> - 1.2.5-1
- new upstream version

* Wed Sep 17 2008 David Hrbáč <david@hrbac.cz> - 1.2.4-2
- initial rebuild

* Fri Jun 20 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 1.2.4-2
- New upstream update
- Minor spec tweaks

* Sun Apr 13 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 1.2.2-1
- New upstream update

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.0-2
- Autorebuild for GCC 4.3

* Wed Sep 5 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 1.2.0-1
- New upstream release
- Employ some macro sanity..

* Sun Sep 3 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.1.8-2
- Bump and rebuild

* Mon May 1 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.1.8-1
- New upstream release

* Sat Feb 18 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.1.7-2
- Small cleanups, including a saner Requires: for httpd
- Don't strip the binary

* Sun Feb 5 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.1.7-1
- Initial review package for Extras

