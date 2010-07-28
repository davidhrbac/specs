%define svn svn135
Name:           fuzzyocr
Version:        3.6.0
Release:        2%{?dist}
Summary:        FuzzyOCR is a spamassassin plugin used to identify image spam
Group:          Applications/Internet
License:        Apache 2.0
URL:            http://fuzzyocr.own-hero.net/
Source0:        http://users.own-hero.net/~decoder/fuzzyocr/fuzzyocr-%{version}.tar.gz
Source1:	fuzzyocr.logrotate
Patch0:         fuzzyocr-log-db.patch
Patch1:         fuzzyocr-C4-netpbm-10.25.patch
Patch2:		fuzzyocr-untaint.patch
BuildArch: 	noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#Requires:  	spamassassin perl-String-Approx perl-Log-Agent netpbm-progs ocrad gifsicle
Requires:       spamassassin perl-String-Approx perl-Log-Agent netpbm netpbm-progs ImageMagick ocrad gifsicle
Requires:       /usr/bin/giffix 
Requires:       perl-MLDBM-Sync perl-Tie-Cache

%description
FuzzyOcr is a plugin for SpamAssassin which is aimed at unsolicited bulk mail 
(also known as "Spam") containing images as the main content carrier. Using 
different methods, it analyzes the content and properties of images to 
distinguish between normal mails (Ham) and spam mails.

%prep
%setup -q -n FuzzyOcr-%{version}
%patch0 -p1
%{?build_centos4:%patch1 -p1}
%patch2 -p1


%build
mkdir docs
mv CHANGES INSTALL LICENSE docs/
mv samples docs/
#mv Utils docs/
mv FuzzyOcr.mysql docs/

touch fuzzyocr.log
touch FuzzyOcr.db
touch FuzzyOcr.safe.db
%install
rm -rf $RPM_BUILD_ROOT
install -p -d -Zsystem_u:object_r:etc_mail_t %{buildroot}%{_sysconfdir}/mail/spamassassin/FuzzyOcr
cp -r FuzzyOcr/* %{buildroot}%{_sysconfdir}/mail/spamassassin/FuzzyOcr/
install -m0644 -Zsystem_u:object_r:etc_mail_t FuzzyOcr.cf %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -m0644 -Zsystem_u:object_r:etc_mail_t FuzzyOcr.scansets %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -m0644 -Zsystem_u:object_r:etc_mail_t FuzzyOcr.preps %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -m0644 -Zsystem_u:object_r:etc_mail_t FuzzyOcr.pm %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -m0644 -Zsystem_u:object_r:etc_mail_t FuzzyOcr.words %{buildroot}%{_sysconfdir}/mail/spamassassin/

install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -Dp -m 755 Utils/fuzzy-cleantmp $RPM_BUILD_ROOT%{_sbindir}/fuzzy-cleantmp
install -Dp -m 755 Utils/fuzzy-find $RPM_BUILD_ROOT%{_sbindir}/fuzzy-find
install -Dp -m 755 Utils/fuzzy-stats $RPM_BUILD_ROOT%{_sbindir}/fuzzy-stats

install -Dp -m 644 fuzzyocr.log %{buildroot}%{_localstatedir}/log/fuzzyocr.log
install -Dp -m 600 FuzzyOcr.db %{buildroot}%{_localstatedir}/amavis/.spamassassin/FuzzyOcr.db
install -Dp -m 600 FuzzyOcr.safe.db %{buildroot}%{_localstatedir}/amavis/.spamassassin/FuzzyOcr.safe.db 

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
%config(noreplace) %{_sysconfdir}/mail/spamassassin/FuzzyOcr.words
%config(noreplace) %{_sysconfdir}/mail/spamassassin/FuzzyOcr.cf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_sbindir}/fuzzy-*

%defattr(644,amavis,amavis,-)
%ghost %{_localstatedir}/log/fuzzyocr.log
%ghost %{_localstatedir}/amavis/.spamassassin/FuzzyOcr.db
%ghost %{_localstatedir}/amavis/.spamassassin/FuzzyOcr.safe.db

%post
for file in /var/log/fuzzyocr.log /var/amavis/.spamassassin/FuzzyOcr.db /var/amavis/.spamassassin/FuzzyOcr.safe.db; do
    if [ ! -e "$file" ]; then
        touch "$file"
        chmod 600 "$file" 
        chown amavis: "$file"
    fi
done

%changelog
* Wed Jul 28 2010 David Hrbáč <david@hrbac.cz> - 3.6.0-2
- updated SA 3.3.x patch

* Tue Mar 30 2010 David Hrbáč <david@hrbac.cz> - 3.6.0-1
- new upstream release
- fix for SA 3.3.0 - http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=568233

* Wed May 13 2009 David Hrbáč <david@hrbac.cz> - 3.5.0-5.svn135
- changed requirements 

* Wed May  6 2009 David Hrbáč <david@hrbac.cz> - 3.5.0-4.svn135
- create log file
- create DB files

* Thu Apr 30 2009 David Hrbáč <david@hrbac.cz> - 3.5.0-3.svn135
- noreplace for FuzzyOcr.words

* Thu Apr 30 2009 David Hrbáč <david@hrbac.cz> - 3.5.0-2.svn135
- added logrotate
- perl path
- hashing db path
- different support for C4/C5 netpbm

* Wed Apr 29 2009 David Hrbáč <david@hrbac.cz> - 3.5.0-1.svn135
- rebuild
- changed requirements

* Fri Mar 6 2009 Andrew Colin Kissa
- Initial creation
