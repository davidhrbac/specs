%define upstream 1.0.7
%define pkg_version 1.0.7
%define my_release 7
%define pkg_release %{my_release}%{?dist}

Summary: Dovecot Secure imap server
Name: dovecot
Version: %{pkg_version}
Release: %{pkg_release}
License: LGPL
Group: System Environment/Daemons

%define build_postgres 1
%define build_mysql 1

Source: http://dovecot.org/releases/%{name}-%{upstream}.tar.gz
Source1: dovecot.init
Source2: dovecot.pam
Source3: maildir-migration.txt
Source4: migrate-folders
Source5: migrate-users
Source6: perfect_maildir.pl
Source7: dovecot-REDHAT-FAQ.txt
Source8: dovecot.sysconfig
Patch100: dovecot-1.0.7-default-settings.patch
Patch102: dovecot-1.0.rc2-pam-setcred.patch
Patch103: dovecot-1.0.beta2-mkcert-permissions.patch
Patch105: dovecot-1.0.rc7-mkcert-paths.patch

# XXX this patch needs review and forward porting
#Patch105: dovecot-auth-log.patch

# Patches 500+ from upstream fixes
Patch500: dovecot-1.0-CVE-2007-6598.patch
Patch501: dovecot-1.0-CVE-2008-1199.patch
Patch502: dovecot-1.0-CVE-2008-1218.patch
Patch503: dovecot-1.0-CVE-2008-4577.patch

#from upstream, required for dovecot <1.1.7
Patch504: dovecot-1.0-CVE-2008-4870.patch

URL: http://www.dovecot.org/
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: openssl-devel
BuildRequires: openldap-devel
BuildRequires: pam-devel
BuildRequires: pkgconfig
BuildRequires: zlib-devel
BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: krb5-devel
# gettext-devel is needed for running autoconf because of the
# presence of AM_ICONV
BuildRequires: gettext-devel
# Explicit Runtime Requirements
Requires: openssl >= 0.9.7f-4
# Package includes an initscript service file, needs to require initscripts package
Requires: initscripts
Requires(pre): /sbin/chkconfig, /usr/sbin/useradd, /sbin/service, /bin/touch, /bin/rm
Requires(post): /sbin/chkconfig, /usr/sbin/useradd, /sbin/chkconfig, /bin/mv, /bin/rm
Requires(preun): /usr/sbin/userdel, /usr/sbin/groupdel, /sbin/chkconfig, /sbin/service

%if %{build_postgres}
BuildRequires: postgresql-devel
%endif

%if %{build_mysql}
BuildRequires: mysql-devel
%endif

%define docdir %{_docdir}/%{name}
%define ssldir %{_sysconfdir}/pki/%{name}
%define restart_flag /var/run/%{name}-restart-after-rpm-install
%define dovecot_uid 97
%define dovecot_gid 97

%description
Dovecot is an IMAP server for Linux/UNIX-like systems, written with security 
primarily in mind.  It also contains a small POP3 server.  It supports mail 
in either of maildir or mbox formats.

%prep

%setup -q -n %{name}-%{upstream}

%patch100 -p1 -b .default-settings
%patch102 -p1 -b .pam-setcred
%patch103 -p1 -b .mkcert-permissions
%patch105 -p1 -b .mkcert-paths
%patch500 -p1 -b .CVE-2007-6598
%patch501 -p1 -b .CVE-2008-1199
%patch502 -p1 -b .CVE-2008-1218
%patch503 -p1 -b .CVE-2008-4577
%patch504 -p1 -b .CVE-2008-4870

%build
rm -f ./configure
libtoolize -f
autoreconf
%configure                           \
    INSTALL_DATA="install -c -p -m644" \
    --with-doc		             \
%if %{build_postgres}
    --with-pgsql                 \
%endif
%if %{build_mysql}
    --with-mysql                 \
%endif
    --with-ssl=openssl           \
    --with-ssldir=%{ssldir}      \
    --with-ldap                  \
    --with-inotify               \
    --with-gssapi

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_datadir}/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/dovecot

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/dovecot

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/dovecot

# generate ghost .pem file
mkdir -p $RPM_BUILD_ROOT/%{ssldir}/certs
mkdir -p $RPM_BUILD_ROOT/%{ssldir}/private
touch $RPM_BUILD_ROOT/%{ssldir}/certs/dovecot.pem
chmod 600 $RPM_BUILD_ROOT/%{ssldir}/certs/dovecot.pem
touch $RPM_BUILD_ROOT/%{ssldir}/private/dovecot.pem
chmod 600 $RPM_BUILD_ROOT/%{ssldir}/private/dovecot.pem

