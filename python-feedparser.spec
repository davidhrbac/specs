%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-feedparser
Version:        4.1
Release:        3%{?dist}
Summary:        Parse RSS and Atom feeds in Python

Group:          Development/Languages
License:        BSD-ish
URL:            http://feedparser.org/
Source0:        http://download.sourceforge.net/feedparser/feedparser-%{version}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel

%description
Universal Feed Parser is a Python module for downloading and parsing 
syndicated feeds. It can handle RSS 0.90, Netscape RSS 0.91, 
Userland RSS 0.91, RSS 0.92, RSS 0.93, RSS 0.94, RSS 1.0, RSS 2.0, 
Atom 0.3, Atom 1.0, and CDF feeds. It also parses several popular extension 
modules, including Dublin Core and Apple's iTunes extensions.


%prep
%setup -q -c
find -type f -exec sed -i 's/\r//' {} ';'
find -type f -exec chmod 0644 {} ';'


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
cp -a docs html
rm -f html/examples/.ht*


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE README html
%{python_sitelib}/*


%changelog
* Fri Oct 24 2008 David Hrbáč <david@hrbac.cz> - 4.1-3
- initial rebuild

* Thu Jun 28 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-3
- Ghostbusting (#205413).
- Remove manual python-abi Requires.
- Appease rpmlint.

* Sat Dec 23 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 4.1-2
- Rebuild for new Python.

* Wed Jan 11 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-1
- Version 4.1

* Sat Jan 07 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.0.2-2
- Set sane permissions on doc files.

* Wed Jan 04 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.0.2-1
- Initial build.
