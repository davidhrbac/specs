%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:           wapiti
Version:        2.2.1
Release:        3%{?dist}
Summary:        Web application vulnerability scanner

Group:          Applications/Internet
License:        GPLv2 and MIT and ASL 2.0
URL:            http://wapiti.sourceforge.net/
Source0:        http://downloads.sourceforge.net/project/wapiti/wapiti/wapiti-%{version}/wapiti-%{version}.tar.bz2
# https://sourceforge.net/tracker/?func=detail&aid=2954112&group_id=168625&atid=847490
Source1:        wapiti-setup.py
# Split wapiti sources between site-packages/wapiti/* and /usr/bin/wapiti,
# move working dirs (generated_report, scans) from site-packages/wapiti/ to ~/.wapiti/,
# move config dir site-packages/wapiti/config/attacks to /etc/wapiti/attacks,
# move gettext MO files from site-packages/wapiti/config/language to /usr/share/locale
# https://sourceforge.net/tracker/?func=detail&aid=2954112&group_id=168625&atid=847490
Patch0:         wapiti-2.2.1-std_lib_paths.patch
# Use system libraries BeautifulSoup, httplib2, SocksiPy
# https://sourceforge.net/tracker/?func=detail&aid=2954109&group_id=168625&atid=847490
Patch1:         wapiti-2.2.1-system_libs.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python2-devel
Requires:       python-BeautifulSoup
Requires:       python-SocksiPy
Requires:       python-httplib2


%description
Wapiti allows you to audit the security of your web applications.
It performs "black-box" scans, i.e. it does not study the source code of the 
application but will scans the webpages of the deployed webapp, looking for 
scripts and forms where it can inject data.
Once it gets this list, Wapiti acts like a fuzzer, injecting payloads to see 
if a script is vulnerable.

Wapiti can detect the following vulnerabilities:
    * File Handling Errors (Local and remote include/require, fopen...)
    * Database Injection (PHP/JSP/ASP SQL Injections and XPath Injections)
    * XSS (Cross Site Scripting) Injection
    * LDAP Injection
    * Command Execution detection (eval(), system(), passtru()...)
    * CRLF Injection (HTTP Response Splitting, session fixation...)

Wapiti is able to differentiate ponctual and permanent XSS vulnerabilities.
Wapiti does not rely on a vulnerability database like Nikto do. Wapiti aims 
to discover unknown vulnerabilities in web applications.


%prep
%setup -q
%patch0 -p1
%patch1 -p1

# Copy setup.py
cp %{SOURCE1} setup.py

# Change an encoding of files to UTF-8
for f in ChangeLog_lswww; do
    iconv -f iso-8859-1 -t utf-8 $f > $f.tmp
    touch -r $f $f.tmp
    mv $f.tmp $f
done

# Use system libraries BeautifulSoup, httplib2, SocksiPy
rm -rf src/net/BeautifulSoup.py src/net/httplib2/


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Remove the interpreter from site-packages
find %{buildroot}%{python_sitelib} -type f -iname "*py" -exec \
    sed -i 's/#!\/usr\/bin\/env python//' {} \;

%find_lang %{name}


%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog_Wapiti ChangeLog_lswww README TODO example.txt
%dir %{_sysconfdir}/wapiti
%dir %{_sysconfdir}/wapiti/attacks
%config(noreplace) %{_sysconfdir}/wapiti/attacks/*
%{_bindir}/wapiti
%{_mandir}/man1/wapiti*
%dir %{python_sitelib}/wapiti/
%{python_sitelib}/wapiti/attack/
%dir %{python_sitelib}/wapiti/config/
%{python_sitelib}/wapiti/config/vulnerabilities/
%{python_sitelib}/wapiti/file/
%{python_sitelib}/wapiti/language/
%{python_sitelib}/wapiti/net/
%{python_sitelib}/wapiti/report/
%{python_sitelib}/wapiti/report_template/
%{python_sitelib}/wapiti/vulnerability.py*
%{python_sitelib}/wapiti-*.egg-info


%changelog
* Sat Mar 13 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 2.2.1-3
- Fix the license
- Fix the summary
- Replace generally useful macros by regular commands

* Thu Mar 11 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 2.2.1-2
- Move gettext MO files to /usr/share/locale
- Preserve timestamps on documentation files

* Sun Feb 14 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 2.2.1-1
- Initial package build

