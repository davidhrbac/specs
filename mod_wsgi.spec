Name:           mod_wsgi
Version:        3.1
Release:        1%{?dist}
Summary:        A WSGI interface for Python web applications in Apache

Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://modwsgi.org
Source0:        http://modwsgi.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:        wsgi.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       httpd-devel

BuildRequires:  httpd-devel
BuildRequires:  python-devel


%description
The mod_wsgi adapter is an Apache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is written completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENCE README
%config(noreplace) %{_sysconfdir}/httpd/conf.d/wsgi.conf
%{_libdir}/httpd/modules/mod_wsgi.so


%changelog
* Tue Mar 09 2010 David Hrbáč <david@hrbac.cz> - 3.1-1
- new upstream release

* Sun Sep 21 2008 David Hrbáč <david@hrbac.cz> - 2.1-1
- new upstream version

* Sat Sep 20 2008 David Hrbáč <david@hrbac.cz> - 1.3-3
- initial rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3-3
- Autorebuild for GCC 4.3

* Sun Jan 06 2008 James Bowes <jbowes@redhat.com> 1.3-2
- Require httpd

* Sat Jan 05 2008 James Bowes <jbowes@redhat.com> 1.3-1
- Update to 1.3

* Sun Sep 30 2007 James Bowes <jbowes@redhat.com> 1.0-1
- Initial packaging for Fedora

