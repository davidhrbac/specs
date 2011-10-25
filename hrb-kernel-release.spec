Summary: Repository hrb-kernel release file and package configuration
Name: hrb-kernel-release
Version: 0.1
Release: 4%{?dist} 
License: GPL
Group: System Environment/Base
URL: http://www.hrbac.cz/repository.htm

#Source0: mirrors-hrb-kernel-mirrors

Source0: RPM-GPG-KEY-hrb.txt
#Source1: RPM-GPG-KEY-hrb.txt
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Release file for hrb-kernel repository.

%prep

%{?el6:path="el6"}
%{?el5:path="el5"}
%{?el4:path="el4"}
%{?el3:path="el3"}

%{__cat} <<EOF >hrb-kernel.yum
# Name: hrb-kernel repository 
# URL: http://www.hrbac.cz/repository.htm
[hrb-kernel-stable]
name = hrb-kernel
#aseurl = http://webmel53.vsb.cz/hrb33/el%centos_ver/hrb-kernel/stable/%{_arch}/
mirrorlist = http://webmel53.vsb.cz/hrb33/mirrors-hrb-kernel
enabled = 1
protect = 0
gpgkey = http://webmel53.vsb.cz/hrb33/RPM-GPG-KEY-hrb.txt
gpgcheck = 1

[hrb-kernel-testing]
name = hrb-kernel-test
#baseurl = http://webmel53.vsb.cz/hrb33/el%centos_ver/hrb-kernel/testing/%{_arch}/
mirrorlist = http://webmel53.vsb.cz/hrb33/mirrors-testing-hrb-kernel
enabled = 0
protect = 0
gpgkey = http://webmel53.vsb.cz/hrb33/RPM-GPG-KEY-hrb.txt
gpgcheck = 1
EOF

%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m0644 hrb-kernel.yum %{buildroot}%{_sysconfdir}/yum.repos.d/hrb-kernel.repo

%clean
%{__rm} -rf %{buildroot}

%post

%files
%defattr(-, root, root, 0755)
%dir %{_sysconfdir}/yum.repos.d/
%config(noreplace) %{_sysconfdir}/yum.repos.d/hrb-kernel.repo

%changelog
* Tue Oct 25 2011 David Hrbáč <david@hrbac.cz> - 0.1-4
- new upstream release

* Thu Jan 21 2010 David Hrbáč <david@hrbac.cz> - 0.1-3
- fixed testing mirrorlist

* Wed May 27 2009 David Hrbáč <david@hrbac.cz> - 0.1-2
- new mirrors

* Sat Jan  3 2009 David Hrbáč <david@hrbac.cz> - 0.1-1
- Initial package. 
