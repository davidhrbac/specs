# $Id: php-pecl-ssh2.spec,v 1.1 2008-05-19 11:38:25 dhrbac Exp $
# Authority: stefan

%define php_extdir %(php-config --extension-dir)

Summary: PECL package for SSH2
Name: php-pecl-ssh2
Version: 0.10
Release: 1
License: PHP
Group: Development/Languages
URL: http://pecl.php.net/package/ssh2

Source: http://pecl.php.net/get/ssh2-%{version}.tgz
Packager: Andreas Winkelbauer <andreas.winkelbauer@gmx.at>

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: php, libssh2
BuildRequires: php, php-devel, libssh2-devel,
# Required by phpize
#BuildRequires: autoconf, automake, libtool, gcc-c++

%description
Provides bindings to the functions of libssh2 which implements the SSH2 protocol.
libssh2 is available from http://www.sourceforge.net/projects/libssh2


%prep
%setup -n ssh2-%{version}


%build
# Workaround for broken phpize on 64 bits
%{_bindir}/phpize
%configure
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/ssh2.ini << 'EOF'
; Enable ssh2 extension module
extension=ssh2.so
EOF


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%config(noreplace) %{_sysconfdir}/php.d/ssh2.ini
%{php_extdir}/ssh2.so


%changelog
* Sat Feb 08 2008 Andreas Winkelbauer <andreas.winkelbauer@gmx.at> 0.10-2
- patched ssh2.c (removed #if LIBSSH2_APINO stuff)
- packaged for fedora 7

* Tue Dec 06 2005 Stefan Pietsch <stefan.pietsch@eds.com> 0.10-1 #4261
- update to new release

* Tue Oct 25 2005 Stefan Pietsch <stefan.pietsch@eds.com> 0.9-1
- Initial RPM release.

