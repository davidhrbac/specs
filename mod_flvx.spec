Name:           mod_flvx
Version:        1.0
Release:        1.%{?dist}
Summary:        An Apache 2.2 module for Flash Video Streaming.
Group:          System Environment/Daemons
License:        Apache License 2.0
URL:            http://journal.paul.querna.org/articles/2006/07/11/mod_flvx/
Source0:        http://people.apache.org/~pquerna/modules/mod_flvx.c
Source1:        flvx.conf
BuildRoot:      %{_tmppath}/%{name}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  httpd-devel

%description
mod_flvx is an Apache 2.2 module for Flash Video Streaming.

%prep
#%setup -q -n %{name}-%{version}

%build
cp %{SOURCE0} .
%{_sbindir}/apxs -c mod_flvx.c

%install
rm -rf $RPM_BUILD_ROOT
mkdir -pm 755 \
    $RPM_BUILD_ROOT%{_libdir}/httpd/modules \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -pm 755 .libs/mod_flvx.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/flvx.conf
%{_libdir}/httpd/modules/mod_flvx.so

%changelog
* Tue Oct 06 2009 David Hrbáč <david@hrbac.cz> - 1.0-1
- rebuild

* Tue May 26 2009 Lucian <lucian@evenstar.lastdot.org> 1.0
- Initial build for Centos
