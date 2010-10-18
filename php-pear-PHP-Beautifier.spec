%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name PHP_Beautifier

Name:           php-pear-PHP-Beautifier
Version:        0.1.14
Release:        1%{?dist}
Summary:        Beautifier for Php

Group:          Development/Libraries
License:        PHP License
URL:            http://pear.php.net/package/PHP_Beautifier
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       php-pear(Log) >= 1.8, php-pear(PEAR) >= 1.4.0b1

%description
This program reformat and beautify PHP 4 and PHP 5 source code files
automatically. The program is Open Source and distributed under the terms
of PHP Licence. It is written in PHP 5 and has a command line tool.

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
%{pear_phpdir}/PHP/Beautifier/Batch/Output/Directory.php
%{pear_phpdir}/PHP/Beautifier/Batch/Output/DirectoryBz2.php
%{pear_phpdir}/PHP/Beautifier/Batch/Output/DirectoryGz.php
%{pear_phpdir}/PHP/Beautifier/Batch/Output/DirectoryTar.php
%{pear_phpdir}/PHP/Beautifier/Batch/Output/Files.php
%{pear_phpdir}/PHP/Beautifier/Batch/Output/FilesBz2.php
%{pear_phpdir}/PHP/Beautifier/Batch/Output/FilesGz.php
%{pear_phpdir}/PHP/Beautifier/Batch/Output/FilesTar.php
%{pear_phpdir}/PHP/Beautifier/Batch/Output.php
%{pear_phpdir}/PHP/Beautifier/Filter/ArrayNested.filter.php
%{pear_phpdir}/PHP/Beautifier/Filter/Default.filter.php
%{pear_phpdir}/PHP/Beautifier/Filter/IndentStyles.filter.php
%{pear_phpdir}/PHP/Beautifier/Filter/ListClassFunction.filter.php
%{pear_phpdir}/PHP/Beautifier/Filter/Lowercase.filter.php
%{pear_phpdir}/PHP/Beautifier/Filter/NewLines.filter.php
%{pear_phpdir}/PHP/Beautifier/Filter/phpBB.filter.php
%{pear_phpdir}/PHP/Beautifier/Filter/Pear.filter.php
%{pear_phpdir}/PHP/Beautifier/StreamWrapper/Tarz.php
%{pear_phpdir}/PHP/Beautifier/Batch.php
%{pear_phpdir}/PHP/Beautifier/Common.php
%{pear_phpdir}/PHP/Beautifier/Decorator.php
%{pear_phpdir}/PHP/Beautifier/Exception.php
%{pear_phpdir}/PHP/Beautifier/Filter.php
%{pear_phpdir}/PHP/Beautifier/StreamWrapper.php
%{pear_phpdir}/PHP/Beautifier/Tokenizer.php
%{pear_phpdir}/PHP/Beautifier.php
%{pear_datadir}/PHP_Beautifier
%{pear_testdir}/PHP_Beautifier
%{_bindir}/php_beautifier
%{_bindir}/php_beautifier.bat

%changelog
