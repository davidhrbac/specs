Name:           mod_cband
Version:        0.9.7.5
Release:        1%{?dist}
Summary:        Bandwidth limiting for virtual hosts
Group:          System Environment/Daemons
License:        GPL
URL:            http://cband.linux.pl/
Source0:        http://cband.linux.pl/download/mod-cband-%{version}.tgz
Source1:        mod_cband.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  httpd-devel
Requires:   	httpd httpd-mmn = %([ -a %{_includedir}/httpd/.mmn ] && cat %{_includedir}/httpd/.mmn || echo missing)    

%description
mod_cband is an Apache 2 module provided to solve the problem of limiting
virtualhosts bandwidth usage. When the configured virtualhost's transfer limit
is exceeded, mod_cband will redirect all further requests to a location
specified in the configuration file.


%prep
%setup -q -n mod-cband-%{version}


%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
install -D -m755 src/.libs/mod_cband.so %{buildroot}/%{_libdir}/httpd/modules/mod_cband.so
install -D -m644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/mod_cband.conf

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS Changes INSTALL LICENSE conf *.copyright
%{_libdir}/httpd/modules/mod_cband.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_cband.conf

%changelog
* Mon Mar 31 2008 David Hrbáč <david@hrbac.cz> 0.9.7.5-1
- CentOS rebuild

* Sun Nov 26 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 0.9.7.5-1
- New upstream release.

* Sun Sep 3 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 0.9.7.4-2
- Rebuild

* Mon May 29 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 0.9.7.4-1
- New upstream release

* Mon May 1 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 0.9.7.3-2
- New upstream release

* Thu Mar 17 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 0.9.7.2-3
- Config file set not to be replaced on upgrade
- Status information URI limited to localhost by default.

* Tue Mar 7 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 0.9.7.2-2
- Updated tarball from upstream (some very small changes in code,
  essentially in integer handling).
- Example config file added and installed in Apache's conf.d dir

* Sun Feb 5 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 0.9.7.2-1
- Fedora Extras review release.
