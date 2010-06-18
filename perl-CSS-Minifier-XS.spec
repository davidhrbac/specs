Name:       perl-CSS-Minifier-XS
Version:    0.05
Release:    1%{?dist}
# lib/CSS/Minifier/XS.pm -> GPL+ or Artistic
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    XS based CSS minifier
Source:     http://search.cpan.org/CPAN/authors/id/G/GT/GTERMARS/CSS-Minifier-XS-%{version}.tar.gz
Url:        http://search.cpan.org/dist/CSS-Minifier-XS
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Module::Build::Compat)
BuildRequires: perl(Test::More)
BuildRequires: perl(Test::Pod)
BuildRequires: perl(Test::Pod::Coverage)

# don't "provide" private Perl libs
%global _use_internal_dependency_generator 0
%global __deploop() while read FILE; do /usr/lib/rpm/rpmdeps -%{1} ${FILE}; done | /bin/sort -u
%global __find_provides /bin/sh -c "%{__grep} -v '%{perl_vendorarch}/.*\\.so$' | %{__deploop P}"
%global __find_requires /bin/sh -c "%{__deploop R}"

%description
'CSS::Minifier::XS' is a CSS "minifier"; it's designed to remove un-
necessary whitespace and comments from CSS files, while also *not*
breaking the CSS. 'CSS::Minifier::XS' is similar in function to
'CSS::Minifier', but is substantially faster as it's written in XS and
not just pure Perl.


%prep
%setup -q -n CSS-Minifier-XS-%{version}

%build
%{__perl} Build.PL installdirs=vendor optimize="$RPM_OPT_FLAGS"
./Build

%install
rm -rf %{buildroot}

./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
./Build test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto
%{_mandir}/man3/*.3*

%changelog
* Thu Jun 10 2010 David Hrbáč <david@hrbac.cz> - 0.05-1
- new upstream version

* Wed Sep 23 2009 David Hrbáč <david@hrbac.cz> - 0.04-1
- initial build
