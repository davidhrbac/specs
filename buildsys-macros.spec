Name:		buildsys-macros
Summary:	Macros for building Fedora Linux packages
Version:	5
Release:	1%{?dist}
License:	GPL
Group:		Development/Buildsystem
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Buildarch:  noarch

%description
Macros for the Fedora Buildsystem

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/rpm/
VERSION=%{version}
printf %s%b "%" "rhel $VERSION\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/etc/rpm/macros.disttag

%changelog
* Wed Jul 12 2006 David Lutterkort <dlutter@redhat.com> - 4-1
- Adapted to RHEL builds

* Tue May 10 2005 Tom "spot" Callaway <tcallawa@redhat.com>
- Initial build.