mkdir -p $RPM_BUILD_ROOT/var/run/dovecot/login
chmod 755 $RPM_BUILD_ROOT/var/run/dovecot
chmod 700 $RPM_BUILD_ROOT/var/run/dovecot/login
	
# Install dovecot.conf and dovecot-openssl.cnf
mkdir -p $RPM_BUILD_ROOT/%{ssldir}
install -p -m644 $RPM_BUILD_DIR/dovecot-%{upstream}/dovecot-example.conf $RPM_BUILD_ROOT/%{_sysconfdir}/dovecot.conf
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/dovecot-*example.conf # dovecot seems to install this by itself
install -p -m644 $RPM_BUILD_DIR/dovecot-%{upstream}/doc/dovecot-openssl.cnf $RPM_BUILD_ROOT/%{ssldir}/dovecot-openssl.cnf

# Install some of our own documentation
install -p -m644 %{SOURCE7} $RPM_BUILD_ROOT%{docdir}/REDHAT-FAQ.txt

# Install the licensing files into the documentation area
install -p -m644 $RPM_BUILD_DIR/dovecot-%{upstream}/COPYING  $RPM_BUILD_ROOT%{docdir}/COPYING
install -p -m644 $RPM_BUILD_DIR/dovecot-%{upstream}/COPYING.MIT  $RPM_BUILD_ROOT%{docdir}/COPYING.MIT
install -p -m644 $RPM_BUILD_DIR/dovecot-%{upstream}/COPYING.LGPL  $RPM_BUILD_ROOT%{docdir}/COPYING.LGPL

mkdir -p $RPM_BUILD_ROOT%{docdir}/examples/
install -p -m755 $RPM_BUILD_DIR/dovecot-%{upstream}/doc/mkcert.sh $RPM_BUILD_ROOT%{docdir}/examples/mkcert.sh
for f in `cd $RPM_BUILD_DIR/dovecot-%{upstream}/doc; echo *.conf`; do
	install -p -m644 $RPM_BUILD_DIR/dovecot-%{upstream}/doc/$f $RPM_BUILD_ROOT%{docdir}/examples/$f;
done

install -p -m755 -d $RPM_BUILD_ROOT%{docdir}/UW-to-Dovecot-Migration
for f in %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6}
do
    install -p -m644 $f $RPM_BUILD_ROOT%{docdir}/UW-to-Dovecot-Migration
done

mv $RPM_BUILD_ROOT%{docdir} $RPM_BUILD_ROOT%{docdir}-%{version}
mkdir -p $RPM_BUILD_ROOT/var/lib/dovecot

%pre
/usr/sbin/useradd -c "dovecot" -u %{dovecot_uid} -s /sbin/nologin -r -d /usr/libexec/dovecot dovecot 2>/dev/null || :

# stop service during installation, keep flag if it was running to restart later
rm -f %{restart_flag}
/sbin/service %{name} status >/dev/null 2>&1
if [ $? -eq 0 ]; then
    touch %{restart_flag}
    /sbin/service %{name} stop >/dev/null 2>&1
fi

%post
/sbin/chkconfig --add %{name}
# create a ssl cert
if [ -f %{ssldir}/%{name}.pem -a ! -e %{ssldir}/certs/%{name}.pem ]; then
    mv  %{ssldir}/%{name}.pem %{ssldir}/certs/%{name}.pem
else
    if [ -f /usr/share/ssl/certs/dovecot.pem -a ! -e %{ssldir}/certs/%{name}.pem ]; then
        mv /usr/share/ssl/certs/dovecot.pem %{ssldir}/certs/%{name}.pem
    fi
    if [ -f /usr/share/ssl/private/dovecot.pem -a ! -e %{ssldir}/private/%{name}.pem ]; then
        mv /usr/share/ssl/private/dovecot.pem %{ssldir}/private/%{name}.pem
    fi
fi
if [ ! -f %{ssldir}/certs/%{name}.pem ]; then
SSLDIR=%{ssldir} OPENSSLCONFIG=%{ssldir}/dovecot-openssl.cnf \
	%{docdir}-%{version}/examples/mkcert.sh &> /dev/null
