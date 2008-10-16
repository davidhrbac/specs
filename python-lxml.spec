%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-lxml
Version:        2.1.2
Release:        1%{?dist}
Summary:        ElementTree-like Python bindings for libxml2 and libxslt

Group:          Development/Libraries
License:        BSD
URL:            http://codespeak.net/lxml/
Source0:        http://cheeseshop.python.org/packages/source/l/lxml/lxml-%{version}.tar.gz
#Source0:        http://codespeak.net/lxml/lxml-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libxslt-devel
BuildRequires:  python-devel

%if 0%{?fedora} >= 8
BuildRequires: python-setuptools-devel
%else
BuildRequires: python-setuptools
%endif

%description
lxml provides a Python binding to the libxslt and libxml2 libraries.
It follows the ElementTree API as much as possible in order to provide
a more Pythonic interface to libxml2 and libxslt than the default
bindings.  In particular, lxml deals with Python Unicode strings
rather than encoded UTF-8 and handles memory management automatically,
unlike the default bindings.

%prep
%setup -q -n lxml-%{version}

chmod a-x doc/rest2html.py

%build
CFLAGS="%{optflags}" %{__python} -c 'import setuptools; execfile("setup.py")' build

%install
rm -rf %{buildroot}
%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.txt LICENSES.txt PKG-INFO CREDITS.txt CHANGES.txt doc/
%{python_sitearch}/*

%changelog
* Mon Oct 13 2008 David Hrbáč <david@hrbac.cz> - 2.0.8-1
- Update to 2.1.2

* Mon Oct 13 2008 David Hrbáč <david@hrbac.cz> - 2.0.8-1
- initial rebuild

* Fri Jul 25 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.8-1
- Update to 2.0.8

* Fri Jun 20 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.7-1
- Update to 2.0.7
- Update download URL

* Sat May 31 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.6-1
- Update to 2.0.6

* Thu May  8 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.5-1
- Update to 2.0.5

* Wed Mar 26 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.3-1
- Update to 2.0.3

* Sat Feb 23 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.2-1
- Update to 2.0.2

* Tue Feb 19 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.1-1
- Update to 2.0.1

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.6-2
- Autorebuild for GCC 4.3

* Mon Nov  4 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.6-1
- Update to 1.3.6.

* Mon Oct 22 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.5-1
- Update to 1.3.5.

* Thu Aug 30 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.4-1
- Update to 1.3.4.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.3.3-3
- Rebuild for selinux ppc32 issue.

* Tue Aug 28 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.3-2
- BR python-setuptools-devel

* Mon Jul 30 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.3-1
- Update to 1.3.3

* Fri Jan 19 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.1.2-1
- Update to 1.1.2

* Thu Dec 14 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.0.3-3
- Rebuild for new Python

* Sat Sep 16 2006 Shahms E. King <shahms@shahms.com> 1.0.3-2
- Rebuild for FC6

* Thu Aug 17 2006 Shahms E. King <shahms@shahms.com> 1.0.3-1
- Update to new upstream version

* Fri Aug 11 2006 Shahms E. King <shahms@shahms.com> 1.0.2-2
- Include, don't ghost .pyo files per new guidelines

* Fri Jul 07 2006 Shahms E. King <shahms@shahms.com> 1.0.2-1
- Update to new upstream release

* Mon Jun 26 2006 Shahms E. King <shahms@shahms.com> 1.0.1-1
- Update to new upstream release

* Fri Jun 02 2006 Shahms E. King <shahms@shahms.com> 1.0-1
- Update to new upstream 1.0 release

* Wed Apr 26 2006 Shahms E. King <shahms@shahms.com> 0.9.1-3
- Add python-setuptools to BuildRequires
- Use dist tag

* Wed Apr 26 2006 Shahms E. King <shahms@shahms.com> 0.9.1-2
- Fix summary and description

* Tue Apr 18 2006 Shahms E. King <shahms@shahms.com> 0.9.1-1
- update the new upstream version
- remove Pyrex build req

* Tue Dec 13 2005 Shahms E. King <shahms@shahms.com> 0.8-1
- Initial package
