# data_stamp should be the date of the included database as Source1.
# When a new database is included, this should be changed.
%define data_stamp %(date +\%Y\%m\%d)

Name:		GeoIP
Version:	1.4.8
Release:	1%{?dist}
Summary:	C library finding what country an IP/hostname originates from

Group:		System Environment/Libraries
License:	GPL
URL:		http://www.maxmind.com/app/c
Source0:	http://www.maxmind.com/download/geoip/api/c/%{name}-%{version}.tar.gz

#added by CentOS, newest GeoIP database as a seperate source
Source1:	http://www.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
Source2:	http://www.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
Source3:	http://www.maxmind.com/download/geoip/database/GeoIPv6.dat.gz
Source4:	http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
Source5:	geoip-fetch

Buildrequires: gzip
Buildrequires: zlib-devel
Buildrequires: csv2bin

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
GeoIP is a C library that enables the user to find the country that any IP
address or hostname originates from. It uses a file based database that is
accurate as of March 2003. This database simply contains IP blocks as keys,
and countries as values. This database should be more complete and accurate
than using reverse DNS lookups. Commercial databases and automatic update
services are available from http://www.maxmind.com/

This module can be used to automatically select the geographically closest
mirror, to analyze your web server logs to determine the countries of your
visitors, for credit card fraud detection, and for software export controls.

%package devel
Summary:	GeoIP headers, libraries
Group:		Development/Libraries
Requires:	%{name} <= %{version}

%description devel
This package contain the devel files for GeoIP.

%package data
Summary: GeoIP database file
Group: System Environment/Libraries
Version: %{data_stamp}
Release: %{release}
Requires: %{name}

%description data
This package contains the database for ipt_geoip.

%package databin
Summary: GeoIP csv to bin file
Group: System Environment/Libraries
Version: %{data_stamp}
Release: %{release}
#Requires: %{name}

%description databin
This package contains the csv file convertet to bin for ipt_geoip.

%package datacsv
Summary: GeoIP csv file
Group: System Environment/Libraries
Version: %{data_stamp}
Release: %{release}
#Requires: %{name}

%description datacsv
This package contains the csv file for GeoIP.

%prep
%setup -q

#added by CentOS ... use latest GeoIP database 
%{__cp} -a  %{SOURCE1} data/
gunzip -f data/GeoIP.dat.gz

%{__mkdir} datacsv
%{__cp} -a  %{SOURCE2} data/
unzip data/GeoIPCountryCSV.zip -d data

%{__cp} -a  %{SOURCE3} data/
gunzip -f data/GeoIPv6.dat.gz

%{__cp} -a  %{SOURCE4} data/
gunzip -f data/GeoLiteCity.dat.gz


csv2bin data/GeoIPCountryWhois.csv
%{__cp} -a geoipdb.* data/
#

%build
# --with-dbdir doesn't work!
%configure --datadir=%{_localstatedir}/lib
%{__make} %{?_smp_mflags}
#%{?!_without_test:%{__make} check}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%makeinstall

# fix CONF_DIR in geoipupdate man page
%{__sed} 's,CONF_DIR,%{_sysconfdir},' man/geoipupdate.1 > $RPM_BUILD_ROOT/%{_mandir}/man1/geoipupdate.1

