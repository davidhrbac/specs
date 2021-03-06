Summary: Dovecot Secure imap server
Name: dovecot
Epoch: 1
Version: 1.1.20
Release: 1%{?dist}
License: MIT and LGPLv2 and BSD with advertising
Group: System Environment/Daemons

%define build_postgres 1
%define build_mysql 1
%define build_sqlite 1
%define build_ldap 1
%define build_gssapi 1

%define build_sieve 1
%define build_managesieve 1
%define sieve_version 1.1.8
%define sieve_name dovecot-sieve
%define managesieve_version 0.10.7
%define managesieve_name dovecot-1.1-managesieve

URL: http://www.dovecot.org/
Source: http://www.dovecot.org/releases/1.1/%{name}-%{version}.tar.gz
Source1: dovecot.init
Source2: dovecot.pam
Source3: maildir-migration.txt
Source4: migrate-folders
Source5: migrate-users
Source6: perfect_maildir.pl
Source7: dovecot-REDHAT-FAQ.txt
Source8: http://dovecot.org/releases/sieve/%{sieve_name}-%{sieve_version}.tar.gz
Source9: dovecot.sysconfig
Source10: http://www.rename-it.nl/dovecot/1.1/%{managesieve_name}-%{managesieve_version}.tar.gz
Source11: http://www.rename-it.nl/dovecot/1.1/dovecot-1.1.19-managesieve-%{managesieve_version}.diff.gz
Patch0: dovecot-1.1.19-managesieve-%{managesieve_version}.diff.gz
Patch1: dovecot-1.1-default-settings.patch
Patch2: dovecot-1.0.beta2-mkcert-permissions.patch
# local filesystem rules
Patch3: dovecot-1.0.rc7-mkcert-paths.patch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: openssl-devel, pam-devel, zlib-devel
BuildRequires: libtool autoconf automake
# gettext-devel is needed for running autoconf because of the
# presence of AM_ICONV
BuildRequires: gettext-devel
# Explicit Runtime Requirements
Requires: openssl >= 0.9.7f-4
# Package includes an initscript service file, needs to require initscripts package
Requires: initscripts
Requires(pre): /usr/sbin/useradd
Requires(post): /sbin/chkconfig, /usr/sbin/useradd, /sbin/chkconfig
Requires(preun): /usr/sbin/userdel, /usr/sbin/groupdel, /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service

%if %{build_postgres}
BuildRequires: postgresql-devel
%endif

%if %{build_mysql}
BuildRequires: mysql-devel
%endif

%if %{build_sqlite}
BuildRequires: sqlite-devel
%endif

%if %{build_ldap}
BuildRequires: openldap-devel
%endif

%if %{build_gssapi}
BuildRequires: krb5-devel
%endif

%define docdir %{_docdir}/%{name}
%define ssldir %{_sysconfdir}/pki/%{name}

%description
Dovecot is an IMAP server for Linux/UNIX-like systems, written with security 
primarily in mind.  It also contains a small POP3 server.  It supports mail 
in either of maildir or mbox formats.

The SQL drivers and authentication plugins are in their subpackages.


%if %{build_sieve}
%package sieve
Requires: %{name} = %{epoch}:%{version}-%{release}
Summary: CMU Sieve plugin for dovecot LDA
Group: System Environment/Daemons
License: MIT and LGPLv2+

%description sieve
This package provides the CMU Sieve plugin version %{sieve_version} for dovecot LDA.
%endif

%if %{build_managesieve}
%package managesieve
Requires: %{name} = %{epoch}:%{version}-%{release}
Summary: Manage Sieve daemon for dovecot
Group: System Environment/Daemons
License: LGPLv2.1

%description managesieve
This package provides the Manage Sieve daemon version %{managesieve_version} for dovecot.
%endif

%if %{build_postgres}
%package pgsql
Requires: %{name} = %{epoch}:%{version}-%{release}
Summary: Postgres SQL backend for dovecot
Group: System Environment/Daemons
%description pgsql
This package provides the Postgres SQL backend for dovecot-auth etc.
%endif

%if %{build_mysql}
%package mysql
Requires: %{name} = %{epoch}:%{version}-%{release}
Summary: MySQL backend for dovecot
Group: System Environment/Daemons
%description mysql
This package provides the MySQL backend for dovecot-auth etc.
%endif

%if %{build_sqlite}
%package sqlite
Requires: %{name} = %{epoch}:%{version}-%{release}
Summary: SQLite backend for dovecot
Group: System Environment/Daemons
%description sqlite
This package provides the SQLite backend for dovecot-auth etc.
%endif

