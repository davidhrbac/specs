
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define pyver %(python -c 'import sys ; print sys.version[:3]')

Name:          pyzor
Version:       0.4.0
Release:       11%{?dist}
Summary:       Pyzor collaborative spam filtering system

Group:         Applications/Internet
License:       GPL
URL:           http://pyzor.sourceforge.net/
Source0:       http://easynews.dl.sourceforge.net/sourceforge/pyzor/pyzor-0.4.0.tar.bz2
Source1:       http://easynews.dl.sourceforge.net/sourceforge/pyzor/pyzor-0.4.0.tar.bz2.asc
Patch0:        http://antispam.imp.ch/patches/patch-pyzor-debian-mbox
Patch1:        http://antispam.imp.ch/patches/patch-pyzor-handle_unknown_encodings
Patch2:        http://antispam.imp.ch/patches/patch-pyzor-unknowntype
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
BuildRequires: python >= 2.2.1
Requires:      python = %{pyver}

%description
Pyzor is a collaborative, networked system to detect
and block spam using identifying digests of messages.
Pyzor is similar to Vipul's Razor except implemented
in python, and using fully open source servers.

Pyzor can be used either standalone, or to augment the
spam filtering ability of spamassassin.  spamassassin
is highly recommended.

%prep
%setup -q
# Add mbox handling support
%patch0 -p0
# Handle unknown encodings
%patch1 -p0
# Treat empty messages as text
%patch2 -p0


%build
%__python setup.py build


%install
rm -rf %{buildroot}
install -m755 -d %{buildroot}%{python_sitelib}/pyzor
install -p -m644 build/lib/pyzor/* %{buildroot}%{python_sitelib}/pyzor
install -m755 -d %{buildroot}%{_bindir}
install -p -m755 build/scripts-%{pyver}/* %{buildroot}%{_bindir}
%__python -c 'from compileall import *; compile_dir("'%{buildroot}'/%{python_sitelib}",10,"%{python_sitelib}")'
%__python -O -c 'from compileall import *; compile_dir("'%{buildroot}'/%{python_sitelib}",10,"%{python_sitelib}")'
chmod -R a+rX %{buildroot}/%{python_sitelib}/pyzor $RPM_BUILD_ROOT%{_bindir}/pyzor*


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%dir %{python_sitelib}/pyzor
%doc docs/usage.html COPYING ChangeLog NEWS README THANKS UPGRADING PKG-INFO
%attr(0644,root,root) %{python_sitelib}/pyzor/client.py*
%attr(0644,root,root) %{python_sitelib}/pyzor/server.py*
%attr(0644,root,root) %{python_sitelib}/pyzor/__init__.py*
%attr(0755,root,root) %{_bindir}/pyzor
%attr(0755,root,root) %{_bindir}/pyzord


%changelog
* Wed Mar 19 2008 David Hrbáč <david@hrbac.cz> - 0.4.0-11
- CentOS rebuild

* Sat Dec 23 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.4.0-11
- Rebuild with Python 2.5.

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 0.9.8-10
- FE6 Rebuild
- Feature enhancements by including certain patches from swinog.

* Mon Feb 07 2005 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.4.0-8
- %%ghost *.pyo files.

* Sat Feb 05 2005 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.4.0-7
- Use python_sitelib macro to fix building on x86_64.
- Change byte compile argumetns so we don't encode the buildroot into the
  byte compiled python files.
- Use python-abi for Requires instead of python package.

* Sat Nov 13 2004 Warren Togami <wtogami@redhat.com> - 0.4.0-6
- bump release

* Fri May 21 2004 Warren Togami <wtogami@redhat.com> - 0.4.0-0.fdr.5
- generalize python version

* Fri Jul 11 2003 Warren Togami <warren@togami.com> - 0.4.0-0.fdr.4
- Change to __python macro

* Fri Jun 27 2003 Warren Togami <warren@togami.com> - 0.4.0-0.fdr.3
- #360 add more docs

* Sat Jun 21 2003 Warren Togami <warren@togami.com> - 0.4.0-0.fdr.2
- Fix some directory macros
- #360 Include .pyc and .pyo so package removes cleanly
- #360 install -p preserve timestamps

* Sun Jun 08 2003 Warren Togami <warren@togami.com> - 0:0.4.0-0.fdr.1
- Convert to Fedora

* Fri Jan 31 2003 Shad L. Lords <slords@mail.com>
- 0.4.0-1
- inital release
