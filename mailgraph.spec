# Only Fedora & RHEL 5+ can use selinux
%if 0%{?rhel} && "%rhel" < "5"
%define without_selinux 1
%endif

%define selinux_variants mls strict targeted

Name:           mailgraph
Version:        1.14
Release:        7%{?dist}%{?repotag:.%{repotag}}
Summary:        A RRDtool frontend for Mail statistics

Group:          System Environment/Daemons
License:        GPL+

URL:            http://mailgraph.schweikert.ch/
Source0:        http://mailgraph.schweikert.ch/pub/%{name}-%{version}.tar.gz
Source1:        mailgraph.init
Source2:        mailgraph.conf
Source3:        mailgraph.sysconfig
Source4:        mailgraph.te
Source5:        mailgraph.fc
Source6:        mailgraph.if
Patch0:         paths.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if ! 0%{?without_selinux}
BuildRequires:  checkpolicy, selinux-policy-devel, hardlink
%endif

Requires:       perl(File::Tail), rrdtool, httpd
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       initscripts

BuildArch:      noarch

%description
Mailgraph is a very simple mail statistics RRDtool frontend for Postfix and
Sendmail that produces daily, weekly, monthly and yearly graphs of
received/sent and bounced/rejected mail.

%if ! 0%{?without_selinux}
%package selinux
Summary:        A RRDtool frontend for Mail statistics

Group:          System Environment/Daemons
%define selinux_policyver %(sed -e 's,.*selinux-policy-\\([^/]*\\)/.*,\\1,' /usr/share/selinux/devel/policyhelp) 
%if "%{selinux_policyver}" != ""
Requires:       selinux-policy >= %{selinux_policyver}
%endif
Requires:       %{name} = %{version}-%{release}

Requires(post):   /usr/sbin/semodule, /sbin/restorecon, /sbin/fixfiles, %{name}
Requires(postun): /usr/sbin/semodule, /sbin/restorecon, /sbin/fixfiles, %{name}

%description selinux
This is the selinux policy for mailgraph.
%endif


%prep
%setup -q
%patch0 -p1 -b .paths

%if ! 0%{?without_selinux}
mkdir selinux
cp -p %{SOURCE4} %{SOURCE5} %{SOURCE6} ./selinux/
%endif

%build
%if ! 0%{?without_selinux}
cd selinux
for selinuxvariant in %{selinux_variants}; do
  make NAME=${selinuxvariant} -f %{_datadir}/selinux/devel/Makefile
  mv %{name}.pp %{name}.pp.${selinuxvariant}
  make NAME=${selinuxvariant} -f %{_datadir}/selinux/devel/Makefile clean
done
cd -
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__install} -d -m 0755 $RPM_BUILD_ROOT/%{_sbindir}
%{__install} -d -m 0755 $RPM_BUILD_ROOT/%{_initrddir}
%{__install} -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
%{__install} -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d
%{__install} -d -m 0755 $RPM_BUILD_ROOT/%{_datadir}/mailgraph
%{__install} -d -m 0755 $RPM_BUILD_ROOT/%{_localstatedir}/lib/mailgraph
%{__install} -d -m 0775 $RPM_BUILD_ROOT/%{_localstatedir}/cache/mailgraph

%{__install} -p -m 0755 mailgraph.cgi $RPM_BUILD_ROOT/%{_datadir}/mailgraph
%{__install} -p -m 0644 mailgraph.css $RPM_BUILD_ROOT/%{_datadir}/mailgraph
%{__install} -p -m 0755 mailgraph.pl $RPM_BUILD_ROOT/%{_sbindir}/mailgraph
%{__install} -p -m 0755 %SOURCE1 $RPM_BUILD_ROOT/%{_initrddir}/mailgraph
%{__install} -p -m 0644 %SOURCE2 $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/
%{__install} -p -m 0644 %SOURCE3 $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/mailgraph

%if ! 0%{?without_selinux}
cd selinux
for selinuxvariant in %{selinux_variants}; do
  install -d $RPM_BUILD_ROOT/%{_datadir}/selinux/${selinuxvariant}
  install -p -m 644 %{name}.pp.${selinuxvariant} \
    $RPM_BUILD_ROOT/%{_datadir}/selinux/${selinuxvariant}/%{name}.pp
done
cd -

# Hardlink identical policy module packages together
/usr/sbin/hardlink -cv $RPM_BUILD_ROOT/%{_datadir}/selinux
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name} 2>&1 > /dev/null || :

if [ "$1" -ge "1" ]; then
  /sbin/service %{name} condrestart 2>&1 > /dev/null || :
