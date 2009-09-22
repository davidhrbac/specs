Summary:          389 Directory, Administration, and Console Suite
Name:             389-ds
Version:          1.1.3
Release:          5%{?dist}
License:          GPLv2
URL:              http://port389.org/
Group:            System Environment/Daemons
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
Provides:         fedora-ds = %{version}-%{release}
Obsoletes:        fedora-ds < 1.1.3-2

Source:           LICENSE

Requires:         389-ds-base
Requires:         389-admin
Requires:         idm-console-framework
Requires:         389-console
Requires:         389-ds-console
Requires:         389-ds-console-doc
Requires:         389-admin-console
Requires:         389-admin-console-doc
Requires:         389-dsgw

%description
The 389 Directory Server, Administration Server, and Console Suite provide
the LDAPv3 server, the httpd daemon used to administer the server, and the
console GUI application used for server and user/group administration.

%prep
cp %{SOURCE0} .

%build
# empty

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE

%changelog
* Wed Aug 12 2009 Rich Megginson <rmeggins@redhat.com> 1.1.3-5
- added doc subpackages

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Rich Megginson <rmeggins@redhat.com> 1.1.3-3
- added empty build section

* Mon May 18 2009 Rich Megginson <rmeggins@redhat.com> 1.1.3-2
- rename to 389

* Tue Mar 31 2009 Rich Megginson <rmeggins@redhat.com> 1.1.3-1
- this is the 1.1.3 release

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep  4 2008 Rich Megginson <rmeggins@redhat.com> 1.1.2-1
- this is the 1.1.2 release
- made noarch because Fedora is supposed to just "do the right thing" now
- added fedora-ds-dsgw

* Wed Jan 16 2008 Rich Megginson <rmeggins@redhat.com> 1.1.1-2
- fedora-admin-console was changed to fedora-ds-admin-console

* Thu Jan 10 2008 Rich Megginson <rmeggins@redhat.com> 1.1.1-1
- changes for fedora package review
- added LICENSE

* Thu Dec 20 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-3
- This is the final Fedora DS 1.1 release

* Wed Nov  7 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-2.0
- this is beta2
- remove dist tag

* Wed Oct 17 2007 Rich Megginson <rmeggins@redhat.com> - 8.0.0-1.2
- forgot comma in defattr

* Tue Oct 16 2007 Rich Megginson <rmeggins@redhat.com> - 8.0.0-1.1
- added defattr to fix file ownership problem

* Wed Aug  8 2007 Rich Megginson <rich@localhost.localdomain> - ds-1
- Initial build.

