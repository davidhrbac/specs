%{!?python_sitelib_platform: %define python_sitelib_platform %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define pkgname hashlib

Summary: Secure hash and message digest algorithm library
Name: python-hashlib
Version: 20081119
Release: 4%{?dist}
Source0: http://code.krypto.org/python/hashlib/%{pkgname}-%{version}.tar.gz
License: Python
Group:   Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: openssl-devel, python-devel
Prefix: %{_prefix}
Url: http://code.krypto.org/python/hashlib/

%description
This is a stand alone packaging of the hashlib library introduced in 
Python 2.5 so that it can be used on older versions of Python.

%prep
%setup -q -n %{pkgname}-%{version}
#fix EOL characters
sed -i -e 's|\r||g' README.txt ChangeLog

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{python_sitelib_platform}/*
%doc README.txt ChangeLog

%changelog
* Wed May 13 2009 David Hrbáč <david@hrbac.cz> - 20081119-4
- initial rebuild

* Fri Feb 20 2009 Dennis Gilmore <dennis@ausil.us> - 20081119-4
- review fixes (License TAG, doc files)

* Thu Jan 29 2009 Seth Vidal <skvidal at fedoraproject.org> - 20081119-3
- few minor spec cleanups
- add Changelog to docs
- first build and packaging

