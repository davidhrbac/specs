%define selinux_variants mls strict targeted 
%define selinux_policyver %(sed -e 's,.*selinux-policy-\\([^/]*\\)/.*,\\1,' /usr/share/selinux/devel/policyhelp)
%define modulename memcached

%define username  memcached
%define groupname memcached

Name:           memcached
Version:        1.4.4
Release:        1%{?dist}
Summary:        High Performance, Distributed Memory Object Cache

Group:          System Environment/Daemons
License:        BSD
URL:            http://www.danga.com/memcached/
#Source0:        http://www.danga.com/memcached/dist/%{name}-%{version}.tar.gz
Source0:        http://memcached.googlecode.com/files/%{name}-%{version}.tar.gz

# custom init script
Source1:        memcached.sysv.patched

# SELinux files
Source10:       %{modulename}.te
Source11:       %{modulename}.fc
Source12:       %{modulename}.if
Patch0:         memcached-test.patch
#Patch1:         memcached-macro.patch
# Fixes

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libevent-devel
BuildRequires:  perl(Test::More)

Requires: initscripts
Requires: libevent
Requires(pre):  shadow-utils
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service

%description
memcached is a high-performance, distributed memory object caching
system, generic in nature, but intended for use in speeding up dynamic
web applications by alleviating database load.


%if "%{centos_ver}" == "5"
%package selinux
Summary:        SELinux policy module supporting memcached
Group:          System Environment/Base
BuildRequires:  checkpolicy, selinux-policy-devel, hardlink
%if "%{selinux_policyver}" != ""
Requires:       selinux-policy >= %{selinux_policyver}
%endif
Requires:       %{name} = %{version}-%{release}
Requires(post):  policycoreutils
Requires(postun): policycoreutils


%description selinux
SELinux policy module supporting memcached.
%endif%

%package devel
Summary:	Files needed for development using memcached protocol
Group:		Development/Libraries 

%description devel
Install memcached-devel if you are developing C/C++ applications that require access to the
memcached binary include files.

%prep
%setup -q
%patch0 -p0 -b .test
#%patch1 -p0 -b .macro

%if "%{centos_ver}" == "5"
mkdir SELinux
cp -p %{SOURCE10} %{SOURCE11} %{SOURCE12} SELinux/
%endif%

%build
%configure --enable-threads

make %{?_smp_mflags}

%if "%{centos_ver}" == "5"
pushd SELinux
for selinuxvariant in %{selinux_variants}; do
    make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
    mv %{modulename}.pp %{modulename}.pp.${selinuxvariant}
    make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
popd
%endif%

%check
# remove failing test that doesn't work in
# build systems
rm -f t/daemonize.t 
make test

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"                                         
# remove memcached-debug
rm -f %{buildroot}/%{_bindir}/memcached-debug

# Perl script for monitoring memcached
install -Dp -m0755 scripts/memcached-tool %{buildroot}%{_bindir}/memcached-tool

# Init script
install -Dp -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/memcached

# Default configs
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cat <<EOF >%{buildroot}/%{_sysconfdir}/sysconfig/%{name}
PORT="11211"
USER="%{username}"
MAXCONN="1024"
CACHESIZE="64"
OPTIONS=""
EOF

# pid directory
mkdir -p %{buildroot}/%{_localstatedir}/run/memcached

%if "%{centos_ver}" == "5"
# Install SELinux policy modules
pushd SELinux
for selinuxvariant in %{selinux_variants}; do
    install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
    install -p -m 644 %{modulename}.pp.${selinuxvariant} \
        %{buildroot}%{_datadir}/selinux/${selinuxvariant}/%{modulename}.pp
done
popd

# Hardlink identical policy module packages together
/usr/sbin/hardlink -cv %{buildroot}%{_datadir}/selinux
%endif%

%clean
rm -rf %{buildroot}


%pre
getent group %{groupname} >/dev/null || groupadd -r %{groupname}
getent passwd %{username} >/dev/null || \
useradd -r -g %{groupname} -d %{_localstatedir}/run/memcached \
    -s /sbin/nologin -c "Memcached daemon" %{username}
exit 0


%post
/sbin/chkconfig --add %{name}


%preun
if [ "$1" = 0 ] ; then
    /sbin/service %{name} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
exit 0


