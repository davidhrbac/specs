%define homedir %{_sysconfdir}/%{name}
%define cgibindir %{_datadir}/%{name}/cgi-bin
Summary: Distributed Checksum Clearinghouse
Name: dcc
Version: 1.3.92
Release: 1%{?dist}
License: GPL
Group: Applications/System
Source0: http://www.dcc-servers.net/dcc/source/dcc-%{version}.tar.Z
Patch0:       dcc.patch
Patch1:       dcc2.patch
URL: http://rhyolite.com/anti-spam/dcc/
BuildRoot: %{_tmppath}/%{name}-root
#BuildRequires: sendmail-devel

%description
The idea of the DCC is that if mail recipients could compare the mail they 
receive, they could recognize unsolicited bulk mail. A DCC server totals 
reports of checksums of messages from clients and answers queries about the 
total counts for checksums of mail messages. A DCC client reports the 
checksums for a mail message to a server and is told the total number of 
recipients of mail with each checksum. If one of the totals is higher than a 
threshold set by the client and according to local whitelists the message is 
unsolicited, the DCC client can log, discard, or reject the message.

%prep
%setup -q -n %{name}-%{version}
%patch -p0
%patch1 -p0

%build
./configure \
      --with-uid=root \
      --homedir=%{homedir} \
      --bindir=%{_bindir} \
      --libexecdir=%{_libexecdir}/%{name} \
      --mandir=%{_mandir} \
      --with-cgibin=%{cgibindir} \
      --with-installroot=%{buildroot} \
      --disable-sys-inst
      --disable-chown
make

%install
rm -rf %{buildroot}
make install \
  SET_BINOWN= SET_MANOWN= SET_DCCOWN=
perl -pi -e's,%{buildroot},,g' %{buildroot}%{homedir}/map.txt
mkdir -p %{buildroot}%{_mandir}/man8/
install *.8 %{buildroot}%{_mandir}/man8/

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc CHANGES FAQ.txt INSTALL.txt LICENSE *.html
%dir %{homedir}
%config(noreplace) %{homedir}/*
%{_bindir}/*
%attr(4555, root, root) %{_bindir}/cdcc
%attr(4555, root, root) %{_bindir}/dccproc
%{_libexecdir}/*
%attr(4555, root, root) %{_libexecdir}/%{name}/dccsight
%{cgibindir}/*
%{_mandir}/man8/*

%changelog
* Wed Sep 10 2008 David Hrbáč <david@hrbac.cz> - 1.3.92-1
- new upstream version

* Mon May 19 2008 David Hrbáč <david@hrbac.cz> - 1.3.90-1
- update to new version

* Wed Apr  2 2008 David Hrbáč <david@hrbac.cz> - 1.3.86-1
- CentOS rebuild

* Fri Apr 06 2007  Douglas E. Warner <silfreed@silfreed.net> 1.3.55-1
- update for 1.3.55

* Mon Aug  1 2005  Douglas E. Warner <silfreed@silfreed.net> 1.3.12-1
- update for 1.3.12

* Mon Apr 11 2005  Douglas E. Warner <silfreed@silfreed.net> 1.3.0-1
- update for 1.3.0

* Fri Jan 28 2005  Douglas E. Warner <silfreed@silfreed.net> 1.2.68-1
- update for 1.2.68

* Sat Apr 10 2004  Douglas E. Warner <dwarner@ctinetworks.com>
- Initial RPM release.

