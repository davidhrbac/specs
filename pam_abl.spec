Name:		pam_abl
Summary:	A Pluggable Authentication Module (PAM) for auto blacklisting
Version:	0.2.3
Release:	3%{?dist}
License:	GPL
Group:		System Environment/Base
URL:		http://www.hexten.net/sw/pam_abl/
Source0:	http://dl.sourceforge.net/sourceforge/pam-abl/%{name}-%{version}.tar.gz	
Patch0:		pam_abl-0.2.3-fixes.patch
BuildRequires:	db4-devel, pam-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Provides auto blacklisting of hosts and users responsible for repeated
failed authentication attempts. Generally configured so that
blacklisted users still see normal login prompts but are guaranteed to
fail to authenticate. A command line tool allows to query or purge the
databases used by the pam_abl module.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
install -D -m 755 pam_abl.so %{buildroot}/%{_lib}/security/pam_abl.so
install -D -m 644 conf/pam_abl.conf %{buildroot}%{_sysconfdir}/security/pam_abl.conf
install -D -m 755 tools/pam_abl %{buildroot}%{_sbindir}/pam_abl
install -d -m 755 %{buildroot}%{_localstatedir}/lib/abl
install -D -m 644 doc/pam_abl.1 %{buildroot}%{_mandir}/man1/pam_abl.1
rm -rf doc/{CVS,._pam_abl.html,pam_abl.1}

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc AUTHORS CONFIGURATION COPYING NEWS QUICKSTART THANKS
%doc Copyright conf/system-auth doc
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/security/pam_abl.conf
/%{_lib}/security/pam_abl.so
%{_sbindir}/pam_abl
%{_localstatedir}/lib/abl/
%{_mandir}/man?/%{name}.*

%changelog
* Wed Mar 19 2008 David Hrbáč <david@hrbac.cz> - 0.2.3-3
- CentOS rebuild

* Sun May 13 2007 Alexander Dalloz <alex {%} dalloz {*} de> - 0.2.3-3
- Rebuild to fix #219947.

* Tue Aug 29 2006 Alexander Dalloz <alex {%} dalloz {*} de> - 0.2.3-2
- Rebuild for FC6.

* Sun Jul 16 2006 Alexander Dalloz <alex {%} dalloz {*} de> - 0.2.3-1
- Upgrade to 0.2.3
  - fixes #165817, #174932, #185866, #192614
- Added manpage, improved documentation
  (big thanks to Robert Scheck)

* Fri Jul 15 2005 Alexander Dalloz <alex {%} dalloz {*} de> - 0.2.2-2
- Defined %%{reldate} and made macro usage consistent
- pam_abl moved to /usr/sbin.

* Wed Jul 13 2005 Alexander Dalloz <alex {%} dalloz {*} de> - 0.2.2-1
- Changes following review:
  - added %%{?dist} tag
  - set Group to System Environment/Base
  - set Source0 to be an absolute URL
  - changed BuildPrereq to be BuildRequires
  - moved instructions into README.Fedora
- dropped release date in tarball name as release number flag
- removed outdated instruction in example system-auth doc file.

* Sun Jul 11 2005 Alexander Dalloz <alex {%} dalloz {*} de> - 0.2.2-20050110
- Initial build.
