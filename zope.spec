%define python_minver 2.4.3

%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define zope_user      zope
%define zope_group     %{zope_user}

%define zope_home      %{_libdir}/zope
%define software_home  %{zope_home}/lib/python
%define instance_home  %{_localstatedir}/lib/zope

%define zopectl        %{_bindir}/zopectl
%define runzope        %{_bindir}/runzope

Name:    zope
Summary: Web application server for flexible content management applications
Version: 2.10.6
Release: 1%{?dist}
License: ZPL
Group: 	 System Environment/Daemons
URL:     http://www.zope.org/
Source0: http://www.zope.org/Products/Zope/2.10.6/Zope-2.10.6-final.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1: zope.init.in
Source2: zope.sysconfig.in
Source3: zope.zopectl.in
Source4: zope-README.Fedora
Source5: zope.logrotate.in
Source6: zope.logrotate.cron.in
Patch0: zope-2.10.4-config.patch
Patch1: zope-2.10.6-configure.patch

BuildRequires: python-devel >= %{python_minver}, python >= %{python_minver} 
Requires:      python >= %{python_minver}, libxml2-python, python-elementtree

Requires(pre): /usr/sbin/useradd
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service

%description
Zope is an application server framework that enables developers to quickly
build web applications such as intranets, portals, and content management
systems.

Zope, by default, will listen on port 8080.

%prep
%setup -q -n Zope-%{version}-final
%patch0 -p0
%patch1 -p1

chmod -x skel/import/README.txt
install -pm 644 %{SOURCE4} README.Fedora
install -pm 644 %{SOURCE5} skel/etc/logrotate.conf.in


%build
rm -rf $RPM_BUILD_ROOT # Configure checks for it
./configure \
  --prefix=$RPM_BUILD_ROOT%{zope_home} \
#  --with-python=%{_bindir}/python
  
#    --no-compile

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

# Create all required additional directories
for dir in %{zope_home} %{software_home} %{instance_home}/{Products,bin,var} \
    %{_sysconfdir}/sysconfig %{_bindir}; do
    install -d $RPM_BUILD_ROOT$dir
done


install -D -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/zope
install -D -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/zope
install -D -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/zopectl
install -D -m 755 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/zope-logrotate
perl -pi -e 's,<<SYSCONFDIR>>,%{_sysconfdir},g;
             s,<<BINDIR>>,%{_bindir},g;
             s,<<LOCALSTATEDIR>>,%{_localstatedir},g;
             s,<<ZOPE_USER>>,%{zope_user},g' \
    $RPM_BUILD_ROOT%{_initrddir}/zope \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/zope \
    $RPM_BUILD_ROOT%{_bindir}/zopectl \
    $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/zope-logrotate \
    README.Fedora skel/etc/zope.conf.in

# Install the skel, translating paths, into the build root
%{__python} "utilities/copyzopeskel.py" \
     --sourcedir="skel" \
     --targetdir="$RPM_BUILD_ROOT%{instance_home}" \
     --replace="INSTANCE_HOME:%{instance_home}" \
     --replace="SOFTWARE_HOME:%{software_home}" \
     --replace="ZOPE_HOME:%{zope_home}" \
     --replace="PYTHON:%{__python}" \

# Actually copy all the other files over
make install

chmod 750 $RPM_BUILD_ROOT%{instance_home}

# Fix permissions, must have changed in the upstream tar
chmod 755 $RPM_BUILD_ROOT%{instance_home}/bin/zopectl
chmod 755 $RPM_BUILD_ROOT%{instance_home}/bin/runzope

# Set needed permissions
# We might go as far as to only allow zope r/w to the .pyc files
for dir in %{instance_home}/{Products,log,lib,var}; do
    chmod 775 $RPM_BUILD_ROOT$dir
done

chmod 755 $RPM_BUILD_ROOT%{zope_home}

# included in %%doc
rm -rf $RPM_BUILD_ROOT%{zope_home}/doc

# write version.txt
echo "Zope %{version}-%{release}" > \
    "$RPM_BUILD_ROOT%{software_home}/version.txt"

# write zope.pth
install -d $RPM_BUILD_ROOT%{python_sitearch}
echo "%{software_home}" > \
    "$RPM_BUILD_ROOT%{python_sitearch}/zope.pth"

# Compile .pyc
%{__python} -c "import compileall; \
    compileall.compile_dir(\"$RPM_BUILD_ROOT%{zope_home}\", \
    ddir=\"%{zope_home}\", force=1)"



%clean
rm -rf $RPM_BUILD_ROOT


%pre
%{_sbindir}/useradd -c "Zope user" -s /bin/false -r -d %{zope_home} \
    %{zope_user} 2>/dev/null || :


%post
# add zope init to runlevels
/sbin/chkconfig --add zope


%preun
if [ $1 -eq 0 ]; then
  /sbin/service zope stop >/dev/null 2>&1
  /sbin/chkconfig --del zope
fi



%files 
%defattr(-, root, root, -)
%doc doc/* README.Fedora ZopePublicLicense.txt
%config(noreplace) %{_sysconfdir}/sysconfig/zope
%config %{_initrddir}/zope
%config %{_sysconfdir}/cron.daily/zope-logrotate
%attr(0755, root, root) %{_bindir}/zopectl
%dir %{zope_home}
%{zope_home}/bin
%{zope_home}/lib
%dir %{zope_home}/skel
%{zope_home}/skel/bin
%{zope_home}/skel/Extensions
%{zope_home}/skel/import
%{zope_home}/skel/log
%{zope_home}/skel/lib
%{zope_home}/skel/Products
%{zope_home}/skel/README.txt
%{zope_home}/skel/var
%config %{zope_home}/skel/etc
%attr(-, root, %{zope_group}) %{instance_home}/*
%{python_sitearch}/zope.pth


%changelog
* Fri Sep 24 2008 David Hrbáč <david@hrbac.cz> - 2.10.6-1
- initial rebuild

* Sun May 11 2008 Jonathan Steffan <jon a fedoraunity.org> 2.10.6-1
- Update to 2.10.6
- Add a patch to allow python 2.4.3

* Thu Nov 8 2007 Jonathan Steffan <jon a fedoraunity.org> 2.10.5-2
- Update permissions for zopectl and runzope

* Sat Nov 3 2007 Jonathan Steffan <jon a fedoraunity.org> 2.10.5-1
- Update to zope 2.10.5

* Mon Sep 3 2007 Jonathan Steffan <jon a fedoraunity.org> 2.10.4-3
- Updated Requires for libxml2-python and python-elementtree

* Tue Aug 14 2007 Jonathan Steffan <jon a fedoraunity.org> 2.10.4-2
- Added config patch

* Wed Aug 1 2007 Jonathan Steffan <jon a fedoraunity.org> 2.10.4-1
- Initial Package

