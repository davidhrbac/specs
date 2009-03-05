Summary: Update notification daemon
Name: yum-updatesd
Epoch: 1
Version: 0.9
Release: 2%{?dist}
License: GPLv2
Group: System Environment/Base
Source0: %{name}-%{version}.tar.bz2
Patch0: yum-updatesd-updaterefresh.patch
URL: http://linux.duke.edu/yum/
BuildArch: noarch
BuildRequires: python
#Requires: python >= 2.4
Requires: python
Requires: yum >= 3.2.0
Requires: dbus-python
#Requires: pygobject2
Requires: gamin-python
Requires(preun): /sbin/chkconfig
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(post): /sbin/service
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
yum-updatesd provides a daemon which checks for available updates and 
can notify you when they are available via email, syslog or dbus. 

%prep
%setup -q

%patch0 -p1

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add yum-updatesd
/sbin/service yum-updatesd condrestart >/dev/null 2>&1
exit 0

%preun
if [ $1 = 0 ]; then
 /sbin/chkconfig --del yum-updatesd
 /sbin/service yum-updatesd stop >/dev/null 2>&1
fi
exit 0

%files
%defattr(-,root,root,-)
%doc COPYING
%{_sysconfdir}/rc.d/init.d/yum-updatesd
%config(noreplace) %{_sysconfdir}/yum/yum-updatesd.conf
%config %{_sysconfdir}/dbus-1/system.d/yum-updatesd.conf
%{_sbindir}/yum-updatesd
%{_libexecdir}/yum-updatesd-helper
%{_mandir}/man*/yum-updatesd*


%changelog
* Fri Jan 18 2008 James Antill <james.antill@redhat.com> - 1:0.9-1
- Import into RHEL-5
- Add updaterefresh match.
- Related: rhbz#384691

* Mon Dec 17 2007 Jeremy Katz <katzj@redhat.com> - 1:0.9-1
- More mail fixes (Pierre Ossman)

* Wed Dec  5 2007 Jeremy Katz <katzj@redhat.com> - 1:0.8-1
- Use sendmail (Pierre Ossman, #397711)
- Don't wake up as often (#391571)
- Improve mail output (Pierre Ossman, #387181)
- Fix some tracebacks (#387051, #374801)

* Fri Oct 12 2007 Jeremy Katz <katzj@redhat.com> - 1:0.7-1
- fix error when download is set, but no packages are available (#329361)

* Wed Oct 10 2007 Jeremy Katz <katzj@redhat.com> - 1:0.6-1
- add lsb initscript header (#247106)
- overly simplistic service start speed-up

* Wed Sep  5 2007 Jeremy Katz <katzj@redhat.com> - 1:0.5-1
- add option for configurable SMTP server
- fix email sending (Rich Fearn, #251196)
- make updates checking in the presence of NetworkManager smarter (#213732)
- ensure group info gets updated
- work with yum 3.0.x (jantill)
- don't poll gamin

* Tue Jul 24 2007 Jeremy Katz <katzj@redhat.com> - 1:0.4-1
- minor review fixes.  add --oneshot mode

* Mon Jul 23 2007 Jeremy Katz <katzj@redhat.com> - 1:0.3-1
- update to new version

* Thu Jul 19 2007 Jeremy Katz <katzj@redhat.com> - 1:0.1-1
- new package for standalone yum-updatesd
