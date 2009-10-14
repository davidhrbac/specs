Name:           gearmand
Version:        0.10
Release:        1%{?dist}
Summary:        A distributed job system

Group:          System Environment/Daemons
License:        BSD
URL:            http://www.gearman.org
Source0:        http://launchpad.net/gearmand/trunk/%{version}/+download/gearmand-%{version}.tar.gz
Source1:        gearmand.init
Source2:        gearmand.sysconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libevent-devel, e2fsprogs-devel, libmemcached-devel, memcached
#BuildRequires:  libevent-devel, libuuid-devel, libmemcached-devel, memcached

%ifnarch ppc64 sparc64
# no google perftools
#BuildRequires: google-perftools-devel
%endif
Requires(pre):   shadow-utils
Requires(post):  chkconfig
Requires(preun): chkconfig, initscripts
Requires:        procps

%description
Gearman provides a generic framework to farm out work to other machines
or dispatch function calls to machines that are better suited to do the work.
It allows you to do work in parallel, to load balance processing, and to
call functions between languages. It can be used in a variety of applications,
from high-availability web sites to the transport for database replication.
In other words, it is the nervous system for how distributed processing
communicates.


%package -n libgearman-devel
Summary:        Development headers for libgearman
Requires:       pkgconfig, libgearman = %{version}-%{release}
Group:          Development/Libraries

%description -n libgearman-devel
Development headers for %{name}

%package -n libgearman
Summary:        Development libraries for gearman
Group:          Development/Libraries


%description -n libgearman
Development libraries for %{name}



%prep
%setup -q
#perl -pi -e "s|memcached_version\(\)|memcached_lib_version\(\)|g" configure
#perl -pi -e "s|memcached_version\(\)|memcached_lib_version\(\)|g" m4/pandora_have_libmemcached.m4
perl -pi -e "s|-Wno-attributes||g" configure

%build
%ifarch ppc64 sparc64
# no tcmalloc
%configure --disable-static
%else
%configure --disable-static --enable-tcmalloc
%endif

#sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
#sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -v %{buildroot}%{_libdir}/libgearman.la
install -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/gearmand
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/gearmand
mkdir -p %{buildroot}/var/run/gearmand


%clean
rm -rf %{buildroot}


%pre
getent group gearmand >/dev/null || groupadd -r gearmand
getent passwd gearmand >/dev/null || \
        useradd -r -g gearmand -d / -s /sbin/nologin \
        -c "Gearmand job server" gearmand
exit 0

%post
if [ $1 -eq 1 ]; then
        /sbin/chkconfig --add gearmand
fi

%preun
if [ $1 -eq 0 ]; then
        /sbin/service gearmand stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del gearmand
fi


%post -n libgearman -p /sbin/ldconfig

%postun -n libgearman -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%dir %attr(755,gearmand,gearmand) /var/run/gearmand
%config(noreplace) %{_sysconfdir}/sysconfig/gearmand
%{_sbindir}/gearmand
%{_bindir}/gearman
%{_initrddir}/gearmand
%{_mandir}/man1/gearman.1.gz
%{_mandir}/man8/gearmand.8.gz


%files -n libgearman-devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%dir %{_includedir}/libgearman
%{_includedir}/libgearman/*.h
%{_libdir}/pkgconfig/gearmand.pc
%{_libdir}/libgearman.so
%{_mandir}/man3/gearman*.3.gz
%dir %{_includedir}/libgearman-server
%{_includedir}/libgearman-server/*.h
%{_libdir}/libgearman-server.la
%{_libdir}/libgearman-server.so.0.0.0

%files -n libgearman
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libgearman.so.*


%changelog
* Wed Oct 14 2009 David Hrbáč <david@hrbac.cz> - 0.10-1
- new upstream version
- patch to build

* Wed Oct 14 2009 David Hrbáč <david@hrbac.cz> - 0.9-1
- initial build

* Fri Jul 31 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.9-1
- Upstream released new version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.8-1
- Upstream released new version
- Enable libmemcached backend

* Mon Jun 22 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.7-1
- Upstream released new version

* Mon Jun 22 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.6-3
- Don't build with tcmalloc on sparc64

* Sun May 24 2009 Peter Lemenkov <lemenkov@gmail.com> 0.6-2
- Fixed issues, reported in https://bugzilla.redhat.com/show_bug.cgi?id=487148#c9

* Wed May 20 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.6-1
- Upstream released new version

* Mon Apr 27 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.5-1
- Upstream released new version
- Cleanups for review (bz #487148)

* Wed Feb 25 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.3-2
- Add init script

* Sat Feb 07 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.3-1
- Initial import

