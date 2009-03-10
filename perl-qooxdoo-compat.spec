Summary:    Perl backend for Qooxdoo
Name:       perl-qooxdoo-compat
Version:    0.7.3
Release:    2%{?dist}
License:    LGPLv2 or EPL
Group:      Development/Languages
URL:        http://qooxdoo.org/
Source0:    http://downloads.sourceforge.net/qooxdoo/qooxdoo-%{version}-backend.zip
Patch0:     perl-qooxdoo-compat-0.7.3-strict.patch
BuildArch:  noarch
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: dos2unix

%description
This package provides the Perl backend for Qooxdoo, a comprehensive
and innovative Ajax application framework. This package supports
Qooxdoo 0.7.

%prep
%setup -q -n qooxdoo-%{version}-backend
%patch0 -p1
dos2unix -k AUTHORS LICENSE README RELEASENOTES TODO VERSION

%build
# nothing to build

%install
%{__rm} -rf %{buildroot}

%{__install} -Dp -m 0644  backend/perl/Qooxdoo/JSONRPC.pm \
    %{buildroot}%{perl_vendorlib}/Qooxdoo/JSONRPC.pm

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc AUTHORS LICENSE README RELEASENOTES TODO VERSION

%{perl_vendorlib}/Qooxdoo

%changelog
* Tue Mar 10 2009 David Hrbáč <david@hrbac.cz> - 0.7.3-2
- initial rebuild
 
* Mon Oct  6 2008 Terje Rosten <terje.rosten@ntnu.no> - 0.7.3-2
- Fix ownership of dir

* Sun Oct  5 2008 Terje Rosten <terje.rosten@ntnu.no> - 0.7.3-1
- initial build

