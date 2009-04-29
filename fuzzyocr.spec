%define svn svn135
Name:           fuzzyocr
Version:        3.5.0
Release:        1.%{svn}%{?dist}
Summary:        FuzzyOCR is a spamassassin plugin used to identify image spam
Group:          Applications/Internet
License:        Apache 2.0
URL:            http://fuzzyocr.own-hero.net/
Source0:        http://fuzzyocr.own-hero.net/fuzzyocr-%{version}-%{svn}.tar.bz2
BuildArch: 	noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#Requires:  	spamassassin perl-String-Approx perl-Log-Agent netpbm-progs ocrad gifsicle
Requires:       spamassassin perl-String-Approx perl-Log-Agent netpbm netpbm-progs ImageMagick libungif libungif-progs ocrad gifsicle 

%description
FuzzyOcr is a plugin for SpamAssassin which is aimed at unsolicited bulk mail 
(also known as "Spam") containing images as the main content carrier. Using 
different methods, it analyzes the content and properties of images to 
distinguish between normal mails (Ham) and spam mails.

%prep
%setup -q -n fuzzyocr-%{version}

%build
mkdir docs
mv CHANGES INSTALL LICENSE docs/
mv samples docs/
mv Utils docs/
mv FuzzyOcr.mysql docs/

%install
rm -rf $RPM_BUILD_ROOT
install -p -d -Zsystem_u:object_r:etc_mail_t %{buildroot}%{_sysconfdir}/mail/spamassassin/FuzzyOcr
cp -r FuzzyOcr/* %{buildroot}%{_sysconfdir}/mail/spamassassin/FuzzyOcr/
install -m0644 -Zsystem_u:object_r:etc_mail_t FuzzyOcr.cf %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -m0644 -Zsystem_u:object_r:etc_mail_t FuzzyOcr.scansets %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -m0644 -Zsystem_u:object_r:etc_mail_t FuzzyOcr.preps %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -m0644 -Zsystem_u:object_r:etc_mail_t FuzzyOcr.pm %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -m0644 -Zsystem_u:object_r:etc_mail_t FuzzyOcr.words %{buildroot}%{_sysconfdir}/mail/spamassassin/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc docs/*
%dir %{_sysconfdir}/mail/spamassassin/FuzzyOcr
%dir %{_sysconfdir}/mail/spamassassin/FuzzyOcr/*
%{_sysconfdir}/mail/spamassassin/FuzzyOcr.scansets
%{_sysconfdir}/mail/spamassassin/FuzzyOcr.preps
%{_sysconfdir}/mail/spamassassin/FuzzyOcr.pm
%{_sysconfdir}/mail/spamassassin/FuzzyOcr.words
%config(noreplace) %{_sysconfdir}/mail/spamassassin/FuzzyOcr.cf

%changelog
* Wed Apr 29 2009 David Hrbáč <david@hrbac.cz> - 3.5.0-1.svn135
- rebuild
- changed requirements

* Fri Mar 6 2009 Andrew Colin Kissa
- Initial creation
