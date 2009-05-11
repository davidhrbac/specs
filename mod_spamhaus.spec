Summary:	mod_spamhaus is an Apache module that uses DNSBL
Name:		mod_spamhaus
Version:	0.7
Release:	1%{?dist}
Group:		System Environment/Daemons
URL:		http://sourceforge.net/projects/mod-spamhaus/
Source:		http://surfnet.dl.sourceforge.net/sourceforge/mod-spamhaus/%{name}05.tar.gz
Source1:	%{name}.conf
License:	Apache Software License
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	httpd-devel >= 2.0.52
Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel)
Requires:       httpd >= %(rpm -q httpd --qf "%%{version}-%%{release}\n")

%description
mod_spamhaus is an Apache module that uses DNSBL in order to block spam relay
via web forms, preventing URL injection, block http DDoS attacks from bots and
generally protecting your web service denying access to a known bad IP address. 
It take advantage of the Spamhaus Block List (SBL) and the Exploits Block List
(XBL) querying xbl-sbl.spamhaus.org Spamhaus's DNSBLs are offered as a free
public service for low-volume non-commercial use. To check if you qualify for
free use, please see: Spamhaus DNSBL usage criteria
(http://www.spamhaus.org/organization/dnsblusage.html)

%prep
%setup -q -n mod-spamhaus 
perl -pi -e "s|apxs2|apxs|g" Makefile
%build
#apxs -c %{name}.c
#configure 

make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/httpd/modules

install -m0755 src/.libs/*.so %{buildroot}%{_libdir}/httpd/modules

# Install the config file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc LICENSE ReadMe.txt
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf
%attr(0755,root,root) %{_libdir}/httpd/modules/%{name}.so

%changelog
* Thu Apr 30 2009  David Hrbáč <david@hrbac.cz> - 0.7-1
- new upstream version

* Tue Sep  9 2008 David Hrbáč <david@hrbac.cz> - 0.5-1
- initial build