%if %{build_ldap}
%package ldap
Requires: %{name} = %{epoch}:%{version}-%{release}
Summary: LDAP auth plugin for dovecot
Group: System Environment/Daemons
%description ldap
This package provides the LDAP auth plugin for dovecot-auth etc.
%endif

%if %{build_gssapi}
%package gssapi
Requires: %{name} = %{epoch}:%{version}-%{release}
Summary: GSSAPI auth mechanism plugin for dovecot
Group: System Environment/Daemons
%description gssapi
This package provides the GSSAPI auth mechanism plugin for dovecot-auth etc.
%endif

%package devel
Requires: %{name} = %{epoch}:%{version}-%{release}
Summary: Development files dor dovecot
Group: Development/Libraries
%description devel
This package provides the development files for dovecot.


%prep

%setup -q

%patch0 -p1 -b .managesieve
%patch1 -p1 -b .default-settings
%patch2 -p1 -b .mkcert-permissions
%patch3 -p1 -b .mkcert-paths

%if %{build_sieve}
%setup -q -D -T -a 8
%endif

%if %{build_managesieve}
%setup -q -D -T -a 10
%endif

%build
rm -f ./configure
autoreconf -i -f
%configure                           \
    INSTALL_DATA="install -c -p -m644" \
    --enable-header-install      \
    --disable-static             \
%if %{build_postgres}
    --with-pgsql                 \
%endif
%if %{build_mysql}
    --with-mysql                 \
%endif
%if %{build_sqlite}
    --with-sqlite                \
%endif
    --with-sql=plugin            \
    --with-sql-drivers           \
    --with-ssl=openssl           \
    --with-ssldir=%{ssldir}      \
%if %{build_ldap}
    --with-ldap=plugin           \
%endif
%if %{build_gssapi}
    --with-gssapi=plugin
%endif

make %{?_smp_mflags}

%if %{build_sieve}
cd %{sieve_name}-%{sieve_version}

rm -f ./configure
autoreconf -i -f
%configure                           \
    INSTALL_DATA="install -c -p -m644" \
    --disable-static                 \
    --with-dovecot=../

make %{?_smp_mflags}
%endif

%if %{build_managesieve}
cd ..
cd %{managesieve_name}-%{managesieve_version}

rm -f ./configure
autoreconf -i -f
%configure                           \
    INSTALL_DATA="install -c -p -m644" \
    --disable-static                 \
    --with-dovecot=../               \
    --with-dovecot-sieve=../%{sieve_name}-%{sieve_version}/

make %{?_smp_mflags}
%endif

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}

install -p -m 755 src/plugins/convert/convert-tool $RPM_BUILD_ROOT%{_libexecdir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/dovecot

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/dovecot

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -p -m 600 %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/dovecot

# generate ghost .pem file
mkdir -p $RPM_BUILD_ROOT%{ssldir}/certs
mkdir -p $RPM_BUILD_ROOT%{ssldir}/private
touch $RPM_BUILD_ROOT%{ssldir}/certs/dovecot.pem
chmod 600 $RPM_BUILD_ROOT%{ssldir}/certs/dovecot.pem
touch $RPM_BUILD_ROOT%{ssldir}/private/dovecot.pem
chmod 600 $RPM_BUILD_ROOT%{ssldir}/private/dovecot.pem

mkdir -p $RPM_BUILD_ROOT/var/run/dovecot/login
chmod 755 $RPM_BUILD_ROOT/var/run/dovecot
chmod 700 $RPM_BUILD_ROOT/var/run/dovecot/login
	
# Install dovecot.conf and dovecot-openssl.cnf
mkdir -p $RPM_BUILD_ROOT%{ssldir}
install -p -m644 dovecot-example.conf $RPM_BUILD_ROOT%{_sysconfdir}/dovecot.conf
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/dovecot-*example.conf # dovecot seems to install this by itself
install -p -m644 doc/dovecot-openssl.cnf $RPM_BUILD_ROOT%{ssldir}/dovecot-openssl.cnf

# Install some of our own documentation
install -p -m644 %{SOURCE7} $RPM_BUILD_ROOT%{docdir}/REDHAT-FAQ.txt

# Install the licensing files into the documentation area
install -p -m644 COPYING* $RPM_BUILD_ROOT%{docdir}

mkdir -p $RPM_BUILD_ROOT%{docdir}/examples/
install -p -m755 doc/mkcert.sh $RPM_BUILD_ROOT%{_libexecdir}/%{name}/mkcert.sh
for f in `cd doc; echo *.conf`; do
     install -p -m644 doc/$f $RPM_BUILD_ROOT%{docdir}/examples/$f;
done

install -p -m755 -d $RPM_BUILD_ROOT%{docdir}/UW-to-Dovecot-Migration
for f in %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6}
do
    install -p -m644 $f $RPM_BUILD_ROOT%{docdir}/UW-to-Dovecot-Migration
