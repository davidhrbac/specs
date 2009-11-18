%define base_version 1.2.8
%define mydns_user   mydns
%define mydns_group  mydns
%define mydns_home   %{_localstatedir}/lib/mydns

Summary: A Database based DNS server
Name: mydns
Version: 1.2.8.27
Release: 4%{?dist}
License: GPLv2+
Group: System Environment/Daemons
URL: http://mydns-ng.com/
#URL: http://mydns.bboy.net/  this is the original website, but mydns is no more  maintaned by it's original creator
#because this mydns-ng in sourceforge was created
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1: HOWTO
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: mysql-devel
BuildRequires: postgresql-devel
BuildRequires: texinfo

Requires(pre):     shadow-utils
Requires(post):    info
Requires(post):    chkconfig
Requires(preun):   info
Requires(preun):   chkconfig
Requires(preun):   initscripts

Patch0: mydns_user.patch
Patch1: mydns-start-after-mysql.patch

%description
A nameserver that serves records directly from your database.

%package mysql
Summary: MyDNS compiled with MySQL support
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires(post):    chkconfig
Requires(preun):   chkconfig
Requires(preun):   initscripts
Requires(postun):  initscripts



%description mysql
MyDNS compiled with MySQL support

%package pgsql
Summary: MyDNS compiled with PostGreSQL support
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires(post):    chkconfig
Requires(preun):   chkconfig
Requires(preun):   initscripts
Requires(postun):  initscripts



%description pgsql
MyDNS compiled with PostGreSQL support

%prep
%setup -q -n %{name}-%{base_version}
%patch0 -p1
%patch1 -p2

#install doc about alternatives
install -Dp -m 644 %{SOURCE1} ./HOWTO

# Convert to utf-8
for file in AUTHORS; do
    mv $file timestamp
    iconv -f ISO-8859-1 -t UTF-8 -o $file timestamp
    touch -r timestamp $file
done

%build
#mydns current doesn't support loadable modules support, so We need to compile it 2 times and use alternatives, :-(
%configure \
    --without-pgsql \
    --with-mysql \
    --with-mysql-lib=%{_libdir}/mysql \
    --with-mysql-include=%{_includedir}/mysql \
    --with-zlib=%{_libdir} \
    --enable-status \
    --enable-alias

make %{?_smp_mflags} 
make install DESTDIR=$(pwd)/mysql

%configure \
    --with-pgsql \
    --without-mysql \
    --with-pgsql-lib=%{_libdir} \
    --with-pgsql-include=%{_includedir} \
    --with-zlib=%{_libdir} \
    --enable-status \
    --enable-alias

make %{?_smp_mflags}
make install DESTDIR=$(pwd)/pgsql

%install
rm -rf %{buildroot}

#create homedir for mydns user
%{__install} -d %{buildroot}%{mydns_home}

#install mysql and pgsql files
for database in mysql pgsql; do
    install -Dp ./$database%{_bindir}/mydnscheck %{buildroot}%{_bindir}/mydnscheck-$database
    install -Dp ./$database%{_bindir}/mydns-conf %{buildroot}%{_bindir}/mydns-conf-$database
    install -Dp ./$database%{_bindir}/mydnsexport %{buildroot}%{_bindir}/mydnsexport-$database
    install -Dp ./$database%{_bindir}/mydnsptrconvert %{buildroot}%{_bindir}/mydnsptrconvert-$database
    install -Dp ./$database%{_bindir}/mydnsimport %{buildroot}%{_bindir}/mydnsimport-$database
    install -Dp ./$database%{_sbindir}/mydns %{buildroot}%{_sbindir}/mydns-$database

    install -d %{buildroot}%{_datadir}/locale
    cp -a ./$database%{_datadir}/locale %{buildroot}%{_datadir}
done

%find_lang %{name}

#main package (all files not linked with mysql or pgsql)
install -Dp -m 755 contrib/mydns.redhat %{buildroot}%{_initrddir}/mydns
install -Dp -m 600 mydns.conf %{buildroot}%{_sysconfdir}/mydns.conf
install -Dp -m 644 contrib/admin.php %{buildroot}%{_datadir}/%{name}/admin.php

install -Dp -m 644 doc/mydns.conf.5 %{buildroot}%{_mandir}/man5/mydns.conf.5
install -Dp -m 644 doc/mydns.8 %{buildroot}%{_mandir}/man8/mydns.8
install -Dp -m 644 doc/mydnscheck.8 %{buildroot}%{_mandir}/man8/mydnscheck.8
install -Dp -m 644 doc/mydnsexport.8 %{buildroot}%{_mandir}/man8/mydnsexport.8
install -Dp -m 644 doc/mydnsimport.8 %{buildroot}%{_mandir}/man8/mydnsimport.8
install -Dp -m 644 doc/mydns-conf.8 %{buildroot}%{_mandir}/man8/mydns-conf.8
install -Dp -m 644 doc/mydns.info %{buildroot}%{_infodir}/mydns.info

%clean
rm -rf %{buildroot}

%pre
getent group %{mydns_group} >/dev/null || groupadd -r %{mydns_group}
getent passwd %{mydns_user} >/dev/null || \
useradd -r -g %{mydns_group} -d %{mydns_home}  -s /sbin/nologin \
-c "MyDNS - database based DNS server account" %{mydns_user}
exit 0
	
%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir
/sbin/chkconfig --add %{name}
exit 0

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
exit 0
	    
