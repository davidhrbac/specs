Summary: Script to change PHP.INI for php-[pecl,pear] packages.
Name: hrb-php
Version: 0.1
Release: 5%{?dist}
License: GPL
Group: System Environment/Base
URL: http://www.hrbac.cz/repository.htm
BuildArch:  noarch
Requires:   php-common
BuildRequires:  php-common
Source:     hrb-php.ini

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Script to change PHP.INI for php-[pecl,pear] packages.

%prep

%build

%install
%{__rm} -rf %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post
[ -f /etc/php.ini ] && sed -i -r "s/memory_limit = [0-9]+/memory_limit = 256/" /etc/php.ini

%files

%changelog
* Tue Oct 19 2010 David Hrbáč <david@hrbac.cz> - 0.1-4
- moved to post

* Tue Oct 19 2010 David Hrbáč <david@hrbac.cz> - 0.1-4
- corrected regular expression

* Tue Oct 19 2010 David Hrbáč <david@hrbac.cz> - 0.1-3
- small correction

* Tue Oct 19 2010 David Hrbáč <david@hrbac.cz> - 0.1-2
- added Requires

* Mon Oct 18 2010 David Hrbáč <david@hrbac.cz> - 0.1-1
- Initial package. 
