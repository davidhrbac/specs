#
# $Id: smokeping_old.spec,v 1.1 2009-02-26 13:42:33 dhrbac Exp $
# Authority: nac
# 
# Source: # http://haus.nakedape.cc/svn/public/trunk/rpm/rpmset/smokeping/smokeping.spec
#

# /usr/lib/%{name} will be the "%{name} home"
#   - www/cgi will hold CGIs
#   - www/images will hold images
%define     app_dir     %{_libdir}/%{name}
%define     cgi_dir     %{app_dir}/cgi
%define     lib_dir     %{app_dir}/lib

# /var/lib/%{name} will hold variable data
#   - rrd/ will hold RRD data files
#   - img/ will hold CGI image cache
%define     var_dir     %{_var}/lib/%{name}
%define     data_dir    %{var_dir}/rrd
%define     img_dir     %{var_dir}/img

# /etc/%{name} will hold configuration
%define     cfg_dir     %{_sysconfdir}/%{name}

%define _use_internal_dependency_generator 0

%define __find_requires sh -c "/usr/lib/rpm/find-requires|%{__sed} -r -e '/Authen::(Radius|Tacas)*/d; /Smokeping/d; /Config::Grammar/d; /BER/d; /Net::(LDAP|Telnet)/d; /Net::Telnet/d; /SNMP_(Session|util)/d; /SNMP_util/d; '"

%define __find_provides sh -c "sed -e '\\#/usr/lib/smokeping#d' | /usr/lib/rpm/find-provides"

Summary:        Latency Logging and Graphing System
Name:           smokeping
Version:        2.4.2
Release:        1%{?dist}
License:        GPL
Group:          Applications/Internet
URL:            http://people.ee.ethz.ch/~oetiker/webtools/%{name}/
Source0:        http://oss.oetiker.ch/smokeping/pub/%{name}-%{version}.tar.gz
Source1:        %{name}.init

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl grep
Requires:       perl >= 5.6.1
Requires:       rrdtool >= 1.0.33
Requires:       fping >= 2.4b2
Requires:       webserver
Requires:       net-tools

%description
SmokePing is a latency logging and graphing system. It
consists of a daemon process which organizes the latency
measurements and a CGI which presents the graphs.

%prep
%setup -q -n %{name}-%{version}

%build

find . -type f|xargs -r %{__perl} -pi.orig -e '
    s#/usr/sepp/bin#%{_bindir}#g;
    s#perl-5\.8\.4#perl#g;
    s#/home/oetiker/\.smokeping#%{cfg_dir}#g;
    s#/home/oetiker/data/projects/AADJ-smokeping/dist/etc#%{cfg_dir}#g;
    s#/home/oetiker/data/projects/AADJ-smokeping/dist/lib#%{lib_dir}#g;
    s#/etc/smokeping/smokemail\.dist#%{cfg_dir}/smokemail#g;
    s#/etc/smokeping/basepage\.html\.dist#%{cfg_dir}/basepage.html#g;
    s#^use lib .*rrdtool.*;##g;
    s#qw\(lib\);#qw(%{lib_dir});#g;
    s#%{_bindir}/speedy#%{__perl}#g;
    s#"etc/config\.dist"#"%{cfg_dir}/config"#g;
    s#/home/oetiker/public_html/smokeping/lib#%{lib_dir}#g;
    s#/usr/local/smokeping/lib#%{lib_dir}#g;
    s#/usr/local/smokeping/bin/tSmoke.pl#/usr/bin/tSmoke#g;
'

%install
%{__rm} -rf %{buildroot}

# Clean up
find -name \*.orig |xargs -r %{__rm}

%{__mkdir} -p   %{buildroot}/%{cgi_dir} \
                %{buildroot}/%{cfg_dir} \
                %{buildroot}/%{img_dir} \
                %{buildroot}/%{lib_dir} \
                %{buildroot}/%{data_dir} \
                %{buildroot}/%{_mandir}/man1 \
                %{buildroot}/%{_mandir}/man3 \
                %{buildroot}/%{_mandir}/man5 \
                %{buildroot}/%{_mandir}/man7

%{__install} -Dpm555 bin/smokeping.dist %{buildroot}/%{_sbindir}/smokeping
%{__install} -Dpm555 bin/tSmoke.dist %{buildroot}/%{_bindir}/tSmoke

cp -pr lib/* %{buildroot}/%{lib_dir}/
find %{buildroot}/%{lib_dir}/ -type f | xargs -r %{__chmod} -R ugo-w 

%{__install} -Dpm555 htdocs/%{name}.cgi.dist \
    %{buildroot}/%{cgi_dir}/%{name}.cgi

%{__install} -Dpm555 %{SOURCE1} %{buildroot}/%{_sysconfdir}/rc.d/init.d/%{name}
%{__install} -Dpm644 etc/config.dist %{buildroot}/%{cfg_dir}/config
%{__install} -Dpm444 etc/config.dist %{buildroot}/%{cfg_dir}/config.dist
%{__install} -Dpm644 etc/basepage.html.dist \
    %{buildroot}/%{cfg_dir}/basepage.html
%{__install} -Dpm444 etc/basepage.html.dist \
    %{buildroot}/%{cfg_dir}/basepage.html.dist
%{__install} -Dpm644 etc/smokemail.dist %{buildroot}/%{cfg_dir}/smokemail
%{__install} -Dpm444 etc/smokemail.dist %{buildroot}/%{cfg_dir}/smokemail.dist
%{__install} -Dpm644 etc/tmail.dist %{buildroot}/%{cfg_dir}/tmail
%{__install} -Dpm444 etc/tmail.dist %{buildroot}/%{cfg_dir}/tmail.dist

%{__install} -pm444 $(find doc -name \*.1) %{buildroot}/%{_mandir}/man1/
%{__install} -pm444 $(find doc -name \*.3) %{buildroot}/%{_mandir}/man3/
%{__install} -pm444 $(find doc -name \*.5) %{buildroot}/%{_mandir}/man5/
%{__install} -pm444 $(find doc -name \*.7) %{buildroot}/%{_mandir}/man7/

find doc -name \*.[1-9] |xargs -r %{__rm}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%{_bindir}/*
%{_sbindir}/*
%{lib_dir}/*

%attr(0775,root,apache) %{img_dir}
%attr(0755,root,root) %{data_dir}
%attr(0755,root,root) %{cgi_dir}

%{_sysconfdir}/rc.d/init.d/%{name}
%config(noreplace)  %{cfg_dir}/*

%{_mandir}/*/*
%doc [A-Z][A-Z]*
%doc doc/

%post
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add %{name}
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi

%changelog
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
