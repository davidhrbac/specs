%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:		gammu
Version:	1.27.92
Release:	1%{?dist}
Summary:	Command Line utility to work with mobile phones

Group:		Applications/System
License:	GPLv2+
URL:		http://cihar.com/gammu/
Source0:	http://dl.cihar.com/gammu/releases/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	autoconf, gettext, cmake
#BuildRequires:	libusb1-devel, doxygen
#BuildRequires:	libcurl-devel
# Enabling bluetooth fonction
BuildRequires:	bluez-libs-devel
# Enabling Database sms fonction
BuildRequires:	postgresql-devel, mysql-devel

Requires:	bluez-utils, dialog

%package smsd
Summary:    SMS message daemon
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Group:              Applications/Communications

%package	libs
Summary:	Libraries files for %{name}
Group:		System Environment/Libraries

%package -n     python-%{name}
Summary:	Python bindings for Gammu
Group:		Development/Languages

BuildRequires:  python-devel
Obsoletes:	python-%{name} <= 0.28

Requires:	%{name} = %{version}-%{release}

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

%description smsd
This package contains Gammu SMS Daemon and tool to inject messages 
into the queue.

%description	libs
The %{name}-libs package contains libraries files that used by %{name}

%description -n python-%{name}
Python bindings for Gammu library.
It currently does not support all Gammu features,
but range of covered functions is increasing,
if you need some specific, feel free to use bug tracking system for feature requests.

%description	devel
The %{name}-devel  package contains Header and libraries files for
developing applications that use %{name}




%prep
%setup -q

#sed -i 's|${INSTALL_LIB_DIR}|%{_libdir}|' CMakeLists.txt libgammu/CMakeLists.txt \
#				smsd/CMakeLists.txt gammu/CMakeLists.txt

%build
mkdir build
pushd build
%cmake					\
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
	docs/user/*.* ; do
	sed -e 's/\r//' -i $docs
done


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
#cp -pR $RPM_BUILD_ROOT%{_docdir}/%{name}/examples/* docs/examples
cp -p $RPM_BUILD_ROOT%{_docdir}/%{name}/*.* .
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%find_lang %{name}
%find_lang lib%{name}
cat lib%{name}.lang >> %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT


%post -n %{name}-libs -p /sbin/ldconfig

%postun -n %{name}-libs -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING ChangeLog README docs/* BUGS *.html *.txt
%{_bindir}/%{name}*
%{_bindir}/jadmaker
%{_mandir}/man1/*.gz
%{_mandir}/man5/*.gz
%{_mandir}/man7/*.gz
%{_mandir}/cs/man1/*.gz
%{_mandir}/cs/man5/*.gz
%{_mandir}/cs/man7/*.gz
%config %{_sysconfdir}/bash_completion.d/%{name}

%files		libs
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files -n       python-%{name}
%defattr(-,root,root,-)
%{python_sitearch}/%{name}

%files		devel
%defattr(-,root,root,-)
%doc devel_docs/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{name}


%changelog
* Sun Feb 28 2010 David Hrbáč <david@hrbac.cz> - 1.27.92-1
- new upstream release

* Thu Feb 04 2010 David Hrbáč <david@hrbac.cz> - 1.27.90-1
- new upstream release

* Thu May  7 2009 Ville Skyttä <ville.skytta at iki.fi> - 1.24.0-2
- Build with $RPM_OPT_FLAGS, use %%cmake macro.

* Wed Apr 29 2009 Xavier Lamien <lxtnow@gmail.com> - 1.24.0-1
- Update release.

* Tue Apr 14 2009 Xavier Lamien <lxtnow@gmail.com> - 1.23.92-1
- Update release.

* Sun Apr 12 2009 Xavier Lamien <lxntow@gmail.com> - 1.23.1-1
- Update release.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22.94-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Xavier Lamien <lxtnow@gmail.com> - 1.22.94-1
- Update release.

* Mon Jan 26 2009 Xavier Lamien <lxtnow@gmail.com> - 1.22.90-3
- Make _libdir in a good shape.

* Mon Jan 26 2009 Tomas Mraz <tmraz@redhat.com> - 1.22.90-2
- rebuild with new openssl and mysql

* Sun Jan 11 2009 Xavier Lamien <lxtnow[at]gmail.com> - 1.22.90-1
- Update release.

* Tue Dec 30 2008 Jan ONDREJ (SAL) <ondrejj(at)salstar.sk> - 1.22.1-2
- Update release.
- -DENABLE_SHARED=ON replaced by -DBUILD_SHARED_LIBS=ON

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
