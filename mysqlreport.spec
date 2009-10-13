Name:           mysqlreport
Version:        3.5
Release:        4%{?dist}
Summary:        A friendly report of important MySQL status values

Group:          Development/Libraries
License:        GPLv2+
URL:            http://hackmysql.com/mysqlreport
Source0:        http://hackmysql.com/scripts/mysqlreport-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
BuildArch:      noarch

Requires:       perl
Requires:       perl(Term::ReadKey)

%description
mysqlreport makes a friendly report of important MySQL status values.  It 
transforms the values from SHOW STATUS into an easy-to-read report that
provides an in-depth understanding of how well MySQL is running, and is a 
better alternative (and practically the only alternative) to manually
interpreting SHOW STATUS. 

%prep%setup -q


%build
# no-op


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
cp -p mysqlreport %{buildroot}%{_bindir}

%check
# no tests


%clean
rm -rf %{buildroot} 


%files
%defattr(-,root,root,-)
%doc COPYING *.html
%{_bindir}/mysqlreport


%changelog
* Tue Oct 13 2009 David Hrbáč <david@hrbac.cz> - 3.5-4
- initial rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 06 2008 Chris Weyl <cweyl@alumni.drew.edu> 3.5-2
- drop :MODULE_COMPAT requires (we don't deliver any modules)

* Tue Dec 02 2008 Chris Weyl <cweyl@alumni.drew.edu> 3.5-1
- initial packaging
