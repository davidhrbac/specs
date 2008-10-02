%{!?python_sitearch: %define python_sitearch %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib(1)')}
# eval to 2.3 if python isn't yet present, workaround for no python in fc4 minimal buildroot
%{!?python_version: %define python_version %(%{__python} -c 'import sys; print sys.version.split(" ")[0]' || echo "2.3")}
%define apacheconfdir   %{_sysconfdir}/httpd/conf.d

Summary: mod_scgi is a replacement for mod_fastcgi, using a similar, but different protocol
Name: python-scgi
Version: 1.13
Release: 1%{?dist}
Epoch: 1
Group: System Environment/Daemons
Source0: http://python.ca/scgi/releases/scgi-%{version}.tar.gz
Source1: scgi.conf
License: BSD-Style
BuildRoot: %{_tmppath}/%{name}-root
BuildPrereq: httpd-devel, python-devel

%description
The SCGI protocol is a replacement for the Common Gateway Interface (CGI) protocol.
It is a standard for applications to interface with HTTP servers.
It is similar to FastCGI but is designed to be easier to implement.

This package contains the python bindings that implements the server side of the protocol.

%package -n mod_scgi
Group: System Environment/Daemons
Requires: httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel)
Summary: Apache module named mod_scgi that implements the client side of the protocol.

%description -n mod_scgi
The SCGI protocol is a replacement for the Common Gateway Interface (CGI) protocol.
It is a standard for applications to interface with HTTP servers.
It is similar to FastCGI but is designed to be easier to implement.

This package contains the apache module that implements the client side of the protocol.

%prep
%setup -q -n scgi-%{version}

%build
pushd apache2
%{_sbindir}/apxs -c mod_scgi.c
popd

%install
rm -rf %{buildroot}

# install python files
python setup.py install --prefix=%{buildroot}%{_prefix}

# install apache module 
mkdir -p %{buildroot}%{_libdir}/httpd/modules
install -m755 apache2/.libs/mod_scgi.so %{buildroot}%{_libdir}/httpd/modules

# install the config file
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
#%{_bindir}/.py*
%{python_sitearch}/*

%files -n mod_scgi
%defattr(-,root,root)
#%doc apache2/README apache2/CONFIGURE apache2/CHANGES
%{_libdir}/httpd/modules/*.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf

%changelog
* Mon Sep 29 2008 David Hrbáč <david@hrbac.cz> - 1.1.13-1
- initial rebuild
- new upstream vesrion
 
* Thu Apr 12 2007 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 1.1.12-1%{dist}
- Updated to 1.1.12
- Enabled and renamed main package to python-scgi
- Rebuilt on RHEL 5 Server

* Sun Feb 05 2006 Jacob Leaver <jleaver@c-corp.net> 
- initial RPM spec
