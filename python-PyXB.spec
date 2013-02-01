%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

%define 	module	PyXB
Summary:	Python XML Schema Bindings
Name:		python-%{module}
Version:	1.1.2
Release:	2%{?dist}
License:	Apache v2.0
Group:		Development/Languages/Python
Source0:	http://downloads.sourceforge.net/project/pyxb/pyxb/%{version}%20%28Beta%29/PyXB-base-%{version}.tar.gz
URL:		http://pyxb.sourceforge.net
BuildRequires:	python-devel
BuildRequires:  python >= 2.4
#Requires:	python-PyXML
#Requires:	python-libs
#Requires:	python-modules
Requires:       python >= 2.4
BuildArch:	noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PyXB (“pixbee”) is a pure Python package that generates Python source
code for classes that correspond to data structures defined by
XMLSchema. In concept it is similar to JAXB for Java and CodeSynthesis
XSD for C++.

%package -n PyXB
Summary:	Python XML Schema Bindings tools
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n PyXB
Tools that generate Python source code for classes that correspond to
data structures defined in XMLSchema.

%package examples
Summary:	Python XML Schema Bindings examples
Group:		Documentation
Requires:	PyXB = %{version}-%{release}

%description examples
Some examples for PyXB package.

%prep
%setup -q -n %{module}-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

#%py_ocomp $RPM_BUILD_ROOT%{python_sitelib}
#%py_comp $RPM_BUILD_ROOT%{python_sitelib}
#%py_postclean

#install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
#cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/* LICENSE NOTICE PKG-INFO README.txt
%{python_sitelib}/*

%files -n PyXB
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pyxbdump
%attr(755,root,root) %{_bindir}/pyxbgen
%attr(755,root,root) %{_bindir}/pyxbwsdl

%files examples
%defattr(644,root,root,755)
%doc examples/*

%changelog
* Mon Oct 08 2012 David Hrbáč <david@hrbac.cz> - 1.1.2-2
- removed python-modules requirement

* Tue Jul 27 2010 David Hrbáč <david@hrbac.cz> - 1.1.2-1
- New upstream version

* Tue Jul 27 2010 David Hrbáč <david@hrbac.cz> - 1.1.1-1
- Initial release

