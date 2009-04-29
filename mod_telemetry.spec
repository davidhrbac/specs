Name:           mod_telemetry
Version:        1.0
Release:        1%{?dist}
Summary:        Scoreboard Enhancements For Apache
Group:          System Environment/Daemons
License:        GPL 2.0
URL:            http://code.google.com/p/modtelemetry/
Source0:        http://modtelemetry.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:        %{name}.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  httpd-devel
Requires:       httpd >= 2.0.0

%description
mod_telemetry is a scoreboard replacement for apache that tracks page response times
across all requests, including a listing of top N ip addresses that access the server

%prep
%setup -q -n modtelemetry-%{version}

%build
#%{_sbindir}/apxs -c mod_telemetry.c
%{_sbindir}/apxs -Wc,"%{optflags}" -c mod_telemetry.c

%install
rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{_libdir}/httpd/modules
%{__install} -d %{buildroot}%{_sysconfdir}/httpd/conf.d
%{__install} -m 0755 -p .libs/%{name}.so %{buildroot}%{_libdir}/httpd/modules/
%{__install} -m 0644 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE TODO mod_telemetry.txt
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_telemetry.conf
%{_libdir}/httpd/modules/mod_telemetry.so

%changelog
* Mon Jul 14 2008 John Adams <jna@twiter.com> - 1.0
- initial packaging