%postun
if [ "$1" -ge 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1
fi
exit 0

%if "%{centos_ver}" == "5"
%post selinux
# Install SELinux policy modules
for selinuxvariant in %{selinux_variants}
do
  /usr/sbin/semodule -s ${selinuxvariant} -i \
    %{_datadir}/selinux/${selinuxvariant}/%{modulename}.pp &> /dev/null || :
done
/usr/sbin/semanage port -a -t memcached_port_t -p tcp 11211 &> /dev/null || :
/sbin/fixfiles -R %{name} restore || :


%postun selinux
# Clean up after package removal
if [ $1 -eq 0 ]; then
  /usr/sbin/semanage port -d -t memcached_port_t -p tcp 11211 &> /dev/null || :
  # Remove SELinux policy modules
  for selinuxvariant in %{selinux_variants}
  do
    /usr/sbin/semodule -s ${selinuxvariant} -r %{modulename} &> /dev/null || :
  done
  /sbin/fixfiles -R %{name} restore || :
fi
%endif%

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README doc/CONTRIBUTORS doc/*.txt
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%dir %attr(755,%{username},%{groupname}) %{_localstatedir}/run/memcached
%{_bindir}/memcached-tool
%{_bindir}/memcached
%{_mandir}/man1/memcached.1*
%{_initrddir}/memcached

%if "%{centos_ver}" == "5"
%files selinux
%defattr(-,root,root,0755)
%doc SELinux/*.te SELinux/*.fc SELinux/*.if
%{_datadir}/selinux/*/%{modulename}.pp
%endif%

%files devel
%defattr(-,root,root,0755)
%{_includedir}/memcached/*

%changelog
* Sun Nov 29 2009 David Hrbáč <david@hrbac.cz> - 1.4.4-1
- new upstream version

* Wed Nov 18 2009 David Hrbáč <david@hrbac.cz> - 1.4.3-1
- new upstream version

* Tue Oct 13 2009 David Hrbáč <david@hrbac.cz> - 1.4.2-1
- new upstream version
  
* Fri Sep 18 2009 David Hrbáč <david@hrbac.cz>  - 1.4.1-2
- patched init script to work

* Mon Sep 14 2009 David Hrbáč <david@hrbac.cz>  - 1.4.1-1
- initial rebuild
- patch to tests
- C5 build patch

* Sat Aug 29 2009 Paul Lindner <lindner@inuus.com> - 1.4.1-1
- Upgrade to 1.4.1 
- http://code.google.com/p/memcached/wiki/ReleaseNotes141

* Wed Apr 29 2009 Paul Lindner <lindner@inuus.com> - 1.2.8-1
- Upgrade to memcached-1.2.8
- Addresses CVE-2009-1255

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 29 2008 Paul Lindner <lindner@inuus.com> - 1.2.6-1
- Upgrade to memcached-1.2.6

* Tue Mar  4 2008 Paul Lindner <lindner@inuus.com> - 1.2.5-1
- Upgrade to memcached-1.2.5

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.4-4
- Autorebuild for GCC 4.3

* Sun Jan 27 2008 Paul Lindner <lindner@inuus.com> - 1.2.4-3
- Adjust libevent dependencies

* Sat Dec 22 2007 Paul Lindner <lindner@inuus.com> - 1.2.4-2
- Upgrade to memcached-1.2.4

* Fri Sep 07 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.2.3-8
- Add selinux policies
- Create our own system user

* Mon Aug  6 2007 Paul Lindner <lindner@inuus.com> - 1.2.3-7
- Fix problem with -P and -d flag combo on x86_64
- Fix init script for FC-6

* Fri Jul 13 2007 Paul Lindner <lindner@inuus.com> - 1.2.3-4
- Remove test that fails in fedora build system on ppc64

* Sat Jul  7 2007 root <lindner@inuus.com> - 1.2.3-2
- Upgrade to 1.2.3 upstream
- Adjust make install to preserve man page timestamp
- Conform with LSB init scripts standards, add force-reload

* Wed Jul  4 2007 Paul Lindner <lindner@inuus.com> - 1.2.2-5
- Use /var/run/memcached/ directory to hold PID file

* Sat May 12 2007 Paul Lindner <lindner@inuus.com> - 1.2.2-4
- Remove tabs from spec file, rpmlint reports no more errors

* Thu May 10 2007 Paul Lindner <lindner@inuus.com> - 1.2.2-3
- Enable build-time regression tests
- add dependency on initscripts
- remove memcached-debug (not needed in dist)
- above suggestions from Bernard Johnson

* Mon May  7 2007 Paul Lindner <lindner@inuus.com> - 1.2.2-2
- Tidyness improvements suggested by Ruben Kerkhof in bugzilla #238994

* Fri May  4 2007 Paul Lindner <lindner@inuus.com> - 1.2.2-1
- Initial spec file created via rpmdev-newspec
