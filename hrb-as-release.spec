Summary: Repository hrb-as release file and package configuration
Name: hrb-as-release
Version: 0.1
Release: 3%{?dist} 
License: GPL
Group: System Environment/Base
URL: http://www.hrbac.cz/repository.htm

#Source0: mirrors-hrb-as-mirrors

Source0: RPM-GPG-KEY-hrb.txt
#Source1: RPM-GPG-KEY-hrb.txt
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Release file for hrb-as repository.

%prep

%{?el6:path="el6"}
%{?el5:path="el5"}
%{?el4:path="el4"}
%{?el3:path="el3"}

%{__cat} <<EOF >hrb-as.yum
# Name: hrb-as repository 
# URL: http://www.hrbac.cz/repository.htm
[hrb-as-stable]
name = hrb-as
#baseurl = http://webmel53.vsb.cz/hrb33/el%centos_ver/hrb-as/stable/%{_arch}/
mirrorlist = http://webmel53.vsb.cz/hrb33/mirrors-hrb-as
enabled = 1
protect = 0
gpgkey = http://webmel53.vsb.cz/hrb33/RPM-GPG-KEY-hrb.txt
gpgcheck = 1

[hrb-as-testing]
name = hrb-as-test
#baseurl = http://webmel53.vsb.cz/hrb33/el%centos_ver/hrb-as/testing/%{_arch}/
mirrorlist = http://webmel53.vsb.cz/hrb33/mirrors-testing-hrb-as
enabled = 0
protect = 0
gpgkey = http://webmel53.vsb.cz/hrb33/RPM-GPG-KEY-hrb.txt
gpgcheck = 1
EOF

%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m0644 hrb-as.yum %{buildroot}%{_sysconfdir}/yum.repos.d/hrb-as.repo

%clean
%{__rm} -rf %{buildroot}

%post

%files
%defattr(-, root, root, 0755)
%dir %{_sysconfdir}/yum.repos.d/
%config(noreplace) %{_sysconfdir}/yum.repos.d/hrb-as.repo

%changelog
* Tue Oct 25 2011 David Hrbáč <david@hrbac.cz> - FIXME
- new mirrorlist server

* Thu Jan 21 2010 David Hrbáč <david@hrbac.cz> - 0.1-2
- fixed testing mirrorlist

* Fri Jun 26 2009 David Hrbáč <david@hrbac.cz> - 0.1-1
- Initial package. 
