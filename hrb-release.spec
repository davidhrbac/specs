Summary: Repository hrb release file and package configuration
Name: hrb-release
Version: 0.1
Release: 2%{?dist}
License: GPL
Group: System Environment/Base
URL: http://www.hrbac.cz/repository.htm

#Source0: mirrors-hrb-mirrors

Source0: RPM-GPG-KEY-hrb.txt
#Source1: RPM-GPG-KEY-hrb.txt
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Release file for hrb-tls repository.

%prep

%{?el5:path="el5"}
%{?el4:path="el4"}
%{?el3:path="el3"}

%{__cat} <<EOF >hrb.yum
# Name: hrb repository 
# URL: http://www.hrbac.cz/repository.htm
[hrb-stable]
name = hrb
baseurl = http://fs12.vsb.cz/hrb33/el%centos_ver/hrb/stable/%{_arch}/
#mirrorlist = 
enabled = 1
protect = 0
gpgkey = http://fs12.vsb.cz/hrb33/RPM-GPG-KEY-hrb.txt
gpgcheck = 1

[hrb-testing]
name = hrb-test
baseurl = http://fs12.vsb.cz/hrb33/el%centos_ver/hrb/testing/%{_arch}/
#mirrorlist =
enabled = 0
protect = 0
gpgkey = http://fs12.vsb.cz/hrb33/RPM-GPG-KEY-hrb.txt
gpgcheck = 1
EOF

%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m0644 hrb.yum %{buildroot}%{_sysconfdir}/yum.repos.d/hrb.repo

%clean
%{__rm} -rf %{buildroot}

%post

%files
%defattr(-, root, root, 0755)
%dir %{_sysconfdir}/yum.repos.d/
%config(noreplace) %{_sysconfdir}/yum.repos.d/hrb.repo

%changelog
* Thu Mar 20 2008 David Hrbáč <david@hrbac.cz> - 0.1-2
- URL update

* Wed Feb  6 2008 David Hrbáč <david@hrbac.cz> - 0.1-1
- Initial package. 
