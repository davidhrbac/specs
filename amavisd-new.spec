#%%define prerelease rc2

Summary:        Email filter with virus scanner and spamassassin support
Name:           amavisd-new
Version:        2.6.2
Release:        3%{?prerelease:.%{prerelease}}%{?dist}
# LDAP schema is GFDL, some helpers are BSD, core is GPLv2+
License:        GPLv2+ and BSD and GFDL
Group:          Applications/System
URL:            http://www.ijs.si/software/amavisd/
Source0:        http://www.ijs.si/software/amavisd/amavisd-new-%{version}%{?prerelease:-%{prerelease}}.tar.gz
Source1:        amavis-clamd.init
Source2:        amavis-clamd.conf
Source3:        amavis-clamd.sysconfig
Source4:        README.fedora
Source5:        README.quarantine
Source6:        amavisd.cron
Patch0:         amavisd-conf.patch
Patch1:         amavisd-init.patch
Patch2:         amavisd-condrestart.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-root/
Requires:       /usr/sbin/clamd, /etc/clamd.d
Requires:       /usr/sbin/tmpwatch, /etc/cron.daily
Requires:       /usr/bin/ar
Requires:       altermime
Requires:       arj
Requires:       bzip2
Requires:       cabextract
Requires:       cpio
Requires:       file
Requires:       freeze
Requires:       gzip
Requires:       lzop
Requires:       nomarch
Requires:       p7zip
Requires:       tar
# We probably should parse the fetch_modules() code in amavisd for this list.
# These are just the dependencies that don't get picked up otherwise.
Requires:       perl(Archive::Tar)
Requires:       perl(Archive::Zip)
Requires:       perl(Authen::SASL)
Requires:       perl(Compress::Zlib) >= 1.35
Requires:       perl(Convert::TNEF)
Requires:       perl(Convert::UUlib)
Requires:       perl(Crypt::OpenSSL::RSA)
Requires:       perl(DBD::SQLite)
Requires:       perl(DBI)
Requires:       perl(Digest::SHA)
Requires:       perl(Digest::SHA1)
Requires:       perl(IO::Socket::INET6)
Requires:       perl(IO::Socket::SSL)
Requires:       perl(IO::Stringy)
Requires:       perl(MIME::Body)
Requires:       perl(MIME::Decoder::Base64)
Requires:       perl(MIME::Decoder::Binary)
Requires:       perl(MIME::Decoder::Gzip64)
Requires:       perl(MIME::Decoder::NBit)
Requires:       perl(MIME::Decoder::QuotedPrint)
Requires:       perl(MIME::Decoder::UU)
Requires:       perl(MIME::Head)
Requires:       perl(Mail::DKIM)
Requires:       perl(Mail::Field)
Requires:       perl(Mail::Header)
Requires:       perl(Mail::Internet)
Requires:       perl(Mail::SPF)
Requires:       perl(Mail::SpamAssassin)
Requires:       perl(Net::DNS)
Requires:       perl(Net::LDAP)
Requires:       perl(Net::SSLeay)
Requires:       perl(NetAddr::IP)
Requires:       perl(Razor2::Client::Version)
Requires:       perl(Socket6)
Requires:       perl(URI)
Requires(pre):  /usr/sbin/useradd
Requires(post): /sbin/chkconfig
Requires(post): /sbin/service
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
BuildArch:      noarch

%description
amavisd-new is a high-performance and reliable interface between mailer
(MTA) and one or more content checkers: virus scanners, and/or
Mail::SpamAssassin Perl module. It is written in Perl, assuring high
reliability, portability and maintainability. It talks to MTA via (E)SMTP
or LMTP, or by using helper programs. No timing gaps exist in the design
which could cause a mail loss.

%prep
%setup -q -n %{name}-%{version}%{?prerelease:-%{prerelease}}
%patch0 -p1
%patch1 -p1
%patch2 -p0
install -m644 %{SOURCE4} %{SOURCE5} README_FILES/

sed -i -e 's,/var/amavis/amavisd.sock\>,/var/spool/amavisd/amavisd.sock,' \
    amavisd-release

%build

%install
rm -rf "$RPM_BUILD_ROOT"

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -m755 amavisd $RPM_BUILD_ROOT%{_sbindir}/
( cd $RPM_BUILD_ROOT%{_sbindir} && ln -s clamd clamd.amavisd )

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m755 amavisd-{agent,nanny,release} $RPM_BUILD_ROOT%{_bindir}/

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m755 amavisd_init.sh $RPM_BUILD_ROOT%{_initrddir}/amavisd
install -m755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/clamd.amavisd

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/amavisd
install -m644 amavisd.conf $RPM_BUILD_ROOT%{_sysconfdir}/amavisd/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/clamd.d
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/clamd.d/amavisd.conf

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/clamd.amavisd

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
install -m755 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/amavisd

