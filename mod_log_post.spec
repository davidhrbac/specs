Summary:	Module for the Apache web server to log all HTTP POST messages
Name:		mod_log_post
Version:	0.1.0
Release:	1%{?dist}
Group:		System Environment/Daemons
License:	GPLv2 with exceptions
URL:		http://ftp.robert-scheck.de/linux/%{name}/
Source:		http://ftp.robert-scheck.de/linux/%{name}/%{name}-%{version}.tar.gz
BuildRequires:	httpd-devel >= 2.0.39
Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel)
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
mod_log_post can be used for logging all HTTP POST messages. The module
is based on mod_security but in difference it never returns any error
messages to the visitors of your websites. Logging of POST data can be
very useful for debugging purposes or analyses. As the module is loaded
and run after the SSL decryption, it even can log POST data transmitted
before via SSL to the Apache web server.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING LICENSING_EXCEPTION README
%{_libdir}/httpd/modules/%{name}.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/log_post.conf

%changelog
* Fri Oct 16 2009 David Hrbáč <david@hrbac.cz> - 0.1.0-1
- initial rebuild

* Fri May 22 2009 Robert Scheck <robert@fedoraproject.org> 0.1.0-1
- Upgrade to 0.1.0
- Initial spec file for Fedora and Red Hat Enterprise Linux
