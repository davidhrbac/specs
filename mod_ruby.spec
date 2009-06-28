Summary:	Mod_ruby is a DSO module for the Apache Web server.
Name:		mod_ruby 
Version:	1.3.0
Release:	1%{?dist}
Group:		System Environment/Daemons
URL:		http://www.modruby.net/
Source:         http://www.modruby.net/archive/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
License:	BSD
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	httpd-devel >= 2.0.52 ruby ruby-devel
Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel)
Requires:       httpd >= %(rpm -q httpd --qf "%%{version}-%%{release}\n")

%description
mod_ruby embeds the Ruby interpreter into the Apache web server,
allowing Ruby CGI scripts to be executed natively. These scripts
will start up much faster than without mod_ruby.

%prep
#%setup -q -n %{name}-4.3_apache22_mod
%setup -q 
#n %{name}-4.3 
%build
#apxs -c %{name}.c
#configure 
%{?build_centos4:./configure.rb --with-apxs=%{_sbindir}/apxs}
%{?build_centos5:./configure.rb --with-apxs=%{_sbindir}/apxs --with-apr-includes=/usr/include/apr-1}

make 
#-f Makefile.dso build APXS=/usr/sbin/apxs

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/httpd/modules

install -m0755 *.so %{buildroot}%{_libdir}/httpd/modules

# Install the config file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog README.en
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf
%attr(0755,root,root) %{_libdir}/httpd/modules/*.so

%changelog
* Sun Jun 28 2009 David Hrbáč <david@hrbac.cz> - 1.3.0-1
- new upstream version

* Mon Oct 13 2008 David Hrbáč <david@hrbac.cz> - 1.2.6-1
- initial build