done

mv $RPM_BUILD_ROOT%{docdir} $RPM_BUILD_ROOT%{docdir}-%{version}
mkdir -p $RPM_BUILD_ROOT/var/lib/dovecot

%if %{build_sieve}
# dovecot-sieve
pushd %{sieve_name}-%{sieve_version}
make install DESTDIR=$RPM_BUILD_ROOT
popd
%endif

%if %{build_managesieve}
# dovecot-managesieve
pushd %{managesieve_name}-%{managesieve_version}
make install DESTDIR=$RPM_BUILD_ROOT
popd
%endif

#remove the libtool archives
find $RPM_BUILD_ROOT%{_libdir}/%{name}/ -name '*.la' | xargs rm -f

#prepare the filelist
(
    find ${RPM_BUILD_ROOT}%{_libdir}/%{name} -type d | sed -e "s|^|%dir |";
    find ${RPM_BUILD_ROOT}%{_libdir}/%{name} -! -type d | \
        grep -v 'dovecot-config\|lib90_cmusieve_plugin\.so\|libdriver_.*\.so\|libauthdb_.*\.so\|libmech_.*\.so';
) | sed -e "s|$RPM_BUILD_ROOT||" >libs.filelist


%clean
rm -rf $RPM_BUILD_ROOT


%pre
getent group dovecot >/dev/null || groupadd -r dovecot
getent passwd dovecot >/dev/null || \
useradd -r -g dovecot -d /usr/libexec/dovecot -s /sbin/nologin -c "Dovecot IMAP server" dovecot
exit 0

%post
/sbin/chkconfig --add %{name}
# generate the ssl certificates
if [ ! -f %{ssldir}/certs/%{name}.pem ]; then
    SSLDIR=%{ssldir} OPENSSLCONFIG=%{ssldir}/dovecot-openssl.cnf \
         %{_libexecdir}/%{name}/mkcert.sh &> /dev/null
fi

if ! test -f /var/run/dovecot/login/ssl-parameters.dat; then
    dovecot --build-ssl-parameters &>/dev/null
fi
exit 0

%preun
if [ $1 = 0 ]; then
    /sbin/service %{name} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" -ge "1" ]; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi


