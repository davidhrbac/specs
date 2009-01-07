%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: Tools for creating presto repositories
Name: presto-utils
Version: 0.3.3
Release: 2%{?dist}
License: GPLv2+
Group: Development/Tools
Source: http://www.lesbg.com/jdieter/presto/%{name}-%{version}.tar.bz2
URL: http://www.lesbg.com/jdieter/presto/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python
Requires: python >= 2.4, deltarpm >= 3.4-2, createrepo >= 0.4.8

%description
Yum-presto is a plugin for yum that looks for deltarpms rather than rpms
whenever they are available.  This has the potential of saving a lot of
bandwidth when downloading updates.

A Deltarpm is the difference between two rpms.  If you already have foo-1.0
installed and foo-1.1 is available, yum-presto will download the deltarpm
for foo-1.0 => 1.1 rather than the full foo-1.1 rpm, and then build the full 
foo-1.1 package from your installed foo-1.0 and the downloaded deltarpm.

Presto-utils is a series of tools for creating presto repositories that
yum-presto can use.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%doc README 
%doc COPYING
%doc ChangeLog
%{_bindir}/createprestorepo
%{_bindir}/createprestorepo-0.2
%{_bindir}/createprestorepo-0.3
%{_bindir}/prunedrpms
%{_bindir}/createdeltarpms
%{python_sitelib}/presto-utils

%changelog
* Wed Oct 15 2008 Jonathan Dieter <jdieter@gmail.com> - 0.3.3-2
- Bring in python in BR

* Thu Aug 14 2008 Jonathan Dieter <jdieter@gmail.com> - 0.3.3-1
- Include a number of patches to make accessible as a library

* Tue Aug 14 2007 Jonathan Dieter <jdieter@gmail.com> - 0.3.2-1
- Fix small bug that didn't allow certain deltarpms to be generated

* Wed Jul 11 2007 Jonathan Dieter <jdieter@gmail.com> - 0.3.1-1
- Fix typo in XML creation

* Wed Jul 11 2007 Jonathan Dieter <jdieter@gmail.com> - 0.3.0-1
- New XML structure (thanks, Jeremy)
- prunedrpms script added

* Tue Jun 19 2007 Jonathan Dieter <jdieter@gmail.com> - 0.2.0-1
- Initial release 
