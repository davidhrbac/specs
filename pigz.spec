Name:           pigz
Version:        2.1.6
Release:        1%{?dist}
Summary:        Parallel implementation of gzip

Group:          Applications/File
License:        zlib
URL:            http://www.zlib.net/pigz/
Source0:        http://www.zlib.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  zlib-devel

%description
pigz, which stands for parallel implementation of gzip,
is a fully functional replacement for gzip that exploits
multiple processors and multiple cores to the hilt when compressing data.

%prep
%setup -q


%build
make %{?_smp_mflags} CFLAGS='%{optflags}'


%install
rm -rf $RPM_BUILD_ROOT
install -p -D pigz $RPM_BUILD_ROOT%{_bindir}/pigz
install -p -D unpigz $RPM_BUILD_ROOT%{_bindir}/unpigz
install -p -D pigz.1 -m 0644 $RPM_BUILD_ROOT%{_datadir}/man/man1/pigz.1

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc pigz.pdf README
%{_bindir}/pigz
%{_bindir}/unpigz
%{_datadir}/man/man1/pigz.*


%changelog
* Thu Sep 23 2010 David Hrbáč <david@hrbac.cz> - 2.1.6-1
- new upstream release
