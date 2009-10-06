Summary:	Postfix Admin is a web based management tool created for Postfix
Name:		postfixadmin
Version:	2.2.1.1
Release:	1.%{dist}
License:	GPL
Group:		System/Servers
URL:		http://sourceforge.net/projects/postfixadmin/
#Source0:	%{name}-%{version}-%{snap}.tar.bz2
Source0:        http://downloads.sourceforge.net/project/postfixadmin/postfixadmin/postfixadmin-%{version}/postfixadmin-%{version}.tar.gz
#Patch0:		postfixadmin-mdv_conf.diff
Requires:	apache-mpm >= 2.0.54
Requires:	apache-conf >= 2.0.54
Requires:	MySQL-server >= 4.0
Requires:	postfix >= 2.0
Requires:	apache-mod_php
Requires:	php-mysqli

Requires: perl-MIME-Charset perl-MIME-EncWords perl-Email-Valid.noarch perl-Mail-Sendmail.noarch

BuildArch:	noarch
#BuildRequires:	apache-base >= 2.0.54-5mdk
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Postfix Admin is a Web Based Management tool created for Postfix.
It is a PHP based application that handles Postfix Style Virtual
Domains and Users that are stored in MySQL.

Postfix Admin supports:
- Virtual Mailboxes / Virtual Aliases / Forwarders.
- Domain to Domain forwarding / Catch-All.
- Vacation (auto-response) for Virtual Mailboxes.
- Quota / Alias & Mailbox limits per domain.
- Backup MX.
- Packaged with over 25 languages.

%prep

%setup -q
#%patch0 -p1

for i in `find . -type d -name .svn`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# fix dir perms
find . -type d | xargs chmod 755

# fix file perms
find . -type f | xargs chmod 644

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}/var/www/%{name}
cp -aRf * %{buildroot}/var/www/%{name}/

# use some generic config
#mv %{buildroot}/var/www/%{name}/config.inc.php.sample %{buildroot}%{_sysconfdir}/%{name}/config.inc.php

# the setup is useless atm
mv %{buildroot}/var/www/%{name}/setup.php %{buildroot}/var/www/%{name}/setup.php.disabled

install -m0755 ADDITIONS/*.sh %{buildroot}%{_datadir}/%{name}/
install -m0755 ADDITIONS/*.pl %{buildroot}%{_datadir}/%{name}/
install -m0644 ADDITIONS/*.php %{buildroot}%{_datadir}/%{name}/

# cleanup
rm -rf %{buildroot}/var/www/%{name}/ADDITIONS
rm -rf %{buildroot}/var/www/%{name}/DOCUMENTS
rm -rf %{buildroot}/var/www/%{name}/VIRTUAL_VACATION
rm -f %{buildroot}/var/www/%{name}/*.TXT

# apache configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf <<EOF
# %{name} Apache configuration file
Alias /%{name} /var/www/%{name}
<Directory /var/www/%{name}>
    Allow from all
</Directory>
EOF
    
%post
%_post_webapp

%postun
%_postun_webapp

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc ADDITIONS/*.TXT ADDITIONS/*.*gz DOCUMENTS/*.TXT VIRTUAL_VACATION *.TXT 
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%attr(0640,apache,root) %config(noreplace) %{_sysconfdir}/%{name}/config.inc.php
%dir /var/www/%{name}
/var/www/%{name}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*


%changelog
* Mon Jun 25 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.1-1.r11.1mdv2008.0
+ Revision: 43870
- new snap, from new svn repository at sf
- new url
- rediffed P0
- fixed deps

* Wed May 09 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.1-0.r79.2mdv2008.0
+ Revision: 25469
- Import postfixadmin



* Thu Apr 27 2006 Oden Eriksson <oeriksson@mandriva.com> 2.1.1-0.r79.2mdk
- relocate the config to /etc/postfixadmin/
- add apache config
- use ccp in %%post

* Tue Jan 10 2006 Oden Eriksson <oeriksson@mandriva.com> 2.1.1-0.r79.1mdk
- initial Mandriva package
- use a recent snapshot with clear license
- added some fixes to the default config (P0)

* Fri Jul 08 2005 Madman <madman@extenzilla.it> 2.1.0-1mdk
- First build for Mandriva 2006 Cooker.

