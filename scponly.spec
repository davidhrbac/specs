Summary: Restricted shell for ssh based file services
Name: scponly
Version: 4.8
Release: 1%{?dist}
License: BSD
Group: Applications/Internet
URL: http://sublimation.org/scponly/
Source: http://mesh.dl.sourceforge.net/sourceforge/scponly/scponly-%{version}.tgz
Patch0: scponly-install.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

# Checks only for location of binaries
BuildRequires: openssh-clients >= 3.4
BuildRequires: openssh-server
BuildRequires: rsync

%description
scponly is an alternative 'shell' for system administrators 
who would like to provide access to remote users to both 
read and write local files without providing any remote 
execution priviledges. Functionally, it is best described 
as a wrapper to the "tried and true" ssh suite of applications. 

%prep
%setup -q
%patch0 -p1

%build
%configure --enable-scp-compat --enable-rsync-compat --enable-winscp-compat \
	--enable-chrooted-binary
%{__make} %{?_smp_mflags} \
	OPTS="%{optflags}"

# Remove executable bit so the debuginfo does not hae executable source files
chmod 0644 scponly.c scponly.h helper.c

%install
%{__rm} -rf %{buildroot}

# 
sed -i "s|%{_prefix}/local/|%{_prefix}/|g" scponly.8* INSTALL README
make install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files 
%defattr(0644, root, root, 0755)
%doc AUTHOR CHANGELOG CONTRIB COPYING INSTALL README TODO BUILDING-JAILS.TXT
%defattr(-, root, root, 0755)
%doc %{_mandir}/man8/scponly.8*
%{_bindir}/scponly
%{_sbindir}/scponlyc
%dir %{_sysconfdir}/scponly/
%config(noreplace) %{_sysconfdir}/scponly/*

%changelog
* Fri Apr 11 2008 David Hrbáč <david@hrbac.cz> - 4.8-1
- Updated to release 4.8.

* Thu Apr 10 2008 David Hrbáč <david@hrbac.cz> - 4.6-7
- CentOS rebuild

* Tue Aug 21 2007 Warren Togami <wtogami@redhat.com> - 4.6-7
- rebuild

* Fri Sep 15 2006 Warren Togami <wtogami@redhat.com> - 4.6-6
- rebuild for FC6

* Tue Jun 27 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 4.6-5
- Add BR: openssh-server so sftp-server is present.
- Make source files nonexecutable so they are nonexecutable in debuginfo.
- Mark the scponly configuration files as %%config.

* Sun Jun 25 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 4.6-4
- --enable-chrooted-binary creates a binary that will operate in a chroot
  environment.  It does not manage creation and updating of a chroot jail.
  This is the user's responsibility.
- Patch the Makefile.in to support install as a non-root user.

* Sun Mar 19 2006 Warren Togami <wtogami@redhat.com> - 4.6-3
- --enable-winscp-compat seems necessary
- --enable-rsync-compat seems useful too 

* Fri Feb 17 2006 Warren Togami <wtogami@redhat.com> - 4.6-1
- 4.6
- --enable-scp-compat so scp works
  upstream seems broken and no longer enables by default
  WinSCP 2.0 compatibilty is not enabled in this build

* Mon Jan 02 2006 Warren Togami <wtogami@redhat.com> - 4.3-1
- security fixes
- Gentoo's patch for optreset which is not supplied by glibc

* Thu Nov 03 2005 Warren Togami <wtogami@redhat.com> - 4.1-6
- use macro in substitution

* Tue Nov 01 2005 Warren Togami <wtogami@redhat.com> - 4.1-5
- BSD license
- fix path to scponly binary in man and docs

* Mon Oct 31 2005 Warren Togami <wtogami@redhat.com> - 4.1-4
- fix doc permissions

* Fri Oct 28 2005 Warren Togami <wtogami@redhat.com> - 4.1-2
- various spec fixes (#171987)

* Fri Oct 28 2005 Warren Togami <wtogami@redhat.com> - 4.1-1
- Fedora

* Tue May 10 2005 Dag Wieers <dag@wwieers.com> - 4.1-1 - 3051+/dag
- Updated to release 4.1.

* Thu Mar 03 2005 Dag Wieers <dag@wwieers.com> - 4.0-1
- Initial package. (using DAR)
