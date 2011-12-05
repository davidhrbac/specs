Name:           perl-Any-Moose
Version:        0.17
Release:        1%{?dist}
Summary:        Use Moose or Mouse modules
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Any-Moose/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SA/SARTAK/Any-Moose-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl >= 0:5.006_002
BuildRequires:  perl(Mouse) >= 0.40
Requires:       perl(Mouse) >= 0.40
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Though we recommend that people generally use Moose, we accept that Moose
cannot yet be used for everything everywhere. People generally like the
Moose sugar, so many people use Mouse, a lightweight replacement for
parts of Moose.

%prep
%setup -q -n Any-Moose-%{version}

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
#make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes dist.ini LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Dec 05 2011 David Hrbáč <david@hrbac.cz> - 0.17-1
- new upstream release

* Wed Apr 06 2011 David Hrbáč <david@hrbac.cz> - 0.13-1
- Specfile autogenerated by cpanspec 1.78.
