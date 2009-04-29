%define cvsver 20070810
%define codename BlameTheSegfault
%define rel 7

Summary: CRM114 Bayesian Spam Detector
Name: crm114
Version: 0
Release: 1.%{rel}.%{cvsver}%{?dist}
URL: http://crm114.sourceforge.net/
License: GPLv2
Group: Applications/Text
Source0: http://crm114.sourceforge.net/%{name}-%{cvsver}-%{codename}.src.tar.gz
Patch0: %{name}-rpm.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildRequires: tre-devel

%description 
CRM114 is a system to examine incoming e-mail, system log streams,
data files or other data streams, and to sort, filter, or alter the
incoming files or data streams according to the user's wildest
desires. Criteria for categorization of data can be by satisfaction of
regexes, by sparse binary polynomial matching with a Bayesian Chain
Rule evaluator, or by other means.

%package emacs
Summary: CRM114 mode for Emacs
Group: Applications/Text
Requires: emacs-el

%description emacs
Major Emacs mode for editing crm114 scripts.

%prep
%setup -q -n %{name}-%{cvsver}-%{codename}.src
%patch0 -p1 -b .r
chmod 644 mailfilter.cf

%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_OPT_FLAGS"

%clean 
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/{%{name},emacs/site-lisp}}
make DESTDIR=$RPM_BUILD_ROOT install
install -pm 755 mail{filter,reaver,trainer}.crm $RPM_BUILD_ROOT%{_datadir}/%{name}/
install -pm 644 maillib.crm $RPM_BUILD_ROOT%{_datadir}/%{name}/

%check
make megatest

%files
%defattr(-,root,root,-)
%doc README *.txt *.recipe *.example mailfilter.cf
%{_bindir}/*
%{_datadir}/%{name}

%files emacs
%defattr(644,root,root,755)
%{_datadir}/emacs/site-lisp/*.el

%changelog
* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0-1.7.20070810
- Autorebuild for GCC 4.3

* Sat Oct 27 2007 Dominik Mierzejewski <rpm@greysector.net> 0-0.6.20070810
- updated to 20070810 "BlameTheSegfault"
- dropped obsolete patch

* Wed Aug 29 2007 Karol Trzcionka <karlikt at gmail.com> - 0-0.5.20070301
- Rebuild for BuildID

* Tue Apr 17 2007 Dominik Mierzejewski <rpm@greysector.net> 0-0.4.20070301
- fix testsuite on 64bit, patch by Jaakko Hyvätti

* Sun Apr 15 2007 Dominik Mierzejewski <rpm@greysector.net> 0-0.3.20070301
- updated to 20070301 "BlameBaltar"
- added missing quine.crm to testsuite
- no more crashes on x86_64, removed ExcludeArch, fixes #202893

* Tue Aug 29 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.2.20060704
- mass rebuild

* Wed Aug 16 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.20060704
- FE-compliant versioning
- emacs subpackage should require emacs-el
- simplified file list
- added %%check
- small patch to make 'make megatest' work from current dir
- ExcludeArch: x86_64 until 64bit tre is fixed

* Wed Jul 26 2006 Dominik Mierzejewski <rpm@greysector.net>
- 20060704a release
- added -emacs package with crm mode for emacs
- fixed parallel make build
- use dist tag
- shut up rpmlint

* Sun Feb 19 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.20060118
- FE compliance
- package mailfilter scripts

* Mon Dec 15 2003 Bill Yerazunis <wsy@merl.com>
- removed -RCx stuff, now version contains it.
- updated for version 20031215-RC12
- License is GPL, not Artistic, so I corrected that.

* Sat Dec 13 2003 Kevin Fenzi <kevin-crm114@tummy.com>
- Converted line endings from dos format to unix. 
- Changed BuildPreReq to be 'tre-devel' 
- Fixed install to install into rpm build root. 
- tested on redhat 9 with latest tre. 

* Tue Oct 22 2003 Nico Kadel-Garcia <nkadel@merl.com>
- Created RedHat compatible .spec file
- Added libtre dependency to avoid building second package
- Hard-coded "INSTALL_DIR" in build/install setups
