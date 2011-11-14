Summary: powerful, easy to use console email client
Name: alpine
Version: 2.02
Release: 2%{?dist}

License: ASL 2.0
Group: Applications/Internet
URL: http://re-alpine.sourceforge.net/ 
Source0:  http://downloads.sourceforge.net/sourceforge/re-alpine/re-alpine-%{version}%{?pre}.tar.bz2

# Using "Conflicts" instead of Obsoletes because while alpine is substantially
# compatible with pine the change to Unicode breaks important user
# functionality such as non-ASCII encoded saved passwords. Additionally, there
# are also many patches to pine floating around that for political/technical
# reasons will not be integrated into alpine. (I'd like to stay out of it...
# just search "Mark Crispin maildir" for the gory details.) Since licensing
# prevents a Fedora pine package, I cannot predict what patches users might
# have and so want to warn them instead of automatically replacing their pine
# install with an alpine that could break their configuration. 
# I understand this to be a special case of the "Optional Functionality"
# description at http://fedoraproject.org/wiki/Packaging/Conflicts
Conflicts: pine
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Provides: re-alpine = %{version}-%{release}

# short-term workaround until gcc is fixed
# http://bugzilla.redhat.com/496400
Patch1: alpine-2.00-gcc44_reply_hack.patch

## upstreamable patches
# this one maybe already, recall grumblings onlinst awhile back -- Rex
Patch50: re-alpine-2.02-openssl.patch

#BuildRequires: automake libtool
BuildRequires: gettext
#BuildRequires: hunspell
## passing --with-npa=/usr/bin/inews
#BuildRequires: inews
BuildRequires: krb5-devel
BuildRequires: ncurses-devel 
BuildRequires: openldap-devel
BuildRequires: openssl-devel
BuildRequires: pam-devel
BuildRequires: passwd
# passing --with-smtp-msa=/usr/sbin/sendmail instead
#BuildRequires: /usr/sbin/sendmail 

Requires: hunspell
Requires: mailcap
Requires: /usr/sbin/sendmail


%description
Alpine -- an Alternatively Licensed Program for Internet
News & Email -- is a tool for reading, sending, and managing
electronic messages.  Alpine is the successor to Pine and was
developed by Computing & Communications at the University of
Washington.  
  Though originally designed for inexperienced email users,
Alpine supports many advanced features, and an ever-growing number of
configuration and personal-preference options.
Changes and enhancements over pine:
  * Released under the Apache Software License, Version 2.0.
  * Internationalization built around new internal Unicode support.
  * Ground-up reorganization of source code around new "pith/" core 
routine library.
  * Ground-up reorganization of build and install procedure based on 
GNU Build System's autotools.


%prep
%setup -q -n re-alpine-%{version}

#%patch1 -p1 -b .gcc44_reply_hack
%patch50 -p1 -b .openssl

#autoreconf -f -i


%build
touch imap/ip6
# --without-tcl disables the TCL-based CGI "Web Alpine"
%configure \
  --enable-debug=no \
  --without-tcl \
  --with-c-client-target=lfd \
  --with-smtp-msa=/usr/sbin/sendmail \
  --with-npa=/usr/bin/inews \
  --with-passfile=.alpine.passfile \
  --with-simple-spellcheck=hunspell \
  --with-interactive-spellcheck=hunspell \
  --with-system-pinerc=%{_sysconfdir}/pine.conf \
  --with-system-fixed-pinerc=%{_sysconfdir}/pine.conf.fixed

make %{?_smp_mflags} EXTRACFLAGS="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# create/touch %ghost'd files
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
touch $RPM_BUILD_ROOT%{_sysconfdir}/pine.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/pine.conf.fixed


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README LICENSE doc/tech-notes.txt
%ghost %config(noreplace) %{_sysconfdir}/pine.conf
%ghost %config(noreplace) %{_sysconfdir}/pine.conf.fixed
%{_bindir}/alpine
%{_bindir}/pico
%{_bindir}/pilot
%{_bindir}/rpload
%{_bindir}/rpdump
%{_mandir}/man1/alpine.1*
%{_mandir}/man1/pico.1*
%{_mandir}/man1/pilot.1*
%{_mandir}/man1/rpload.1*
%{_mandir}/man1/rpdump.1*


