Name:		hrb-bar
Summary:	Testing package
Version:	1
Release:	1%{?dist}
License:	GPL
Group:		Development/Buildsystem
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Buildarch:  noarch
Obsoletes:	hrb-foo

%description
Testing package

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/
NAME=%{name}
echo $NAME > $RPM_BUILD_ROOT/etc/hrb-bar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/etc/hrb-bar

%changelog
* Tue Mar  3 2009 David Hrbáč <david@hrbac.cz> - 1.1
- initial release
