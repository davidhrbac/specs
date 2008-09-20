%define	major 0
%define libname colorer1
%define develname colorer2

Summary:	Syntax highlighting and text parsing library
Name:		colorer-take5
Version:	0
Release:	0.beta5.2
Group:		Text tools
License:	MPL
URL:		http://colorer.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/colorer/Colorer-take5-linux.be5.tar.bz2
Patch0:		colorer-optflags.diff
Patch1:		colorer-soname.diff
Patch2:		colorer-DESTDIR.diff
BuildRequires:	libstdc++-devel
Requires:	%{libname} = %{version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
Colorer take5 is a syntax highlighting and text parsing library, that provides
services of text parsing in host editor systems in real-time and transforming
results into colored text. Result information allows to search and build
outlined lists of functions, structures, and to search and indent programming
language constructions (brackets, paired tags). Colorer uses pure C++, XML, it
is fully portable and works on either win32/unix/mac platforms. Top level Java
language API is also available. 

%package -n	%{libname}
Summary:	Syntax highlighting and text parsing library
Group:          System/Libraries

%description -n	%{libname}
Colorer take5 is a syntax highlighting and text parsing library, that provides
services of text parsing in host editor systems in real-time and transforming
results into colored text. Result information allows to search and build
outlined lists of functions, structures, and to search and indent programming
language constructions (brackets, paired tags). Colorer uses pure C++, XML, it
is fully portable and works on either win32/unix/mac platforms. Top level Java
language API is also available. 

%package -n	%{develname}
Summary:	Static library and header files for the %{name} library
Group:		Development/C++
Requires:	%{libname} = %{version}
Requires:	%{name}-base = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	libcolorer-devel = %{version}-%{release}
#Obsoletes:	%{mklibname colorer 0 -d}

%description -n	%{develname}
Colorer take5 is a syntax highlighting and text parsing library, that provides
services of text parsing in host editor systems in real-time and transforming
results into colored text. Result information allows to search and build
outlined lists of functions, structures, and to search and indent programming
language constructions (brackets, paired tags). Colorer uses pure C++, XML, it
is fully portable and works on either win32/unix/mac platforms. Top level Java
language API is also available. 

This package contains the development files for the %{name} library.

%package	docs
Summary:	Documentation for Colorer take5
Group:		Development/C++

%description	docs
Colorer take5 is a syntax highlighting and text parsing library, that provides
services of text parsing in host editor systems in real-time and transforming
results into colored text. Result information allows to search and build
outlined lists of functions, structures, and to search and indent programming
language constructions (brackets, paired tags). Colorer uses pure C++, XML, it
is fully portable and works on either win32/unix/mac platforms. Top level Java
language API is also available. 

This package contains the documentation for Colorer take5.

%package	base
Summary:	Common files for Colorer take5
Group:		Text tools

%description	base
Colorer take5 is a syntax highlighting and text parsing library, that provides
services of text parsing in host editor systems in real-time and transforming
results into colored text. Result information allows to search and build
outlined lists of functions, structures, and to search and indent programming
language constructions (brackets, paired tags). Colorer uses pure C++, XML, it
is fully portable and works on either win32/unix/mac platforms. Top level Java
language API is also available. 

This package contains common files for Colorer take5.

%prep

%setup -q -c -n %{name}
%patch0 -p0
%patch1 -p0
%patch2 -p0

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%configure

make RPM_OPT_FLAGS="%{optflags} -fpermissive -Wall -fPIC"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

#makeinstall_std

#ln -snf libcolorer.so.%{major} %{buildroot}%{_libdir}/libcolorer.so

rm -f %{buildroot}%{_datadir}/colorer/{LICENSE,README}

rm -rf installed_docs
#mv %{buildroot}%{_datadir}/doc/colorer-take5 installed_docs

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/colorer

%files -n %{libname}
%defattr(-,root,root,-)
%doc LICENSE README
%attr(0755,root,root) %{_libdir}/libcolorer.so

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/colorer
%{_libdir}/libcolorer.so
%{_datadir}/colorer/bin

%files docs
%defattr(-,root,root,-)
%doc installed_docs/*

%files base
%defattr(-,root,root,-)
%{_datadir}/colorer/catalog.xml
%{_datadir}/colorer/hrc
%{_datadir}/colorer/hrd


%changelog
* Mon Feb 18 2008 Thierry Vignaud <tvignaud@mandriva.com> 0-0.beta5.2mdv2008.1
+ Revision: 170230
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 0-0.beta5.2mdv2008.0
+ Revision: 83708
- new devel naming


* Tue Dec 19 2006 Oden Eriksson <oeriksson@mandriva.com> 0-0.beta5.1mdv2007.0
+ Revision: 100352
- Import colorer-take5

* Tue Dec 19 2006 Oden Eriksson <oeriksson@mandriva.com> 0-0.beta5.1mdv2007.1
- beta5
- rediffed P2

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 0-0.beta4.3mdk
- rebuild

* Mon Mar 20 2006 Oden Eriksson <oeriksson@mandriva.com> 0-0.beta4.2mdk
- fix deps and add the base sub package

* Mon Mar 20 2006 Oden Eriksson <oeriksson@mandriva.com> 0-0.beta4.1mdk
- initial Mandriva package

