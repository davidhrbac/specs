%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Mail_Queue

Name:           php-pear-Mail-Queue
Version:        1.2.6
Release:        1%{?dist}
Summary:        Class for put mails in queue and send them later in background

Group:          Development/Libraries
License:        BSD
URL:            http://pear.php.net/package/Mail_Queue
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       php-pear(Mail), php-pear(Mail_Mime), php-pear(PEAR) >= 1.4.0b1

%description
Class to handle mail queue managment.
Wrapper for PEAR::Mail and PEAR::DB (or PEAR::MDB/MDB2). It can load, save
and send saved mails in background and also backup some mails.

The Mail_Queue class puts mails in a temporary container, waiting to be
fed to the MTA (Mail Transport Agent), and sends them later (e.g. a
certain amount of mails every few minutes) by crontab or in other way.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml
cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT docdir
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Move documentation
mkdir -p docdir
mv $RPM_BUILD_ROOT%{pear_docdir}/* docdir


# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/tests

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.php.net/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_name}-%{version}/docdir/%{pear_name}/*


%{pear_xmldir}/%{name}.xml
# Expand this as needed to avoid owning dirs owned by our dependencies
# and to avoid unowned dirs
%{pear_phpdir}/Mail/Queue/Container/creole.php
%{pear_phpdir}/Mail/Queue/Container/db.php
%{pear_phpdir}/Mail/Queue/Container/mdb.php
%{pear_phpdir}/Mail/Queue/Container/mdb2.php
%{pear_phpdir}/Mail/Queue/Body.php
%{pear_phpdir}/Mail/Queue/Container.php
%{pear_phpdir}/Mail/Queue/Error.php
%{pear_phpdir}/Mail/Queue.php
%{pear_testdir}/Mail_Queue

%changelog
* Wed Dec 01 2010 David Hrbáč <david@hrbac.cz> - 1.2.6-1
- new upstream release

* Sun Feb 28 2010 David Hrbáč <david@hrbac.cz> - 1.2.3-1
- initial release
