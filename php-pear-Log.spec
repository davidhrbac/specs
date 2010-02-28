%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Log

Name:           php-pear-Log
Version:        1.12.0
Release:        1%{?dist}
Summary:        Logging Framework

Group:          Development/Libraries
License:        MIT License
URL:            http://pear.php.net/package/Log
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}


%description
The Log package provides an abstracted logging framework.  It includes
output handlers for log files, databases, syslog, email, Firebug, and the
console.  It also provides composite and subject-observer logging
mechanisms.

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
%{pear_phpdir}/Log/composite.php
%{pear_phpdir}/Log/console.php
%{pear_phpdir}/Log/daemon.php
%{pear_phpdir}/Log/display.php
%{pear_phpdir}/Log/error_log.php
%{pear_phpdir}/Log/file.php
%{pear_phpdir}/Log/firebug.php
%{pear_phpdir}/Log/mail.php
%{pear_phpdir}/Log/mcal.php
%{pear_phpdir}/Log/mdb2.php
%{pear_phpdir}/Log/null.php
%{pear_phpdir}/Log/observer.php
%{pear_phpdir}/Log/sql.php
%{pear_phpdir}/Log/sqlite.php
%{pear_phpdir}/Log/syslog.php
%{pear_phpdir}/Log/win.php
%{pear_phpdir}/Log.php
%{pear_datadir}/Log
%{pear_testdir}/Log


%changelog
* Sun Feb 28 2010 David Hrbáč <david@hrbac.cz> - 1.12.0-1
- initial release
