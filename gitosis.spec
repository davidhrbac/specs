%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           gitosis
Version:        0.2
Release:        12.20090917git%{?dist}
Summary:        Git repository hosting application

Group:          Applications/System
License:        GPL+
URL:            http://eagain.net/gitweb/?p=gitosis.git;a=summary
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# $ git-clone --bare git://eagain.net/gitosis.git gitosis
# $ cd gitosis
# $ git-archive --format=tar --prefix=gitosis-0.2/ 44c7e7f0dca54f55fcc254d0344984fb8390098b | gzip > ../gitosis-0.2.tar.gz
Source0:        gitosis-%{version}.tar.gz
#Source1:        README.fedora
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires(pre):  shadow-utils
Requires:       python-setuptools
Requires:       openssh-clients
Requires:       git

%description
Gitosis aims to make hosting git repos easier and safer. It manages
multiple repositories under one user account, using SSH keys to identify
users. End users do not need shell accounts on the server, they will talk
to one shared account that will not let them run arbitrary commands.

%prep
%setup -q -n gitosis-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%{__install} -d -m 0755 %{buildroot}%{_localstatedir}/lib/gitosis
#cp %{SOURCE1} .
 
%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Add "gitosis" user per http://fedoraproject.org/wiki/Packaging/UsersAndGroups
getent group gitosis >/dev/null || groupadd -r gitosis
getent passwd gitosis >/dev/null || \
useradd -r -g gitosis -d %{_localstatedir}/lib/gitosis -s /bin/sh \
-c "git repository hosting" gitosis
exit 0

%files
%defattr(-,root,root,-)
#%doc COPYING example.conf README.fedora README.rst TODO.rst gitweb.conf
%doc COPYING example.conf README.rst TODO.rst gitweb.conf
%{_bindir}/gitosis-init
%{_bindir}/gitosis-run-hook
%{_bindir}/gitosis-serve
%{python_sitelib}/*
%dir %attr(0755,gitosis,gitosis) %{_localstatedir}/lib/gitosis

%changelog
* Mon Sep 26 2011 David Hrbáč <david@hrbac.cz> - 0.2-12.20090917git
- initial rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-11.20080825git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.2-10.20080825git
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-9.20080825git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-8.20080825git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2-7.20080825git
- Rebuild for Python 2.6

* Tue Sep  2 2008 John A. Khvatov <ivaxer@fedoraproject.org> 0.2-6.20080825git
- upstream update for compatibility with git 1.6.

* Wed Aug 13 2008 John A. Khvatov <ivaxer@gmail.com> 0.2-5.20080730git
- Changed license tag GPL+
- Wrote Source URL comment
- Moved README.fedora in Source1
- Fixed requires
- Added /var/lib/gitosis

* Thu Aug 7 2008 John A. Khvatov <ivaxer@gmail.com> 0.2-4.20080730git
- Created README.fedora
- Added creation 'gitosis' user

* Tue Aug 5 2008 John A. Khvatov <ivaxer@gmail.com> 0.2-1.20080730git
- Initial release

