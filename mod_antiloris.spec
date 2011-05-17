Summary: Protect apache against the slowloris attack.
Name: mod_antiloris
Version: 0.4
Release: 1%{dist}
Group: System Environment/Daemons
URL: ftp://ftp.monshouwer.eu/pub/linux/mod_antiloris/
Source0: ftp://ftp.monshouwer.eu/pub/linux/mod_antiloris/mod_antiloris-%{version}.tar.bz2
Source1: README
Source2: antiloris.conf
License: Apache Licence 2.0
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildPrereq: httpd-devel >= 2.0.40-6
Requires: httpd >= 2.0.40

%description
With this module, apache is protected against the slowloris attack. The module limits the
number of threads in READ state on a per IP basis. 

%prep
%setup -q

%build
%{_sbindir}/apxs -c %{name}.c
mv .libs/%{name}.so .
%{__strip} -g %{name}.so

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -m755 %{name}.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules

# Install the config file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m 644 $RPM_SOURCE_DIR/antiloris.conf \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/
    
install %{SOURCE1} README
    
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README	
%doc ChangeLog
%attr(755,root,root)%{_libdir}/httpd/modules/*.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf


%changelog
* Tue May 17 2011 David Hrbáč <david@hrbac.cz> - 0.4-1
- new upstream release

* Sun Jun 28 2009 David Hrbáč <david@hrbac.cz> - 0.3-2
- a few spec file improvements

* Wed Jun 24 2009 Kees Monshouwer <km|monshouwer_com> 0.3-1
- Changed loglevel from error to warn.

* Wed Jun 24 2009 Kees Monshouwer <km|monshouwer_com> 0.2-1
- Added module version to signature.
- Code cleanup.

* Sun Jun 21 2008 Kees Monshouwer <km|monshouwer_com> 0.1-1
- Initial build.
