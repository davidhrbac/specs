%define pkgname   dirsrv

Summary:          389 Directory Server Gateway (dsgw)
Name:             389-dsgw
Version:          1.1.3
Release:          1%{?dist}
License:          GPLv2
URL:              http://port389.org/
Group:            System Environment/Daemons
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    nspr-devel
BuildRequires:    nss-devel
BuildRequires:    svrcore-devel
BuildRequires:    mozldap-devel
BuildRequires:    cyrus-sasl-devel
BuildRequires:    icu
BuildRequires:    libicu-devel
BuildRequires:    adminutil-devel >= 1.1.8

Requires:         /etc/dirsrv/admin-serv/httpd.conf
# orgchart uses perldap
Requires:         perl-Mozilla-LDAP
Provides:         fedora-ds-dsgw = %{version}-%{release}
Obsoletes:        fedora-ds-dsgw < 1.1.3-1

Source0:          http://port389.org/sources/%{name}-%{version}.tar.bz2

%description
389 Directory Server Gateway is a collection of 3 web applications
that run on top of the Administration Server used by the Directory
Server.  These 3 applications are:
* phonebook - a simple phonebook application geared towards end users,
with simple search screens and simple self-service management
* orgchart - an organization chart viewer
* gateway - a more advanced search interface that allows admins to
create and edit user entries, and allows creation of templates for
different types of user and group entries

%prep
%setup -q -n %{name}-%{version}

%build
%configure --disable-rpath

# Generate symbolic info for debuggers
export XCFLAGS=$RPM_OPT_FLAGS

%ifarch x86_64 ppc64 ia64 s390x sparc64
export USE_64=1
%endif

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT 

make DESTDIR="$RPM_BUILD_ROOT" install

# make cookie db directory
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/%{pkgname}/dsgw/cookies

%clean
rm -rf $RPM_BUILD_ROOT

%post
# this has been problematic - if this directory
# does not exist, the server will silently fail to
# start - however, if the user has already created
# it, we don't want to overwrite the permissions
# on it - so we can't list it explicitly in the
# files section
if [ ! -d %{_localstatedir}/run/%{pkgname}/dsgw/cookies ] ; then
    mkdir -p %{_localstatedir}/run/%{pkgname}/dsgw/cookies
fi

%files
%defattr(-,root,root,-)
%doc LICENSE
%dir %{_sysconfdir}/%{pkgname}/dsgw
%config(noreplace)%{_sysconfdir}/%{pkgname}/dsgw/*.conf
%{_datadir}/%{pkgname}/dsgw
%{_datadir}/%{pkgname}/manual/*/dsgw
%{_datadir}/%{pkgname}/properties/dsgw
%{_sbindir}/*
%{_libdir}/%{pkgname}/dsgw-cgi-bin

%changelog
* Tue Sep 22 2009 David Hrbáč <david@hrbac.cz> - 1.1.3-1
- initial build

* Wed Jun  3 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.3-1
- bump version to 1.1.3 for fedora package review

* Fri May 15 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.2-3
- rename to 389

* Tue Apr 21 2009 Orion Poplawski <orion@cora.nwra.com> - 1.1.2-2
- Make adminutil-devel BR >= 1.1.8

* Tue Mar 31 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.2-1
- this is the 1.1.2 release

* Thu Sep  4 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.1-1
- this is the 1.1.1 release

* Mon Mar  3 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1
- Initial version based on fedora-ds-admin.spec
