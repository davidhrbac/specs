%define with_java %{?_without_java: 0} %{?!_without_java: 1}
%define with_php %{?_without_php: 0} %{?!_without_php: 1}
%define with_python %{?_without_python: 0} %{?!_without_python: 1}
%define with_wsf %{?_without_wsf: 0} %{?!_without_wsf: 1}
%define php_version %(php-config --version | cut -d. -f1)
%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)

%define with_java 0
%define with_php 0
%define with_python 0

Summary: Liberty Alliance Single Sign On
Name: lasso
Version: 2.2.1
Release: 1%{?dist}
License: GPL
Group: System Environment/Libraries
Source: https://labs.libre-entreprise.org/frs/download.php/594/lasso-%{version}.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%(id -u -n)
%if %{with_wsf}
BuildRequires: cyrus-sasl-devel
%endif
BuildRequires: glib2-devel, swig >= 1.3.28
BuildRequires: libxml2-devel, xmlsec1-devel >= 1.2.6
BuildRequires: openssl-devel, xmlsec1-openssl-devel >= 1.2.6
Requires: libxml2, xmlsec1 >= 1.2.6
Requires: openssl, xmlsec1-openssl >= 1.2.6
Url: http://lasso.entrouvert.org/

%description
Lasso is the first GPLed implementation library of the Liberty Alliance standards.

Lasso allows to manage the federation of scattered identities and Single Sign On.
Using Lasso and respecting the Liberty Alliance standards, is the way to couple
the needs for a strong authentication with an absolute respect of the users private life.

%package devel
Summary: Header files and libraries for %{name} development.
Group: Development/Libraries
BuildRequires: gtk-doc, python-docutils
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%package perl
Summary: Perl Bindings for %{name}
Group: Development/Libraries
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: %{name} = %{version}-%{release}
Obsoletes: perl-%{name} < %{version}-%{release}
Provides: perl-%{name} = %{version}-%{release}

%description perl
The %{name}-perl package contains a module that permits applications
written in Perl programming language to use the interface
supplied by %{name}.

%if %{with_java}
%package java
Summary: Java module for %{name}
Group: Development/Libraries
BuildRequires: java-devel >= 1.4.2
BuildRequires: python-lxml
Requires: jre-gcj >= 1.4.2, jpackage-utils >= 1.5
Requires: %{name} = %{version}-%{release}
Obsoletes: java-%{name} < %{version}-%{release}
Provides: java-%{name} = %{version}-%{release}

%description java
The %{name}-java package contains a module that permits applications
written in Java programming language to use the interface
supplied by %{name}.
%endif

%if %{with_php}
%package php
Summary: PHP module for %{name}
Group: Development/Libraries
BuildRequires: php-devel >= 4.0, expat-devel
BuildRequires: python-lxml
Requires: php >= 4.0
Requires: %{name} = %{version}-%{release}
Obsoletes: php-%{name} < %{version}-%{release}
Provides: php-%{name} = %{version}-%{release}

%description php
The %{name}-php package contains a module that permits applications
written in PHP programming language to use the interface
supplied by %{name}.
%endif

%if %{with_python}
%package python
Summary: Python Bindings for %{name}
Group: Development/Libraries
BuildRequires: python-devel
BuildRequires: python-lxml
Requires: python >= %{python_version}
Requires: %{name} = %{version}-%{release}
Obsoletes: python-%{name} < %{version}-%{release}
Provides: python-%{name} = %{version}-%{release}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib(1)')}
# eval to 2.3 if python isn't yet present, workaround for no python in fc4 minimal buildroot
%{!?python_version: %define python_version %(%{__python} -c 'import sys; print sys.version.split(" ")[0]' || echo "2.3")}

%description python
The %{name}-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by %{name}.
%endif

%prep
%setup -q -n %{name}-%{version}

%build
%configure --prefix=%{_prefix} \
	%if !%{with_java}
	   --disable-java \
	%endif
	%if !%{with_python}
	   --disable-python \
	%endif
	%if %{with_php}
	   --enable-php%{php_version}=yes \
           --with-php%{php_version}-extension-dir=%{php_extdir} \
           --with-php5-config-dir=/etc/php.d \
	%else
	   --enable-php4=no \
	   --enable-php5=no \
	%endif
	%if %{with_wsf}
           --enable-wsf \
           --with-sasl2 \
	%endif
           --enable-gtk-doc \
	   --with-html-dir=%{_datadir}/gtk-doc/html/%{name} 

%install
rm -rf %{buildroot}

install -m 755 -d %{buildroot}%{_datadir}/gtk-doc/html/%{name}

make install exec_prefix=%{_prefix} DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.la' -exec rm -f {} \;

# Perl subpackage
find %{buildroot} \( -name perllocal.pod -o -name .packlist \) -exec rm -v {} \;

find %{buildroot}/usr/lib/perl5 -type f -print |
        sed "s@^%{buildroot}@@g" |
        grep -v perllocal.pod |
        grep -v "\.packlist" > %{name}-perl-filelist
