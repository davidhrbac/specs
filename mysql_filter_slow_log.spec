Name:           mysql-log-filter
Version:        1.9b
Release:        1%{?dist}
Summary:        MySQL high performance tuning script

Group:          Applications/Databases
License:        GPLv2
URL:            http://code.google.com/p/mysql-log-filter/
Source0:        http://mysql-log-filter.googlecode.com/files/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
Requires:       mysql
Requires:       which
Requires:       python-sqlite2

%description
MySQLTuner is a script written in Perl that will assist you with your
MySQL configuration and make recommendations for increased performance
and stability.  Within seconds, it will display statistics about your
MySQL installation and the areas where it can be improved.


%prep
%setup -q -c -T
cp -p %{SOURCE0} ./mysql_filter_slow_log.py
dos2unix mysql_filter_slow_log.py

%build


%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 755 mysql_filter_slow_log.py $RPM_BUILD_ROOT%{_bindir}/mmysql_filter_slow_log


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/mmysql_filter_slow_log


%changelog
* Mon Oct 13 2008 David Hrbáč <david@hrbac.cz> - 0.9.9-1
- initial build
