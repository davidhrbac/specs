Name:           mod_substitute
Version:        2.2.11
Release:        1%{?dist}
Summary:        An Apache 2.2 module for substituting content sed style
Group:          System Environment/Daemons
License:        Apache License 2.0
URL:            http://httpd.apache.org/docs/2.2/mod/mod_substitute.html
Source0:        mod_substitute.c
Source1:        mod_substitute.conf
BuildRoot:      %{_tmppath}/%{name}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  httpd-devel

%description
mod_substitute provides a mechanism to perform both regular expression and fixed string
substitutions on response bodies.

%prep

%build
cp %{SOURCE0} .
%{_sbindir}/apxs -c mod_substitute.c

%install
rm -rf $RPM_BUILD_ROOT
mkdir -pm 755 \
    $RPM_BUILD_ROOT%{_libdir}/httpd/modules \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -pm 755 .libs/mod_substitute.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_substitute.conf
%{_libdir}/httpd/modules/mod_substitute.so

%changelog
* Tue Oct 06 2009 David Hrbáč <david@hrbac.cz> - 2.2.11-1
- rebuild

* Sat Jul 25 2009 Lucian <lucian@evenstar.lastdot.org> 1.0
- Initial build for Centos
