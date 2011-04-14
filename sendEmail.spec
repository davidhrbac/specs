Summary: A lightweight, completly command line based, SMTP email agent
Name: sendEmail
Version: 1.56
Release: 1%{?dist}
Group: Applications/Internet
License: GPLv2+
URL: http://caspian.dotconf.net/menu/Software/SendEmail/
Source0: http://caspian.dotconf.net/menu/Software/SendEmail/%{name}-v%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
SendEmail is a lightweight tool written in Perl for sending SMTP
email from the console. It was designed to be used in bash scripts,
Perl programs, and Web pages. It requires no special modules, and
has a simple interface, making it very easy to install and use.
It should work on any platform that has Perl and supports Unix
sockets, but was designed for Linux.

%prep
%setup -q -n %{name}-v%{version}

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{_bindir}
%{__install} -m 0755 -p %{name} %{buildroot}%{_bindir}/

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/%{name}
%doc CHANGELOG README TODO

%changelog
* Thu Apr 14 2011 David Hrbáč <david@hrbac.cz> - 1.56-1
- initial rebuild

* Mon Oct 02 2009 Simon Matter <simon.matter@invoca.ch> 1.56-1
- upgrade to 1.56
- change license tag to GPLv2+

* Fri Dec 15 2006 Simon Matter <simon.matter@invoca.ch> 1.55-1
- update to version 1.55

* Sun Nov 19 2006 Simon Matter <simon.matter@invoca.ch> 1.54-2
- add bindaddr patch

* Tue Oct 31 2006 Simon Matter <simon.matter@invoca.ch> 1.54-1
- update to version 1.54

* Thu Mar 10 2005 Simon Matter <simon.matter@invoca.ch>
- update to version 1.52

* Fri Dec 03 2004 Simon Matter <simon.matter@invoca.ch>
- update to version 1.51

* Thu Oct 07 2004 Simon Matter <simon.matter@invoca.ch>
- update to version 1.50

* Thu Nov 13 2003 Simon Matter <simon.matter@invoca.ch>
- initial build

