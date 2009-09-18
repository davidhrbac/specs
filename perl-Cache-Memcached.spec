Name:           perl-Cache-Memcached
Version:        1.26
Release:        4%{?dist}
Summary:        Perl client for memcached

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Cache-Memcached/
Source0:        http://search.cpan.org/CPAN/authors/id/B/BR/BRADFITZ/Cache-Memcached-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker) perl(Storable) perl(Time::HiRes) perl(String::CRC32) perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Cache::Memcached - client library for memcached (memory cache daemon)

%prep
%setup -q -n Cache-Memcached-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*


#%check
# This requires a running memcached on the local host, which isn't very
# convenient or suitable. YMMV. BR's are there if we REALLY want this.
#make test


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README ChangeLog
%dir %{perl_vendorlib}/Cache/
%dir %{perl_vendorlib}/Cache/Memcached/
%{perl_vendorlib}/Cache/Memcached.pm
%{perl_vendorlib}/Cache/Memcached/GetParser.pm
%{_mandir}/man3/Cache::Memcached.3*


%changelog
* Fri Sep 18 2009 David Hrbáč <david@hrbac.cz> - 1.26-4
- initial rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 9 2009 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 1.2.6-3
- More cleanups
- Change license

* Sat Jun 6 2009 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 1.2.6-2
- Cleaned up for Fedora review

* Sat Jun 6 2009 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 1.2.6-1.mf
- Initial Revision
