Summary: Repository hrb-tls release file and package configuration
Name: hrb-tls-release
Version: 0.2
Release: 1%{?dist} 
License: GPL
Group: System Environment/Base
URL: http://repository.hrbac.cz

#Source0: mirrors-hrb-tls-mirrors

Source0: RPM-GPG-KEY-hrb.txt
#Source1: RPM-GPG-KEY-hrb.txt
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Release file for hrb-tls repository.

%prep

%{?el6:path="el6"}
%{?el5:path="el5"}
%{?el4:path="el4"}
%{?el3:path="el3"}

%{__cat} <<EOF >hrb-tls.yum
# Name: hrb-tls repository 
# URL: http://repository.hrbac.cz
[hrb-tls-stable]
name = hrb-tls
#baseurl = http://repository.hrbac.cz/mirrors/el%centos_ver/hrb-tls/stable/%{_arch}/
mirrorlist = http://repository.hrbac.cz/mirrors/mirrors-hrb-tls
enabled = 1
protect = 0
gpgkey = http://repository.hrbac.cz/mirrors/RPM-GPG-KEY-hrb.txt
gpgcheck = 1

[hrb-tls-testing]
name = hrb-tls-test
#baseurl = http://repository.hrbac.cz/mirrors/el%centos_ver/hrb-tls/testing/%{_arch}/
mirrorlist = http://repository.hrbac.cz/mirrors/mirrors-testing-hrb-tls
enabled = 0
protect = 0
gpgkey = http://repository.hrbac.cz/mirrors/RPM-GPG-KEY-hrb.txt
gpgcheck = 1
EOF

%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m0644 hrb-tls.yum %{buildroot}%{_sysconfdir}/yum.repos.d/hrb-tls.repo

%clean
%{__rm} -rf %{buildroot}

%post

%files
%defattr(-, root, root, 0755)
%dir %{_sysconfdir}/yum.repos.d/
%config(noreplace) %{_sysconfdir}/yum.repos.d/hrb-tls.repo

%changelog
* Fri Feb 01 2013 David Hrbáč <david@hrbac.cz> - 0.2-1
- moving to github site

* Tue Oct 25 2011 David Hrbáč <david@hrbac.cz> - 0.1-5
- new mirrorlist server

* Thu Jan 21 2010 David Hrbáč <david@hrbac.cz> - 0.1-4
- fixed testing mirrorlist

* Wed May 27 2009 David Hrbáč <david@hrbac.cz> - 0.1-3
- new mirrors

* Thu Mar 20 2008 David Hrbáč <david@hrbac.cz> - 0.1-2
- URL update

* Sat Dec  8 2007 David Hrbáč <david@hrbac.cz> - 0.1-1
- Initial package. 
