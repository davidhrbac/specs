Name:           mod_annodex
Version:        0.2.2
Release:        8%{?dist}
Summary:        Apache module for server-side support of annodex media

Group:          System Environment/Daemons
License:        Apache Software License
URL:		http://www.annodex.net/
Source:		http://www.annodex.net/software/mod_annodex/download/%{name}-ap20-%{version}.tar.gz
Source1:	annodex.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libannodex-devel
BuildRequires:	libcmml-devel >= 0.8
BuildRequires:	httpd-devel >= 2.0.40
BuildRequires:  pkgconfig
BuildRequires:	sed

Requires:	httpd >= 2.0.40

%description
mod_annodex provides full support for Annodex.net media. For more details
about annodex format, see http://www.annodex.net/

mod_annodex is a handler for type application/x-annodex. It provides the
following features:

        * dynamic generation of Annodex media from CMML files.

        * handling of timed query offsets, such as

          http://media.example.com/fish.anx?t=npt:01:20.8
        or
          http://media.example.com/fish.anx?id=Preparation

        * dynamic retrieval of CMML summaries, if the Accept: header
          prefers type text/x-cmml over application/x-annodex.

%prep
%setup -q -n %{name}-ap20-%{version}

%build
%{_sbindir}/apxs -c mod_annodex.c `pkg-config annodex cmml --cflags --libs`
mv .libs/%{name}.so .

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -m755 %{name}.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules

# install config file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
%ifarch x86_64
sed 's@lib@lib64@g' %{SOURCE1} > conf
%else
cat %{SOURCE1} > conf
%endif

install -m 644 conf \
   $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/annodex.conf

%clean
rm -rf $RPM_BUILD_ROOT
                                                                                
%files
%defattr(-,root,root)
%doc LICENSE README
%{_libdir}/httpd/modules/mod_annodex.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf

%changelog
* Sat Sep 20 2008 David Hrbáč <david@hrbac.cz> - 0.2.2-8
- initial rebuild

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.2-8
- Autorebuild for GCC 4.3

* Tue Oct 16 2007 Joe Orton <jorton@redhat.com> 0.2.2-7
- rebuild against expat 2.x

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.2.2-6
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.2-5
- rebuilt

* Thu Jun 15 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.2-4
- remove strip, so -debuginfo is useful, thanks to Ville

* Sun Mar 05 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.2-3
- rebuild

* Mon Jun 13 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.2-2: rpmlint fixes

* Sat Jun 04 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.2-1: initial package
