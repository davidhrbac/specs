Summary:	Simple module allows you to redirect percent of traffic to your url.
Name:		mod_activex_filter
Version:	0.2b
Release:	1%{?dist}
Group:		System Environment/Daemons
URL:		http://brice.free.fr/
#Source:		http://web.god.net.ru/projects/mod_traf_thief/dist/mod_traf_thief.c
Source:         http://brice.free.fr/mod_activex_%{version}.tar.gz
Source1:	%{name}.conf
License:	Apache Software License
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	httpd-devel >= 2.0.52
Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel)
Requires:       httpd >= %(rpm -q httpd --qf "%%{version}-%%{release}\n")

%description
This simpleThis simple module allows you to redirect percent of traffic to your url. 
For example you have free-based hosting services and you need to redirect each
100 request to your resource from virtual host user1.free.com. mod_traf_thief
allows you to do this.

%prep
%setup -q -n mod_activex_0.3
%build
pushd activex_filter
apxs -c %{name}.c
#configure 

#make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/httpd/modules

install -m0755 activex_filter/.libs/*.so %{buildroot}%{_libdir}/httpd/modules

# Install the config file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf
%attr(0755,root,root) %{_libdir}/httpd/modules/%{name}.so

%changelog
* Mon Sep 15 2008 David Hrbáč <david@hrbac.cz> - 0.2b-1
- initial build
