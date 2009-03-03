%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Support for using OpenSSL in python scripts
Name: m2crypto
Version: 0.16
Release: 6%{?dist}.2
Source0: http://wiki.osafoundation.org/pub/Projects/MeTooCrypto/m2crypto-%{version}.tar.gz
Patch0: m2crypto-0.16-m2urllib2.patch
Patch1: m2crypto-0.16-proxy-connect.patch
Patch2: m2crypto-0.16-timeouts.patch
Patch3: m2crypto-0.16-connect-host.patch
Patch4: m2crypto-0.16-multisubject.patch
License: BSDish
Group: System Environment/Libraries
URL: http://wiki.osafoundation.org/bin/view/Projects/MeTooCrypto
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: openssl-devel, python-devel
BuildRequires: perl, pkgconfig, swig, unzip
Requires: python

%description
This package allows you to call OpenSSL functions from python scripts.

%prep
%setup -q
%patch0 -p1
%patch1 -p0 -b .proxy-connect
%patch2 -p1
%patch3 -p1 -b .connect-host
%patch4 -p1 -b .multisubject

# Red Hat opensslconf.h #includes an architecture-specific file, but SWIG
# doesn't follow the #include.

# Determine which arch opensslconf.h is going to try to #include.
basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif
sed -i -e "s/opensslconf/opensslconf-${basearch}/" SWIG/_ec.i

%build
CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
	LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

# -cpperraswarn is necessary for including opensslconf-${basearch} directly
SWIG_FEATURES=-cpperraswarn python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
	LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

python setup.py install --root=$RPM_BUILD_ROOT

for i in medusa medusa054; do
	sed -i -e '1s,#! /usr/local/bin/python,#! /usr/bin/python,' \
		demo/$i/http_server.py
done

# Windows-only
rm demo/Zope/starts.bat

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGES LICENCE README demo tests
%{python_sitearch}/M2Crypto

%changelog
* Fri Jan  4 2008 Miloslav Trmač <mitr@redhat.com> - 0.16-6.el5.2
- Send the Host: header when using a HTTP/1.1 proxy for https (patch by Karl
  Grindley)
  Resolves: #239034
- Backport support of multiple CN values and multiple patterns in subjectAltName
  from m2crypto-0.18
  Resolves: #363591

* Tue Dec 12 2006 Miloslav Trmac <mitr@redhat.com> - 0.16-6.el5.1
- Rebuild with updates build tools to avoid DT_TEXTREL on s390x
  Resolves: #218578

* Mon Oct 23 2006 Miloslav Trmac <mitr@redhat.com> - 0.16-6
- Add support for SSL socket timeouts (based on a patch by James Bowes
  <jbowes@redhat.com>)
  Resolves: #219966

* Fri Oct 20 2006 Miloslav Trmac <mitr@redhat.com> - 0.16-5
- Backport the urllib2 wrapper (code by James Bowes <jbowes@redhat.com>)
  Resolves: #210956
- Add proxy support for https using CONNECT (original patch by James Bowes
  <jbowes@redhat.com>)
  Resolves: #210963

* Tue Sep 26 2006 Miloslav Trmac <mitr@redhat.com> - 0.16-4
- Drop Obsoletes: openssl-python, openssl-python was last shipped in RHL 7.1
- Fix interpreter paths in demos

* Sat Sep 23 2006 Miloslav Trmac <mitr@redhat.com> - 0.16-3
- Make more compliant with Fedora guidelines
- Update URL:

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.16-2.1
- rebuild

* Thu Jul  6 2006 Miloslav Trmac <mitr@redhat.com> - 0.16-2
- Fix build with rawhide swig

* Thu Jul  6 2006 Miloslav Trmac <mitr@redhat.com> - 0.16-1
- Update to m2crypto-0.16

* Wed Apr 19 2006 Miloslav Trmac <mitr@redhat.com> - 0.15-4
- Fix SSL.Connection.accept (#188742)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.15-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.15-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan  3 2006 Miloslav Trmac <mitr@redhat.com> - 0.15-3
- Add BuildRequires: swig

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Miloslav Trmac <mitr@redhat.com> - 0.15-2
- Rebuild with newer openssl

* Mon Aug 29 2005 Miloslav Trmac <mitr@redhat.com> - 0.15-1
- Update to m2crypto-0.15
- Drop bundled swig

* Tue Jun 14 2005 Miloslav Trmac <mitr@redhat.com> - 0.13-5
- Better fix for #159898, by Dan Williams

* Thu Jun  9 2005 Miloslav Trmac <mitr@redhat.com> - 0.13-4
- Fix invalid handle_error override in SSL.SSLServer (#159898, patch by Dan
  Williams)

* Tue May 31 2005 Miloslav Trmac <mitr@redhat.com> - 0.13-3
- Fix invalid Python version comparisons in M2Crypto.httpslib (#156979)
- Don't ship obsolete xmlrpclib.py.patch
- Clean up the build process a bit

* Wed Mar 16 2005 Nalin Dahyabhai <nalin@redhat.com> 0.13-2
- rebuild

* Tue Nov 23 2004 Karsten Hopp <karsten@redhat.de> 0.13-1
- update, remove now obsolete patches

* Mon Nov 22 2004 Karsten Hopp <karsten@redhat.de> 0.09-7
- changed pythonver from 2.3 to 2.4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Harald Hoyer <harald@redhat.com> - 0.09-5
- changed pythonver from 2.2 to 2.3
- patched setup.py to cope with include path

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 14 2003 Nalin Dahyabhai <nalin@redhat.com> 0.09-1
- Update to version 0.09
- Build using bundled copy of SWIG
- Pick up additional CFLAGS and LDFLAGS from OpenSSL's pkgconfig data, if
  there is any
- Handle const changes in new OpenSSL
- Remove unnecessary ldconfig calls in post/postun

* Thu Dec 12 2002 Elliot Lee <sopwith@redhat.com> 0.07_snap3-2
- Update to version 0.07_snap3

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Nalin Dahyabhai <nalin@redhat.com> 0.05_snap4-4
- rebuild with Python 2.2

* Wed Apr 24 2002 Nalin Dahyabhai <nalin@redhat.com> 0.05_snap4-3
- remove a stray -L at link-time which prevented linking with libssl (#59985)

* Thu Aug 23 2001 Nalin Dahyabhai <nalin@redhat.com> 0.05_snap4-2
- drop patch which isn't needed because we know swig is installed

* Mon Apr  9 2001 Nalin Dahyabhai <nalin@redhat.com> 0.05_snap4-1
- break off from openssl-python
