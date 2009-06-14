%define svn svn20061123
Name:           postfix-pfloggrep
Version:        0.5
Release:        1.%{svn}%{?dist}
Summary:        pfloggrep -- where the heck is my mai

Group: 		System Environment/Daemons
License:        Own
URL:            http://www.dt.e-technik.uni-dortmund.de/~ma/postfix/
Source0:        http://home.pages.de/~mandree/postfix/pfloggrep.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

%description
This script takes one or more message-IDs and looks up associated
information (information with the same queue ID as the cleanup log
entry for the given message-IDs) in the log.

%prep
%setup -q -c -T
cp -p %{SOURCE0} ./pfloggrep.sh
sed -i 's/log=\/var\/log\/mail/log=\/var\/log\/maillog/'  pfloggrep.sh

%build

%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 755 pfloggrep.sh $RPM_BUILD_ROOT%{_bindir}/pfloggrep


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/pfloggrep


%changelog
* Thu Jun 11 2009 David Hrbáč <david@hrbac.cz> - 0.5-1
- initial build