mkdir -p $RPM_BUILD_ROOT/var/spool/amavisd/{tmp,db,quarantine}
touch $RPM_BUILD_ROOT/var/spool/amavisd/clamd.sock
mkdir -p $RPM_BUILD_ROOT/var/run/amavisd/

%clean
rm -rf "$RPM_BUILD_ROOT"

%pre
if ! id amavis &>/dev/null ; then
    /usr/sbin/useradd -r -s /sbin/nologin -d /var/spool/amavisd amavis
fi

%preun
if [ "$1" = 0 ]; then
    /sbin/service amavisd stop 2>/dev/null || :
    /sbin/chkconfig --del amavisd || :
    /sbin/service clamd.amavisd stop 2>/dev/null || :
    /sbin/chkconfig --del clamd.amavisd || :
fi

%post
/sbin/chkconfig --add clamd.amavisd || :
/sbin/service clamd.amavisd condrestart || :
/sbin/chkconfig --add amavisd || :
/sbin/service amavisd condrestart || :

%files
%defattr(-,root,root)
%doc AAAREADME.first LDAP.schema LICENSE RELEASE_NOTES TODO
%doc README_FILES test-messages amavisd.conf-*
%dir %{_sysconfdir}/amavisd/
%attr(755,root,root) %{_initrddir}/amavisd
%attr(755,root,root) %{_initrddir}/clamd.amavisd
%config(noreplace) %{_sysconfdir}/amavisd/amavisd.conf
%config(noreplace) %{_sysconfdir}/clamd.d/amavisd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/clamd.amavisd
%config(noreplace) %{_sysconfdir}/cron.daily/amavisd
%{_sbindir}/amavisd
%{_sbindir}/clamd.amavisd
%{_bindir}/amavisd-*
%dir %attr(700,amavis,amavis) /var/spool/amavisd
%dir %attr(700,amavis,amavis) /var/spool/amavisd/tmp
%dir %attr(700,amavis,amavis) /var/spool/amavisd/db
%dir %attr(700,amavis,amavis) /var/spool/amavisd/quarantine
%dir %attr(755,amavis,amavis) /var/run/amavisd
%ghost /var/spool/amavisd/clamd.sock

