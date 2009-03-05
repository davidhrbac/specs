Name:      enhancerepo
Version:   0.3.2
Release:   2.27
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
%{__install} -d -m 0755 %{buildroot}%{_libdir}/ruby/vendor_ruby/%{rb_ver}/
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -m 0755 bin/enhancerepo %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{_libdir}/ruby/vendor_ruby/%{rb_ver}/%{name}
%{__mkdir_p} %{buildroot}%{_libdir}/ruby/vendor_ruby/%{rb_ver}/%{name}/rpmmd
%{__install} -m 0644 lib/%{name}.rb %{buildroot}%{_libdir}/ruby/vendor_ruby/%{rb_ver}
%{__install} -m 0644 lib/%{name}/*.rb %{buildroot}%{_libdir}/ruby/vendor_ruby/%{rb_ver}/%{name}
%{__install} -m 0644 lib/%{name}/rpmmd/*.rb %{buildroot}%{_libdir}/ruby/vendor_ruby/%{rb_ver}/%{name}/rpmmd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/enhancerepo
%{_libdir}/ruby/vendor_ruby/%{rb_ver}/%{name}/
%{_libdir}/ruby/vendor_ruby/%{rb_ver}/%{name}.rb

%changelog
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
