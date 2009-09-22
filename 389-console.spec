%define major_version 1.1
%define minor_version 3

Name: 389-console
Version: %{major_version}.%{minor_version}
Release: 4%{?dist}
Summary: 389 Management Console

Group: Applications/System
License: LGPLv2
URL: http://port389.org

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Source: http://port389.org/sources/%{name}-%{version}.tar.bz2
Requires: idm-console-framework >= 1.1
Requires: java >= 1:1.6.0
BuildRequires: ant >= 1.6.2
BuildRequires: ldapjdk
BuildRequires: jss >=  4.2
BuildRequires: idm-console-framework >= 1.1
BuildRequires: java-devel >= 1:1.6.0
Provides: fedora-idm-console = %{version}-%{release}
Obsoletes: fedora-idm-console < 1.1.3-2

%description
A Java based remote management console used for managing 389
Administration Server and 389 Directory Server.

%prep
%setup -q
                                                                                
%build
%{ant} \
    -Dbuilt.dir=`pwd`/built

# add -Dlib.dir and -Dneed_libdir on those platforms where
# jss is installed in a non-standard location
# -Dneed_libdir=yes

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
install -m644 built/*.jar $RPM_BUILD_ROOT%{_javadir}
install -d $RPM_BUILD_ROOT%{_bindir}
install -m755 built/%{name} $RPM_BUILD_ROOT/%{_bindir}

# create symlinks
pushd $RPM_BUILD_ROOT%{_javadir}
ln -s %{name}-%{version}_en.jar %{name}-%{major_version}_en.jar
ln -s %{name}-%{version}_en.jar %{name}_en.jar
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_javadir}/%{name}-%{version}_en.jar
%{_javadir}/%{name}-%{major_version}_en.jar
%{_javadir}/%{name}_en.jar
%{_bindir}/%{name}

%changelog
* Wed Aug 12 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.3-4
- final rebuild for 1.1.3 release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 13 2009 Rich Megginson <rmeggins@redhat.com> 1.1.3-2
- rename to 389

* Tue Mar 31 2009 Rich Megginson <rmeggins@redhat.com> 1.1.3-1
- the 1.1.3 release

* Tue Apr 15 2008 Rich Megginson <rmeggins@redhat.com> 1.1.1-2
- use java > 1.5.0 for requirements

* Thu Jan 10 2008 Rich Megginson <rmeggins@redhat.com> 1.1.1-1
- this is the fedora package review candidate
- added LICENSE file
- changed permissions on jar files and shell script

* Wed Dec 19 2007 Rich Megginson <rmeggins@redhat.com> 1.1.0-5
- for the Fedora DS 1.1 release

* Thu Oct 25 2007 Nathan Kinder <nkinder@redhat.com> 1.1.0-4
- Removed noarch to ensure we find the 64-bit library.

* Wed Aug  1 2007 Nathan Kinder <nkinder@redhat.com> 1.1.0-3
- Separated theme package.

* Fri Jul 27 2007 Nathan Kinder <nkinder@redhat.com> 1.1.0-2
- Modified package name to be less generic.

* Mon Jul 26 2007 Nathan Kinder <nkinder@redhat.com> 1.1.0-1
- Initial creation
