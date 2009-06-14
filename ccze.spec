Summary:	A robust log colorizer
Name:		ccze
Version:	0.2.1
Release:	1%{?dist}
License:	GPL
Group:		Applications/Text
Source0:	ftp://bonehunter.rulez.org/pub/ccze/stable/%{name}-%{version}.tar.gz
# Source0-md5:	221966bce7c5f011eca38157241a0432
URL:		http://bonehunter.rulez.org/CCZE.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	pcre-devel >= 3.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-root-%(id -u -n)

%description
CCZE is a roboust and modular log colorizer, with plugins for apm,
exim, fetchmail, httpd, postfix, procmail, squid, syslog, ulogd,
vsftpd, xferlog and more.

%package devel
Summary:	Header file for CCZE plugins
Group:		Development/Libraries
Requires:	ncurses-devel >= 5.0
Requires:	pcre-devel >= 3.1

%description devel
Header file for CCZE plugins.


%prep
%setup -q

%build
%{__aclocal}
%{__autoheader}
%{__autoconf}
#CFLAGS="%{rpmcflags} -I/usr/include/ncurses"
%configure \
	--with-builtins=all

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

src/ccze-dump >$RPM_BUILD_ROOT%{_sysconfdir}/cczerc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog ChangeLog-0.1 NEWS README THANKS FAQ
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cczerc
%attr(755,root,root) %{_bindir}/ccze
%attr(755,root,root) %{_bindir}/ccze-cssdump
%{_mandir}/man1/ccze.1*
%{_mandir}/man1/ccze-cssdump.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/ccze.h
%{_mandir}/man7/ccze-plugin.7*

%changelog
* Wed Jun 10 2009 David Hrbáč <david@hrbac.cz> - 0.2.1-1
- initial build

