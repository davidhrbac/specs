Summary: Repository spc release file and package configuration
Name: spc-release
Version: 0.1
Release: 1%{?dist}
License: GPL
Group: System Environment/Base
URL: http://spc.vsb.cz/
BuildArch: noarch

#Source0: mirrors-spc-mirrors

Source0: RPM-GPG-KEY-hrb.txt
#Source1: RPM-GPG-KEY-spc.txt
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Release file for spc repository.

%prep

%{?el6:path="el6"}
%{?el5:path="el5"}
%{?el4:path="el4"}
%{?el3:path="el3"}

%{__cat} <<EOF >spc.yum
# Name: spc repository 
# URL: http://spc.vsb.cz/
[spc-stable]
name = spc
#baseurl = http://webmel53.vsb.cz/spc33/el%centos_ver/hrb/stable/%{_arch}/
baseurl = http://repository.vsb.cz/spc/ofed-1.5.3.1/%{_arch}/
#mirrorlist = http://webmel53.vsb.cz/spc33/mirrors-hrb
enabled = 1
protect = 0
gpgkey = http://webmel53.vsb.cz/hrb33/RPM-GPG-KEY-hrb.txt
gpgcheck = 1

#[spc-testing]
#name = spc-test
##baseurl = http://webmel53.vsb.cz/spc33/el%centos_ver/hrb/testing/%{_arch}/
##mirrorlist = http://webmel53.vsb.cz/spc33/mirrors-testing-hrb
#enabled = 0
#protect = 0
#gpgkey = http://webmel53.vsb.cz/spc33/RPM-GPG-KEY-hrb.txt
#gpgcheck = 1
#EOF

%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m0644 spc.yum %{buildroot}%{_sysconfdir}/yum.repos.d/spc.repo

%clean
%{__rm} -rf %{buildroot}

%post

%files
%defattr(-, root, root, 0755)
%dir %{_sysconfdir}/yum.repos.d/
%config(noreplace) %{_sysconfdir}/yum.repos.d/spc.repo

%changelog
* Fri Jan 13 2012 David Hrbáč <david@spcac.cz> - 0.1-1
- initial release