if [ "$(cat %{name}-perl-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi

%if %{with_php}
# PHP subpackage
install -m 755 -d %{buildroot}%{_sysconfdir}/php.d

cat > %{buildroot}%{_sysconfdir}/php.d/%{name}.ini <<EOF
; Enable %{name} extension module
extension=%{name}.so
EOF
%endif

%post
/sbin/ldconfig 2>/dev/null

%postun
/sbin/ldconfig 2>/dev/null

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%{_libdir}/*.so*

%files devel
%defattr(-,root,root)
%doc %{_defaultdocdir}/%{name}
%doc %{_datadir}/gtk-doc/html/%{name}
%{_libdir}/pkgconfig/lasso.pc
%{_includedir}/%{name}
%{_libdir}/*.a
%if %{with_java}
%{_libdir}/java/*.a
%endif

%files perl -f %{name}-perl-filelist
%defattr(-,root,root)

%if %{with_java}
%files java
%defattr(-,root,root)
%{_libdir}/java/*.so
%{_datadir}/java/*.jar
%endif

%if %{with_php}
%files php
%defattr(-,root,root)
%attr(755,root,root) %{php_extdir}/*
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php.d/%{name}.ini
%endif

%if %{with_python}
%files python
%defattr(-,root,root)
%{python_sitearch}/*
%endif

%changelog
* Mon Oct 13 2008 David Hrbáč <david@hrbac.cz> - 2.2.1-1
- initial rebuild

* Fri Oct 03 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.2.1-1%{?dist}
- Updated to final 2.2.1
- Rebuilt on CentOS 4,5 and Fedora 9

* Mon May 05 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.2.0-1%{?dist}
- Updated to final 2.2.0
- Rebuilt on CentOS 4,5 and Fedora 8

* Mon Apr 28 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.98-1%{?dist}
- Updated to test 2.1.98 (Fix CentOS 4 build)
- Rebuilt on CentOS 4,5 and Fedora 8

* Mon Apr 21 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.97-1%{?dist}
- Updated to test 2.1.97
- Added missing BuildRequires expat-devel for php package
- Added missing BuildRequires python-devel for python package
- Rebuilt on CentOS 4,5 and Fedora 8

* Tue Apr 08 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.96-1%{?dist}
- Updated to test 2.1.96 (Fix ElementTree build)
- Added missing BuildRequires python-lxml instead of
  python-elementtree for java, php and python packages
- Added missing BuildRequires glib2-devel
- Added missing BuildRequires cyrus-sasl-devel and
  added conditionnal build support for ID-WSF
- Rebuilt on CentOS 5 and Fedora 8

* Mon Apr 07 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.95-1%{?dist}
- Updated to test 2.1.95 (Fix ID-WSF changes)
- Changed BuildRequires gcc-java to java-devel
- Rebuilt on CentOS 5

* Wed Apr 02 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.94-1%{?dist}
- Updated to test 2.1.94 (Fix ID-WSF changes)
- Rebuilt on CentOS 5

* Fri Mar 28 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.93-1%{?dist}
- Updated to test 2.1.93 (Fix for Java Bindings and WSF changes)
- Rebuilt on CentOS 5

* Fri Mar 14 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.92-1%{?dist}
- Updated to test 2.1.92 (Fix for Java Bindings)
- Rebuilt on CentOS 5

* Fri Mar 14 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.91-1%{?dist}
- Updated to test 2.1.91 (Fix for Java Bindings)
- Rebuilt on CentOS 5

* Thu Feb 28 2008 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.9-1%{?dist}
- Updated to test 2.1.9 (New Java and PHP Bindings !)
- Rebuilt on CentOS 5

* Mon Aug 23 2007 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.1-1%{?dist}
- Updated to 2.1.1 
- Rebuilt on CentOS 5

* Mon Aug 13 2007 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.1.0-1%{?dist}
- Updated to 2.1.0 
- Removed static librairies
- Rebuilt on CentOS 5

* Mon Jan 22 2007 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 2.0.0-1%{?dist}
- Updated to 2.0.0 
- Disabled swig broken support for PHP version 5
- Changed %doc to %{_datadir}/gtk-doc/html/lasso/* in devel subpackage
- Built on Fedora Core 3 / RHEL 4 and Fedora Core 6 / RHEL 5

* Wed Dec 20 2006 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 1.9.9-1
- Updated to test 1.9.9 (SAML 2.0 full support !)
- Changed Provides/Obsoletes to follow new Fedora naming rules
- Choosed BuildRequires to be more OpenSUSE/Mandriva compliant
- Added php_extdir macro to support both PHP version 4 and 5
- Built on Fedora Core 3 / RHEL 4 and Fedora Core 6 / RHEL 5

* Mon Oct 23 2006 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 0.6.6-1
- Updated to 0.6.6
- Added conditional build for java, php, python
- Built on Fedora Core 3 / RHEL 4

* Mon Jun 12 2006 Jean-Marc Liger <jmliger@siris.sorbonne.fr> 0.6.5-1
- First 0.6.5
- Built on Fedora Core 3 / RHEL 4
