Summary: mod_auth_mellon is a SAML 2.0 authentication module for apache
Name: mod_auth_mellon
Version: 0.0.7
Release: 1%{?dist}
Epoch: 1
Group: System Environment/Daemons
Source0: http://modmellon.googlecode.com/files/%{name}-%{version}.tar.gz
Source1: auth_mellon.conf
License: GPL v2
BuildRoot: %{_tmppath}/%{name}-root
BuildPrereq: httpd-devel, lasso-devel, curl-devel, openssl-devel, xmlsec1-devel
Requires: httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel), lasso >= 2.1, openssl

%description
mod_auth_mellon is a authentication module for apache. It authenticates
the user against a SAML 2.0 IdP, and and grants access to directories
depending on attributes received from the IdP.

%prep
%setup -q -n %{name}-%{version}

%build

%configure --with-apxs2=%{_sbindir}/apxs

make

%install
rm -rf %{buildroot}

# install apache module
mkdir -p %{buildroot}%{_libdir}/httpd/modules
install -m 755 .libs/%{name}.so %{buildroot}%{_libdir}/httpd/modules

# install the config file
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README TODO
%{_libdir}/httpd/modules/*.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf

%changelog
* Thu Sep 25 2008 David Hrbáč <david@hrbac.cz> - 0.0.7-1
- initial rebuild

* Mon Aug 18 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 0.0.7-1%{dist}
- Updated to 0.0.7
- Rebuilt on CentOS 5

* Fri Nov 16 2007 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 0.0.6-1%{dist}
- First 0.0.6
- Built on CentOS 5
