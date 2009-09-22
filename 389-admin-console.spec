%define major_version 1.1
%define minor_version 4

%define shortname 389-admin
%define pkgname dirsrv

Name: 389-admin-console
Version: %{major_version}.%{minor_version}
Release: 2%{?dist}
Summary: 389 Admin Server Management Console

Group: Applications/System
License: GPLv2
URL: http://port389.org

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Source: http://port389.org/sources/%{name}-%{version}.tar.bz2
Requires: 389-admin
BuildRequires: ant >= 1.6.2
BuildRequires: ldapjdk
BuildRequires: idm-console-framework
BuildRequires: java-devel >= 1:1.6.0
Provides: fedora-ds-admin-console = %{version}-%{release}
Obsoletes: fedora-ds-admin-console < 1.1.4-1

%description
A Java based remote management console used for Managing 389
Admin Server.  Requires the 389 Console to load and run the
jar files.

%package          doc
Summary:          Web docs for 389 Admin Server Management Console
Group:            Documentation
Requires:         %{name} = %{version}-%{release}

%description      doc
Web docs for 389 Admin Server Management Console

%prep
%setup -q
                                                                                
%build
%{ant} \
    -Dconsole.location=%{_javadir} \
    -Dbuilt.dir=`pwd`/built

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/html/java
install -m644 built/package/%{shortname}* $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/html/java
install -d $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/manual/en/admin/help
install -m644 help/en/*.html $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/manual/en/admin
install -m644 help/en/tokens.map $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/manual/en/admin
install -m644 help/en/help/*.html $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/manual/en/admin/help

# create symlinks
pushd $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/html/java
ln -s %{shortname}-%{version}.jar %{shortname}-%{major_version}.jar
ln -s %{shortname}-%{version}.jar %{shortname}.jar
ln -s %{shortname}-%{version}_en.jar %{shortname}-%{major_version}_en.jar
ln -s %{shortname}-%{version}_en.jar %{shortname}_en.jar
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_datadir}/%{pkgname}/html/java/%{shortname}-%{version}.jar
%{_datadir}/%{pkgname}/html/java/%{shortname}-%{major_version}.jar
%{_datadir}/%{pkgname}/html/java/%{shortname}.jar
%{_datadir}/%{pkgname}/html/java/%{shortname}-%{version}_en.jar
%{_datadir}/%{pkgname}/html/java/%{shortname}-%{major_version}_en.jar
%{_datadir}/%{pkgname}/html/java/%{shortname}_en.jar

%files doc
%defattr(-,root,root,-)
%dir %{_datadir}/%{pkgname}/manual/en/admin
%doc %{_datadir}/%{pkgname}/manual/en/admin/tokens.map
%doc %{_datadir}/%{pkgname}/manual/en/admin/*.html
%doc %{_datadir}/%{pkgname}/manual/en/admin/help/*.html

%changelog
* Tue Sep 22 2009 David Hrbáč <david@hrbac.cz> - 1.1.4-2
- initial build

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Rich Megginson <rmeggins@redhat.com> 1.1.4-1
- relicense source files under GPLv2
- create doc sub package

* Fri May 15 2009 Rich Megginson <rmeggins@redhat.com> 1.1.3-2
- rename to 389

* Tue Mar 31 2009 Rich Megginson <rmeggins@redhat.com> 1.1.3-1
- this is the 1.1.3 release

* Thu Jul  3 2008 Rich Megginson <rmeggins@redhat.com> 1.1.2-1
- disable SSLv2 settings

* Wed Jan 16 2008 Rich Megginson <rmeggins@redhat.com> 1.1.1-2
- rename package to fedora-ds-admin-console

* Thu Jan 10 2008 Rich Megginson <rmeggins@redhat.com> 1.1.1-1
- changes for fedora package review
- added requires for icedtea java
- added LICENSE

* Wed Dec 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-4
- This is for the Fedora DS 1.1 release

* Thu Oct 25 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-3
- updated sources - use dirsrv as package name

* Wed Aug  8 2007 Nathan Kinder <nkinder@redhat.com> 1.1.0-2
- Added online help files into package.

* Thu Aug  2 2007 Nathan Kinder <nkinder@redhat.com> 1.1.0-1
- Initial creation
