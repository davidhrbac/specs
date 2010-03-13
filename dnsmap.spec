Name:           dnsmap
Version:        0.30
Release:        1%{?dist}
Summary:        Passive DNS network mapper a.k.a. subdomains bruteforcer

Group:          Applications/Internet
License:        GPLv2+
URL:            http://code.google.com/p/dnsmap/
Source0:        http://dnsmap.googlecode.com/files/dnsmap-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
dnsmap is mainly meant to be used by pentesters during the information 
gathering/enumeration phase of infrastructure security assessments
as subdomains bruteforcer tool which reads subdomains from built-in list
or wordlist file and saves output to txt/csv format.


%prep
%setup -q


%build
make %{?_smp_mflags} CFLAGS="%{optflags}"


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} BINDIR="%{_bindir}"


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc Changelog.txt CREDITS.txt README.txt TODO.txt gpl-2.0.txt use_cases.txt
%{_bindir}/dnsmap*


%changelog
* Sat Mar 13 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 0.30-1
- Update to 0.30
- Fix the license
- Remove dnsmap-0.25-Makefile.patch (included by the upstream)
- Replace generally useful macros by regular commands

* Tue Feb 02 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 0.25-1
- Initial package build
