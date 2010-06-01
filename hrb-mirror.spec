Summary: Script to mirror hrb repositories
Name: hrb-mirror
Version: 0.1
Release: 1%{?dist}
License: GPL
Group: System Environment/Base
URL: http://www.hrbac.cz/repository.htm
BuildArch:  noarch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Script to mirror hrb repositories.

%prep

%{__cat} <<EOF >hrb.cron
#Script to mirror hrb repositories
#rsync --delete-delay --delay-updates --delete -a 158.196.128.251::hrb/ /var/www/html/hrb33/
rsync --delete-delay --delay-updates --delete -a repository.vsb.cz::hrb /var/www/html/hrb33/
EOF
%build
%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m0755 hrb.cron %{buildroot}%{_sysconfdir}/cron.hourly/hrb33
%clean
%{__rm} -rf %{buildroot}

%post

%files
%defattr(-, root, root, 0755)
%config %{_sysconfdir}/cron.hourly/hrb33

%changelog
* Thu Nov 12 2009 David Hrbáč <david@hrbac.cz> - 0.1-1
- Initial package. 
