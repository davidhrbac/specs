Name:		clamav-unofficial-sigs
Version:	3.6
Release:	1%{?dist}
Summary:	update script for 3rd-party clamav signatures
Group:		Applications/System
License:	Own
URL:		http://www.inetmsg.com/pub/
Source0:	http://www.inetmsg.com/pub/clamav-unofficial-sigs-%{version}.tar.gz
Patch0:		clamav-unofficial-sigs-conf.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	gnupg, rsync, curl, clamd

%description
This package provides a script for updating the following sources of
3rd-party clamav signatures until freshclamav gains support for such
signatures.

The SaneSecurity/OITC signatures provide detection of phishing, spear
phishing, fake lottery, ecard malware, casino, fake jobs, fake loans,
419s, fake diplomas, porn, emailed malware and other general spam.

MSRBL signatures provide detection of image spam and general spam.

SecuriteInfo signatures provide various badware signatures,
securiteinfo.com honeypot signatures, honeynet.cz signatures
and French anti-spam signatures

MalwarePatrol provides detection of mail containing URLs to malware.

%prep
%setup -q
%patch0 -p0 -b .conf
#cp -p %{SOURCE0} ./pfloggrep.sh
#sed -i 's/log=\/var\/log\/mail/log=\/var\/log\/maillog/'  pfloggrep.sh

%build

%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
install -Dpm 755 %{name}.sh $RPM_BUILD_ROOT%{_bindir}/clamav-unofficial-sigs
install -Dpm 444 %{name}.8 $RPM_BUILD_ROOT%{_mandir}/man8/%{name}.8

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGELOG README INSTALL LICENSE
%{_bindir}/clamav-unofficial-sigs
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_mandir}/man8/*
%changelog
* Thu Nov 05 2009 David Hrbáč <david@hrbac.cz> - 3.6-1
- initial build

