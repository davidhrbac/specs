Summary:	Program for efficient remote updates of files
Name:		rsyncrypto
Version:	1.12
Release:	1%{?dist}
License:	GPLv2
Group:		Networking/Utilities
Source0:	http://sourceforge.net/projects/rsyncrypto/files/rsyncrypto/%{name}-%{version}.tar.gz
# Source0-md5:	b04df4561d5f9847b647f9c60912d2af
URL:		http://rsync.samba.org/
BuildRequires:	argtable2-devel
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	openssl-devel
Requires:	gzip(rsyncable)
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
rsync is a replacement for rcp that has many more features.

rsync uses the "rsync algorithm" which provides a very fast method for
bringing remote files into sync. It does this by sending just the
differences in the files across the link, without requiring that both
sets of files are present at one of the ends of the link beforehand.

A technical report describing the rsync algorithm is included with
this package.

%prep
%setup -q

%build
#cp -f /usr/share/automake/config.sub .
#%{__autoheader}
#%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Wed Jul 15 2009 David Hrbáč <david@hrbac.cz>  - 1.23-1
- initial rebuild

