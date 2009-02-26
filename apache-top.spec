Name:           apache-top
Version:        1.0
Release:        1%{?dist}
Summary:        Real-time display processes from a remote apache server

Group:          Applications/Internet
License:        GPLv2+
URL:            http://www.fr3nd.net/projects/apache-top/
Source0:        http://www.fr3nd.net/stuff/projects/apache-top/apache-top.py
Source1:        apache-top.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
Requires:       httpd

%description
apache-top provides real-time display of the active processes from a remote
apache server. I’ts like the top linux command.


%prep


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/%{_bindir} %{buildroot}/%{_sysconfdir}/httpd/conf.d
install -m 0755 %{SOURCE0} %{buildroot}/%{_bindir}/%{name}
sed -i 's|url = None|url = "http://127.0.0.1/server-status"|' \
  %{buildroot}/%{_bindir}/%{name}
install -m 0644 %{SOURCE1} \
  %{buildroot}/%{_sysconfdir}/httpd/conf.d/%{name}.conf


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_bindir}/%{name}


%changelog
* Tue Jan 20 2009 David Hrbáč <david@hrbac.cz> - 1.0-1
- initial rebuild
 
* Wed Jan 23 2008 Jan ONDREJ (SAL) <ondrejj(at)salstar.sk> - 1.0-1
- default URL changed to localhost, enables to run script without parameters
