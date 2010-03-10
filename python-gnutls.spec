Name:           python-gnutls
Version:        1.2.0
Release:        1%{?dist}
Summary:        Python wrapper for the GNUTLS library
URL:            http://cheeseshop.python.org/pypi/python-gnutls
License:        LGPL
Group:          Development/Libraries/Python
Source:         http://pypi.python.org/packages/source/p/python-gnutls/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-buildroot
BuildRequires:  gnutls-devel python-devel

%description
This package provides a high level object oriented wrapper around libgnutls, as well as low level bindings to the GNUTLS types and functions via ctypes. The high level wrapper hides the details of accessing the GNUTLS library via ctypes behind a set of classes that encapsulate GNUTLS sessions, certificates and credentials and expose them to python applications using a simple API.
The package also includes a Twisted interface that has seamless intergration with Twisted, providing connectTLS and listenTLS methods on the Twisted reactor once imported (the methods are automatically attached to the reactor by simply importing the GNUTLS Twisted interface module).
The high level wrapper is written using the GNUTLS library bindings that are made available via ctypes. This makes the wrapper very powerful and flexible as it has direct access to all the GNUTLS internals and is also very easy to extend without any need to write C code or recompile anything.

Authors:
--------
    Dan Pascu <dan@ag-projects com>

%prep
%setup -q

%build
export CFLAGS="$RPM_OPT_FLAGS"
%{__python} setup.py build

%install
rm -rf %{buildroot}
#python setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc README
%{_bindir}/.py*
%{python_sitearch}/*

%changelog
* Tue Mar 09 2010 David Hrbáč <david@hrbac.cz> - 1.2.0-1
- new upstream release
* Thu Oct 16 2008 David Hrbáč <david@hrbac.cz> - 1.1.4-1
- initial build
