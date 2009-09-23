Name:           perl-JavaScript-Minifier
Version:        1.05
Release:        1%{?dist}
Summary:        Perl extension for minifying JavaScript code
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/JavaScript-Minifier/
Source0:        http://www.cpan.org/authors/id/P/PM/PMICHAUX/JavaScript-Minifier-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module removes unnecessary whitespace from JavaScript code. The
primary requirement developing this module is to not break working
code: if working JavaScript is in input then working JavaScript is
output. It is ok if the input has missing semi-colons, snips like '++
+' or '12 .toString()', for example. Internet Explorer conditional
comments are copied to the output but the code inside these comments
will not be minified.

%prep
%setup -q -n JavaScript-Minifier-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Sep 23 2009 David Hrbáč <david@hrbac.cz> - 1.05-1
- initial build
