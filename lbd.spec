Name:           lbd
Version:        0.1
Release:        2%{?dist}
Summary:        DNS/HTTP load balancing detector

Group:          Applications/Internet
License:        GPLv2
URL:            http://ge.mine.nu/lbd.html
Source0:        http://ge.mine.nu/code/lbd
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       bind-utils
Requires:       nc


%description
lbd (load balancing detector) detects if a given domain uses DNS and/or HTTP 
Load-Balancing (via Server: and Date: header and diffs between server answers)


%prep


%build


%install
rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE0} %{buildroot}%{_bindir}/


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/lbd


%changelog
* Sat Mar 13 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 0.1-2
- Replace generally useful macros by regular commands

* Tue Feb 02 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 0.1-1
- Initial package build

