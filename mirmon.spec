Summary:        Monitor the state of mirrors
Name:           mirmon
Version:        2.3
Release:        1%{?dist}
License:        BSD
Group:          Applications/Internet
URL:            http://people.cs.uu.nl/henkp/mirmon/
Source:         http://people.cs.uu.nl/henkp/mirmon/mirmon-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildArch: noarch

%description
This packages contains a mirmon program - an utility to monitor the state of mirrors.

%prep
%setup -q
sed -i 's,/sw/bin/,%_bindir/,g' mirmon

%install
mkdir -p %buildroot{%_bindir,%_datadir/%name}
install -pm755 mirmon %buildroot%_bindir/
cp -a countries.list icons %buildroot%_datadir/%name/

%files
%_bindir/*
%_datadir/%name
%doc *.txt

%changelog
* Wed Sep 01 2010 David Hrbáč <david@hrbac.cz> - 2.3-1
- initial release
