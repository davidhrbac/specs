Summary:        Monitor the state of mirrors
Name:           mirmon
Version:        2.3
Release:        1%{?dist}
License:        BSD
Group:          Applications/Internet
URL:            http://people.cs.uu.nl/henkp/mirmon/
Source:         http://people.cs.uu.nl/henkp/mirmon/mirmon-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildArch:      noarch

%description
This packages contains a mirmon program - an utility to monitor the state of mirrors.

%prep
%setup -q

%{__cat} <<EOF >mirmon.conf
EOF

%{__cat} <<EOF >mirmon.cron
#*/05 * * * * root /bin/date +\%s > /var/www/html/TIME
*/15 * * * * root /usr/bin/mirmon -get all
EOF


%{__cat} <<EOF >mirmon.httpd
#
#  Web application to manage mirrors
#

Alias /mirmon /usr/share/mirmon

#<Directory "/usr/share/mirmon">
#  Order Deny,Allow
#  Deny from all
#  Allow from 127.0.0.1
#</Directory>
6EOF

%install
mkdir -p %buildroot{%_bindir,%_datadir/%name}
install -pm755 mirmon %buildroot%_bindir/
install -Dp -m0644 mirmon.cron %{buildroot}%{_sysconfdir}/cron.d/mirmon
install -Dp -m0644 mirmon.httpd %{buildroot}%{_sysconfdir}/httpd/conf.d/mirmon.conf
cp -a countries.list icons %buildroot%_datadir/%name/

%files
%defattr(-, root, root, 0755)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf
%config(noreplace) %{_sysconfdir}/cron.d/mirmon
%{_bindir}/*
%{_datadir}/%{name}
%doc *.txt

%changelog
* Wed Sep 01 2010 David Hrbáč <david@hrbac.cz> - 2.3-1
- initial release
