Summary:	Convert a CSV database to format suitable for GeoIP library
Name:		csv2bin
Version:	20041103
Release:	1%{?dist}
License:	GPLv2
Group:		Applications
Source0:	http://people.netfilter.org/peejix/geoip/tools/%{name}-%{version}.tar.gz
# Source0-md5:	b92bff0fc2adba02a48cfbb4b401205c
URL:		http://people.netfilter.org/peejix/GeoIP/tools/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
csv2bin is a tool specially written for the iptables/netfilter's GeoIP
match purpose. csv2bin's only task is to convert a
comma-seperated-value database containing all IPv4 subnets and their
associated countries to an understable binary format for the iptables'
GeoIP shared library.

You can create your own database (perhaps you feel sado) or simply
gets the latest GeoIP's free database from MaxMind.

%prep
%setup -q -n %{name}

%build
%{__make} 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/csv2bin

%define date	%(echo `LC_ALL="C" date +"%a %b %d %Y"`)
%changelog
* Thu Jul 16 2009 David Hrbáč <david@hrbac.cz> - 20041103-1
- initial rebuild
