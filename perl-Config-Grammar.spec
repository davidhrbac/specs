Name:           perl-Config-Grammar
Version:        1.10
Release:        1%{?dist}
Summary:        Grammar-based, user-friendly config parser
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Config-Grammar/
Source0:        http://www.cpan.org/authors/id/D/DS/DSCHWEI/Config-Grammar-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker) perl(Test::Simple)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Config::Grammar is a module to parse configuration files. The
configuration may consist of multiple-level sections with assignments
and tabular data.  The parsed data will be returned as a hash
containing the whole configuration. Config::Grammar uses a grammar
that is supplied upon creation of a Config::Grammar object to parse
the configuration file and return helpful error messages in case of
syntax errors. Using the makepod method you can generate documentation
of the configuration file format.

%prep
%setup -q -n Config-Grammar-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}/*

%check
%{__make} test

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc Changes README
%{perl_vendorlib}/Config/Grammar*
%{_mandir}/man3//Config::Grammar*

%changelog
* Tue Mar 10 2009 David Hrbáč <david@hrbac.cz> - 1.10-1
- Initial rebuild

* Tue Sep 09 2008 Terje Rosten <terje.rosten@ntnu.no> - 1.10-1
- initial build based on cpanspec
