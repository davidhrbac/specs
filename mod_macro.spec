Summary: Define and use macros within the Apache configuration
Name: mod_macro
Version: 1.1.11
Release: 1%{dist}
Group: System Environment/Daemons
URL: http://cri.ensmp.fr/~coelho/mod_macro/
Source0: http://cri.ensmp.fr/~coelho/mod_macro/mod_macro-%{version}.tar.gz
License: Apache Licence 2.0
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: httpd-devel >= 2.0.40-6
Requires: httpd >= 2.0.40

%description
mod_macro is a third-party module for the Apache HTTP Server. It is
distributed with a BSD-style license similar to Apache. It allows the
definition and use of macros within Apache runtime configuration files.

%prep
%setup -q

%{__cat} <<'EOF' >%{name}.conf
LoadModule macro_module modules/%{name}.so
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
* Wed Nov 02 2011 David Hrbáč <david@hrbac.cz> - 1.1.11-1
- new upstream release

* Wed Aug 12 2009 David Hrbáč <david@hrbac.cz> - 1.1.6-1
- Initial build.