fi

if ! test -f /var/run/dovecot/login/ssl-parameters.dat; then
    dovecot --build-ssl-parameters &>/dev/null
fi

# Restart if it had been running before installation
if [ -e %{restart_flag} ]; then
  rm %{restart_flag}
  /sbin/service %{name} start >/dev/null 2>&1
fi
exit 0


%preun
if [ $1 = 0 ]; then
 /usr/sbin/userdel dovecot 2>/dev/null || :
 /usr/sbin/groupdel dovecot 2>/dev/null || :
 [ -f /var/lock/subsys/%{name} ] && /sbin/service %{name} stop > /dev/null 2>&1
 /sbin/chkconfig --del %{name}
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc %{docdir}-%{version}
%config(noreplace) %{_sysconfdir}/dovecot.conf
%config %{_sysconfdir}/rc.d/init.d/dovecot
%config(noreplace) %{_sysconfdir}/pam.d/dovecot
%config(noreplace) %{_sysconfdir}/sysconfig/dovecot
%dir %{ssldir}
%dir %{ssldir}/certs
%dir %{ssldir}/private
%config(noreplace) %{ssldir}/dovecot-openssl.cnf
%attr(0600,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{ssldir}/certs/dovecot.pem
%attr(0600,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{ssldir}/private/dovecot.pem
%{_libexecdir}/%{name}
%{_libdir}/%{name}
%{_sbindir}/dovecot
%{_sbindir}/dovecotpw
%attr(0755,root,dovecot) %dir /var/run/dovecot
%attr(0750,root,dovecot) %dir /var/run/dovecot/login
%attr(0750,root,dovecot) %{docdir}-%{version}/examples/mkcert.sh
%attr(0750,dovecot,dovecot) %dir /var/lib/dovecot


%changelog
* Mon Nov 24 2008 Michal Hlavinka <mhlavink@redhat.com> - 1.0.7-7
- permissions of deliver and dovecot.conf from 1.0.7-5 reverted
- password can be stored in different file readable only for root now
- Resolves: #436287, CVE-2008-4870

* Fri Oct 31 2008 Michal Hlavinka <mhlavink@redhat.com> - 1.0.7-6
- added missing directory in file list
- Resolves: #436287

* Fri Oct 31 2008 Michal Hlavinka <mhlavink@redhat.com> - 1.0.7-5
- change permissions of deliver and dovecot.conf to prevent possible password exposure
- Resolves: #436287

* Wed Oct 29 2008 Michal Hlavinka <mhlavink@redhat.com> - 1.0.7-4
- fix handling of negative rights in the ACL plugin
- Resolves: #469015, CVE-2008-4577

* Fri Sep 12 2008 Dan Horak <dhorak@redhat.com> - 1.0.7-3
- fix package ownership for /etc/pki/dovecot/private (#448089)
- update init script (#238016)
- ask for SSL cert password during start-up (#436287)
- fix for illegal characters in passwd (#439369)
- Resolves: #448089, #238016, #436287, #439369

* Thu Mar 13 2008 Tomas Janousek <tjanouse@redhat.com> - 1.0.7-2
- LDAP+auth cache user login mixup (CVE-2007-6598, #427575)
- insecure mail_extra_groups option (CVE-2008-1199, #436927)

* Mon Nov 26 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0.7-1
- update to latest upstream, fixes a few bugs (#331441, #245249), plus two
  security vulnerabilities (CVE-2007-2231, CVE-2007-4211)
- increased default login_process_size to 64 (#253363)

* Fri Dec 22 2006 Tomas Janousek <tjanouse@redhat.com> - 1.0-1.2.rc15
- reenabled GSSAPI (#220582)

* Tue Nov 21 2006 Petr Rockai <prockai@redhat.com> - 1.0-1.rc15
- update to latest upstream, fixes a few bugs, plus a security
  vulnerability (#216510, CVE-2006-5973)

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
- move the ssl cert to %{_datadir}/ssl/certs
- create a dummy ssl cert in %post
- own /var/run/dovecot
- make the config file a source so we get default mbox locks of fcntl

* Sun Dec  1 2002 Seth Vidal <skvidal@phy.duke.edu>
- 0.99.4 and fix startup so it starts imap-master not vsftpd :)

* Tue Nov 26 2002 Seth Vidal <skvidal@phy.duke.edu>
- first build
