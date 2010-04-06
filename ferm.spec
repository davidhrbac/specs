Summary:		For Easy Rule Making
Name:		ferm
Version:		2.0.7
Release:		1%{?dist}
Group:		Applications/System
License:		GPLv2+
Source:		http://ferm.foo-projects.org/download/2.0/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL:			http://ferm.foo-projects.org/
BuildArchitectures:		noarch

%description
Ferm is a tool to maintain complex firewalls, without having the
trouble to rewrite the complex rules over and over again. Ferm
allows the entire firewall rule set to be stored in a separate
file, and to be loaded with one command. The firewall configuration
resembles structured programming-like language, which can contain
levels and lists.

%prep
%setup -q

sed -i 's/PREFIX = /#PREFIX = /' config.mk
sed -i 's/MANDIR = /#MANDIR = /' config.mk
sed -i 's/DOCDIR = /#DOCDIR = /' config.mk

%build

%install
rm -Rf $RPM_BUILD_ROOT

make install PREFIX=$RPM_BUILD_ROOT%{_prefix} DOCDIR=$RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README TODO NEWS examples/
%{_mandir}/man1/*

%{_sbindir}/import-ferm
%{_sbindir}/ferm

%changelog
* Tue Apr 06 2010 David Hrbáč <david@hrbac.cz> - 2.0.7-1
- initial rebuild

* Tue Mar 9 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 2.0.7-8
- Update to 2.0.7

* Mon Dec 21 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 2.0.6-7
- Update to upstream 2.0.6 version.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 25 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 2.0.2-3
- License changed to GPLv2+ by answer of uptream developer Max Kellerman.

* Mon Aug 25 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 2.0.2-2
- In changelog fixed version representation by warning of rpmlint.
- Add NEWS to documentation.

* Fri Aug 22 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 2.0.2-1
- Step to version 2.0.2
- Group changed from "system/firewalls" to "Applications/System"
- Delete redundant "ferm -" from Summary tag.
- Delete Hu-part of Release to conform Fedora rules (by note in review).
- License changed rfom GPL to GPLv2 by source.
- Requires: perl removed.
- Setting variables in config.mk moved to %%prep section.
- Replace lost /usr to %%{_prefix} in make install instruction.
- %%defattr(-,root,root) changed to %%defattr(-,root,root,-)

* Fri Jul 11 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 1.3.4-0.Hu.1
- Changes to conform rpmlint ( http://fedoraproject.org/wiki/Packaging/Guidelines ):
	Setup made quiet
	Remove "mkdir -p $RPM_BUILD_ROOT" from %%prep
	Escape all %% in Changelog.
	Add %%build section

* Thu Jul 10 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 1.3.4-0.Hu.0
- Version 1.3.4
- Reformat with tabs.
- Clear old comments.
- Delete Packager: A. Kok <sofar@foo-projects.org>
- Add %%{?dist} part into release
- Replace hardcoded /usr/sbin to %%_sbindir
- Replace Build Root: "/tmp/%%{name}-%%{version}-root" by more standard.

* Mon Oct 22 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 1.2.5
- Steep to version 1.2.5

* Mon Jul  2 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su>
- Steep to version 1.2.4

* Mon Mar  5 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su>
- Steep to version 1.2
- Restructure dirs and files in package