%postun mysql
if [ "$1" -ge "1" ] ; then
   /sbin/service %{name} condrestart >/dev/null 2>&1
fi
exit 0

%postun pgsql
if [ "$1" -ge "1" ] ; then
   /sbin/service %{name} condrestart >/dev/null 2>&1
fi

%post pgsql
%{_sbindir}/alternatives --install %{_sbindir}/mydns MyDNS %{_sbindir}/mydns-pgsql 1 \
    --slave %{_bindir}/mydnscheck mydnscheck %{_bindir}/mydnscheck-pgsql \
    --slave %{_bindir}/mydnsexport mydnsexport %{_bindir}/mydnsexport-pgsql \
    --slave %{_bindir}/mydnsimport mydnsimport %{_bindir}/mydnsimport-pgsql \
    --slave %{_bindir}/mydnsptrconvert mydnsptrconvert %{_bindir}/mydnsptrconvert-pgsql

exit 0

%post mysql
%{_sbindir}/alternatives --install %{_sbindir}/mydns MyDNS %{_sbindir}/mydns-mysql 2 \
    --slave %{_bindir}/mydnscheck mydnscheck %{_bindir}/mydnscheck-mysql \
    --slave %{_bindir}/mydnsexport mydnsexport %{_bindir}/mydnsexport-mysql \
    --slave %{_bindir}/mydnsimport mydnsimport %{_bindir}/mydnsimport-mysql \
    --slave %{_bindir}/mydnsptrconvert mydnsptrconvert %{_bindir}/mydnsptrconvert-mysql

exit 0

%preun pgsql
# When not removal, exit immediately
[ $1 = 0 ] || exit 0
( LANG=C ; \
	if ( %{_sbindir}/alternatives --display MyDNS | \
		grep point | grep -q %{_sbindir}/mydns-pgsql ) ; \
		then %{_sbindir}/service %{name} stop >/dev/null 2>&1 ; \
	fi ; \
)
%{_sbindir}/alternatives -remove MyDNS %{_sbindir}/mydns-pgsql
exit 0


%preun mysql
# When not removal, exit immediately
[ $1 = 0 ] || exit 0
( LANG=C ; \
	if ( %{_sbindir}/alternatives --display MyDNS | \
		grep point | grep -q %{_sbindir}/mydns-mysql ) ; \
		then %{_sbindir}/service %{name} stop >/dev/null 2>&1 ; \
	fi ; \
)
%{_sbindir}/alternatives -remove MyDNS %{_sbindir}/mydns-mysql
exit 0


%files -f %{name}.lang
%defattr(-,root,root,-)
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_infodir}/mydns.info.gz
%doc AUTHORS ChangeLog COPYING NEWS README TODO HOWTO
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/mydns.conf
%{_initrddir}/mydns
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/admin.php
%attr(-,%{mydns_user},%{mydns_group}) %dir %{mydns_home}

%files mysql
%defattr(-,root,root,-)
%doc QUICKSTART.mysql
%{_bindir}/mydnscheck-mysql
%{_bindir}/mydns-conf-mysql
%{_bindir}/mydnsexport-mysql
%{_bindir}/mydnsptrconvert-mysql
%{_bindir}/mydnsimport-mysql
%{_sbindir}/mydns-mysql

%files pgsql
%defattr(-,root,root,-)
%doc QUICKSTART.postgres
%{_bindir}/mydnscheck-pgsql
%{_bindir}/mydns-conf-pgsql
%{_bindir}/mydnsexport-pgsql
%{_bindir}/mydnsptrconvert-pgsql
%{_bindir}/mydnsimport-pgsql
%{_sbindir}/mydns-pgsql

%changelog
* Wed Nov 18 2009 David Hrbáč <david@hrbac.cz> - 1.2.8.27-4
- initial rebuild

* Mon Aug 17 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.2.8.27-4
- make mydns start after mysql

* Tue Aug 04 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.2.8.27-3
- fix spec file for rhel

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 25 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.2.8.27-1
- New version 1.2.8.27

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 09 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 1.2.8.25-1
- upgrade to a new version
- various fixes from Comment #21 From  Mamoru Tasaka, bz #476832

* Tue Feb 03 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 1.2.8.23-3
- remove QUICKSTART.mysql from main package, let it alive in -mysql subpackage
- change the way to create user and group 
- enforce /etc/mydns.conf permissions

* Mon Feb 02 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 1.2.8.23-2
- add postun requires, simplify HOWTO about alternatives install

* Wed Feb 02 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 1.2.8.23-1
- upgrade to new version, remove init.d patch merged with upstream
- add --enable-status --enable-alias to configure script

* Wed Jan 30 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 1.2.8.22-2
- create separated mydns user and group

* Wed Jan 30 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 1.2.8.22-1
- upgrade to new version
- alot of improviments from bz #476832 Comment #10 From  Mamoru Tasaka

* Wed Jan 27 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 1.2.8.19-3
- fix some rpmlint messages about install-info and chkconfig

* Wed Jan 27 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 1.2.8.19-2
- add installinfo scriptlets

* Wed Jan 27 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 1.2.8.19-1
- upgrade to new version, improve spec files with alternatives

* Wed Jan 23 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 1.2.8.18-1
- create sub-packages for mysql and postgresql
- Rebuild for Fedora 10

* Thu Mar 27 2003 Don Moore <bboy@bboy.net>
- now installs startup scripts

* Fri Jul 12 2002 Don Moore <bboy@bboy.net>
- initial public release
