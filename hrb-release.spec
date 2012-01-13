Summary: Repository hrb release file and package configuration
Name: hrb-release
Version: 0.1
Release: 7%{?dist}
License: GPL
Group: System Environment/Base
URL: http://www.hrbac.cz/repository.htm

#Source0: mirrors-hrb-mirrors

Source0: RPM-GPG-KEY-hrb.txt
#Source1: RPM-GPG-KEY-hrb.txt
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Release file for hrb repository.

%prep

%{?el6:path="el6"}
%{?el5:path="el5"}
%{?el4:path="el4"}
%{?el3:path="el3"}

%{__cat} <<EOF >hrb.yum
# Name: hrb repository 
# URL: http://www.hrbac.cz/repository.htm
[hrb-stable]
name = hrb
#baseurl = http://webmel53.vsb.cz/hrb33/el%centos_ver/hrb/stable/%{_arch}/
mirrorlist = http://webmel53.vsb.cz/hrb33/mirrors-hrb
enabled = 1
protect = 0
gpgkey = http://webmel53.vsb.cz/hrb33/RPM-GPG-KEY-hrb.txt
gpgcheck = 1

[hrb-testing]
name = hrb-test
#baseurl = http://webmel53.vsb.cz/hrb33/el%centos_ver/hrb/testing/%{_arch}/
mirrorlist = http://webmel53.vsb.cz/hrb33/mirrors-testing-hrb
enabled = 0
protect = 0
gpgkey = http://webmel53.vsb.cz/hrb33/RPM-GPG-KEY-hrb.txt
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
* Fri Jan 13 2012 David Hrbáč <david@hrbac.cz> - 0.1-7
- corrected description

* Tue Oct 25 2011 David Hrbáč <david@hrbac.cz> - 0.1-6
- new mirrorlist server

* Tue Aug 23 2011 David Hrbáč <david@hrbac.cz> - 0.1-5
- el6 repo added

* Thu Jan 21 2010 David Hrbáč <david@hrbac.cz> - 0.1-4
- fixed testing mirrorlist

* Wed May 27 2009 David Hrbáč <david@hrbac.cz> - 0.1-3
- new mirrors
 
* Thu Mar 20 2008 David Hrbáč <david@hrbac.cz> - 0.1-2
- URL update

* Wed Feb  6 2008 David Hrbáč <david@hrbac.cz> - 0.1-1
- Initial package. 
