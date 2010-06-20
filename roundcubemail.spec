%define roundcubedir %{_datadir}/roundcubemail
%global _logdir /var/log  
Name: roundcubemail
Version:  0.3.1
Release:  2%{?dist}
Summary: Round Cube Webmail is a browser-based multilingual IMAP client

Group: Applications/System         
License: GPLv2
URL: http://www.roundcube.net
Source0: http://downloads.sourceforge.net/project/roundcubemail/roundcubemail-dependent/%{version}/roundcubemail-%{version}-dep.tar.gz
Source1: roundcubemail.conf
Source2: roundcubemail.logrotate
#Source4: roundcubemail-README.fedora
Patch0: roundcubemail-0.2-beta-confpath.patch
# From upstream, not in a release yet, BZ 476223.
#Patch1: roundcubemail-0.2-beta-html2text.patch
# From upstream, not in a release yet, BZ 476830.
#Patch2: roundcubemail-0.2-beta-CVE-2008-5620.patch
#Patch3: roundcubemail-0.2-CVE-2009-0413.patch
#Patch4: roundcubemail-0.2-stable-pg-mdb2.patch
Patch5: roundcubemail-0.3.1-CVE-2010-0464.patch

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root%(%{__id_u} -n)
Requires: php-pear-Auth-SASL
Requires: php-pear-DB
Requires: php-pear-Mail-Mime
Requires: php-pear-Net-SMTP
Requires: php-pear-Net-Socket
Requires: php, httpd
Requires: php-pear-Mail-mimeDecode
Requires: php-mcrypt
Requires: php-pear-MDB2
Requires: php-pear-MDB2-Driver-mysql
Requires: php-pecl-Fileinfo
Requires: php-xml
Requires: php-mbstring

%description
RoundCube Webmail is a browser-based multilingual IMAP client
with an application-like user interface. It provides full
functionality you expect from an e-mail client, including MIME
support, address book, folder manipulation, message searching
and spell checking. RoundCube Webmail is written in PHP and 
requires the MySQL database or the PostgreSQL database. The user
interface is fully skinnable using XHTML and CSS 2.

%prep
%setup -q -n roundcubemail-%{version}-dep

%patch0 -p0
#%patch1 -p0
#%patch2 -p0
#%patch3 -p0
#%patch4 -p0
%patch5 -p0

# fix permissions and remove any .htaccess files
find . -type f -print | xargs chmod a-x
find . -name \.htaccess -print | xargs rm -f

# fixup paths to use the right paths
sed -i 's|temp/|${_tmppath}|' config/main.inc.php.dist
sed -i 's|config/|%{_sysconfdir}/roundcubemail/|' config/main.inc.php.dist
sed -i 's|logs/|%{_logdir}/roundcubemail/|' config/main.inc.php.dist
sed -i 's|logs/|%{_logdir}/roundcubemail/|' program/include/main.inc
sed -i 's|config/|%{_sysconfdir}/roundcubemail/|' program/include/main.inc

# remove any reference to sqlite in config file so people don't mistakely
# assume it works
sed -i '/sqlite/d' config/db.inc.php.dist
sed -i 's/\r//' SQL/mssql.initial.sql

%build

%install

rm -rf %{buildroot}
install -d %{buildroot}%{roundcubedir}
cp -pr * %{buildroot}%{roundcubedir}

#ln -s ../../../pear/PEAR.php %{buildroot}%{roundcubedir}/program/lib/PEAR.php
#ln -s ../../../pear/Auth %{buildroot}%{roundcubedir}/program/lib/Auth
#ln -s ../../../pear/DB %{buildroot}%{roundcubedir}/program/lib/DB
#ln -s ../../../pear/DB.php %{buildroot}%{roundcubedir}/program/lib/DB.php
#ln -s ../../../pear/Mail %{buildroot}%{roundcubedir}/program/lib/Mail
#ln -s ../../../pear/Net %{buildroot}%{roundcubedir}/program/lib/Net

rm -rf %{buildroot}%{roundcubedir}/installer

mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
cp -pr %SOURCE1 %{buildroot}%{_sysconfdir}/httpd/conf.d

mkdir -p %{buildroot}%{_sysconfdir}/roundcubemail
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
cp -pr %SOURCE2 %{buildroot}%{_sysconfdir}/logrotate.d/roundcubemail

mkdir -p %{buildroot}/var/log/roundcubemail

#cp -pr %SOURCE4 .

# use dist files as config files
mv %{buildroot}%{roundcubedir}/config/db.inc.php.dist %{buildroot}%{_sysconfdir}/roundcubemail/db.inc.php
mv %{buildroot}%{roundcubedir}/config/main.inc.php.dist %{buildroot}%{_sysconfdir}/roundcubemail/main.inc.php
# keep any other config files too
mv %{buildroot}%{roundcubedir}/config/* %{buildroot}%{_sysconfdir}/roundcubemail/

# clean up the buildroot
rm -rf %{buildroot}%{roundcubedir}/{config,logs,temp}
rm -rf %{buildroot}%{roundcubedir}/{CHANGELOG,INSTALL,LICENSE,README,UPGRADING,SQL}

%clean
rm -rf %{buildroot}

%post
# replace default des string in config file for better security
function makedesstr
(
chars=(0 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z A
B C D E F G H I J K L M N O P Q R S T U V W X Y Z)

max=${#chars[*]}

for i in `seq 1 24`; do
    let rand=${RANDOM}%%${max}
    str="${str}${chars[$rand]}"
done
echo $str
)

sed -i "s/rcmail-\!24ByteDESkey\*Str/`makedesstr`/" /etc/roundcubemail/main.inc.php || : &> /dev/null
exit 0


%files
%defattr(-,root,root,-)
%doc CHANGELOG INSTALL LICENSE README UPGRADING SQL 
#roundcubemail-README.fedora
%{roundcubedir}
%dir %{_sysconfdir}/%{name}
%attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/%{name}/db.inc.php
%attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/%{name}/main.inc.php
%attr(0640,root,apache) %{_sysconfdir}/%{name}/mimetypes.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/roundcubemail.conf
%attr(0775,root,apache) %dir /var/log/roundcubemail
%config(noreplace) %{_sysconfdir}/logrotate.d/roundcubemail

%changelog
* Sun Jun 20 2010 David Hrbáč <david@hrbac.cz> - 0.3.1-2
- initial release

* Mon Feb 01 2010 Jon Ciesla <limb@jcomserv.net> = 0.3.1-2
- Patch to fix CVE-2010-0464, BZ 560143.

* Mon Nov 30 2009 Jon Ciesla <limb@jcomserv.net> = 0.3.1-1
- New upstream.

* Thu Oct 22 2009 Jon Ciesla <limb@jcomserv.net> = 0.3-2
- Macro fix, BZ530037.

* Wed Sep 23 2009 Jon Ciesla <limb@jcomserv.net> = 0.3-1
- New upstream.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Jon Ciesla <limb@jcomserv.net> = 0.2.2-2
- Incorporated Chris Eveleigh's config changes to fix mimetype bug, BZ 511857.

* Wed Jul 01 2009 Jon Ciesla <limb@jcomserv.net> = 0.2.2-1
- New upstream.

* Fri Apr 10 2009 Jon Ciesla <limb@jcomserv.net> = 0.2.1-1
- New upstream.

* Mon Mar 30 2009 Jon Ciesla <limb@jcomserv.net> = 0.2-9.stable
- Patch for PG until php-pear-MDB2 hits 1.5.0 stable. BZ 489505.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-8.stable
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Jon Ciesla <limb@jcomserv.net> = 0.2-7.stable
- Patch for CVE-2009-0413, BZ 484052.

* Mon Jan 05 2009 Jon Ciesla <limb@jcomserv.net> = 0.2-6.stable
- New upstream.
- Dropped two most recent patches, applied upstream.

* Wed Dec 17 2008 Jon Ciesla <limb@jcomserv.net> = 0.2-5.beta
- Security fix, BZ 476830.

* Fri Dec 12 2008 Jon Ciesla <limb@jcomserv.net> = 0.2-4.beta
- Security fix, BZ 476223.

* Thu Oct 09 2008 Jon Ciesla <limb@jcomserv.net> = 0.2-3.beta
- New upstream.

* Mon Jun 16 2008 Jon Ciesla <limb@jcomserv.net> = 0.2-2.alpha
- osx files removed upstream.

* Mon Jun 16 2008 Jon Ciesla <limb@jcomserv.net> = 0.2-1.alpha
- Fixed php-xml, php-mbstring Requires.  BZ 451652.
- Removing osx files, will be pulled from next upstream release.

* Fri Jun 13 2008 Jon Ciesla <limb@jcomserv.net> = 0.2-0.alpha
- Update to 0.2-alpha, security fixes for BZ 423271. 
- mysql update and pear patches applied upstream.
- Patched config paths.

* Fri Apr 18 2008 Jon Ciesla <limb@jcomserv.net> = 0.1.1-5
- Added php-pecl-Fileinfo Reqires. BZ 442728.

* Wed Apr 16 2008 Jon Ciesla <limb@jcomserv.net> = 0.1.1-4
- Added mcrypt, MDB2 Requires.  BZ 442728.

* Thu Apr 10 2008 Jon Ciesla <limb@jcomserv.net> = 0.1.1-3
- Patch to fix PEAR path issue, drop symlinks.

* Thu Apr 10 2008 Jon Ciesla <limb@jcomserv.net> = 0.1.1-2
- Drop %%pre script that was breaking pear packages.

* Wed Apr 09 2008 Jon Ciesla <limb@jcomserv.net> = 0.1.1-1
- New upstream release.
- Added patch to fix mysql update.

* Tue Mar 18 2008 Jon Ciesla <limb@jcomserv.net> = 0.1-1
- Updgrade to 0.1 final, -dep.
- Added new mimeDecode dep.

* Mon Feb 04 2008 Jon Ciesla <limb@jcomserv.net> = 0.1-0.10rc2.1
- Changed to upstream -dep tarball, GPL-compliant.

* Fri Feb 01 2008 Jon Ciesla <limb@jcomserv.net> = 0.1-0.9rc2.1
- re-removed PEAR components that slipped back in after rc1.

* Fri Oct 26 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-0.8rc2
- Upgrade to 0.1-rc2

* Thu Aug 16 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-0.7rc1.1
- License tag correction.

* Tue Jul 03 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-0.6rc1.1
- New upstream release, all GPL, all current languages included.

* Mon May 14 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-0.5.beta2.2
- Fixed source timestamps, added Russian langpack.
- Added logpath fix to main.inc.php
- Fixed logrotate filename.

* Fri May 11 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-0.4.beta2.2
- Cleanup/elegantization of spec, .conf.

* Thu May 10 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-0.3.beta2.2
- Fixed bad chars in script.

* Thu May 10 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-0.2.beta2.2
- Added all langpacks.

* Thu May 10 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-0.1.beta2.2
- Versioning fix.

* Wed May 09 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-beta2.3
- Fixed generation of DES.
- Cleanup re patch.

* Mon May 07 2007 Jon Ciesla <limb@jcomserv.net> - 0.1-beta2.2.3
- Removed duplicate docs.
- Moved SQL to doc.
- Fixed perms on log dir, sysconfdir.
- Fixed Requires.  
- Fixed config.
- Fixed changelog spacing.
  
* Fri May 04 2007 Jon Ciesla <limb@jcomserv.net> - 0.1-beta2.2.2
- Created new source tarball with PEAR code removed. Added script for creation.

* Tue Feb 13 2007 Jon Ciesla <limb@jcomserv.net> - 0.1-beta2.2.1
- Excluded Portions from PEAR, included as dependancies
- Fixed log/temp issues, including logrotate

* Tue Jan 30 2007 Jon Ciesla <limb@jcomserv.net> - 0.1-beta2.2
- Initial packaging.
