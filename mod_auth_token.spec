Summary:	Token-based authentication module for the apache Web server.
Name:		mod_auth_token
Version:	1.0.2
Release:	1%{?dist}
Group:		System Environment/Daemons
URL:		http://static.synd.info/downloads/releases/
Source:		http://static.synd.info/downloads/releases/%{name}-%{version}.tar.gz
Patch0:		mod_auth_token-config.patch
License:	Apache Software License
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	httpd-devel >= 2.0.52
BuildRequires:  automake
Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel)
Requires:       httpd = %(rpm -q httpd --qf "%%{version}-%%{release}\n")

%description
Token-based authentication similar to mod_secdownload in LIGHTTPD. Have your 
script generate a token and let Apache handle the file transfer without 
having to pipe it through a script for security.

%prep
%setup -q
#%{__rm} install-sh

#%patch0 -p0 -b .config

%build

%configure 

make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -m 755 .libs/%{name}.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc LICENSE README
%{_libdir}/httpd/modules/*.so

%changelog
* Tue Apr  1 2008 David Hrbáč <david@hrbac.cz> - 1.0.2-1
- Initial build on CentOS
