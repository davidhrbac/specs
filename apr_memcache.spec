Summary:    A client for memcached
Name:       apr_memcache
Version:    0.7.0
Release:    1%{?dist}
License:    Apache v2.0
Group:      Libraries
Source0:    http://www.outoforder.cc/downloads/apr_memcache/%{name}-%{version}.tar.bz2
#Patch0:     %{name}-libtool.patch
Patch0:     apr_reslist_invalidate.patch
URL:        http://www.outoforder.cc/projects/libs/apr_memcache/
BuildRequires:  apr-devel 
BuildRequires:  apr-util-devel
BuildRequires:  autoconf >= 2.53
BuildRequires:  automake
BuildRequires:  libtool
BuildRoot: %{_tmppath}/%{name}-root

%description
apr_memcache is a client for memcached written in C, using APR and
APR-Util. It provides pooled client connections and is thread safe,
making it perfect for use inside Apache Modules.

%package devel
Summary:    Development files for apr_memcache
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   apr-devel
Requires:   apr-util-devel

%description devel
Header files for apr_memcache.

%package static
Summary:    Static apr_memcache library
Group:      Development/Libraries
Requires:   %{name}-devel = %{version}-%{release}

%description static
Static apr_memcache library.

%prep
%setup -q
#{?el4: %patch1 -p}

%build
#{__libtoolize}
#{__aclocal} -I m4
#{__autoheader}
#{__automake}
#{__autoconf}

%configure \
    --with-apr=%{_bindir}/apr-1-config \
    --with-apr-util=%{_bindir}/apu-1-config

%{__make} \
    CFLAGS="`apu-1-config --includes` `apr-1-config --includes`"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
    DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE NOTICE test
%attr(755,root,root) %{_libdir}/libapr_memcache.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libapr_memcache.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libapr_memcache.so
%{_libdir}/libapr_memcache.la
%{_includedir}/apr_memcache-0

%files static
%defattr(644,root,root,755)
%{_libdir}/libapr_memcache.a

%changelog
* Tue Aug 07 2012 David Hrbáč <david@hrbac.cz> - 0.7.0-1
- initial build
