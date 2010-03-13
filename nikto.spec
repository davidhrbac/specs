Name:           nikto
Version:        2.1.1
Release:        1%{?dist}
Summary:        Web server scanner 

Group:          Applications/Internet
License:        GPLv2+
URL:            http://www.cirt.net/code/nikto.shtml
Source0:        http://www.cirt.net/nikto/%{name}-%{version}.tar.bz2
Source1:        nikto-database-license.txt
#use system libwhisker2
Patch0:         nikto-2.03-libwhisker2.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
Requires:       nmap


%description
Nikto is a web server scanner which performs comprehensive tests against web
servers for multiple items, including over 3300 potentially dangerous
files/CGIs, versions on over 625 servers, and version specific problems
on over 230 servers. Scan items and plugins are frequently updated and
can be automatically updated (if desired).

%prep
#%setup -qn %{name}
%setup -q
#%patch0 -p1

#change configfile path
sed -i 's:$NIKTO{configfile} = "config.txt";:$NIKTO{configfile}="%{_sysconfdir}/nikto/config";:' nikto.pl
sed -i 's:# EXECDIR=/usr/local/nikto:EXECDIR=%{_datadir}/nikto:' config.txt
#enable nmap by default and set plugindir path
sed -i "s:#NMAP=/usr/bin/nmap:NMAP=%{_bindir}/nmap:;
        s:# PLUGINDIR=/usr/local/nikto/plugins:PLUGINDIR=%{_datadir}/nikto/plugins:" config.txt

%build
#no build required


%install
rm -rf $RPM_BUILD_ROOT
cp %{SOURCE1} $RPM_BUILD_DIR/%{name}/database-license.txt
install -pD nikto.pl $RPM_BUILD_ROOT%{_bindir}/nikto
install -m 0644 -pD docs/nikto.1 $RPM_BUILD_ROOT%{_mandir}/man1/nikto.1
mkdir -p $RPM_BUILD_ROOT%{_datadir}/nikto/plugins/
install -m 0644 -p plugins/* $RPM_BUILD_ROOT%{_datadir}/nikto/plugins/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/nikto/templates/
install -m 0644 -p templates/* $RPM_BUILD_ROOT%{_datadir}/nikto/templates/
install -m 0644 -pD config.txt $RPM_BUILD_ROOT%{_sysconfdir}/nikto/config

#remove unneeded files
rm -f $RPM_BUILD_ROOT%{_datadir}/nikto/plugins/LW2.pm

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc docs/CHANGES.txt docs/LICENSE.txt database-license.txt
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/nikto
%{_datadir}/nikto
%{_mandir}/man?/*


%changelog
* Mon Feb 08 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 2.03-3
- Resolve rhbz #515871

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 01 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 2.03-1
- New upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.36-4
- fix license tag

* Wed May 30 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 1.36-3
- Add sed magic to really replace nikto-1.36-config.patch
* Mon May 28 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 1.36-2
- Remove libwhisker Requires
- Replace configfile patch with sed magic
- Update License
- Add database-license.txt to %%doc
* Fri May 04 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 1.36-1
- Initial build
