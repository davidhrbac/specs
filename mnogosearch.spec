%{?dist: %{expand: %%define dist_%dist 1}}

Summary:     A fast WWW search engine for websites
Name:        mnogosearch
Version:     3.3.6
Release:     2.%{mysig}
#Release:     7.%{?dist}%{?pext}
License:     GPL
Group:       Applications/Internet
Source0:     http://www.%{name}.org/Download/%{name}-%{version}.tar.gz
URL:         http://www.%{name}.org/
Buildroot:   /var/tmp/%{name}-root
Vendor:      Lavtech.Com Corp.
Packager: David Hrbac <david@hrbac.cz>
Provides:    %{name}.pp
#Requires:    mysql openssl oracle-runtime >= 9.2 readline unixODBC
Requires:    mysql openssl readline 
%if %{?dist_el3:1}%{!?dist_el3:0}
Requires:    rh-postgresql-libs
%else
Requires:    postgresql-libs
%endif
Prereq:      coreutils glibc
BuildPrereq: coreutils glibc-devel gcc make
BuildPrereq: mysql-devel openssl-devel 
#oracle-runtime-devel >= 9.2
BuildPrereq: readline-devel 
#unixODBC-devel
%if %{?dist_el3:1}%{!?dist_el3:0}
BuildPrereq: rh-postgresql-devel
%else
BuildPrereq: postgresql-devel
%endif
ExclusiveOS: linux

%description
mnoGoSearch (formerly known as UdmSearch) is a full-featured Web
search engine which you can use to build search engines over HTTP,
HTTPS, FTP, and NTTP servers, local files, and database big text
fields. It supports Oracle, MySQL, PostgreSQL, miniSQL, Solid,
Virtuoso, InterBase, SAPDB, iODBC, EasySoft ODBC, and unixODBC
database backends. mnoGoSearch is also known to work with MS SQL,
SyBase, and Oracle through ODBC. It has text/html and text/plain
built-in support, and external parsers support for other document
types. An automatic language/charset guesser for more 70 language/
charset combinations is included, along with basic authorization
support, and you may index password-protected intranet HTTP servers
with proxy authorization support.


%package devel
Summary:     Development tools for %{name}
Group:       Development/Libraries
Provides:    %{name}-devel.pp
Requires:    %{name} = %{version}-%{release} %{name}.pp

%description devel
The %{name}-devel package contains the static libraries and
header files for developing software using %{name}.


%prep
%setup -q

%ifarch x86_64
  perl -pi -e "s|/lib\b|/%{_lib}|g" configure*
%endif 

%build
export CFLAGS="${RPM_OPT_FLAGS}"
./configure \
	--prefix=%{_prefix}                             \
	--sysconfdir=%{_sysconfdir}/%{name}             \
	--localstatedir=%{_localstatedir}/cache/%{name} \
	--datadir=%{_datadir}/%{name}                   \
	--mandir=%{_mandir}                             \
	--enable-shared                                 \
	--enable-static                                 \
	--enable-syslog                                 \
	--with-openssl=%{_prefix}                       \
	--with-zlib                                     \
	--with-readline                                 \
	--with-mysql=%{_prefix}                         \
	--with-pgsql=%{_prefix}                        
# \
#	--with-unixODBC=%{_prefix}                      \
#	--with-oracle8i=/usr/lib/oracle/10.2.0.3/client/lib/
make all


# Do not strip, only compress documentation
%define __os_install_post /usr/lib/rpm/brp-compress


%install
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/cache/%{name}/{cache,raw,splitter,tree}
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/www/icons

make \
	DESTDIR=${RPM_BUILD_ROOT} \
	install

install -m 0644 misc/*.gif ${RPM_BUILD_ROOT}%{_localstatedir}/www/icons
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/doc


%post
ldconfig


%postun
ldconfig


%clean
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README* TODO
%doc doc/*.html doc/*.xml doc/*.css doc/*.dsl
%doc %dir doc/samples
%attr(755,root,root) %dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_bindir}/*
%{_libdir}/*.so*
%{_sbindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%attr(755,root,root) %dir %{_localstatedir}/cache/%{name}
%attr(755,root,root) %dir %{_localstatedir}/cache/%{name}/*
%{_localstatedir}/www/icons/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.*a


%changelog
* Mon Mar 31 2008 David Hrbáč <david@hrbac.cz> 3.3.6-2
- rewrite for Mock

* Mon Feb  4 2008 David Hrbáč <david@hrbac.cz> 3.3.6-1
- update to 3.3.6

* Fri Jul 27 2007 David Hrbáč <david@hrbac.cz> 3.3.3-2
- small changes

* Thu Jun 19 2007 David Hrbáč <david@hrbac.cz> 3.3.3-1
- initial spec created for CentOS-4
