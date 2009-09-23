Name:       perl-CSS-Minifier 
Version:    0.01 
Release:    1%{?dist}
# lib/CSS/Minifier.pm -> GPL+ or Artistic
License:    GPL+ or Artistic 
Group:      Development/Libraries
Summary:    Remove unnecessary whitespace from CSS files 
Source:     http://search.cpan.org/CPAN/authors/id/P/PM/PMICHAUX/CSS-Minifier-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/CSS-Minifier
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker)
# tests
BuildRequires: perl(Test::More)

%description
This module removes unnecessary whitespace from CSS. The primary
requirement developing this module is to not break working stylesheets:
if working CSS is in input then working CSS is output. The Mac/Internet
Explorer comment hack will be minimized but not stripped and so will
continue to function.This module understands space, horizontal tab, new
line, carriage return, and form feed characters to be whitespace. Any
other characters that may be considered whitespace are not minimized.
These other characters include paragraph separator and vertical tab.For
static CSS files, it is recommended that you minify during the build
stage of web deployment. If you minify on-the-fly then it might be a
good idea to cache the minified file. Minifying static files on-the-fly
repeatedly is wasteful.

%prep
%setup -q -n CSS-Minifier-%{version}
perl -pi -e "s,5.008006,5.008005,g" Makefile.PL

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
make test

%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%doc README Changes 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Wed Sep 23 2009 David Hrbáč <david@hrbac.cz> - 0.01-1
- initial build