# Fixup permissions on shared libraries so that findreqs will work right.
%{__chmod} 755 $RPM_BUILD_ROOT%{_libdir}/*

# strip binaries
%{__strip} $RPM_BUILD_ROOT%{_bindir}/*
%{__strip} $RPM_BUILD_ROOT%{_libdir}/*.so.*

# put databases where they should be
%{__install} -d $RPM_BUILD_ROOT/%{_localstatedir}/lib
%{__mv} $RPM_BUILD_ROOT/%{_datadir}/%{name} $RPM_BUILD_ROOT/%{_localstatedir}/lib/

install -D -m 0644 data/GeoIPv6.dat $RPM_BUILD_ROOT/%{_localstatedir}/lib/%{name}/GeoIPv6.dat
install -D -m 0644 data/GeoLiteCity.dat $RPM_BUILD_ROOT/%{_localstatedir}/lib/%{name}/GeoLiteCity.dat
install -D -m 0644 data/GeoIPCountryWhois.csv $RPM_BUILD_ROOT/%{_localstatedir}/lib/%{name}/GeoIPCountryWhois.csv
install -D -m 0644 data/geoipdb.* $RPM_BUILD_ROOT/%{_localstatedir}/lib/%{name}/
install -D -m 0755 %{SOURCE5} %{buildroot}%{_sbindir}/geoip-fetch


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README TODO conf/GeoIP.conf.default
%attr(0755,root,root) %{_libdir}/*.so.*
%{_bindir}/*
%{_sbindir}/geoip-fetch
%config(noreplace) %{_sysconfdir}/*
%exclude %{_sysconfdir}/*.default
%dir %{_localstatedir}/lib/%{name}
%{_mandir}/*/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%exclude %{_libdir}/*.la

%files data
%defattr(-,root,root)
%{_localstatedir}/lib/%{name}/*.dat

%files databin
%defattr(-,root,root)
%{_localstatedir}/lib/%{name}/geoipdb.*

%files datacsv
%defattr(-,root,root)
%{_localstatedir}/lib/%{name}/*.csv

%changelog
* Fri Feb 22 2013 David Hrbáč <david@hrbac.cz> - 1.4.8-1
- new upstream release

* Mon Oct 24 2011 David Hrbáč <david@hrbac.cz> - 1.4.7-1
- new upstream release

* Thu Jul 16 2009 David Hrbáč <david@hrbac.cz> - 1.4.6-2
- added CVS to bin database for ipt_geoip

* Thu Jul  2 2009 David Hrbáč <david@hrbac.cz> - 1.4.6-1
- new upstream version
- added CVS database
- added IPV6 database
- added City Lite database
- new GeoIP data fetch tool (geoip-fetch)

* Wed Sep 17 2008 David Hrbáč <david@hrbac.cz> - 1.4.5-1
- new upstream version

* Wed Sep 17 2008 David Hrbáč <david@hrbac.cz> - 1.4.4-1
- initial rebuild, upgrade db to Sep 2008

* Tue Apr  1 2008 Johnny Hughes
- upgraded to upstream version 1.4.4 and to the Mar 2008 dataabse

* Wed Jul  4 2007 Johnny Hughes <johnny@centos.org> 1.4.2-1%{?dist}
- upgraded to upstream version 1.4.2 and to the Jul 2007 database

* Wed Sep 13 2006 Johnny Hughes <johnny@centos.org> 1.4.0-1%{?dist}
- upgraded to upstream version 1.4.0 and to the Sep 2006 database

* Thu May  4 2006 Johnny Hughes <johnny@centos.org> 1.3.14-2%{dist}
- modified to add the May 2006 database

* Sat Feb 11 2006 Johnny Hughes <johnny@centos.org> 1.3.14-1%{dist}
- built for Centos Extras, modified to allow importing new database
 
* Thu Feb 02 2006 Marius FERARU <altblue@n0i.net> 1.3.14-1.n0i.1
- version 1.3.14

* Mon Aug 01 2005 Marius FERARU <altblue@n0i.net> 1.3.13-1.n0i.1
- version 1.3.13

* Sat Jul 23 2005 Marius FERARU <altblue@n0i.net> 1.3.8-3.n0i.1
- minor spec tweaks
- rebuild

* Sat Dec 04 2004 Marius FERARU <altblue@n0i.net> 0:1.3.8-2.n0i.2
- version 1.3.8

* Thu Jan 08 2004 Marius FERARU <altblue@n0i.net> 0:1.3.1-0.n0i.1
- Fedora-ized spec file
- moved .so files into devel package
- excluded duplicate configuration file
- excluded *.la filed from devel package
- stripped binaries
- moved dbdir into /var/lib/%{name}
- moved database file into a separate package
- fixed CONF_DIR in geoipupdate man page

* Mon Sep  8 2003 Dr. Peter Bieringer
- Fix for RHL 9, created a new devel package definition.

* Thu Feb 27 2003 Ryan Weaver <ryanw@falsehope.com>
- Initial RPM Build
