Name:           nmbscan
Version:        1.2.5
Release:        2%{?dist}
Summary:        NMB/SMB network scanner

Group:          Applications/Internet
License:        GPLv2+
URL:            http://nmbscan.gbarbier.org/
Source0:        http://nmbscan.gbarbier.org/down/nmbscan-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       samba-client


%description
Scans a SMB shares network, using NMB and SMB protocols. Useful to acquire
an information on a local area network (security audit, etc.)

Matches the information such as NMB/SMB/Windows hostname, IP address, IP
hostname, ethernet MAC address, Windows username, NMB/SMB/Windows domain name
and master browser.

Can discover all NMB/SMB/Windows hosts on a local area network thanks to 
hosts lists maintained by master browsers.


%prep
%setup -q -c %{name}-%{version}


%build


%install
rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
install -p -m 755 nmbscan %{buildroot}%{_bindir}/


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc Documentation/HOWTO_contribute.txt Documentation/gplv2.txt
%{_bindir}/nmbscan


%changelog
* Sat Mar 13 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 1.2.5-2
- Fix the license
- Fix the summary
- Replace generally useful macros by regular commands

* Thu Feb 04 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 1.2.5-1
- Initial package build