fi

%preun
if [ $1 = 0 ]; then
  /sbin/service %{name} stop 2>&1 > /dev/null || :
  /sbin/chkconfig --del %{name} 2>&1 > /dev/null || :
fi
exit 0

%postun
if [ "$1" -ge "1" ]; then
  /sbin/service %{name} condrestart 2>&1 > /dev/null || :
fi

%if ! 0%{?without_selinux}
%post selinux
/sbin/service %{name} status &> /dev/null ||:
STATUS=$?

if [ $STATUS -eq 0 ]; then
  /sbin/service %{name} stop &> /dev/null ||:
fi

for selinuxvariant in %{selinux_variants}; do
  /usr/sbin/semodule -s ${selinuxvariant} -i \
    %{_datadir}/selinux/${selinuxvariant}/%{name}.pp &> /dev/null || :
done

if [ $STATUS -eq 0 ]; then
  /sbin/service %{name} start &> /dev/null ||:
fi

# Fix up non-standard file contexts
/sbin/fixfiles -R %{name} restore || :
/sbin/restorecon -R %{_localstatedir}/cache/%{name} || :

%postun selinux
# Clean up after package removal
if [ $1 -eq 0 ]; then
  /sbin/service %{name} status &> /dev/null ||:
  STATUS=$?

  if [ $STATUS -eq 0 ]; then
    /sbin/service %{name} stop &> /dev/null ||:
  fi

  # Remove SELinux policy modules
  for selinuxvariant in %{selinux_variants}
  do
    /usr/sbin/semodule -s ${selinuxvariant} -r %{name} &> /dev/null || :
  done

  if [ $STATUS -eq 0 ]; then
    /sbin/service %{name} start &> /dev/null ||:
  fi

  /sbin/fixfiles -R %{name} restore || :

  # Clean up any remaining file contexts (shouldn't be any really)
  [ -d %{_localstatedir}/cache/%{name} ] && \
    /sbin/restorecon -R %{_localstatedir}/cache/%{name} &> /dev/null || :
fi
%endif

%files
%defattr(-,root,root,-)
%dir %{_localstatedir}/lib/mailgraph
%dir %attr(0775,root,apache) %{_localstatedir}/cache/mailgraph
%{_sbindir}/*
%{_datadir}/mailgraph
%{_initrddir}/mailgraph
%config(noreplace) %{_sysconfdir}/sysconfig/mailgraph
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mailgraph.conf
%doc CHANGES COPYING README

%if ! 0%{?without_selinux}
%files selinux
%defattr(-,root,root,-)
%{_datadir}/selinux/*/%{name}.pp
%doc selinux/*
%endif

%changelog
* Tue Jun 01 2010 David Hrbáč <david@hrbac.cz> - 1.14-7
- fixed script permissions

* Tue Jun 01 2010 David Hrbáč <david@hrbac.cz> - 1.14-6
- fixed missing mailgraph.css

* Fri Oct 30 2009 David Hrbáč <david@hrbac.cz> - 1.14-5
- initial rebuild
- patch to build on C4

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 30 2008 Bernard Johnson <bjohnson@symetrix.com> - 1.14-3
- fix patch fuzz

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.14-2
Rebuild for new perl

* Tue Oct 30 2007 Bernard Johnson <bjohnson@symetrix.com> - 1.14-1
- v 1.14
- fix broken URLs (bz #251280)
- selinux policy fu (bz #243302)
- Mailgraph needs AddHandler cgi-script .cgi (bz #289021)
- Make initscript LSB compliant (bz #246977)

* Sun Mar 25 2007 Bernard Johnson <bjohnson@symetrix.com> - 1.12-5
- require initscripts because initfile uses daemon function
- use perl(...) requires (bz #233769)
- use /sbin/service instead of invoking initscript directly
- one line under %%files to own both %%{_datadir} and files below it

* Sun Jan 28 2007 Bernard Johnson <bjohnson@symetrix.com> - 1.12-4
- replace %%{_var} with %%{_localstatedir}

* Sun Jan 28 2007 Bernard Johnson <bjohnson@symetrix.com> - 1.12-3
- consistent use of mode in creating directories
- add Requires for httpd
- preserve timestamps on install

* Sat Jan 27 2007 Bernard Johnson <bjohnson@symetrix.com> - 1.12-2
- add Requires(preun), Requires(post) for chkconfig

* Sat Jan 13 2007 Bernard Johnson <bjohnson@symetrix.com> - 1.12-1
- initial release
