%define _use_internal_dependency_generator 0

%define __find_requires sh -c "/usr/lib/rpm/find-requires | %{__sed} -r -e '/Authen::(Radius|Tacas)*/d;  /Smokeping/d; '"

%define __find_provides sh -c "sed -e '\\#/usr/share/smokeping#d' | /usr/lib/rpm/find-provides"

Summary:          Latency Logging and Graphing System
Name:             smokeping
Version:          2.4.2
Release:          8%{?dist}
License:          GPLv2+
Group:            Applications/Internet
URL:              http://oss.oetiker.ch/smokeping/
Source0:          %{url}/pub/%{name}-%{version}.tar.gz
Source1:          smokeping.init
Source2:          smokeping-httpd.conf.d
Source3:          http://oss.oetiker.ch/smokeping-demo/img/smokeping.png
Source4:          http://oss.oetiker.ch/smokeping-demo/img/rrdtool.png
Source5:          README.fedora
Patch0:           smokeping-2.4.2-path.patch
Patch1:           smokeping-2.4.2-config.patch
Patch2:           smokeping-2.4.2-tr.patch
Patch3:           smokeping-2.3.5-silence.patch
Patch4:           smokeping-2.4.2-jsonrpc-strict.patch
Patch99:          smokeping-2.4.2-path2.patch

BuildRequires:    glibc-common
Requires:         perl >= 5.6.1 rrdtool >= 1.0.33 fping traceroute
# Not picked up for some reason
Requires:         perl(Config::Grammar)
Requires:         webserver net-tools
Requires(post):   chkconfig
Requires(preun):  chkconfig initscripts
Requires(postun): initscripts
BuildArch:        noarch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
SmokePing is a latency logging and graphing system. It consists of a
daemon process which organizes the latency measurements and a CGI
which presents the graphs.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch99 -p1

%{__install} -p -m 0644 %{SOURCE5} . 
iconv -f ISO-8859-1 -t utf-8 -o CHANGES.utf8 CHANGES
touch -r CHANGES CHANGES.utf8 
%{__mv} CHANGES.utf8 CHANGES

# ship only html docs
find doc -name *.pod -print | xargs rm 
find doc -name *.txt -print | xargs rm
find doc -name *.[1-9] -print | xargs rm

# remove some external modules
%{__rm} -rf lib/{CGI,Config,Digest,JSON}
%{__rm} -rf lib/{SNMP_Session,SNMP_util,BER,JSON}.pm
%{__rm} -f  lib/Qooxdoo/JSONRPC.pm

%build
# nothing to build

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{_sysconfdir}/%{name} \
                %{buildroot}%{_datadir}/%{name}/{lib,cgi,htdocs} \
                %{buildroot}%{_localstatedir}/lib/%{name}/{rrd,images} \
                %{buildroot}%{_localstatedir}/run/%{name}

%{__install} -Dp -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%{__install} -Dp -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

%{__install}  -p -m 0644 %{SOURCE3} %{SOURCE4} %{buildroot}%{_datadir}/%{name}/htdocs

for f in config basepage.html smokemail tmail smokeping_secrets ; do
    %{__install} -p -m 0644 etc/$f.dist %{buildroot}%{_sysconfdir}/%{name}/$f
done
%{__chmod} 0640 %{buildroot}%{_sysconfdir}/%{name}/smokeping_secrets

%{__install} -Dp -m 0755 bin/smokeping.dist %{buildroot}%{_sbindir}/smokeping
%{__install} -Dp -m 0755 bin/tSmoke.dist %{buildroot}%{_bindir}/tSmoke

%{__install} -Dp -m 0755 htdocs/%{name}.cgi.dist \
    %{buildroot}%{_datadir}/%{name}/cgi/%{name}.cgi

%{__install} -Dp -m 0755 htdocs/tr.cgi.dist \
    %{buildroot}%{_datadir}/%{name}/cgi/tr.cgi

%{__cp} -rp htdocs/{cropper,resource,script,tr.html} %{buildroot}%{_datadir}/%{name}/htdocs

