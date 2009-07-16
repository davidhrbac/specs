Name:		argtable2
Version:	11
Release:	2%{?dist}
License:	LGPLv2+
Group:		System Environment/Libraries
Summary:	A library for parsing GNU style command line arguments
URL:		http://argtable.sourceforge.net/	
Source0:	http://downloads.sourceforge.net/argtable/%{name}-%{version}.tar.gz	
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
 Argtable is an ANSI C library for parsing GNU style command line arguments.
 It enables a program's command line syntax to be defined in the source
 code as an array of argtable structs. The command line is then parsed 
 according to that specification and the resulting values are returned in 
 those same structs where they are accessible to the main program. Both tagged 
 (-v, --verbose, --foo=bar) and untagged arguments are supported, as are 
 multiple instances of each argument. Syntax error handling is automatic and 
 the library also provides the means for displaying the command line syntax 
 directly from the array of argument specifications.
 Argtable can function as a "getopt_long" replacement, without the user 
 of the program noticing the difference. Unlike "getopt_long", argtable is
 cross platform and works on Windows and Mac as well as Posix systems.

%package devel
Group:		Development/Libraries
Summary:	Development libraries and headers for the %{name} library 
Requires:	%{name} = %{version}-%{release}

%description devel
Development libraries and headers for use in building applications that
use the %{name} library.

%package doc
Group: Documentation
Summary: Documentation for the %{name} library
Requires: %{name} = %{version}-%{release}

%description doc
The %{name}-doc package contains documentation for using 
the %{name} library.

%prep
%setup -q

%build
%configure --enable-static=no --docdir=%{_defaultdocdir}/%{name}-doc-%{version} --target=%{_build_cpu} 
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -type f -name '*.la' -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name 'debug' -exec rm -f {} \;
%{__rm} -rf $RPM_BUILD_ROOT/usr/src/debug
%{__rm} -rf /var/tmp/argtable2-9-2.el4.hrb-root-root/usr/lib/debug/  
%check
%{__make} check

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README 
%{_libdir}/*.so.*
%{_mandir}/man3/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/argtable2.h
%{_libdir}/*.so

%files doc
%defattr(-,root,root)
%doc %{_defaultdocdir}/%{name}-doc-%{version}

%changelog
* Wed Jul 15 2009 David Hrbáč <david@hrbac.cz> - 11-2
- initial rebuild

* Tue Mar 20 2009 Jess Portnoy <kernel01@gmail.com> 11-2
- Added --target= passing the _build_cpu macro
* Tue Mar 17 2009 Stewart Heitmann <sheitmann@users.sourceforge.net> 11-1
- Minor tweaks to the Makefile install process. The source code is unchanged.
* Sun Mar 8 2009 Jess Portnoy <kernel01@gmail.com> 10-5
- Added make check, moved docs from devel to a separate doc package, excluded Makefile.nmake.
* Thu Feb 19 2009 Jess Portnoy <kernel01@gmail.com> 10-4
- Package repack due to adding this spec file to the source tar ball.
* Thu Feb 19 2009 Jess Portnoy <kernel01@gmail.com> 10-3
- Added --enable-static=no and --docdir=/usr/share/doc/argtable2-devel-version to configure command.
* Tue Feb 17 2009 Jess Portnoy <kernel01@gmail.com> 10-2
- Omitted tests dir and added the example dir to the devel package documentation.
* Tue Jan 27 2009 Stewart Heitmann <sheitmann@users.sourceforge.net> 10-1
- Minor tweaks to the documentation and configuration scripts. The source code is unchanged.
* Sat Dec 20 2008 Jess Portnoy <kernel01@gmail.com> 9-2
- Reworked the rpm package to satisfy Fedora Core 10 conventions.
* Wed Mar 26 2008 Stewart Heitmann <sheitmann@users.sourceforge.net> 9-1
- Fixed a makefile bug. The source code remains unchanged from argtable2-8.
* Tue Jan 1 2008 Stewart Heitmann <sheitmann@users.sourceforge.net> 8-1
- Added extra foolproofing to miscellaneous library functions.
* Wed Jul 18 2007 Stewart Heitmann <sheitmann@users.sourceforge.net> 7-1
- Improved argument checking features plus bug fixes for TI DSP and Solaris platforms.
* Sun Feb 12 2006 Stewart Heitmann <sheitmann@users.sourceforge.net> 6-1
- Windows makefiles are re-instated. The source code remains unchanged from argtable2-5.
* Fri Dec 23 2005 Stewart Heitmann <sheitmann@users.sourceforge.net> 5-1
- Migration to automake plus enhanced glossary printing features.
* Mon Jan 31 2005 Stewart Heitmann <sheitmann@users.sourceforge.net> 4-0
- Added new date and string argument parsing features and improved error reporting.
* Mon Feb 10 2004 Stewart Heitmann <sheitmann@users.sourceforge.net> 3-0
- Initial rpm package release.

