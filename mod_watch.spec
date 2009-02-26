Summary:	Apache module: Monitoring Interface for MRTG.
Name:		mod_watch 
Version:	4.03
Release:	5%{?dist}
Group:		System Environment/Daemons
#Source:         %{name}-4.3.tar.gz
Source:         %{name}-%{version}.tar.gz
Source1:	%{name}.conf
Patch0:		mod_watch-apache220.patch
License:	BSD
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	httpd-devel >= 2.0.52
Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel)
Requires:       httpd >= %(rpm -q httpd --qf "%%{version}-%%{release}\n")

%description
This module will watch and collect the bytes, requests, and documents
in & out per virtual host, file owner, remote IP address, directory or
location, and the web server as a whole. This module was designed for
use with MRTG, which will make nice graphical representations of the
data, but is general enough that it can be applied to other purposes,
as the raw data is accessed by a URL. This module supports
mod_vhost_alias and mod_gzip.

%prep
#%setup -q -n %{name}-4.3_apache22_mod
%setup -q -n %{name}-4.3 
%{?build_centos5:%patch0 -p0}

%build
#apxs -c %{name}.c
#configure 

make -f Makefile.dso build APXS=/usr/sbin/apxs

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/httpd/modules

install -m0755 .libs/*.so %{buildroot}%{_libdir}/httpd/modules

# Install the config file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf
#%attr(0755,root,root) %{_libdir}/httpd/modules/%{name}.so
%attr(0755,root,root) %{_libdir}/httpd/modules/*.so

%changelog
* Tue Feb 17 2009 David Hrbáč <david@hrbac.cz> - 4.03-5
- added missing watch-table handler to conf
 
* Thu Nov  4 2008 David Hrbáč <david@hrbac.cz> - 4.03-4
-  patch to build with apache 2.2

* Sat Sep 20 2008 David Hrbáč <david@hrbac.cz> - 4.03-3
- added missing modules

* Sat Sep 20 2008 David Hrbáč <david@hrbac.cz> - 4.03-2
- rebuild

* Sat Sep 20 2008 David Hrbáč <david@hrbac.cz> - 4.03-1
- initial build
