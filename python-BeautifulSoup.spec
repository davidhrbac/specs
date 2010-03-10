%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

%define oname   BeautifulSoup

Name:           python-BeautifulSoup
Version:        3.0.8
Release:        1%{?dist}
Summary:        HTML/XML parser for quick-turnaround applications like screen-scraping

Group:          Development/Languages
License:        BSD
URL:            http://www.crummy.com/software/BeautifulSoup/
Source0:        http://www.crummy.com/software/BeautifulSoup/download/3.x/BeautifulSoup-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel

%description
Beautiful Soup is a Python HTML/XML parser designed for quick
turnaround projects like screen-scraping. Three features make it
powerful:

Beautiful Soup won't choke if you give it bad markup.

Beautiful Soup provides a few simple methods and Pythonic idioms for
navigating, searching, and modifying a parse tree.

Beautiful Soup automatically converts incoming documents to Unicode
and outgoing documents to UTF-8.

Beautiful Soup parses anything you give it.

Valuable data that was once locked up in poorly-designed websites is
now within your reach. Projects that would have taken hours take only
minutes with Beautiful Soup.


%prep
%setup -q -n %{oname}-%{version}


%build
%{__python} setup.py build
%{__python} -c 'import %{oname} as bs; print bs.__doc__' > COPYING
touch -r %{oname}.py COPYING


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

#Files installed by error
rm -rf $RPM_BUILD_ROOT%{_bindir}

 
%clean
rm -rf $RPM_BUILD_ROOT


%check
%{__python} BeautifulSoupTests.py


%files
%defattr(-,root,root,-)
%doc COPYING
%{python_sitelib}/%{oname}.py*
%exclude %{python_sitelib}/%{oname}Tests.py*
%if 0%{?fedora} >= 9 || 0%{?rhel} >= 6
%{python_sitelib}/%{oname}-%{version}-py%{pyver}.egg-info
%endif

%changelog
* Tue Mar 09 2010 David Hrbáč <david@hrbac.cz> - 3.0.8-1
- initial release
