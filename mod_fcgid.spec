# FC5, RHEL5 and later include SELinux policy module packages
%if 0%{?fedora}%{?rhel} < 5
%define selinux_module 0
%define selinux_variants %{nil}
%define selinux_buildreqs %{nil}
%else
%define selinux_module 1
%define selinux_variants mls strict targeted
%define selinux_buildreqs checkpolicy, selinux-policy-devel, hardlink
%endif

Name:		mod_fcgid
Version:	2.2
Release:	4%{?dist}
Summary:	Apache2 module for high-performance server-side scripting 
Group:		System Environment/Daemons
License:	GPL+
URL:		http://fastcgi.coremail.cn/
Source0:	http://downloads.sf.net/mod-fcgid/mod_fcgid.%{version}.tar.gz
Source1:	fcgid.conf
Source2:	fastcgi.te
Source3:	fastcgi.fc
Source4:	mod_fcgid-2.1-README.RPM
Source5:	http://fastcgi.coremail.cn/doc.htm
Source6:	http://fastcgi.coremail.cn/configuration.htm
Source7:	mod_fcgid-2.1-README.SELinux
Source8:	fastcgi-2.5.te
Patch0:		mod_fcgid.2.1-docurls.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	gawk, httpd-devel >= 2.0, pkgconfig
Requires:	httpd-mmn = %([ -a %{_includedir}/httpd/.mmn ] && %{__cat} %{_includedir}/httpd/.mmn || echo missing)

%description
mod_fcgid is a binary-compatible alternative to the Apache module mod_fastcgi.
mod_fcgid has a new process management strategy, which concentrates on reducing
the number of fastcgi servers, and kicking out corrupt fastcgi servers as soon
as possible.

%if %{selinux_module}
%define selinux_policyver %(%{__sed} -e 's,.*selinux-policy-\\([^/]*\\)/.*,\\1,' /usr/share/selinux/devel/policyhelp)
%define selinux_policynum %(echo %{selinux_policyver} | %{__awk} -F. '{ printf "%d%02d%02d", $1, $2, $3 }')
%package selinux
Summary:	  SELinux policy module supporting FastCGI applications with mod_fcgid
Group:		  System Environment/Base
BuildRequires:	  %{selinux_buildreqs}
# selinux-policy is required for directory ownership of %{_datadir}/selinux/*
# Modules built against one version of a policy may not work with older policy
# versions, as noted on fedora-selinux-list:
# http://www.redhat.com/archives/fedora-selinux-list/2006-May/msg00102.html
# Hence the versioned dependency. The versioning will hopefully be replaced by
# an ABI version requirement or something similar in the future
%if "%{selinux_policyver}" != ""
Requires:	  selinux-policy >= %{selinux_policyver}
%endif
Requires:	  %{name} = %{version}-%{release}
Requires(post):	  /usr/sbin/semodule, /sbin/restorecon
Requires(postun): /usr/sbin/semodule, /sbin/restorecon

%description selinux
SELinux policy module supporting FastCGI applications with mod_fcgid.
%endif

%prep
%setup -q -n mod_fcgid.%{version}
%{__cp} -p %{SOURCE1} fcgid.conf
%if 0%{?selinux_policynum} < 20501
%{__cp} -p %{SOURCE2} fastcgi.te
%else
%{__cp} -p %{SOURCE8} fastcgi.te
%endif
%{__cp} -p %{SOURCE3} fastcgi.fc
%{__cp} -p %{SOURCE4} README.RPM
%{__cp} -p %{SOURCE5} directives.htm
%{__cp} -p %{SOURCE6} configuration.htm
%{__cp} -p %{SOURCE7} README.SELinux
%patch0 -p1
%{__sed} -i -e 's/\r$//' directives.htm configuration.htm
/usr/bin/iconv -f gb2312 -t utf8 < configuration.htm > configuration.htm.utf8
%{__mv} -f configuration.htm.utf8 configuration.htm

