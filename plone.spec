%define python_minver 2.4.3
%define zope_minver 2.10.4

%define zope_home      %{_libdir}/zope
%define software_home  %{zope_home}/lib/python

Name:           plone
Version:        3.1.2
Release:        1%{?dist}
Summary:        User friendly and powerful open source Content Management System
License:        GPLv2+
Group:          System Environment/Daemons
URL:            http://www.plone.org/
Source0:        http://launchpad.net/plone/3.1/3.1.2/+download/Plone-3.1.2.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       zope >= %{zope_minver}
Requires:       python >= %{python_minver}, python-imaging
Requires:	python-feedparser, python-lxml, python-elementtree

%description
Plone is a user friendly and powerful content management system based on Zope.
It is easy to use, translated into over 35 languages and carefully follows
standards. It's under active development and easily extensible with add-on
products.

%prep
%setup -q -n Plone-%{version}
# Clean up sources
find . -type d -name CVS | xargs rm -rf
find . -type f -name .cvsignore | xargs rm -rf
find . -type d -name .svn | xargs rm -rf
find . -type f -name "*~" | xargs rm -rf


%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{software_home}/Products
install -d $RPM_BUILD_ROOT%{software_home}/lib/python
cp -pr Products/* $RPM_BUILD_ROOT%{software_home}/Products
cp -pr lib/python/* $RPM_BUILD_ROOT%{software_home}/

%clean
rm -rf $RPM_BUILD_ROOT


%post
# Make it available to Zope, be it on install or on upgrade
/sbin/service zope condrestart >/dev/null 2>&1


%files
%defattr(644,root,root,755)
%doc README.txt RELEASENOTES.txt INSTALL.txt
%{software_home}/Products/*
%{software_home}/archetypes/
%{software_home}/five/
%{software_home}/kss/
%{software_home}/plone/
%{software_home}/wicked/
%{software_home}/borg/

%changelog
* Fri Sep 24 2008 David Hrbáč <david@hrbac.cz> - 3.1.2-1
- initial rebuild

* Sat Jun 14 2008 Jonathan Steffan <jon a fedoraunity.org> 3.1.2-1
- Update to plone 3.1.2

* Sun May 11 2008 Jonathan Steffan <jon a fedoraunity.org> 3.1.1-1
- Update to plone 3.1.1

* Tue Feb 19 2008 Jonathan Steffan <jon a fedoraunity.org> 3.0.6-1
- Update to plone 3.0.6
- Fix ownership so zope owns non-plone folders and plone doesn't own
  zope folders

* Mon Jan 7 2008 Jonathan Steffan <jon a fedoraunity.org> 3.0.5-1
- Update to plone 3.0.5

* Wed Dec 12 2007 Jonathan Steffan <jon a fedoraunity.org> 3.0.4-1
- Update to plone 3.0.4

* Sun Nov 11 2007 Jonathan Steffan <jon a fedoraunity.org> 3.0.3-1
- Update to plone 3.0.3
- Remove hotfix 20071106 as it's included in 3.0.3

* Tue Nov 6 2007 Jonathan Steffan <jon a fedoraunity.org> 3.0.2-2
- Add plone hotfix 20071106 (CVE-2007-5741)

* Tue Oct 16 2007 Jonathan Steffan <jon a fedoraunity.org> 3.0.2-1
- Update to Plone 3.0.2

* Fri Sep 14 2007 Jonathan Steffan <jon a fedoraunity.org> 3.0.1-1
- Update to Plone 3.0.1

* Thu Aug 23 2007 Jonathan Steffan <jon a fedoraunity.org> 3.0-1
- Moved plone install back to software_home
- Updated to Plone 3.0 final release

* Wed Aug 2 2007 Jonathan Steffan <jon a fedoraunity.org> 3.0-0.2rc2
- Moved plone install from software_home to instance_home (workaround)

* Wed Aug 1 2007 Jonathan Steffan <jon a fedoraunity.org> 3.0-0.1rc2
- Initial Package
