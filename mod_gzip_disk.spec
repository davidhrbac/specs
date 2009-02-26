Summary:	Module that serves gzip compressed HTML from disk rather than compressing on the fly.
Name:		mod_gzip_disk
Version:	0.5
Release:	1%{?dist}
Group:		System Environment/Daemons
URL:		http://www.s5h.net/code/mod-gzip/
Source:         http://www.s5h.net/code/mod-gzip/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
License:	Apache Software License
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	httpd-devel >= 2.0.52
BuildRequires:  zlib-devel
Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel)
Requires:       httpd >= %(rpm -q httpd --qf "%%{version}-%%{release}\n")

%description
Mod_gzip_disk is an Apache module that serves gzip compressed HTML from disk rather
than compressing on the fly. If compression is not available, the decompressed file
is sent to the client.

%prep
%setup -q -n %{name} 
%build
apxs -c %{name}.c
#configure 

#make

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
%attr(0755,root,root) %{_libdir}/httpd/modules/%{name}.so

%changelog
* Wed Feb 18 2009 David Hrbáč <david@hrbac.cz> - 0.5-1
- new upstream version

* Mon Sep 15 2008 David Hrbáč <david@hrbac.cz> - 0.03-1
- initial build
