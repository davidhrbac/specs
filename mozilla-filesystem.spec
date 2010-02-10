Name:           mozilla-filesystem
Version:        1.9
Release:        5%{?dist}
Summary:        Mozilla filesytem layout
Group:          Applications/Internet
License:        MPLv1.1
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
This package provides some directories required by packages which use
Mozilla technologies such as NPAPI plugins or toolkit extensions.

%prep

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/{lib,%{_lib}}/mozilla/{plugins,extensions}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mozilla/extensions
mkdir -p $RPM_BUILD_ROOT/etc/skel/.mozilla/{plugins,extensions}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
/usr/lib*/mozilla
%{_datadir}/mozilla
/etc/skel/.mozilla

%changelog
* Wed Feb 10 2010 David Hrbáč <david@hrbac.cz> - 1.9-5
- CentOS rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.9-3
- fix license tag

* Wed Apr 30 2008 Christopher Aillon <caillon@redhat.com> 1.9-2
- Also own the */mozilla parent dirs

* Wed Apr 30 2008 Christopher Aillon <caillon@redhat.com> 1.9-1
- Initial RPM
