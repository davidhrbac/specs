# We need to regenerate the HMAC values after the buildroot policies have
# mucked around with binaries.  This overrides the default which was in place
# at least from Red Hat Linux 9 through Fedora 11's development cycle.

Name:		hmaccalc
Version:	0.9.6
Release:	1%{?dist}
Summary:	Tools for computing and checking HMAC values for files

Group:		System Environment/Base
License:	MIT
URL:		https://fedorahosted.org/hmaccalc/
Source0:	https://fedorahosted.org/released/hmaccalc/hmaccalc-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	nss-devel

%description
The hmaccalc package contains tools which can calculate HMAC (hash-based
message authentication code) values for files.  The names and interfaces are
meant to mimic the sha*sum tools provided by the coreutils package.

%prep
%setup -q

%build
%configure --enable-sum-directory=%{_libdir}/%{name}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%check
make check

%files
%defattr(-,root,root,-)
%doc README LICENSE
%{_bindir}/sha1hmac
%{_bindir}/sha256hmac
%{_bindir}/sha384hmac
%{_bindir}/sha512hmac
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/sha1hmac.hmac
%{_libdir}/%{name}/sha256hmac.hmac
%{_libdir}/%{name}/sha384hmac.hmac
%{_libdir}/%{name}/sha512hmac.hmac
%{_mandir}/*/*

%changelog
* Fri May 15 2009 David Hrbáč <david@hrbac.cz> - 0.9.6-1
- initial rebuild

* Wed Apr  8 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.6-1
- fix 'make check' by using binaries built with a different path for their
  own check files
- add a non-fips compile-time option, which we don't use

* Mon Mar 30 2009 Nalin Dahyabhai <nalin@redhat.com>
- handle '-' as indicating that stdin should be used for the input file

* Fri Mar 27 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.5-1
- add a -t option, for truncating HMAC outputs

* Wed Mar 25 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.4-1
- use a longer default key, when we use the default key

* Tue Mar 24 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.3-1
- fix the -k option
- move self-check files to %%{_libdir}/%{name}

* Tue Mar 24 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.2-1
- provide a way to override the directory which will be searched for self-check
  values (part of #491719)

* Tue Mar 24 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.1-1
- store self-check values in hex rather than in binary form (part of #491719)

* Tue Mar 24 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9-2
- add URL to fedorahosted home page, and mention it in the man page as a means
  to report bugs and whatnot (part of #491719)
- correct the license tag: "X11" -> "MIT" (part of #491719)
- expand the acronym HMAC in the description (part of #491719)
- disable the sumfile prefix (part of #491719)

* Fri Mar 20 2009 Nalin Dahyabhai <nalin@redhat.com>
- initial .spec file

