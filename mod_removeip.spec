Summary:	mod_removeip - remove information about the remote IP
Name:		mod_removeip
Version:	1.0b
Release:	1%{?dist}
Group:		System Environment/Daemons
URL:		http://code.autistici.org/trac/privacy/browser/trunk/libapache-mod-removeip
Source:		%{name}.tar.gz
Source1:	%{name}.conf
License:	Apache Software License
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	httpd-devel >= 2.0.52
Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel)
Requires:       httpd >= %(rpm -q httpd --qf "%%{version}-%%{release}\n")

%description
This module throws away the information on the remote IP and hostname right at
the beginning of handling the request. That means its not logged, is not
available to any web apps, and can't leak into error logs and the like.
 	
This is written for use on servers with a strict policy on protecting the
identity of their users.  If the Spooks come and demand that you hand over your
server so they can try to identify one of your users, this should be enough that
you can categorically state that there is no IP info to be found, and might mean
your server doesn't go offline.

%prep
%setup -q -n %{name} 
perl -pi -e "s|apxs2|apxs|g" Makefile
%build
#apxs -c %{name}.c
#configure 

make removeip

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
%doc CHANGES README
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf
%attr(0755,root,root) %{_libdir}/httpd/modules/%{name}.so

%changelog
* Mon Sep 15 2008 David Hrbáč <david@hrbac.cz> - 1.0b-1
- initial build