%changelog
* Sun Mar 01 2009 Robert Scheck <robert@fedoraproject.org> 2.6.2-3
- Re-diffed amavisd-new configuration patch for no fuzz

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 17 2008 Steven Pritchard <steve@kspei.com> 2.6.2-1
- Update to 2.6.2.
- Drop smtpdaemon dependency (BZ# 438078).

* Wed Jul 15 2008 Steven Pritchard <steve@kspei.com> 2.6.1-1
- Update to 2.6.1.
- Require Crypt::OpenSSL::RSA, Digest::SHA, Digest::SHA1, IO::Socket::SSL,
  Mail::DKIM, Net::SSLeay, NetAddr::IP, and Socket6.

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.2-3
- fix license tag
- fix db patch to apply with fuzz=0

* Sun Aug 12 2007 Steven Pritchard <steve@kspei.com> 2.5.2-2
- Fix pre/preun/post dependencies and improve scriptlets a bit.
- Drop dependencies on DBD::mysql and Mail::SPF::Query.
- Add dependencies on IO::Socket::INET6, Mail::SPF, and altermime.

* Sun Jul 08 2007 Steven Pritchard <steve@kspei.com> 2.5.2-1
- Update to 2.5.2.

* Fri Jun 22 2007 Steven Pritchard <steve@kspei.com> 2.5.2-0.1.rc2
- Update to 2.5.2-rc2.

* Fri Jun 22 2007 Steven Pritchard <steve@kspei.com> 2.5.1-1
- Update to 2.5.1.
- Fix amavis-clamd.conf (bug #237252).
- Update amavisd-conf.patch.
- Require p7zip and tar.
- Improve pre/preun/post scripts.

* Thu Feb 22 2007 Steven Pritchard <steve@kspei.com> 2.4.5-1
- Update to 2.4.5.

* Mon Dec 18 2006 Steven Pritchard <steve@kspei.com> 2.4.4-2
- Fix the path to amavisd.sock in amavisd-release.

* Tue Dec 05 2006 Steven Pritchard <steve@kspei.com> 2.4.4-1
- Update to 2.4.4.

* Fri Dec 01 2006 Steven Pritchard <steve@kspei.com> 2.4.3-5
- Add missing amavisd-release script.

* Tue Nov 14 2006 Steven Pritchard <steve@kspei.com> 2.4.3-4
- Rebuild.

* Tue Nov 14 2006 Steven Pritchard <steve@kspei.com> 2.4.3-3
- Add dependency on file. (#215492)

* Sat Oct 14 2006 Steven Pritchard <steve@kspei.com> 2.4.3-2
- Fix permissions on the cron.daily script.

* Tue Oct 10 2006 Steven Pritchard <steve@kspei.com> 2.4.3-1
- Update to 2.4.3.
- Add quarantine directory and instructions for enabling it.
- Add tmpwatch cron script.

* Thu Sep 28 2006 Steven Pritchard <steve@kspei.com> 2.4.2-4
- Drop lha dependency and add arj.

* Sun Sep 17 2006 Steven Pritchard <steve@kspei.com> 2.4.2-3
- Rebuild.

* Wed Aug 02 2006 Steven Pritchard <steve@kspei.com> 2.4.2-2
- Fix path to clamd socket in amavisd-conf.patch.

* Mon Jul 31 2006 Steven Pritchard <steve@kspei.com> 2.4.2-1
- Update to 2.4.2
- Fix permissions on README.fedora (bug #200769)

* Tue Jun 20 2006 Steven Pritchard <steve@kspei.com> 2.4.1-1
- Update to 2.4.1
- Drop zoo dependency due to Extras maintainer security concerns

* Tue Apr 25 2006 Steven Pritchard <steve@kspei.com> 2.4.0-1
- Update to 2.4.0

* Thu Feb 02 2006 Steven Pritchard <steve@kspei.com> 2.3.3-5
- Add dist to Release

* Wed Sep 21 2005 Steven Pritchard <steve@kspei.com> 2.3.3-4
- Add TODO and amavisd.conf-* to %%doc

* Mon Sep 19 2005 Steven Pritchard <steve@kspei.com> 2.3.3-3
- Add amavisd-db.patch to fix the path to the db directory in
  amavisd-agent and amavisd-nanny.  (Thanks to Julien Tognazzi.)

* Fri Sep 02 2005 Steven Pritchard <steve@kspei.com> 2.3.3-2
- Requires: perl(Compress::Zlib) >= 1.35

* Thu Sep 01 2005 Steven Pritchard <steve@kspei.com> 2.3.3-1
- Update to 2.3.3
- Remove explicit dependencies on core perl modules

* Fri Aug 19 2005 Steven Pritchard <steve@kspei.com> 2.3.2-10
- Recommend using 127.0.0.1 instead of localhost in README.fedora
- .deb support requires ar

* Wed Aug 17 2005 Steven Pritchard <steve@kspei.com> 2.3.2-9
- Set $virus_admin, $mailfrom_notify_admin, $mailfrom_notify_recip,
  and $mailfrom_notify_spamadmin to undef in the default config to
  turn off notification emails

* Fri Aug 12 2005 Steven Pritchard <steve@kspei.com> 2.3.2-8
- Add dependencies for freeze, lzop, nomarch, zoo, cabextract

* Wed Jul 27 2005 Steven Pritchard <steve@kspei.com> 2.3.2-7
- Add README.fedora with simplified Postfix instructions

* Mon Jul 25 2005 Steven Pritchard <steve@kspei.com> 2.3.2-6
- Create /var/spool/amavisd/db

* Thu Jul 21 2005 Steven Pritchard <steve@kspei.com> 2.3.2-5
- Add perl(Mail::SPF::Query) (now packaged for Extras) dependency
- Drop /var/log/amavisd since we weren't using it
- Fix paths for clamd.sock and amavisd.pid in a couple of places

* Tue Jul 12 2005 Steven Pritchard <steve@kspei.com> 2.3.2-4
- Add a bunch of other missing Requires (both actually required modules
  and optional modules)

* Tue Jul 12 2005 Steven Pritchard <steve@kspei.com> 2.3.2-3
- Add missing Requires: perl(Convert::TNEF)

* Wed Jul 06 2005 Steven Pritchard <steve@kspei.com> 2.3.2-2
- Fix init script ordering
- Don't enable amavisd by default

* Wed Jul 06 2005 Steven Pritchard <steve@kspei.com> 2.3.2-1
- Update to 2.3.2

* Wed Jun 29 2005 Steven Pritchard <steve@kspei.com> 2.3.2-0.1.rc1
- Update to 2.3.2-rc1
- Fedora Extras clamav integration
- Drop amavisd-syslog.patch (Unix::Syslog is in Extras)

* Mon Feb 23 2004 Steven Pritchard <steve@kspei.com> 0.20030616.p7-0.fdr.0.1
- Add amavisd-syslog.patch to eliminate Unix::Syslog dependency
- Add in clamd helper
- Fix up init script
- Initial package
