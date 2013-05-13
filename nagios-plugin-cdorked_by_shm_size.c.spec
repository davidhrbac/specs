Summary: Plugin to check the content of a shared memory blockused by Linux/Cdorked.
Name: nagios-plugin-cdorked_by_shm_size
Version: 0.1
Release: 1%{?dist}
License: GPL
Group: Applications/System
URL: https://github.com/kumina/nagios-plugins-kumina

Source: https://raw.github.com/kumina/nagios-plugins-kumina/master/check_cdorked_by_shm_size.c
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
This program dumps the content of a shared memory block
used by Linux/Cdorked.A into a file named httpd_cdorked_config.bin
when the machine is infected.

Some of the data is encrypted. If your server is infected and you
would like to help, please send the httpd_cdorked_config.bin
and your httpd executable to our lab for analysis. Thanks!

%prep

%build
gcc -o check_cdorked_by_shm_size  %{SOURCE0}
%install
%{__rm} -rf %{buildroot}

%{__install} -d -m0755 %{buildroot}%{_libdir}/nagios/plugins/contrib/
%{__install} -m0755 check_* %{buildroot}%{_libdir}/nagios/plugins/contrib/

### Clean up buildroot
%{__rm} -f %{buildroot}%{_libdir}/nagios/plugins/*.{c,o}
%{__rm} -f %{buildroot}%{_libdir}/nagios/plugins/contrib/*.orig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%dir %{_libdir}/nagios/plugins/contrib/
%{_libdir}/nagios/plugins/contrib/check_cdorked_by_shm_size

%changelog
* Mon May 13 2013 David Hrbáč <david@hrbac.cz> - 0.1-1
- initial build
