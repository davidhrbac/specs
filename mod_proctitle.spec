%define svn .20080707
Summary: Define and use proctitles within the Apache configuration
Name: mod_proctitle
Version: 0.1
Release: 1%{svn}%{dist}
Group: System Environment/Daemons
URL: http://cri.ensmp.fr/~coelho/mod_proctitle/
#Source0: ftp://ftp.springdaemons.com/soft/mod_proctitle-%{version}.tar.bz2
Source0: mod_proctitle.c
#Source1: README
#Source2: antiloris.conf
License: Apache Licence 2.0
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: httpd-devel >= 2.0.40-6
Requires: httpd >= 2.0.40

%description
mod_proctitle is a third-party module for the Apache HTTP Server. It is
distributed with a BSD-style license similar to Apache. It allows the
definition and use of proctitles within Apache runtime configuration files.

%prep
%setup -q -c -T
install %{SOURCE0} .

%{__cat} <<'EOF' >%{name}.conf
LoadModule proctitle_module modules/%{name}.so
EOF


%build
%{_sbindir}/apxs -c %{name}.c
mv .libs/%{name}.so .
%{__strip} -g %{name}.so

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -m755 %{name}.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -Dp -m0644 %{name}.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

#install %{SOURCE1} README
    
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
#%doc README, INSTALL
#%doc ChangeLog
%attr(755,root,root)%{_libdir}/httpd/modules/*.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf

%changelog
* Wed Aug 26 2009 David Hrbáč <david@hrbac.cz> - 0.1-1.20080707
- Initial build.