%changelog
* Wed Oct 26 2011 David Hrbáč <david@hrbac.cz> - 2.02-2
- initial rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.02-1
- re-alpine-2.02 (#465341)

* Mon Jul 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.00-9
- --with-npa=/usr/bin/inews
- --with-smtp-msa=/usr/sbin/sendmail

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.00-8
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 CaolÃ¡n McNamara <caolanm@redhat.com> - 2.00-6
- --with-spellcheck-prog isn't a configure option use
  --with-simple-spellcheck/--with-interactive-spellcheck and patch
  to prefer hunspell to aspell (#509387)

* Wed May 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.00-5
- "reply to all recipients" doesn't include anyone on the Cc list (#496400)

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> 2.00-3
- rebuild with new openssl

* Wed Nov 26 2008 Joshua Daniel Franklin <joshuadfranklin@yahoo.com> 2.00-2
- Fix package Summary text to not include package name
- http://www.redhat.com/archives/fedora-devel-list/2008-November/msg01484.html

* Wed Aug 27 2008 Rex Dieter <rdieter@fedoraproject.org> 2.00-1
- alpine-2.00 (#460332)

* Mon Mar 24 2008 Joshua Daniel Franklin <joshuadfranklin@yahoo.com> 1.10-4
- No changes; Bump for tag system

* Mon Mar 24 2008 Joshua Daniel Franklin <joshuadfranklin@yahoo.com> 1.10-3
- No changes; Bump for tag system

* Mon Mar 24 2008 Joshua Daniel Franklin <joshuadfranklin@yahoo.com> 1.10-2
- Change License string to "ASL 2.0" instead of "Apache Software License"
- Disable debug files with "--enable-debug=no" (BZ #427013)

* Mon Mar 24 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.10-1
- alpine-1.10
- cosmetic (Build)Req cleanup

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.00-3
- Autorebuild for GCC 4.3

* Fri Dec 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.00-2
- --with-system-pinerc=%%_sysconfdir/pine.conf
  --with-system-fixed-pinerc=%%_sysconfdir/pine.conf.fixed (#426512)

* Fri Dec 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.00-1
- alpine-1.00

* Tue Dec 04 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 0.99999-4
- Bump-n-build for openldap/openssl soname changes

* Thu Nov 15 2007 Joshua Daniel Franklin <joshuadfranklin@yahoo.com> 0.99999-3
- BuildRequires aspell to make configure happy

* Thu Nov 09 2007 Joshua Daniel Franklin <joshuadfranklin@yahoo.com> 0.99999-2
- update to latest 

* Thu Oct 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org. 0.9999-4
- omit sample pine.conf, instead use %%ghost to preserve existing pine.conf's

* Wed Oct 24 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9999-3
- include stock pine.conf, pine.conf.fixed

* Fri Sep 07 2007 Joshua Daniel Franklin <joshuadfranklin@yahoo.com> 0.9999-2
- update to latest 

* Fri Aug 24 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.999-3
- EXTRACFLAGS=$RPM_OPT_FLAGS
- --with-c-client-target=lfd
- --with-passfile=.alpine.passfile
- Requires: mailcap

* Mon Jul 24 2007 Joshua Daniel Franklin <joshuadfranklin@yahoo.com> 0.999-2.2
- remove problem cc5.sol file
- integrate changes from Patrick "Jima" Laughton <jima@beer.tclug.org>

* Mon Jul 24 2007 Joshua Daniel Franklin <joshuadfranklin@yahoo.com> 0.999-2.1
- correct spec syntax, explain Conflicts tag

* Mon Jul 23 2007 Joshua Daniel Franklin <joshuadfranklin@yahoo.com> 0.999-2.0
- initial alpine spec
- Apache Software License 2.0
