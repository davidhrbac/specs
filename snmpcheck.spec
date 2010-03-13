Name:           snmpcheck
Version:        1.7
Release:        1%{?dist}
Summary:        An utility to get information via SNMP protocols

Group:          Applications/Internet
License:        GPL+
URL:            http://www.nothink.org/perl/snmpcheck/
Source0:        http://www.nothink.org/perl/snmpcheck/download/snmpcheck-%{version}.txt
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
snmpcheck supports the following enumerations:
   * Contact
   * Description
   * Devices
   * Domain
   * Hardware and storage informations
   * Hostname
   * IIS statistics
   * IP forwarding
   * Listening UDP ports
   * Location
   * Motd
   * Mountpoints
   * Network interfaces
   * Network services
   * Processes
   * Routing information
   * Software components (Windows programs or RPMs etc.)
   * System Uptime
   * TCP connections
   * Total Memory
   * Uptime
   * User accounts
   * Web server informations (IIS)


%prep


%build


%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_bindir}
%{__install} -p -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/%{name}


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}


%changelog
* Sat Feb 13 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 1.7-1
- Initial package build

