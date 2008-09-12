Summary:	Mod_chroot makes running Apache in a secure chroot environment easy
Name:		mod_spamhaus
Version:	0.5
Release:	1%{?dist}
Group:		System Environment/Daemons
URL:		http://sourceforge.net/projects/mod-spamhaus/
Source:		http://surfnet.dl.sourceforge.net/sourceforge/mod-spamhaus/%{name}05.tar.gz
Source1:	mod_chroot.conf
License:	Apache Software License
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	httpd-devel >= 2.0.52
#BuildRequires:  gnutls >= 1.2.0, gnutls-devel >= 2.1.0, gnutls-utils >= 2.1.0, apr-devel
Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel)
#Requires:       gnutls >= 2.1
#Requires:       gnutls >= 2.1, httpd >= 2.0.52
Requires:       httpd = %(rpm -q httpd --qf "%%{version}-%%{release}\n")

%description
mod_chroot makes running Apache in a secure chroot environment easy. You don't
need to create a special directory hierarchy containing /dev, /lib, /etc...

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

install -m0755 .libs/*.so %{buildroot}%{_libdir}/httpd/modules

# Install the config file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m 644 %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CAVEATS ChangeLog INSTALL LICENSE README README.Apache20
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf
%attr(0755,root,root) %{_libdir}/httpd/modules/mod_chroot.so

%changelog
* Tue Sep  9 2008 David Hrbáč <david@hrbac.cz> - 0.5-1
- initial build
