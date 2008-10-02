Summary:	Apache module that filter ActiveX on a proxy
Name:		mod_activex_filter
Version:	0.2b
Release:	2%{?dist}
Group:		System Environment/Daemons
URL:		http://brice.free.fr/
#Source:		http://web.god.net.ru/projects/mod_traf_thief/dist/mod_traf_thief.c
Source:         http://brice.free.fr/mod_activex_%{version}.tar.gz
Source1:	%{name}.conf
Patch0:		mod_activex_0.2-apx1.diff
License:	Apache Software License
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	httpd-devel >= 2.0.52
Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel)
Requires:       httpd >= %(rpm -q httpd --qf "%%{version}-%%{release}\n")

%description
It's only a simple hack of mod_case_filter to get a way to filter
ActiveX on a proxy. Actualy, the only way to filter ActiveX if
your proxy is unable to do it is to use a TIS module chained with
your proxy. But the TIS is only capable of doing HTTP/1.0. If you
need real performances, you'll want to use HTTP/1.1.

%prep
%setup -q -n mod_activex_0.3
%{?build_centos5:%patch0 -p0}

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
* Thu Oct  2 2008 David Hrbáč <david@hrbac.cz> - 0.2b-2
-  patch to build with apache 2.2

* Mon Sep 15 2008 David Hrbáč <david@hrbac.cz> - 0.2b-1
- initial build
