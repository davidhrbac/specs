Name:             tokyotyrant
Version:          1.1.39
Release:          1%{?dist}
Summary:          A network interface to Tokyo Cabinet

Group:            Applications/Databases
License:          LGPLv2+
URL:              http://1978th.net/tokyotyrant/
Source0:          http://1978th.net/tokyotyrant/%{name}-%{version}.tar.gz
Source1:          tokyotyrant.logrotate
Source2:          tokyotyrant.init
Source3:          tokyotyrant.sysconfig
Patch0:           tokyotyrant-1.1.33.build.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:         %{name}-libs = %{version}-%{release}
Requires:         logrotate
Requires(post):   chkconfig
Requires(postun): initscripts
Requires(pre):    shadow-utils
Requires(preun):  chkconfig
Requires(preun):  initscripts

BuildRequires:    autoconf
BuildRequires:    bzip2-devel
BuildRequires:    lua-devel
BuildRequires:    tokyocabinet-devel >= 1.4.30
BuildRequires:    zlib-devel

%description
Tokyo Tyrant is a network interface to Tokyo Cabinet.

%package          libs
Summary:          Runtime library files for %{name}
Group:            System Environment/Libraries

%description      libs
Tokyo Tyrant is a network interface to Tokyo Cabinet.

The %{name}-libs package contains libraries for running %{name}
applications.

%package          devel
Summary:          Development files for %{name}
Group:            Development/Libraries
Requires:         %{name}-libs = %{version}-%{release}
Requires:         pkgconfig
Requires:         tokyocabinet-devel

%description      devel
Tokyo Tyrant is a network interface to Tokyo Cabinet.

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1

%build
%{__sed} -i '/LD_RUN_PATH/d' Makefile.in
autoconf
%configure --enable-lua
%{__make} %{?_smp_mflags}

%install
%{__rm} -fr %{buildroot}
%{__make} DESTDIR=%{buildroot} install
# Install sysconfig and init files
%{__install} -p -m 0644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -p -m 0755 -D %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
%{__install} -p -m 0644 -D %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -p -m 0755 -d %{buildroot}%{_localstatedir}/log/%{name}
%{__install} -p -m 0755 -d %{buildroot}%{_localstatedir}/run/%{name}
%{__install} -p -m 0755 -d %{buildroot}%{_sharedstatedir}/%{name}
# Remove un-needed files
%{__rm} -f %{buildroot}%{_sbindir}/ttservctl
%{__rm} -f %{buildroot}%{_libdir}/lib%{name}.a
# Remove doc files installed by make
%{__rm} -f %{buildroot}%{_datadir}/%{name}/COPYING
%{__rm} -f %{buildroot}%{_datadir}/%{name}/ChangeLog
%{__rm} -f %{buildroot}%{_datadir}/%{name}/THANKS
%{__rm} -fr %{buildroot}%{_datadir}/%{name}/doc
# Move non lib* shared libraries into sub-directory
%{__mkdir_p} %{buildroot}%{_libdir}/%{name}
%{__mv} %{buildroot}%{_libdir}/t*.so %{buildroot}%{_libdir}/%{name}

%clean
%{__rm} -fr %{buildroot}

%post
/sbin/chkconfig --add tokyotyrant

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
-c 'Tokyo Tyrant Server' %{name}
exit 0

%preun
if [ $1 = 0 ]; then
  /sbin/service tokyotyrant stop &> /dev/null
  /sbin/chkconfig --del tokyotyrant
fi

%files
%defattr(-,root,root,-)
%doc ChangeLog doc/
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_bindir}/t*
%{_datadir}/%{name}
%{_initrddir}/%{name}
%attr(0755,tokyotyrant,tokyotyrant) %dir %{_localstatedir}/log/%{name}
%attr(0755,tokyotyrant,tokyotyrant) %dir %{_localstatedir}/run/%{name}
%{_mandir}/man1/t*.gz
%{_mandir}/man8/t*.gz
%attr(0755,tokyotyrant,tokyotyrant) %dir %{_sharedstatedir}/%{name}

%files libs
%defattr(-,root,root,-)
%doc COPYING README THANKS
%{_libdir}/%{name}
%{_libdir}/lib%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/t*.h
%{_libdir}/libtokyotyrant.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/t*.gz

%changelog
* Thu Jan 07 2010 David Hrbáč <david@hrbac.cz> - 1.1.39-1
- new upstream release

* Thu Jan 07 2010 David Hrbáč <david@hrbac.cz> - 1.1.38-1
- new upstream release

* Thu Jan 07 2010 David Hrbáč <david@hrbac.cz> - 1.1.37-1
- new upstream release

* Thu Jan 07 2010 David Hrbáč <david@hrbac.cz> - 1.1.35-1
- new upstream release

* Wed Nov 11 2009 David Hrbáč <david@hrbac.cz> - 1.1.34-1
- initial rebuild

* Mon Sep 07 2009 Silas Sewell <silas@sewell.ch> - 1.1.34-1
- Update to 1.1.34

* Fri Aug 21 2009 Silas Sewell <silas@sewell.ch> - 1.1.33-5
- Fix url

* Thu Aug 20 2009 Silas Sewell <silas@sewell.ch> - 1.1.33-4
- Add requires tokyocabinet to tokyotyrant.pc

* Tue Aug 18 2009 Silas Sewell <silas@sewell.ch> - 1.1.33-3
- Add tokyocabinet to tokyotyrant.pc
- More spec fixes

* Sun Aug 16 2009 Silas Sewell <silas@sewell.ch> - 1.1.33-2
- Various spec fixes

* Tue Aug 11 2009 Silas Sewell <silas@sewell.ch> - 1.1.33-1
- Initial package
