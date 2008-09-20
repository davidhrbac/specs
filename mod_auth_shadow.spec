Name:		mod_auth_shadow
Version:	2.2
Release:	4%{?dist}
Source:		http://downloads.sourceforge.net/mod-auth-shadow/%{name}-%{version}.tar.gz
Source1:	mod_auth_shadow.conf
URL:		http://mod-auth-shadow.sourceforge.net
License:	GPL
Group:		System Environment/Daemons
Summary:	An Apache module for authentication using /etc/shadow
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	httpd-devel
%description

When performing this task one encounters one fundamental
difficulty: The /etc/shadow file is supposed to be
read/writeable only by root.  However, the webserver is
supposed to run under a non-root user, such as "nobody".

mod_auth_shadow addresses this difficulty by opening a pipe
to an suid root program, validate, which does the actual
validation.  When there is a failure, validate writes an
error message to the system log, and waits three seconds
before exiting.

%prep
%setup -q

sed -i 's#/usr/local#/usr#' makefile
sed -i 's/chown/#chown/' makefile
sed -i 's/chmod/#chmod/' makefile

%build
gcc -o validate validate.c -lcrypt
make %{?_smp_mflags} all

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/httpd/modules
mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
install validate $RPM_BUILD_ROOT/%{_sbindir}
install .libs/mod_auth_shadow.so $RPM_BUILD_ROOT/%{_libdir}/httpd/modules
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/conf.d/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(4755,root,root) %{_sbindir}/validate
%{_libdir}/httpd/modules/*
%attr(0644,root,root) %config(noreplace) /etc/httpd/conf.d/%{name}.conf
%doc CHANGES INSTALL README COPYING

%changelog
* Wed Sep 17 2008 David Hrbáč <david@hrbac.cz> - 2.2-4
- initial rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.2-4
- Autorebuild for GCC 4.3

* Tue Apr 03 2007 David Anderson <fedora-packaging@dw-perspective.org.uk> 2.2-3
- Removed chmod/chown from makefile (sometimes caused root builds to fail)

* Mon Apr 02 2007 David Anderson <fedora-packaging@dw-perspective.org.uk> 2.2-1
- Upstream new release (includes license file)

* Sat Mar 24 2007 David Anderson <fedora-packaging@dw-perspective.org.uk> 2.1-3
- First packaging for Fedora Extras (modified from upstream spec file)