%{__cp} -rp lib/* %{buildroot}/%{_datadir}/%{name}/lib

find %{buildroot}%{_datadir}/%{name} -name *.pm | xargs chmod 0644

%clean
%{__rm} -rf %{buildroot}

%post
if [ $1 = 1 ] ; then
    /sbin/chkconfig --add %{name}
fi

%preun
if [ $1 = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ] ; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-, root, root, -)
%doc doc CHANGES CONTRIBUTORS COPYRIGHT COPYING README TODO README.fedora
%{_sbindir}/smokeping
%{_bindir}/tSmoke
%{_initrddir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datadir}/%{name}
%dir %{_localstatedir}/lib/%{name}
%{_localstatedir}/lib/%{name}/rrd
%{_localstatedir}/run/%{name}
%attr(0755, apache, root) %{_localstatedir}/lib/%{name}/images

%changelog
* Tue Feb 17 2009 David Hrbáč <david@hrbac.cz>  - 2.4.2-8
- mrtg lib path patch

* Tue Feb 17 2009 David Hrbáč <david@hrbac.cz>  - 2.4.2-7
- initial rebuild
- small change to build on Centos 4.x too

* Tue Oct 27 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-7
- Add some SELinux information, thanks to wolfy for help
  with this and other improvements.

* Sat Oct 18 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-6
- Fix README.fedora

* Sun Oct  5 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-5
- move Qooxdoo::JSONRPC to separate package

* Tue Sep 16 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-4
- use mv macro
- fix cut-n-paste error in rm lines
- remove perl as buildreq

* Mon Sep 15 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-3
- Fix perms on writeable dir for apache
- More sane handling of external perl modules
- Add smoketrace instructions and patches

* Sat Aug 23 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-2
- Fix README.fedora
- New rpm is picky, fixed

* Sat Aug 23 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-1
- 2.4.2

* Thu Jul  3 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.4.1-1
- 2.4.1

* Mon Apr  7 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.3.5-1
- 2.3.5
- More or less a complete rewrite

* Sun Jan 14 2007 Wil Cooley <wcooley@nakedape.cc> - 2.0.9-2
- Disable internal dependency generator; I was doing this in my ~/.rpmmacros,
  which probably isn't a good idea.

* Tue Dec 05 2006 Wil Cooley <wcooley@nakedape.cc> - 2.0.9-1
- Updated to 2.0.9.
- Use 'dist' variable like Fedora Extras instead of vendor_tag and dist_tag.
- Do chkconfig/service in the correct places with appropriate checks.

* Wed Nov 09 2005 Wil Cooley <wcooley@nakedape.cc> - 2.0.4-0.0
- Updated to 2.0.4.
- Filter requirements for some internally-provided or optional modules.

* Tue Jun 21 2005 Wil Cooley <wcooley@nakedape.cc> - 2.0-0.2rc5
- Added chkconfig in post and preun sections.
- Changed some permissions to make rpmlint less unhappy.

* Thu Jun 16 2005 Wil Cooley <wcooley@nakedape.cc> - 2.0-2.nac.0.5
- Updated for 2.0rc5.

* Wed Mar 17 2004 Wil Cooley <wcooley@nakedape.cc> 1.28-2.nac
- Rebuilt for 1.28.
- Removed unnecessary stuff for setting up Apache.

* Fri Mar 12 2004 Curtis Doty <Curtis@GreenKey.net>
- [1.27] rebuilt without issue

* Sun Jan 25 2004 Curtis Doty <Curtis@GreenKey.net>
- [1.25] merge with upstream and hanecak
- add dependency on new perl-PersistentPerl (SpeedyCGI)
- use working config in the right location
- more rabid decrufting of hard-coded references to rrdtool

* Mon Oct 06 2003 Curtis Doty <Curtis@GreenKey.net>
- [1.24] merge with upstream
- change default config and doc to reflect loss coloring accurately
- rebuild man pages and html to reflect above, but forget txt
- remove IfModule mod_alias.c since apache2 cannot handle

* Thu Oct  2 2003 Peter Hanecak <hanecak@megaloman.sk> 1.23-1
- changed group from Networking/Utilities to Applications/Internet

* Wed Jul 30 2003 Curtis Doty <Curtis@GreenKey.net>
- [1.23] bump and build
- fix on Shrike since libnet subsumed by perl-5.8 and we really only
  need Net:SNMP out of it anyways
- quick hacks to make apache 2 compatible

* Tue Dec 17 2002 Curtis Doty <Curtis@GreenKey.net>
- [1.18] with some cosmetic changes
- add perl-libnet dependency neede for at least Net::SMTP
- maxhight patch so apache puts temp files in imgcache dir not datadir
- prefer my config.dist

* Sat Nov 02 2002 Curtis Doty <Curtis@GreenKey.net>
- [1.16] with updated specfile
- fix perms on /var/smokeping so apache cannot write
- fork and distribute my own defailt config instead of patching the
  screwey one that comes in the tarball

* Tue Mar 12 2002 Curtis Doty <Curtis@GreenKey.net>
- [1.5] with a bunch of my additions including SysV init script

* Tue Feb 19 2002 Curtis Doty <Curtis@GreenKey.net>
- new rpm package [1.1]
