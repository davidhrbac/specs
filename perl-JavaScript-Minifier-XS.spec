Name:           perl-JavaScript-Minifier-XS
Version:        0.05
Release:        1%{?dist}
Summary:        XS based JavaScript minifier
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/JavaScript-Minifier-XS/
Source0:        http://www.cpan.org/authors/id/G/GT/GTERMARS/JavaScript-Minifier-XS-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::More)
#BuildRequires:  perl(JavaScript::Minifier)
BuildRequires:  perl(Test::Pod)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# don't "provide" private Perl libs
%global _use_internal_dependency_generator 0
%global __deploop() while read FILE; do /usr/lib/rpm/rpmdeps -%{1} ${FILE}; done | /bin/sort -u
%global __find_provides /bin/sh -c "%{__grep} -v '%{perl_vendorarch}/.*\\.so$' | %{__deploop P}"
%global __find_requires /bin/sh -c "%{__deploop R}"

%description
JavaScript::Minifier::XS is a JavaScript "minifier"; its designed
to remove un-necessary whitespace and comments from JavaScript
files without breaking the JavaScript.

%prep
%setup -q -n JavaScript-Minifier-XS-%{version}

%build
%{__perl} Build.PL installdirs=vendor optimize="$RPM_OPT_FLAGS"
./Build

%install
rm -rf $RPM_BUILD_ROOT

./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/JavaScript*
%{_mandir}/man3/*

%changelog
* Wed Sep 23 2009 David Hrbáč <david@hrbac.cz> - 0.05-1
- initial build
