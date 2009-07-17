Name:		gammu
Version:	1.25.05
Release:        1%{?dist}
Summary:        Command Line utility to work with mobile phones

Group:          Applications/System
License:        GPLv2+
URL:            http://cihar.com/gammu/
Source0:        http://dl.cihar.com/gammu/releases/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	autoconf, gettext, cmake
#enabling bluetooth fonction
BuildRequires:	bluez-libs-devel
#enabling mysql sms fonction
BuildRequires:	postgresql-devel, mysql-devel
Requires:       bluez-utils, dialog

%package	libs
Summary:	Libraries files for %{name}
Group:		System Environment/Libraries

%package	devel
Summary:	Development files for %{name}	
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	pkgconfig

%description
Gammu is command line utility and library to work with mobile phones
from many vendors.
Support for different models differs, but basic functions should work
with majority of them. Program can work with contacts,
messages (SMS, EMS and MMS), calendar, todos, filesystem,
integrated radio, camera, etc.
It also supports daemon mode to send and receive SMSes.

%description	libs
The %{name}-libs package contains libraries files that used by %{name}

%description	devel
The %{name}-devel  package contains Header and libraries files for
developing applications that use %{name}

%prep
%setup -q


%build
mkdir build
pushd build
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix}	\
	-DENABLE_SHARED=ON		\
	-DENABLE_BACKUP=ON		\
	-DWITH_NOKIA_SUPPORT=ON		\
	-DWITH_Bluez=ON			\
	-DWITH_IrDA=On			\
	../
make
popd

#fix lines ending 
for docs in \
	docs/develop/{protocol/'*',sounds/*,sms/'*'}	\
	docs/develop/{*.htm,*.txt}			\
	docs/user/{*.html,*.txt} ; do
	sed -e 's/\r//' -i $docs
done

#fix libdir
sed -i 's|${CMAKE_INSTALL_PREFIX}/lib|%{_libdir}|g' build/cmake_install.cmake

%install
rm -rf $RPM_BUILD_ROOT

make -C build  install DESTDIR=$RPM_BUILD_ROOT
 
#remove library
rm -f $RPM_BUILD_ROOT%{_libdir}/libGammu.a

#Improve installed documentations directories
mkdir devel_docs
mkdir -p docs/symbian
cp -pR $RPM_BUILD_ROOT%{_docdir}/%{name}/devel/* devel_docs
cp -pR $RPM_BUILD_ROOT%{_docdir}/%{name}/symbian/* docs/symbian
cp -pR $RPM_BUILD_ROOT%{_docdir}/%{name}/examples/php* docs/examples
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT


%post -n %{name}-libs -p /sbin/ldconfig

%postun -n %{name}-libs -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING ChangeLog README docs/* BUGS SUPPORTERS
%{_bindir}/%{name}*
%{_bindir}/jadmaker
%{_mandir}/man1/*.1.gz
#%config %{_sysconfdir}/bash_completion.d/%{name}

%files		libs
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files		devel
%defattr(-,root,root,-)
%doc devel_docs/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{name}


%changelog
* Fri Jul 17 2009 David Hrbáč <david@hrbac.cz> - 1.25.0-1
- new upstream release

* Tue Feb 26 2009 David Hrbáč <david@hrbac.cz> - 1.22.95-1
- Update release.

* Wed Feb 25 2009 David Hrbáč <david@hrbac.cz> - 1.21.0-1
- initial rebuild

* Sat Oct 11 2008 Xavier Lamien <lxtnow[at]gmail.com> - 1.21.0-1
- Update release.

* Thu Sep 11 2008 Xavier Lamien <lxtnow[at]gmail.com> - 1.20.90-2
- Rebuild against new libbluetooth.

* Mon Aug 25 2008 Xavier Lamien <lxtnow[at]gmail.com> - 1.20.90-1
- Update release.

* Mon Aug 23 2008 Xavier Lamien <lxntow[at]gmail.com> - 1.20.0-1
- Update release.

* Mon Jun 02 2008 Xavier Lamien <lxtnow[at]gmail.com> - 1.19.0-2
- Added Require dialog.

* Thu Apr 15 2008 Xavier Lamien <lxtnow[at]gmail.com> - 1.19.0-1
- Updated Release.

* Fri Feb 29 2008 Xavier Lamien <lxtnow[at]gmail.com> - 1.18.91-1
- Updated Release.

* Thu Feb 28 2008 Xavier Lamien <lxtnow[at]gmail.com> - 1.18.0-1
- Updated Release.

* Sat Jan 26 2008 Xavier Lamien < lxtnow[at]gmail.com > - 1.17.92-1
- Updated Release.
- Included new binary file.

* Sat Dec 22 2007 Xavier Lamien < lxtnow[at]gmail.com > - 1.17.0-1
- Updated Release.

* Fri Oct 12 2007 Xavier Lamien < lxtnow[at]gmail.com > - 1.13.0-1
- Updated Release.

* Wed Aug 02 2007 Xavier Lamien < lxtnow[at]gmail.com > - 1.12.92-1
- Updated Release.

* Wed Jul 25 2007 Xavier Lamien < lxtnow[at]gmail.com > - 1.12.91-1
- Updated Release.

* Thu May 24 2007 Xavier Lamien < lxtnow[at]gmail.com > - 1.11.0-1
- Updated release.

* Wed May 23 2007 Xavier Lamien < lxtnow[at]gmail.com > - 1.10.6-1
- Updated release.

* Tue May 08 2007 Xavier Lamien < lxtnow[at]gmail.com > - 1.10.0-1
- Initial RPM release.
