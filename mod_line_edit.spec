#Module-Specific definitions
%define mod_name mod_line_edit
%define mod_conf %{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	A general-purpose filter for text documents
Name:		%{mod_name}
Version:	1.0.0
Release:	4%{?dist}
Group:		System Environment/Daemons
License:	GPLv2+
URL:		http://apache.webthing.com/mod_line_edit/
Source0:	http://apache.webthing.com/mod_line_edit/mod_line_edit.c
Source1:	%{mod_conf}
Source2:	http://apache.webthing.com/mod_line_edit/index.html
Requires:	httpd httpd-mmn = %([ -a %{_includedir}/httpd/.mmn ] && cat %{_includedir}/httpd/.mmn || echo missing)
BuildRequires:	httpd-devel
BuildRequires:	file
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
mod_line_edit is a general-purpose filter for text documents. It operates as a
simple on-the-fly line editor, applying search-and-replace rules defined in a
configuration or .htaccess file.

Unlike most of Webthing's filter modules, it is not markup-aware, so it is not 
an optimal choice for processing HTML or XML, though it may nevertheless be
used with caution (and may be far better than semi-markup-aware options such as
mod_layout).

For non-markup document types such as plain text, and non-markup Web documents
such as Javascript or Stylesheets, it is the best available option in the
absence of a filter that parses any relevant document structures.

mod_line_edit is written for performance and reliability, and should scale
without problems as document size grows. mod_line_edit is fully compatible with
Apache 2.0 and 2.2, and all operating systems and MPMs.

%prep

%setup -q -T -c -n %{mod_name}-%{version}
cp %{SOURCE0} %{mod_name}.c
cp %{SOURCE1} %{mod_conf}
cp %{SOURCE2} README.html

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

head -19 %{mod_name}.c > LICENSE

%build
%{_sbindir}/apxs -c %{mod_name}.c

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/httpd/modules/
install -d %{buildroot}%{_sysconfdir}/httpd/conf.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/httpd/modules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{mod_conf}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/httpd/modules/%{mod_so}

%changelog
* Sat Sep 20 2008 David Hrbáč <david@hrbac.cz> - 1.0.0-4
- initial rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.0-4
- Autorebuild for GCC 4.3

* Tue Jan 22 2008 Rob Myers <rob.myers@gtri.gatech.edu> 1.0.0-3
- spec fixups from tibbs (#428981)

* Tue Jan 15 2008 Rob Myers <rob.myers@gtri.gatech.edu> 1.0.0-2
- initial fedora submission

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2mdv2008.0
+ Revision: 82603
- rebuild


* Wed Mar 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1mdv2007.1
+ Revision: 143722
- Import apache-mod_line_edit

* Wed Mar 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1mdv2007.1
- initial Mandriva package

