Name:           mysqltuner
Version:        1.1.0
Release:        2%{?dist}
Summary:        MySQL high performance tuning script

Group:          Applications/Databases
License:        GPLv3+
URL:            http://mysqltuner.com/
#ource0:        http://mysqltuner.com/releases/mysqltuner-%{version}.pl
#ource0:        http://github.com/rackerhacker/MySQLTuner-perl/tarball/master
Source0:        http://mysqltuner.pl/mysqltuner.pl
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
Requires:       mysql
Requires:       which

%description
MySQLTuner is a script written in Perl that will assist you with your
MySQL configuration and make recommendations for increased performance
and stability.  Within seconds, it will display statistics about your
MySQL installation and the areas where it can be improved.


%prep
%setup -q -c -T
cp -p %{SOURCE0} ./mysqltuner.pl


%build


%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 755 mysqltuner.pl $RPM_BUILD_ROOT%{_bindir}/mysqltuner


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/mysqltuner


%changelog
* Wed Sep 16 2009 David Hrbáč <david@hrbac.cz> - 1.1.0-1
- new upstream version

* Thu Dec  9 2008 David Hrbáč <david@hrbac.cz> - 1.0.0-1
- new upstream version

* Mon Oct 13 2008 David Hrbáč <david@hrbac.cz> - 0.9.9-1
- initial rebuild

* Thu Sep 11 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.9.9-1
- 0.9.9.
- Update description.

* Mon Jul 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.9.8-1
- 0.9.8, --checkversion patch applied upstream.

* Sat Jun 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.9.1-4
- Don't warn if --skipversion is used (#452172).

* Thu Jun 19 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.9.1-1
- 0.9.1.
- Patch to not "phone home" by default (--skipversion -> --checkversion).

* Sat Apr 12 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.9.0-1
- 0.9.0.

* Sun Mar  2 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.8.6-1
- 0.8.6.

* Mon Feb 18 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.8.5-1
- 0.8.5.
