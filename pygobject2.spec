%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

### Abstract ###

Name: pygobject2
Version: 2.12.1
Release: 5%{?dist}
License: LGPL
Group: Development/Languages
Summary: Python bindings for GObject
URL: http://www.pygtk.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Source: pygobject-%{version}.tar.bz2

### Dependencies ###

#Requires: glib2 >= 2.8
Requires: glib2
#Requires: python2 >= 2.3.5
Requires: python2

### Build Dependencies ###

BuildRequires: automake >= 1.6.3-5
#BuildRequires: glib2-devel >= 2.8
BuildRequires: glib2-devel
BuildRequires: libtool
#BuildRequires: python2-devel >= 2.3.5
BuildRequires: python2-devel

%description
pygobject2 provides a convenient wrapper for the GObject library
for use in Python programs.

%package devel
Summary: Development files for building add-on libraries
Group: Development/Languages
Requires: pygobject2 = %{version}
Requires: pygobject2-doc = %{version}-%{release}
Requires: glib2-devel
Requires: pkgconfig

%description devel
This package contains files required to build wrappers for
pygobject2-based libraries such as pygtk2.

%package doc
Summary: Documentation files for pygobject2
Group: Development/Languages

%description doc
This package contains documentation files for pygobject2.

%prep
%setup -q -n pygobject-%{version}

%build
# --disable-docs doesn't work; it builds the docs anyway.
%configure --enable-thread --disable-docs
export tagname=CC
make LIBTOOL=/usr/bin/libtool

%install
rm -rf $RPM_BUILD_ROOT
export tagname=CC
make LIBTOOL=/usr/bin/libtool DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f

rm examples/Makefile*

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(644, root, root, 755)
%doc AUTHORS NEWS README ChangeLog
%doc examples

%dir %{python_sitearch}/gtk-2.0
%{python_sitearch}/gtk-2.0/dsextras.*
%{python_sitearch}/pygtk.*

%defattr(755, root, root, 755)
%{python_sitearch}/gtk-2.0/gobject

%files devel
%defattr(644, root, root, 755)
%dir %{_datadir}/pygobject
%dir %{_includedir}/pygtk-2.0
%{_includedir}/pygtk-2.0/pygobject.h
%{_libdir}/pkgconfig/pygobject-2.0.pc

%files doc
%defattr(644, root, root, 755)
%{_datadir}/gtk-doc/html/pygobject
%{_datadir}/pygobject/xsl

%changelog
* Thu Jan 18 2007 Matthew Barnes <mbarnes@redhat.com> - 2.12.1-5.el5
- Add subpackage pygobject2-doc (RH bug #222169).

* Thu Jan 11 2007 Matthew Barnes <mbarnes@redhat.com> - 2.12.1-4.el5
- Use the python_sitearch macro instead of python_sitelib (RH bug #222169).

* Sun Sep 24 2006 Matthew Barnes <mbarnes@redhat.com> - 2.12.1-3.fc6
- Require glib2-devel for the -devel package.

* Fri Sep 22 2006 Matthew Barnes <mbarnes@redhat.com> - 2.12.1-2.fc6
- Define a python_sitelib macro for files under site_packages.
- Spec file cleanups.

* Tue Sep  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.1-1.fc6
- Update to 2.12.1
- Require pkgconfig for the -devel package

* Sun Aug 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.4-1.fc6
- Update to 2.11.4
- Use pre-built docs

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.3-1.fc6
- Update to 2.11.3

* Sun Aug 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.2-2.fc6
- BR libxslt

* Sun Aug 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.2-1.fc6
- Update to 2.11.2

* Wed Jul 19 2006 Jesse Keating <jkeating@redhat.com> - 2.11.0-2
- rebuild

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.0-1
- Update to 2.11.0

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.10.1-3
- rebuild
- Add missing br libtool

* Fri May 19 2006 John (J5) Palmieri <johnp@redhat.com> - 2.10.1-2
- Cleanup

* Fri May 12 2006 John (J5) Palmieri <johnp@redhat.com> - 2.10.1-1
- Initial package
