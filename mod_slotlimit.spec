Name:           mod_slotlimit
Version:        1.1
Release:        1%{?dist}
Summary:        An apache module for managing resources by virtualhost
Group:          System Environment/Daemons
License:        GPL
URL:            http://sourceforge.net/projects/mod-slotlimit/
Source0:        http://heanet.dl.sourceforge.net/sourceforge/mod-slotlimit/%{name}.tar.gz
Source1:        slotlimit.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  httpd-devel



%description
mod_slotlimit is an Apache module that by using dynamic slot allocation algorithm
and static rules, can manage resources used for each running site.


%prep
%setup -q -n %{name}-%{version}


%build
cd src
%{_sbindir}/apxs -c mod_slotlimit.c


%install
pushd src
rm -rf $RPM_BUILD_ROOT
mkdir -pm 755 \
    $RPM_BUILD_ROOT%{_libdir}/httpd/modules \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -pm 755 .libs/mod_slotlimit.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/
popd

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE Readme
%config(noreplace) %{_sysconfdir}/httpd/conf.d/slotlimit.conf
%{_libdir}/httpd/modules/mod_slotlimit.so


%changelog
* Tue Oct 06 2009 David Hrbáč <david@hrbac.cz> - 1.1-1
- rebuild

* Wed May 20 2009 Lucian <lucian@evenstar.lastdot.org> 2.5-1
- Initial build for Centos
