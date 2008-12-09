Name:           perl-DBD-Oracle
Version:        1.22
Release: 	1%{?dist}
Summary:        A Oracle interface for perl

Group:          Development/Libraries
License:        GPL or Artistic
URL:            http://search.cpan.org/dist/DBD-Oracle
Source0:        http://search.cpan.org/CPAN/authors/id/P/PY/PYTHIAN/DBD-Oracle-%{version}.tar.gz
Source1:        filter-requires-dbdmysql.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl >= 1:5.6.1
BuildRequires:  perl(DBI)
BuildRequires:  zlib-devel
BuildRequires:  oracle-instantclient-devel
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides:       perl-DBD-Oracle = %{version}-%{release}
Requires:  oracle-instantclient-basic = %(rpm -q oracle-instantclient-basic --qf "%%{version}-%%{release}\n")

%define __perl_requires %{SOURCE1}

%description 
An implementation of DBI for Oracle for Perl.


%prep
%setup -q -n DBD-Oracle-%{version}
# Correct file permissions
find . -type f -exec chmod -x {} ';'


%build
export ORACLE_HOME=/usr/lib/oracle/10.2.0.3/client
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL -m /usr/share/oracle/10.2.0.3/client/demo.mk INSTALLDIRS=vendor 
make %{?_smp_mflags} OPTIMIZE="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name 'ora_explain*' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

#file=$RPM_BUILD_ROOT%{_mandir}/man3/DBD::mysql.3pm
#iconv -f iso-8859-1 -t utf-8 < "$file" > "${file}_"
#mv -f "${file}_" "$file"


%check || :
# Full test coverage requires a live Oracle database
# make test


%clean 
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
#%doc ChangeLog INSTALL.html README TODO
#%{perl_vendorarch}/Bundle/
%{perl_vendorarch}/DBD/
%{perl_vendorarch}/Ora*
%{perl_vendorarch}/ora*
%{perl_vendorarch}/auto/DBD/
%{_mandir}/man3/*.3*


%changelog
* Thu Nov 18 2008 David Hrbáč <david@hrbac.cz> - 1.22-1
- update to new version

* Fri Apr 18 2008 David Hrbáč <david@hrbac.cz> - 1.21-1
- update to new version

* Sat Feb  2 2008 David Hrbáč <david@hrbac.cz> - 1.20-1
- update to 1.20

* Fri Jul 27 2007 David Hrbáč <david@hrbac.cz> - 1.19-1
- initial spec created for CentOS-4

