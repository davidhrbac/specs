Summary:	Web-based PostgreSQL administration
Name:		phpPgAdmin
Version:	4.2.2
Release:	1%{?dist}
License:	GPL
Group:		Applications/Databases
URL:		http://phppgadmin.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	http://osdn.dl.sourceforge.net/sourceforge/phppgadmin/%{name}-%{version}.tar.bz2
Source1:	%{name}.conf

Requires:	php >= 4.2, gawk
Requires:	php-pgsql >= 4.2, httpd
Requires(Post):	/sbin/service
Buildarch:	noarch

%define		_phppgadmindir	%{_datadir}/%{name}

Patch1:		%{name}-langcheck.patch

%description
phpPgAdmin is a fully functional web-based administration utility for
a PostgreSQL database server. It handles all the basic functionality
as well as some advanced features such as triggers, views and
functions (stored procedures). It also has Slony-I support.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p0

%build
# Cleanup encoding problem
sed -i 's/\r//' lang/php2po
sed -i 's/\r//' lang/po2php

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_phppgadmindir}
install -d %{buildroot}%{_phppgadmindir}/conf
install -d %{buildroot}%{_sysconfdir}/%{name}
install -m 644 -p *.php %{buildroot}%{_phppgadmindir}
cp -ap *.js robots.txt classes images lang libraries sql themes xloadtree help %{buildroot}%{_phppgadmindir}
install -d  %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -d %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -m 755 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
install -m 755 conf/* %{buildroot}%{_sysconfdir}/%{name}
ln -s %{_sysconfdir}/%{name}/config.inc.php %{buildroot}/%{_phppgadmindir}/conf/config.inc.php
ln -s %{_sysconfdir}/%{name}/config.inc.php-dist %{buildroot}/%{_phppgadmindir}/conf/config.inc.php-dist

%post
	/sbin/service httpd reload > /dev/null 2>&1

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc CREDITS DEVELOPERS FAQ HISTORY INSTALL LICENSE TODO TRANSLATORS
%dir %{_phppgadmindir}
%dir %{_sysconfdir}/%{name}
%dir %{_phppgadmindir}/conf
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%attr(644,root,root) %{_phppgadmindir}/*.php
%{_phppgadmindir}/*.js
%{_phppgadmindir}/robots.txt
%{_phppgadmindir}/classes
%{_phppgadmindir}/images
%dir %{_phppgadmindir}/lang
%dir %attr(755,root,root) %{_phppgadmindir}/lang/recoded
%attr(644,root,root) %{_phppgadmindir}/lang/*.php
%attr(644,root,root) %{_phppgadmindir}/lang/recoded/*
%attr(644,root,root) %{_phppgadmindir}/lang/Makefile
%attr(755,root,root) %{_phppgadmindir}/lang/convert.awk
%attr(755,root,root) %{_phppgadmindir}/lang/langcheck
%attr(755,root,root) %{_phppgadmindir}/lang/php2po
%attr(755,root,root) %{_phppgadmindir}/lang/po2php
%attr(755,root,root) %{_phppgadmindir}/lang/synch
%{_phppgadmindir}/libraries
%{_phppgadmindir}/sql
%{_phppgadmindir}/themes
%{_phppgadmindir}/xloadtree
%{_phppgadmindir}/help
%{_phppgadmindir}/conf/config.inc.php*

%changelog
* Sat Dec 20 2008 David Hrbáč <david@hrbac.cz> - 4.2.2-1
- update to 4.2.2

* Thu Oct 16 2008 David Hrbáč <david@hrbac.cz> - 4.2.1-1
- update to 4.2.1

* Thu Oct 16 2008 David Hrbáč <david@hrbac.cz> - 4.2-1
- initial rebuild

* Sun Apr 6 2008 Devrim Gunduz <devrim@commandprompt.com> 4.2-1
- Update to 4.2
- Removed patch #2

* Wed Jul 11 2007 Devrim Gunduz <devrim@commandprompt.com> 4.1.3-2
- Added temporary patch #2 , per sf.net bug #1751614

* Tue Jul 10 2007 Devrim Gunduz <devrim@commandprompt.com> 4.1.3-1
- Update to 4.1.3

* Mon Jun 01 2007 Devrim Gunduz <devrim@commandprompt.com> 4.1.2-1
- Update to 4.1.2
- Fix for Red Hat Bugzilla  #241489

* Mon Mar 26 2007 Devrim Gunduz <devrim@commandprompt.com> 4.1.1-1
- Update to 4.1.1
- Fix for Red Hat Bugzilla  #233902

* Sun Jan 21 2007 Devrim Gunduz <devrim@commandprompt.com> 4.1-2
- Rebuilt
- Fixed changelog entry

* Thu Jan 4 2007 Devrim Gunduz <devrim@commandprompt.com> 4.1-1
- Update to 4.1
- Fix for rh bugzilla #222740

* Thu Jan 4 2007 Devrim Gunduz <devrim@commandprompt.com> 4.0.1-7
- Rebuilt

* Thu Jan 4 2007 Devrim Gunduz <devrim@commandprompt.com> 4.0.1-6
- Fixed phppgadmin.conf file.

* Thu Dec 21 2006 Devrim Gunduz <devrim@commandprompt.com> 4.0.1-5
- More specfile fixes per bugzilla review #200600

* Thu Dec 21 2006 Devrim Gunduz <devrim@commandprompt.com> 4.0.1-4
- More specfile fixes per bugzilla review #200600

* Sun Aug 6 2006 Devrim Gunduz <devrim@commandprompt.com> 4.0.1-3
- Changed awk dependency to gawk
- Fixed changelog entry

* Tue Aug 1 2006 Devrim Gunduz <devrim@commandprompt.com> 4.0.1-2
- Rebuilt for FC Extras Submission
- Fixed rpmlint errors
- Spec file cleanup

* Tue Dec 17 2005 Devrim Gunduz <devrim@commandprompt.com> 4.0.1
- Update to 4.0.1
- Added xloadtree and help among installed file lists
- rename pgadmindir to phppgadmindir

* Tue Oct 18 2005 Devrim Gunduz <devrim@gunduz.org> 3.5.6
- Updated to 3.5.6

* Wed Aug 24 2005 Devrim Gunduz <devrim@gunduz.org> 3.5.5
- Updated to 3.5.5

* Tue Jul 19 2005 Devrim Gunduz <devrim@gunduz.org> 3.5.4
- Updated to 3.5.4