%build
topdir=$(/usr/bin/dirname $(/usr/sbin/apxs -q exp_installbuilddir))
%{__make} top_dir=${topdir}
%if %{selinux_module}
for selinuxvariant in %{selinux_variants}
do
	%{__make} NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
	%{__mv} fastcgi.pp fastcgi.pp.${selinuxvariant}
	%{__make} NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
%endif

%install
%{__rm} -rf %{buildroot}
topdir=$(/usr/bin/dirname $(/usr/sbin/apxs -q exp_installbuilddir))
%{__make} \
	top_dir=${topdir} \
	DESTDIR=%{buildroot} \
	MKINSTALLDIRS="%{__mkdir_p}" \
	install
%{__install} -D -m 644 fcgid.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/fcgid.conf
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/run/mod_fcgid

# Install SELinux policy modules
%if %{selinux_module}
for selinuxvariant in %{selinux_variants}
do
	%{__install} -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
	%{__install} -p -m 644 fastcgi.pp.${selinuxvariant} \
		%{buildroot}%{_datadir}/selinux/${selinuxvariant}/fastcgi.pp
done
# Hardlink identical policy module packages together
/usr/sbin/hardlink -cv %{buildroot}%{_datadir}/selinux
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{selinux_module}
%post selinux
# Install SELinux policy modules
for selinuxvariant in %{selinux_variants}
do
	/usr/sbin/semodule -s ${selinuxvariant} -i \
		%{_datadir}/selinux/${selinuxvariant}/fastcgi.pp &> /dev/null || :
done
# Fix up non-standard directory context
/sbin/restorecon -R %{_localstatedir}/run/mod_fcgid || :

%postun selinux
# Clean up after package removal
if [ $1 -eq 0 ]; then
	# Remove SELinux policy modules
	for selinuxvariant in %{selinux_variants}; do
		/usr/sbin/semodule -s ${selinuxvariant} -r fastcgi &> /dev/null || :
	done
	# Clean up any remaining file contexts (shouldn't be any really)
	[ -d %{_localstatedir}/run/mod_fcgid ] && \
		/sbin/restorecon -R %{_localstatedir}/run/mod_fcgid &> /dev/null || :
fi
exit 0
%endif

%files
%defattr(-,root,root,-)
%doc ChangeLog AUTHOR COPYING configuration.htm directives.htm
%doc README.RPM
%{_libdir}/httpd/modules/mod_fcgid.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/fcgid.conf
%dir %attr(0755,apache,apache) %{_localstatedir}/run/mod_fcgid/

