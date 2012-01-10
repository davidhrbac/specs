%global         git b737f60
Summary:        A top clone for MySQL
Name:           mytop
Version:        1.7
Release:        4.%{git}%{?dist}
Group:          Applications/System
License:        GPLv2
URL:            http://jeremy.zawodny.com/mysql/mytop
# Tarball created by
# $ git clone git://github.com/jzawodn/mytop.git
# $ cd mytop
# $ git archive --format=tar --prefix=mytop-1.7/ %{git} | xz > mytop-1.7-%{git}.tar.xz
Source0:        mytop-%{version}-%{git}.tar.bz
Patch01:        mytop-1.7-long.patch
Patch02:        mytop-1.7-undef-resolv.patch
Requires:       perl(DBD::mysql) >= 1
Requires:       perl(Term::ReadKey) >= 2.1
Requires:       perl(Term::ANSIColor) perl(Time::HiRes)
BuildRequires:  perl(DBD::mysql) >= 1
BuildRequires:  perl(DBI) >= 1.13
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Term::ReadKey) >= 2.1
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description 
mytop is a console-based tool for monitoring the threads and overall
performance of MySQL servers. The user interface is modeled after
familiar top application.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

%build
%{__perl} Makefile.PL
%{__make}

%install
%{__rm} -rf %{buildroot}
%{__install} -D -m 0644 blib/man1/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
%{__install} -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

%check
%{__make} test

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc Changes README
%{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}

%changelog
* Tue Jan 10 2012 David Hrbáč <david@hrbac.cz> - 1.7-4.b737f60
- initial rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-4.b737f60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun May 09 2010 Terje Rosten <terje.rosten@ntnu.no> - 1.7-3.b737f60
- add patch to fix #589366

* Mon May 03 2010 Terje Rosten <terje.rosten@ntnu.no> - 1.7-2.b737f60
- add patch to fix #584602

* Sat Mar 27 2010 Terje Rosten <terje.rosten@ntnu.no> - 1.7-1.b737f60
- 1.7 (from github), fixing bz #577528

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 30 2007 Terje Rosten <terje.rosten@ntnu.no> - 1.6-2
- remove explicit req on dbi, let rpm to the job

* Wed Dec 26 2007 Terje Rosten <terje.rosten@ntnu.no> - 1.6-1
- initial package
