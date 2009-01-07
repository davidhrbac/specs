Summary:	C library for parsing command line parameters
Name:		popt
Version:	1.13
Release:	4%{?dist}
License:	MIT
Group:		System Environment/Libraries
URL:		http://www.rpm5.org/
Source0:	http://www.rpm5.org/files/%{name}/%{name}-%{version}.tar.gz
Source1:	http://people.redhat.com/jantill/fedora/png-mtime.py
Patch0:		popt-1.13-multilib.patch
Patch1:		popt-1.13-popt_fprintf.patch
BuildRequires:	gettext, doxygen, graphviz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Popt is a C library for parsing command line parameters. Popt was
heavily influenced by the getopt() and getopt_long() functions, but
it improves on them by allowing more powerful argument expansion.
Popt can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments. Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

%package devel
Summary:	Development files for the popt library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The popt-devel package includes header files and libraries necessary
for developing programs which use the popt C library. It contains the
API documentation of the popt library, too.

%package static
Summary:	Static library for parsing command line parameters
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
The popt-static package includes static libraries of the popt library.
Install it if you need to link statically with libpopt.

%prep
%setup -q
%patch0 -p1 -b .multilib
%patch1 -p1 -b .popt_fprintf

%build
%configure --libdir=/%{_lib}
make %{?_smp_mflags}
doxygen

# Solve multilib problems by changing the internal PNG timestamp to a reference timestamp;
# see http://fedoraproject.org/wiki/PackagingDrafts/MultilibTricks for further information.
if [ $(ls doxygen/html/*{__,graph_legend}*.png 2> /dev/null | wc -l) -gt 0 ]; then
  for png in doxygen/html/*{__,graph_legend}*.png; do python %{SOURCE1} $png CHANGES; done
fi

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Move libpopt.{so,a} to %{_libdir}
rm -f $RPM_BUILD_ROOT/%{_lib}/libpopt.{la,so}
pushd $RPM_BUILD_ROOT/%{_lib}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
ln -sf ../../%{_lib}/$(ls libpopt.so.?.?.?) $RPM_BUILD_ROOT%{_libdir}/libpopt.so
popd
mv -f $RPM_BUILD_ROOT/%{_lib}/libpopt.a $RPM_BUILD_ROOT%{_libdir}/libpopt.a

# Multiple popt configurations are possible
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/popt.d

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc CHANGES COPYING
%{_sysconfdir}/popt.d
/%{_lib}/libpopt.so.*

%files devel
%defattr(-,root,root)
%doc README doxygen/html
%{_libdir}/libpopt.so
%{_includedir}/popt.h
%{_mandir}/man3/popt.3*

%files static
%defattr(-,root,root)
%{_libdir}/libpopt.a

%changelog
* Sun May 25 2008 Robert Scheck <robert@fedoraproject.org> 1.13-4
- Solved multilib problems at doxygen generated files (#342921)

* Wed Feb 20 2008 Robert Scheck <robert@fedoraproject.org> 1.13-3
- Revert the broken bind_textdomain_codeset() patch (#433324)

* Thu Feb 14 2008 Robert Scheck <robert@fedoraproject.org> 1.13-2
- Added patch to work around missing bind_textdomain_codeset()

* Sun Dec 30 2007 Robert Scheck <robert@fedoraproject.org> 1.13-1
- Upgrade to 1.13 (#290531, #332201, #425803)
- Solved multilib problems at doxygen generated files (#342921)

* Thu Aug 23 2007 Robert Scheck <robert@fedoraproject.org> 1.12-3
- Added buildrequirement to graphviz (#249352)
- Backported bugfixes from CVS (#102254, #135428 and #178413)

* Sun Aug 12 2007 Robert Scheck <robert@fedoraproject.org> 1.12-2
- Move libpopt to /lib[64] (#249814)
- Generate API documentation, added buildrequirement to doxygen

* Mon Jul 23 2007 Robert Scheck <robert@fedoraproject.org> 1.12-1
- Changes to match with Fedora Packaging Guidelines (#249352)

* Tue Jul 10 2007 Jeff Johnson <jbj@rpm5.org>
- release popt-1.12 through rpm5.org.

* Sat Jun  9 2007 Jeff Johnson <jbj@rpm5.org>
- release popt-1.11 through rpm5.org.

* Thu Dec 10 1998 Michael Johnson <johnsonm@redhat.com>
- released 1.2.2; see CHANGES

* Tue Nov 17 1998 Michael K. Johnson <johnsonm@redhat.com>
- added man page to default install

* Thu Oct 22 1998 Erik Troan <ewt@redhat.com>
- see CHANGES file for 1.2

* Thu Apr 09 1998 Erik Troan <ewt@redhat.com>
- added ./configure step to spec file
