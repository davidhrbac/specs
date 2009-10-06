Name:           mod_layout
Version:        5.1
Release:        1.%{?dist}
Summary:        Add custom header and/or footers for apache

Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://tangent.org/362/mod_layout.html
Source0:        http://download.tangent.org/%{name}-%{version}.tar.gz
Source1:        mod_layout.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel


%description
Mod_Layout creates a framework for doing design. Whether you need a simple
copyright or ad banner attached to every page, or need to have something more
challenging such a custom look and feel for a site that employs an array of
technologies (Java Servlets, mod_perl, PHP, CGI's, static HTML, etc...),
Mod_Layout creates a framework for such an environment. By allowing you to
cache static components and build sites in pieces, it gives you the tools for
creating large custom portal sites.


%prep
%setup -q


%build
%{_sbindir}/apxs -c mod_layout.c utility.c layout.c


%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/httpd/modules
install -d %{buildroot}%{_sysconfdir}/httpd/conf.d

install -D -m755 .libs/mod_layout.so %{buildroot}/%{_libdir}/httpd/modules/mod_layout.so
install -D -m644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/mod_layout.conf

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE README
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_layout.conf
%{_libdir}/httpd/modules/mod_layout.so


%changelog
* Tue Oct 06 2009 David Hrbáč <david@hrbac.cz> - 5.1-1
- rebuild

* Sat Jul 25 2009 Lucian <lucian@evenstar.lastdot.org> 5.1-1
- Initial build
