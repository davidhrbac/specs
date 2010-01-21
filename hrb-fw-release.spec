Summary: Repository hrb-fw release file and package configuration
Name: hrb-fw-release
Version: 0.1
Release: 3%{?dist} 
License: GPL
Group: System Environment/Base
URL: http://www.hrbac.cz/repository.htm

#Source0: mirrors-hrb-fw-mirrors

Source0: RPM-GPG-KEY-hrb.txt
#Source1: RPM-GPG-KEY-hrb.txt
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Release file for hrb-fw repository.

%prep

%{?el5:path="el5"}
%{?el4:path="el4"}
%{?el3:path="el3"}

%{__cat} <<EOF >hrb-fw.yum
# Name: hrb-fw repository 
# URL: http://www.hrbac.cz/repository.htm
[hrb-fw-stable]
name = hrb-fw
#baseurl = http://webmel4.vsb.cz/hrb33/el%centos_ver/hrb-fw/stable/%{_arch}/
mirrorlist = http://webmel4.vsb.cz/hrb33/mirrors-hrb-fw
enabled = 1
protect = 0
gpgkey = http://webmel4.vsb.cz/hrb33/RPM-GPG-KEY-hrb.txt
gpgcheck = 1

[hrb-fw-testing]
name = hrb-fw-test
#aseurl = http://webmel4.vsb.cz/hrb33/el%centos_ver/hrb-fw/testing/%{_arch}/
mirrorlist = http://webmel4.vsb.cz/hrb33/mirrors-testing-hrb-fw
enabled = 0
protect = 0
gpgkey = http://webmel4.vsb.cz/hrb33/RPM-GPG-KEY-hrb.txt
gpgcheck = 1
EOF

%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m0644 hrb-fw.yum %{buildroot}%{_sysconfdir}/yum.repos.d/hrb-fw.repo

%clean
%{__rm} -rf %{buildroot}

%post

%files
%defattr(-, root, root, 0755)
%dir %{_sysconfdir}/yum.repos.d/
%config(noreplace) %{_sysconfdir}/yum.repos.d/hrb-fw.repo

%changelog
* Thu Jan 21 2010 David Hrbáč <david@hrbac.cz> - 0.1-3
- fixed testing mirrorlist

* Wed May 27 2009 David Hrbáč <david@hrbac.cz> - 0.1-2
- new mirrors

* Wed Apr  9 2008 David Hrbáč <david@hrbac.cz> - 0.1-1
- Initial package. 
