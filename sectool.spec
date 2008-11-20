Summary: A security audit system and intrusion detection system
Name: sectool
Version: 0.9.1
Release: 1%{?dist}
URL: https://hosted.fedoraproject.org/sectool/wiki/WikiStart
Source0: %{name}-%{version}.tar.bz2
Source1: sectool.log
License: GPLv2+
Group: Applications/System
Requires: gettext coreutils  libselinux
Requires: python2 rpm-python libselinux-python
BuildRequires: desktop-file-utils gettext intltool rpm-devel asciidoc libselinux-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%package gui
Summary: GUI for sectool - security audit system and intrusion detection system
License: GPLv2+
Group: Applications/System
Requires: sectool = %{version}-%{release}
Requires: pygtk2 usermode

%description
sectool is a security tool that can be used both as a security audit 
and intrusion detection system. It consists of set of tests, library 
and command line interface tool. Tests are sorted into groups and security 
levels. Admins can run certain tests, groups or whole security levels. 
The library and the tools are implemented in python and tests are 
language independent.

%description gui
sectool-gui provides a GTK-based graphical user interface to sectool.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
desktop-file-install --delete-original      \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  --vendor=fedora \
   $RPM_BUILD_ROOT%{_datadir}/applications/sectool.desktop

#logrotate
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/sectool
#adjust paths in sectool.conf
sed -i 's,DSC_DIR=\(.*\),DSC_DIR=%{_sysconfdir}/sectool/tests,' $RPM_BUILD_ROOT%{_sysconfdir}/sectool/sectool.conf
sed -i 's,TESTS_DIRS=\(.*\),TESTS_DIRS=%{_datadir}/sectool/tests,' $RPM_BUILD_ROOT%{_sysconfdir}/sectool/sectool.conf
sed -i 's,TDATA_DIR_BASE=\(.*\),TDATA_DIR_BASE=%{_localstatedir}/lib/sectool,' $RPM_BUILD_ROOT%{_sysconfdir}/sectool/sectool.conf
#adjust icons path in guiOutput.py
sed -i 's,__ico_path = \(.*\),__ico_path = "%{_datadir}/pixmaps/sectool/",' $RPM_BUILD_ROOT%{_datadir}/sectool/guiOutput.py
#this file is just for development
rm $RPM_BUILD_ROOT/%{_datadir}/sectool/scheduler/selftest.py

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING AUTHORS README doc/tests_documentation.html
%config(noreplace) %{_sysconfdir}/sectool/
%config(noreplace) %{_sysconfdir}/logrotate.d/sectool
%dir %{_localstatedir}/lib/sectool
%dir %{_datadir}/sectool
%{_sbindir}/sectool
#library with tests
%{_datadir}/sectool/scheduler
%{_datadir}/sectool/tests
# command line tool
%{_datadir}/sectool/actions.py*
%{_datadir}/sectool/__init__.py*
%{_datadir}/sectool/output.py*
%{_datadir}/sectool/mailoutput.py*
%{_datadir}/sectool/sectool.py*
%{_datadir}/sectool/tuierrors.py*
%{_mandir}/man8/sectool.8.gz


%files gui
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pam.d/sectool-gui
%config(noreplace) %{_sysconfdir}/security/console.apps/sectool-gui
%{_bindir}/sectool-gui
%{_datadir}/sectool/gui*.py*
%{_datadir}/sectool/sectool-gui.py*
%{_datadir}/pixmaps/sectool-gui.png
%{_datadir}/pixmaps/sectool-min.png
%{_datadir}/applications/fedora-sectool.desktop
%{_datadir}/pixmaps/sectool/*.png


%changelog
* Wed Nov 19 2008 David Hrbáč <david@hrbac.cz> - 0.9.1-1
- initial rebuild

* Wed Oct 22 2008 Peter Vrabec <pvrabec@redhat.com> - 0.9.1-1
- upgrade, bugfix release

* Thu Oct 09 2008 Peter Vrabec <pvrabec@redhat.com> - 0.9.0-1
- upgrade, see changelog for changes

* Sat Sep 06 2008 Peter Vrabec <pvrabec@redhat.com> - 0.8.6-2
- fix selinux DEPS, quick workaround

* Fri Sep 05 2008 Peter Vrabec <pvrabec@redhat.com> - 0.8.6-1
- upgrade, see changelog

* Thu Jul 03 2008 Peter Vrabec <pvrabec@redhat.com> - 0.8.0-1
- upgrade

* Fri Jun 06 2008 Peter Vrabec <pvrabec@redhat.com> - 0.7.6-1
- upgrade

* Mon May 26 2008 Peter Vrabec <pvrabec@redhat.com> - 0.7.5-1
- upgrade

* Wed May 21 2008 Peter Vrabec <pvrabec@redhat.com> - 0.7.4-1
- new upstream release, lots of fixes and improvements,
  see changelog

* Mon Apr 28 2008 Peter Vrabec <pvrabec@redhat.com> - 0.7.3-1
- new upstream release
- better test integration

* Fri Apr 25 2008 Peter Vrabec <pvrabec@redhat.com> - 0.7.2-1
- new upstream release
- Support overriding level configuration in ~/.sectoolrc
- Add saving level configuration in GUI:

* Mon Apr 21 2008 Peter Vrabec <pvrabec@redhat.com> - 0.7.1-1
- new upstream release

* Tue Apr 08 2008 Peter Vrabec <pvrabec@redhat.com> - 0.7.0-1
- new upstream release

* Mon Mar 31 2008 Maros Barabas <mbarabas@redhat.com> - 0.6.0-4
- improved killing system in gui

* Fri Mar 28 2008 Maros Barabas <mbarabas@redhat.com> - 0.6.0-3
- code review: cleaning code in OuputFormatter
               adding comments
               migrating public formatter  methods to private

* Tue Mar 25 2008 Maros Barabas <mbarabas@redhat.com> - 0.6.0-2
- repaired sensitivity of popup buttons 
- code review: migrating public methods to private
               more comments

* Fri Mar 21 2008 Peter Vrabec <pvrabec@redhat.com> - 0.6.0-1
- gui improvements
- new feature include/exclude tests
- new sectool.conf

* Mon Mar 18 2008 Jakub Hrozek <jhrozek@redhat.com> - 0.5.1-1
- Fix mail output

* Wed Mar 05 2008 Peter Vrabec <pvrabec@redhat.com> - 0.5.0-1
- email sending support

* Wed Mar 05 2008 Peter Vrabec <pvrabec@redhat.com> - 0.4.0-1
- new tests
- bugfixes
- support diff results
- improved GUI

* Wed Jan 23 2008 Peter Vrabec <pvrabec@redhat.com> - 0.2.0-1
- stable demo release

* Fri Jan 18 2008 Peter Vrabec <pvrabec@redhat.com> - 0.1.0-4
- fix rpmbuild on fc8

* Wed Jan 16 2008 Peter Vrabec <pvrabec@redhat.com> - 0.1.0-3
- fix license issues 
- some macros clean up in makefile and spec

* Wed Jan 16 2008 Peter Vrabec <pvrabec@redhat.com> - 0.1.0-2
- make rpmlint happy, very important cleanup

* Tue Jan 15 2008 Peter Vrabec <pvrabec@redhat.com> - 0.1.0-1
- initial packaging
