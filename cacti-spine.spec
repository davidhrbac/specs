Summary:	A backend data gatherer for cacti
Name:		cacti-spine
Version:	0.8.7g
Release:	1%{?dist}
License:	GPL
Group:		Applications
Source0:	http://www.cacti.net/downloads/spine/%{name}-%{version}.tar.gz
#Source0:        cacti-spine-SVN20080923.tar.gz
#Patch0:		snmp_v3_fix.patch
#Patch1:		mysql_client_reconnect.patch
#Patch2:		ping_reliability.patch
URL:		http://www.cacti.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	mysql-devel
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
Requires:	cacti
Provides:	cacti-cactid
Obsoletes:	cacti-cactid
BuildRoot:	%{_tmppath}/%{name}-root

%description
A backend data gatherer for cacti. This package represents the future
replacement for cacti's cmd.php. It is almost 100% compatible with the
legacy cmd.php processor.

%prep
%setup -q  
#%patch0 -p1
#%patch1 -p1
#%patch2 -p1

%build
%{__libtoolize} --force
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	--with-mysql \
	--with-snmp=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install spine.conf.dist $RPM_BUILD_ROOT%{_sysconfdir}
mv $RPM_BUILD_ROOT%{_sysconfdir}/spine.conf.dist $RPM_BUILD_ROOT%{_sysconfdir}/spine.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/spine.conf

%changelog
* Wed Jul 14 2010 David Hrbáč <david@hrbac.cz> - 0.8.7g-1
- new upstream release

* Fri Jan 08 2010 David Hrbáč <david@hrbac.cz> - 0.8.7e-2
- added three patches (2009/08/18) from http://www.cacti.net/spine_download_patches.php

* Tue Sep 23 2008 David Hrbáč <david@hrbac.cz> - 0.8.7a-3.20080923svn
- take the svn version

* Tue Sep 23 2008 David Hrbáč <david@hrbac.cz> - 0.8.7a-2
- patch for buffer overflow on 64bit

* Mon May 19 2008 David Hrbáč <david@hrbac.cz> - 0.8.7a-1
- CentOS rebuild
