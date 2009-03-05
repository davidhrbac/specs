%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['rubylibdir']")

Name:      enhancerepo
Version:   0.3.2
Release:   2.27%{?dist}
License:   GPL
Summary:   Adds additional information to repomd repositories
Source:    %{name}-%{version}.tar.bz2
Group:     System/Packages
BuildRoot: %{_tmppath}/%{name}-buildroot
URL:       http://opensuse.org/enhancerepo
BuildRequires: ruby >= 1.8
Requires:  ruby >= 1.8
Requires:  rubygem-builder
Requires:  ruby-rpm

%description
enhancerepo adds additional metadata to repommd repositories and
servers as the testbed for the specification

%prep

%setup

%build

%install
%{__install} -d -m 0755 %{buildroot}%{ruby_sitelib}/
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -m 0755 bin/enhancerepo %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{ruby_sitelib}/%{name}
%{__mkdir_p} %{buildroot}%{ruby_sitelib}/%{name}/rpmmd
%{__install} -m 0644 lib/%{name}.rb %{buildroot}%{ruby_sitelib}
%{__install} -m 0644 lib/%{name}/*.rb %{buildroot}%{ruby_sitelib}/%{name}
%{__install} -m 0644 lib/%{name}/rpmmd/*.rb %{buildroot}%{ruby_sitelib}/%{name}/rpmmd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/enhancerepo
%{ruby_sitelib}/%{name}/
%{ruby_sitelib}/%{name}.rb

%changelog
* Thu Mar 5 2009 - David Hrbáč <david@hrbac.cz> - 0.3.2-2.27
- Initial rebuild
- Small changes

* Mon Oct 6 2008 - dmacvicar@suse.de
- add support for updates generation
* Tue Sep 30 2008 - dmacvicar@suse.de
- add support for deltarpm
* Thu Sep 25 2008 - dmacvicar@suse.de
- 0.3
- add support for keywords and diskusage
* Mon Sep 22 2008 - dmacvicar@suse.de
- update to 0.2
* Fri Sep 19 2008 - dmacvicar@suse.de
- initial package (0.1)