%if %{selinux_module}
%files selinux
%defattr(-,root,root,-)
%doc fastcgi.fc fastcgi.te README.SELinux
%{_datadir}/selinux/*/fastcgi.pp
%endif

%changelog
* Wed Sep 17 2008 David Hrbáč <david@hrbac.cz> - 2.2-4
- initial rebuild

* Thu Feb 14 2008 Paul Howarth <paul@city-fan.org> 2.2-4
- Rebuild with gcc 4.3.0 for Fedora 9

* Mon Jan 14 2008 Paul Howarth <paul@city-fan.org> 2.2-3
- Update SELinux policy to fix occasional failures on restarts
  (move shared memory file into /var/run/mod_fcgid directory)

* Thu Jan  3 2008 Paul Howarth <paul@city-fan.org> 2.2-2
- Update SELinux policy to support file transition to httpd_tmp_t for
  temporary files

* Fri Sep 14 2007 Paul Howarth <paul@city-fan.org> 2.2-1
- Update to version 2.2
- Make sure docs are encoded as UTF-8

* Mon Sep  3 2007 Joe Orton <jorton@redhat.com> 2.1-6
- rebuild for fixed 32-bit APR (#254241)

* Thu Aug 23 2007 Paul Howarth <paul@city-fan.org> 2.1-5
- Update source URL to point to downloads.sf.net rather than dl.sf.net
- Upstream released new tarball without changing version number, though the
  only change was in arch/win32/fcgid_pm_win.c, which is not used to build the
  RPM package
- Clarify license as GPL (unspecified/any version)
- Unexpand tabs in spec
- Add buildreq of gawk

* Fri Aug  3 2007 Paul Howarth <paul@city-fan.org> 2.1-4
- Add buildreq of pkgconfig, a missing dependency of both apr-devel and
  apr-util-devel on FC5

* Fri Jun 15 2007 Paul Howarth <paul@city-fan.org> 2.1-3
- Major update of SELinux policy, supporting accessing data on NFS/CIFS shares
  and a new boolean, httpd_fastcgi_can_sendmail, to allow connections to SMTP
  servers
- Fix for SELinux policy on Fedora 7, which didn't work due to changes in the
  permissions macros in the underlying selinux-policy package

* Wed Mar 21 2007 Paul Howarth <paul@city-fan.org> 2.1-2
- Add RHEL5 with SELinux support
- Rename README.Fedora to README.RPM

* Fri Feb 16 2007 Paul Howarth <paul@city-fan.org> 2.1-1
- Update to 2.1
- Update documentation and patches
- Rename some source files to reduce chances of conflicting names
- Include SharememPath directive in conf file to avoid unfortunate upstream
  default location

* Mon Oct 30 2006 Paul Howarth <paul@city-fan.org> 2.0-1
- Update to 2.0
- Source is now hosted at sourceforge.net
- Update docs

* Wed Sep  6 2006 Paul Howarth <paul@city-fan.org> 1.10-7
- Include the right README* files

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 1.10-6
- Buildreqs for FC5 now identical to buildreqs for FC6 onwards

* Fri Jul 28 2006 Paul Howarth <paul@city-fan.org> 1.10-5
- Split off SELinux module into separate subpackage to avoid dependency on
  the selinux-policy package for the main package

* Fri Jul 28 2006 Paul Howarth <paul@city-fan.org> 1.10-4
- SELinux policy packages moved from %%{_datadir}/selinux/packages/POLICYNAME
  to %%{_datadir}/selinux/POLICYNAME
- hardlink identical policy module packages together to avoid duplicate files

* Thu Jul 20 2006 Paul Howarth <paul@city-fan.org> 1.10-3
- Adjust buildreqs for FC6 onwards
- Figure out where top_dir is dynamically since the /etc/httpd/build
  symlink is gone in FC6

* Wed Jul  5 2006 Paul Howarth <paul@city-fan.org> 1.10-2
- SELinux policy update: allow FastCGI apps to do DNS lookups

* Tue Jul  4 2006 Paul Howarth <paul@city-fan.org> 1.10-1
- Update to 1.10
- Expand tabs to shut rpmlint up

* Tue Jul  4 2006 Paul Howarth <paul@city-fan.org> 1.09-10
- SELinux policy update:
  * allow httpd to read httpd_fastcgi_content_t without having the
  | httpd_builtin_scripting boolean set
  * allow httpd_fastcgi_script_t to read /etc/resolv.conf without
  | having the httpd_can_network_connect boolean set

* Sun Jun 18 2006 Paul Howarth <paul@city-fan.org> 1.09-9
- Discard output of semodule in %%postun
- Include some documentation from upstream

* Fri Jun  9 2006 Paul Howarth <paul@city-fan.org> 1.09-8
- Change default context type for socket directory from var_run_t to
  httpd_fastcgi_sock_t for better separation

* Thu Jun  8 2006 Paul Howarth <paul@city-fan.org> 1.09-7
- Add SELinux policy module and README.Fedora
- Conflict with selinux-policy versions older than what we're built on

* Mon May 15 2006 Paul Howarth <paul@city-fan.org> 1.09-6
- Instead of conflicting with mod_fastcgi, don't add the handler for .fcg etc.
  if mod_fastcgi is present

* Fri May 12 2006 Paul Howarth <paul@city-fan.org> 1.09-5
- Use correct handler name in fcgid.conf
- Conflict with mod_fastcgi
- Create directory %%{_localstatedir}/run/mod_fcgid for sockets

* Thu May 11 2006 Paul Howarth <paul@city-fan.org> 1.09-4
- Cosmetic tweaks (personal preferences)
- Don't include INSTALL.TXT, nothing of use to end users

* Wed May 10 2006 Thomas Antony <thomas@antony.eu> 1.09-3
- Initial release