%files -f libs.filelist
%defattr(-,root,root,-)
%doc %{docdir}-%{version}
%config(noreplace) %{_sysconfdir}/dovecot.conf
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/dovecot
%{_initrddir}/dovecot
%config(noreplace) %{_sysconfdir}/pam.d/dovecot
%dir %{ssldir}
%dir %{ssldir}/certs
%dir %{ssldir}/private
%config(noreplace) %{ssldir}/dovecot-openssl.cnf
%attr(0600,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{ssldir}/certs/dovecot.pem
%attr(0600,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{ssldir}/private/dovecot.pem
%{_libexecdir}/%{name}
%{_sbindir}/dovecot
%{_sbindir}/dovecotpw
%attr(0755,root,dovecot) %dir /var/run/dovecot
%attr(0750,root,dovecot) %dir /var/run/dovecot/login
#%attr(0755,root,dovecot) %{_libexecdir}/%{name}/mkcert.sh
%attr(0750,dovecot,dovecot) %dir /var/lib/dovecot

%if %{build_sieve}
%files sieve
%defattr(-,root,root,-)
%{_libdir}/%{name}/lda/lib90_cmusieve_plugin.so
%endif

%if %{build_managesieve}
%files managesieve
%defattr(-,root,root,-)
%{_libexecdir}/%{name}/managesieve
%{_libexecdir}/%{name}/managesieve-login
%endif

%if %{build_mysql}
%files mysql
%defattr(-,root,root,-)
%{_libdir}/%{name}/sql/libdriver_mysql.so
%{_libdir}/%{name}/auth/libdriver_mysql.so
%{_libdir}/%{name}/dict/libdriver_mysql.so
%endif

%if %{build_postgres}
%files pgsql
%defattr(-,root,root,-)
%{_libdir}/%{name}/sql/libdriver_pgsql.so
%{_libdir}/%{name}/auth/libdriver_pgsql.so
%{_libdir}/%{name}/dict/libdriver_pgsql.so
%endif

%if %{build_sqlite}
%files sqlite
%defattr(-,root,root,-)
%{_libdir}/%{name}/sql/libdriver_sqlite.so
%{_libdir}/%{name}/auth/libdriver_sqlite.so
%{_libdir}/%{name}/dict/libdriver_sqlite.so
%endif

%if %{build_ldap}
%files ldap
%defattr(-,root,root,-)
%{_libdir}/%{name}/auth/libauthdb_ldap.so
%endif

%if %{build_gssapi}
%files gssapi
%defattr(-,root,root,-)
%{_libdir}/%{name}/auth/libmech_gssapi.so
%endif

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/%{name}/dovecot-config


%changelog
* Tue Nov 10 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.20-1
- dovecot updated to 1.1.20:
- upgraded to Unicode 5.2.0
- Maildir: Fixed crash when using a lot of keywords.

* Fri Sep 18 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.19-1
- dovecot updated to 1.1.19
- ldap: Fixed hang when >128 requests were sent at once.
- fixed a crash in saving messages where message contained a CR
  character that wasn't followed by LF (and the CR happened to be the
  last character in an internal buffer).
- deliver: Don't send rejects to any messages that have Auto-Submitted
  header. This avoids emails loops.
- Message decoding fixes (mainly for IMAP SEARCH, Sieve).

* Mon Sep 14 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.18-2
- dovecot-sieve updated to 1.1.7
- fixes bug similar to CVE-2009-2632 (buffer overflow)

* Wed Jul 29 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.18-1
- updated to 1.1.18
- Maildir++ quota: Quota was sometimes updated wrong when it was
  being recalculated.
- Searching quoted-printable message body internally converted "_"
  characters to spaces and didn't match search keys with "_".

* Mon Jul 13 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.17-1
- updated to 1.1.17
- IMAP: Don't crash if IDLE command is pipelined after a long-running
  UID FETCH or UID SEARCH.
- mbox: Don't write garbage to mbox if message doesn't have a body.
- Maildir: Fixed using in-memory indexes when some required directory
  was missing.
- auth: Don't assert-crash if trying to log in as master user but
  with empty login username.
- Several fixes to expire plugin / expire-tool
- managesive updated: improved handling of script truncation 
  bugs: connection is now closed

* Wed Jun 03 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.16-1
- updated to 1.1.16

* Fri May 22 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.15-1
- updated to 1.1.15

* Wed Feb 11 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.14-1
- updated to 1.1.14

* Wed Feb 11 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.11-1
- updated to 1.1.11
- IMAP: PERMANENTFLAGS list didn't contain \*, causing some clients
  not to save keywords.
- auth: Using "username" or "domain" passdb fields caused problems
  with cache and blocking passdbs in v1.1.8 .. v1.1.10.
- userdb prefetch + blocking passdbs was broken with non-plaintext
  auth in v1.1.8 .. v1.1.10.

* Tue Jan 27 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.10-1
- update dovecot to 1.1.10
- added managesieve support

* Thu Jan 8 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.8-1
- update dovecot to 1.1.8 (Resolves: #475848)
- update dovecot sieve plugin to 1.1.6

* Mon Nov 3 2008 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.7-1
- update to upstream version 1.1.7
- revert changes from 1.1.6-2 and 1.1.6-1
- password can be stored in different file readable only for root 
  via !include_try directive

* Mon Nov 3 2008 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.6-2
- changed comment in sysconfig to match actual state

* Mon Nov 3 2008 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.6-1
- update to upstream version 1.1.6
- change permissions of deliver and dovecot.conf to prevent possible password exposure

* Wed Oct 29 2008 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.5-1
- update to upstream version 1.1.5 (Resolves: CVE-2008-4577, CVE-2008-4578)

* Tue Sep  2 2008 Dan Horak <dan[at]danny.cz> - 1:1.1.3-1
- update to upstream version 1.1.3

* Tue Jul 29 2008 Dan Horak <dan[at]danny.cz> - 1:1.1.2-2
- really ask for the password during start-up

* Tue Jul 29 2008 Dan Horak <dan[at]danny.cz> - 1:1.1.2-1
- update to upstream version 1.1.2
- final solution for #445200 (add /etc/sysconfig/dovecot for start-up options)

* Fri Jun 27 2008 Dan Horak <dan[at]danny.cz> - 1:1.1.1-2
- update default settings to listen on both IPv4 and IPv6 instead of IPv6 only

* Sun Jun 22 2008 Dan Horak <dan[at]danny.cz> - 1:1.1.1-1
- update to upstream version 1.1.1

* Sat Jun 21 2008 Dan Horak <dan[at]danny.cz> - 1:1.1.0-1
- update to upstream version 1.1.0
- update sieve plugin to 1.1.5
- remove unnecessary patches
- enable ldap and gssapi plugins
- change ownership of dovecot.conf (Resolves: #452088)

* Wed Jun 18 2008 Dan Horak <dan[at]danny.cz> - 1:1.0.14-4
- update init script (Resolves: #451838)

* Fri Jun  6 2008 Dan Horak <dan[at]danny.cz> - 1:1.0.14-3
- build devel subpackage (Resolves: #306881)

* Thu Jun  5 2008 Dan Horak <dan[at]danny.cz> - 1:1.0.14-2
- install convert-tool (Resolves: #450010)

* Tue Jun  3 2008 Dan Horak <dan[at]danny.cz> - 1:1.0.14-1
- update to upstream version 1.0.14
- remove setcred patch (use of setcred must be explictly enabled in config)

* Thu May 29 2008 Dan Horak <dan[at]danny.cz> - 1:1.0.13-8
- update scriptlets to follow UsersAndGroups guideline
- remove support for upgrading from version < 1.0 from scriptlets
- Resolves: #448095

* Tue May 20 2008 Dan Horak <dan[at]danny.cz> - 1:1.0.13-7
- spec file cleanup
- update sieve plugin to 1.0.3
- Resolves: #445200, #238018

* Sun Mar 09 2008 Tomas Janousek <tjanouse@redhat.com> - 1:1.0.13-6
- update to latest upstream stable (1.0.13)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:1.0.10-5
- Autorebuild for GCC 4.3

* Fri Jan 07 2008 Tomas Janousek <tjanouse@redhat.com> - 1:1.0.10-4
- update to latest upstream stable (1.0.10)

* Wed Dec 05 2007 Jesse Keating <jkeating@redhat.com> - 1:1.0.7-3
- Bump for deps

* Mon Nov 05 2007 Tomas Janousek <tjanouse@redhat.com> - 1:1.0.7-2
- update to latest upstream stable (1.0.7)
- added the winbind patch (#286351)

* Tue Sep 25 2007 Tomas Janousek <tjanouse@redhat.com> - 1:1.0.5-1
- downgraded to lastest upstream stable (1.0.5)

* Wed Aug 22 2007 Tomas Janousek <tjanouse@redhat.com> - 1.1-16.1.alpha3
- updated license tags

* Mon Aug 13 2007 Tomas Janousek <tjanouse@redhat.com> - 1.1-16.alpha3
- updated to latest upstream alpha
- update dovecot-sieve to 0367450c9382 from hg

* Fri Aug 10 2007 Tomas Janousek <tjanouse@redhat.com> - 1.1-15.alpha2
- updated to latest upstream alpha
- split ldap and gssapi plugins to subpackages

* Wed Jul 25 2007 Tomas Janousek <tjanouse@redhat.com> - 1.1-14.6.hg.a744ae38a9e1
- update to a744ae38a9e1 from hg
- update dovecot-sieve to 131e25f6862b from hg and enable it again

* Thu Jul 19 2007 Tomas Janousek <tjanouse@redhat.com> - 1.1-14.5.alpha1
- update to latest upstream alpha
- don't build dovecot-sieve, it's only for 1.0

* Sun Jul 15 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0.2-13.5
- update to latest upstream

* Mon Jun 18 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0.1-12.5
- update to latest upstream

* Fri Jun 08 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0.0-11.7
- specfile merge from 145241 branch
    - new sql split patch
    - support for not building all sql modules
    - split sql libraries to separate packages

* Sat Apr 14 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0.0-11.1
- dovecot-1.0.beta2-pam-tty.patch is no longer needed

* Fri Apr 13 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0.0-11
- update to latest upstream

* Tue Apr 10 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-10.rc31
- update to latest upstream

* Fri Apr 06 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-9.rc30
- update to latest upstream

* Fri Mar 30 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-8.1.rc28
- spec file cleanup (fixes docs path)

* Fri Mar 23 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-8.rc28
- update to latest upstream

* Mon Mar 19 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-7.rc27
- use dovecot-sieve's version for the package

* Mon Mar 19 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-6.rc27
- update to latest upstream
- added dovecot-sieve

* Fri Mar 02 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-5.rc25
- update to latest upstream

* Sun Feb 25 2007 Jef Spaleta <jspaleta@gmail.com> - 1.0-4.rc22
- Merge review changes

* Thu Feb 08 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-3.rc22
- update to latest upstream, fixes a few bugs

* Mon Jan 08 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-2.rc17
- update to latest upstream, fixes a few bugs

* Thu Dec 21 2006 Tomas Janousek <tjanouse@redhat.com> - 1.0-1.1.rc15
- reenabled GSSAPI (#220377)

* Tue Dec 05 2006 Tomas Janousek <tjanouse@redhat.com> - 1.0-1.rc15
- update to latest upstream, fixes a few bugs, plus a security
  vulnerability (#216508, CVE-2006-5973)

* Tue Oct 10 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.3.rc7
- fix few inconsistencies in specfile, fixes #198940

* Wed Oct 04 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.2.rc7
- fix default paths in the example mkcert.sh to match configuration
  defaults (fixes #183151)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.0-0.1.rc7
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.rc7
- update to latest upstream release candidate, should fix occasional
  hangs and mbox issues... INBOX. namespace is still broken though
- do not run over symlinked certificates in new locations on upgrade

* Tue Aug 15 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.rc2.2
- include /var/lib/dovecot in the package, prevents startup failure
  on new installs

* Mon Jul 17 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.rc2.1
- reenable inotify and see what happens

* Thu Jul 13 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.rc2
- update to latest upstream release candidate
- disable inotify for now, doesn't build -- this needs fixing though

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0-0.beta8.2.1
- rebuild

* Thu Jun 08 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta8.2
- put back pop3_uidl_format default that got lost
  in the beta2->beta7 upgrade (would cause pop3 to not work
  at all in many situations)

* Thu May 04 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta8.1
- upgrade to latest upstream beta release (beta8)
- contains a security fix in mbox handling

* Thu May 04 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta7.1
- upgrade to latest upstream beta release
- fixed BR 173048

* Fri Mar 17 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta2.8
- fix sqlite detection in upstream configure checks, second part
  of #182240

* Wed Mar  8 2006 Bill Nottingham <notting@redhat.com> - 1.0-0.beta2.7
- fix scriplet noise some more

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 1.0-0.beta2.6
- fix scriptlet error (mitr, #184151)

* Mon Feb 27 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta2.5
- fix #182240 by looking in lib64 for libs first and then lib
- fix comment #1 in #182240 by copying over the example config files
  to documentation directory

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0-0.beta2.4.1
- bump again for double-long bug on ppc(64)

* Thu Feb 09 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta2.4
- enable inotify as it should work now (#179431)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0-0.beta2.3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta2.3
- change the compiled-in defaults and adjust the default's configfile
  commented-out example settings to match compiled-in defaults,
  instead of changing the defaults only in the configfile, as per #179432
- fix #179574 by providing a default uidl_format for pop3
- half-fix #179620 by having plaintext auth enabled by default... this
  needs more thinking (which one we really want) and documentation
  either way

* Tue Jan 31 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta2.2
- update URL in description
- call dovecot --build-ssl-parameters in postinst as per #179430

* Mon Jan 30 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta2.1
- fix spec to work with BUILD_DIR != SOURCE_DIR
- forward-port and split pam-nocred patch

* Mon Jan 23 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta2
- new upstream version, hopefully fixes #173928, #163550
- fix #168866, use install -p to install documentation

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 12 2005 Tom Lane <tgl@redhat.com> - 0.99.14-10.fc5
- Rebuild due to mysql update.

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> - 0.99.14-9.fc5
- rebuilt with new openssl

* Fri Sep 30 2005 Tomas Mraz <tmraz@redhat.com> - 0.99.14-8.fc5
- use include instead of pam_stack in pam config

* Wed Jul 27 2005 John Dennis <jdennis@redhat.com> - 0.99.14-7.fc5
- fix bug #150888, log authenication failures with ip address

* Fri Jul 22 2005 John Dennis <jdennis@redhat.com> - 0.99.14-6.fc5
- fix bug #149673, add dummy PAM_TTY

* Thu Apr 28 2005 John Dennis <jdennis@redhat.com> - 0.99.14-5.fc4
- fix bug #156159 insecure location of restart flag file

* Fri Apr 22 2005 John Dennis <jdennis@redhat.com> - 0.99.14-4.fc4
- openssl moved its certs, CA, etc. from /usr/share/ssl to /etc/pki

* Tue Apr 12 2005 Tom Lane <tgl@redhat.com> 0.99.14-3.fc4
- Rebuild for Postgres 8.0.2 (new libpq major version).

* Mon Mar  7 2005 John Dennis <jdennis@redhat.com> 0.99.14-2.fc4
- bump rev for gcc4 build

* Mon Feb 14 2005 John Dennis <jdennis@redhat.com> - 0.99.14-1.fc4
- fix bug #147874, update to 0.99.14 release
  v0.99.14 2005-02-11  Timo Sirainen <tss at iki.fi>
  - Message address fields are now parsed differently, fixing some
    issues with spaces. Affects only clients which use FETCH ENVELOPE
    command.
  - Message MIME parser was somewhat broken with missing MIME boundaries
  - mbox: Don't allow X-UID headers in mails to override the UIDs we
    would otherwise set. Too large values can break some clients and
    cause other trouble.
  - passwd-file userdb wasn't working
  - PAM crashed with 64bit systems
  - non-SSL inetd startup wasn't working
  - If UID FETCH notices and skips an expunged message, don't return
    a NO reply. It's not needed and only makes clients give error
    messages.

* Wed Feb  2 2005 John Dennis <jdennis@redhat.com> - 0.99.13-4.devel
- fix bug #146198, clean up temp kerberos tickets

* Mon Jan 17 2005 John Dennis <jdennis@redhat.com> 0.99.13-3.devel
- fix bug #145214, force mbox_locks to fcntl only
- fix bug #145241, remove prereq on postgres and mysql, allow rpm auto
  dependency generator to pick up client lib dependency if needed.

* Thu Jan 13 2005 John Dennis <jdennis@redhat.com> 0.99.13-2.devel
- make postgres & mysql conditional build
- remove execute bit on migration example scripts so rpm does not pull
  in additional dependences on perl and perl modules that are not present
  in dovecot proper.
- add REDHAT-FAQ.txt to doc directory

* Thu Jan  6 2005 John Dennis <jdennis@redhat.com> 0.99.13-1.devel
- bring up to date with latest upstream, 0.99.13, bug #143707
  also fix bug #14462, bad dovecot-uid macro name

* Thu Jan  6 2005 John Dennis <jdennis@redhat.com> 0.99.11-10.devel
- fix bug #133618, removed LITERAL+ capability from capability string

* Wed Jan  5 2005 John Dennis <jdennis@redhat.com> 0.99.11-9.devel
- fix bug #134325, stop dovecot during installation

* Wed Jan  5 2005 John Dennis <jdennis@redhat.com> 0.99.11-8.devel
- fix bug #129539, dovecot starts too early,
  set chkconfig to 65 35 to match cyrus-imapd
- also delete some old commented out code from SSL certificate creation

* Thu Dec 23 2004 John Dennis <jdennis@redhat.com> 0.99.11-7.devel
- add UW to Dovecot migration documentation and scripts, bug #139954
  fix SSL documentation and scripts, add missing documentation, bug #139276

* Thu Nov 15 2004 Warren Togami <wtogami@redhat.com> 0.99.11-2.FC4.1
- rebuild against MySQL4

* Thu Oct 21 2004 John Dennis <jdennis@redhat.com>
- fix bug #136623
  Change License field from GPL to LGPL to reflect actual license

* Thu Sep 30 2004 John Dennis <jdennis@redhat.com> 0.99.11-1.FC3.3
- fix bug #124786, listen to ipv6 as well as ipv4

* Wed Sep  8 2004 John Dennis <jdennis@redhat.com> 0.99.11-1.FC3.1
- bring up to latest upstream,
  comments from Timo Sirainen <tss at iki.fi> on release v0.99.11 2004-09-04  
  + 127.* and ::1 IP addresses are treated as secured with
    disable_plaintext_auth = yes
  + auth_debug setting for extra authentication debugging
  + Some documentation and error message updates
  + Create PID file in /var/run/dovecot/master.pid
  + home setting is now optional in static userdb
  + Added mail setting to static userdb
  - After APPENDing to selected mailbox Dovecot didn't always notice the
    new mail immediately which broke some clients
  - THREAD and SORT commands crashed with some mails
  - If APPENDed mail ended with CR character, Dovecot aborted the saving
  - Output streams sometimes sent data duplicated and lost part of it.
    This could have caused various strange problems, but looks like in
    practise it rarely caused real problems.

* Wed Aug  4 2004 John Dennis <jdennis@redhat.com>
- change release field separator from comma to dot, bump build number

* Mon Aug  2 2004 John Dennis <jdennis@redhat.com> 0.99.10.9-1,FC3,1
- bring up to date with latest upstream, fixes include:
- LDAP support compiles now with Solaris LDAP library
- IMAP BODY and BODYSTRUCTURE replies were wrong for MIME parts which
  didn't contain Content-Type header.
- MySQL and PostgreSQL auth didn't reconnect if connection was lost
  to SQL server
- Linking fixes for dovecot-auth with some systems
- Last fix for disconnecting client when downloading mail longer than
  30 seconds actually made it never disconnect client. Now it works
  properly: disconnect when client hasn't read _any_ data for 30
  seconds.
- MySQL compiling got broken in last release
- More PostgreSQL reconnection fixing


* Mon Jul 26 2004 John Dennis <jdennis@redhat.com> 0.99.10.7-1,FC3,1
- enable postgres and mySQL in build
- fix configure to look for mysql in alternate locations
- nuke configure script in tar file, recreate from configure.in using autoconf

- bring up to latest upstream, which included:
- Added outlook-pop3-no-nuls workaround to fix Outlook hang in mails with NULs.
- Config file lines can now contain quoted strings ("value ")
- If client didn't finish downloading a single mail in 30 seconds,
  Dovecot closed the connection. This was supposed to work so that
  if client hasn't read data at all in 30 seconds, it's disconnected.
- Maildir: LIST now doesn't skip symlinks


* Wed Jun 30 2004 John Dennis <jdennis@redhat.com>
- bump rev for build
- change rev for FC3 build

* Fri Jun 25 2004 John Dennis <jdennis@redhat.com> - 0.99.10.6-1
- bring up to date with upstream,
  recent change log comments from Timo Sirainen were:
  SHA1 password support using OpenSSL crypto library
  mail_extra_groups setting
  maildir_stat_dirs setting
  Added NAMESPACE capability and command
  Autocreate missing maildirs (instead of crashing)
  Fixed occational crash in maildir synchronization
  Fixed occational assertion crash in ioloop.c
  Fixed FreeBSD compiling issue
  Fixed issues with 64bit Solaris binary

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 27 2004 David Woodhouse <dwmw2@redhat.com> 0.99.10.5-1
- Update to 0.99.10.5 to fix maildir segfaults (#123022)

* Fri May 07 2004 Warren Togami <wtogami@redhat.com> 0.99.10.4-4
- default auth config that is actually usable
- Timo Sirainen (author) suggested functionality fixes
  maildir, imap-fetch-body-section, customflags-fix

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com>
- Use ':' instead of '.' as separator for chown.

* Tue Feb 17 2004 Jeremy Katz <katzj@redhat.com> - 0.99.10.4-3
- restart properly if it dies (#115594)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Nov 24 2003 Jeremy Katz <katzj@redhat.com> 0.99.10.4-1
- update to 0.99.10.4

* Mon Oct  6 2003 Jeremy Katz <katzj@redhat.com> 0.99.10-7
- another patch from upstream to fix returning invalid data on partial 
  BODY[part] fetches
- patch to avoid confusion of draft/deleted in indexes

* Tue Sep 23 2003 Jeremy Katz <katzj@redhat.com> 0.99.10-6
- add some patches from upstream (#104288)

* Thu Sep  4 2003 Jeremy Katz <katzj@redhat.com> 0.99.10-5
- fix startup with 2.6 with patch from upstream (#103801)

* Tue Sep  2 2003 Jeremy Katz <katzj@redhat.com> 0.99.10-4
- fix assert in search code (#103383)

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 0.99.10-3
- rebuild

* Thu Jul 17 2003 Bill Nottingham <notting@redhat.com> 0.99.10-2
- don't run by default

* Thu Jun 26 2003 Jeremy Katz <katzj@redhat.com> 0.99.10-1
- 0.99.10

* Mon Jun 23 2003 Jeremy Katz <katzj@redhat.com> 0.99.10-0.2
- 0.99.10-rc2 (includes ssl detection fix)
- a few tweaks from fedora
  - noreplace the config file
  - configure --with-ldap to get LDAP enabled

* Mon Jun 23 2003 Jeremy Katz <katzj@redhat.com> 0.99.10-0.1
- 0.99.10-rc1
- add fix for ssl detection
- add zlib-devel to BuildRequires
- change pam service name to dovecot
- include pam config

* Thu May  8 2003 Jeremy Katz <katzj@redhat.com> 0.99.9.1-1
- update to 0.99.9.1
- add patch from upstream to fix potential bug when fetching with 
  CR+LF linefeeds
- tweak some things in the initscript and config file noticed by the 
  fedora folks

* Sun Mar 16 2003 Jeremy Katz <katzj@redhat.com> 0.99.8.1-2
- fix ssl dir
- own /var/run/dovecot/login with the correct perms
- fix chmod/chown in post

* Fri Mar 14 2003 Jeremy Katz <katzj@redhat.com> 0.99.8.1-1
- update to 0.99.8.1

* Tue Mar 11 2003 Jeremy Katz <katzj@redhat.com> 0.99.8-2
- add a patch to fix quoting problem from CVS

* Mon Mar 10 2003 Jeremy Katz <katzj@redhat.com> 0.99.8-1
- 0.99.8
- add some buildrequires
- fixup to build with openssl 0.9.7
- now includes a pop3 daemon (off by default)
- clean up description and %%preun
- add dovecot user (uid/gid of 97)
- add some buildrequires
- move the ssl cert to %%{_datadir}/ssl/certs
- create a dummy ssl cert in %%post
- own /var/run/dovecot
- make the config file a source so we get default mbox locks of fcntl

* Sun Dec  1 2002 Seth Vidal <skvidal@phy.duke.edu>
- 0.99.4 and fix startup so it starts imap-master not vsftpd :)

* Tue Nov 26 2002 Seth Vidal <skvidal@phy.duke.edu>
- first build
