%global tag     git20090314
%global git_tag a77521aa84ea5b8c5bcc3e387451acd9368292ee

%global httpd_mod_dir  %{_libdir}/httpd/modules
%global httpd_conf_dir %{_sysconfdir}/httpd/conf.d

Name:           mod_perlite
Version:        0.09
# I'm treating this as a pre-release as we don't have any actual tarballs yet.
Release:        0.2%{?tag:.%{tag}}%{?dist}
Summary:        Kinder, gentler embedded Perl for the Apache HTTP Server

Group:          System Environment/Daemons
# see Build.PL, README
License:        GPL+ or Artistic
URL:            http://modperlite.org
# git://github.com/sodabrew/mod_perlite.git
# can be recreated with: 
#   TAG=a77521aa84ea5b8c5bcc3e387451acd9368292ee \
#   git archive --prefix mod_perlite/ $TAG | gzip > mod_perlite-$TAG.tar.gz
Source0:        mod_perlite-%{tag}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel >= 2.2.0, httpd, gdbm-devel
BuildRequires:  apr-devel >= 1.2.0, apr-util-devel

BuildRequires:  perl(:WITH_PERLIO)

BuildRequires:  perl(Module::Build)
BuildRequires:  perl(ExtUtils::Embed)
BuildRequires:  perl(File::Which)
BuildRequires:  perl(Test::More)

Requires:       httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(:WITH_PERLIO)

%description
mod_perlite is a lightweight Apache module that embeds a Perl interpreter
and suggests a default configuration where any file ending in ".pl" is
interpreted by Perl.  It is the Perl equivalent of PHP in its simplicity
and nothing like mod_perl in its complexity.

%prep
%setup -q -n %{name}

%build
%{__perl} Build.PL installdirs=vendor optimize="%{optflags} -fpic"
./Build build

%install
rm -rf %{buildroot}

./Build install destdir=%{buildroot} create_packlist=0

# and our apache module...
mkdir -p %{buildroot}%{httpd_mod_dir}
cp mod_perlite.so %{buildroot}%{httpd_mod_dir}/

# install our conf file...
mkdir -p %{buildroot}%{httpd_conf_dir}
cat mod_perlite.conf | sed -re 's/^\s+//; s/AddDir/Dir/; /IfDefine/d' \
    > %{buildroot}%{httpd_conf_dir}/perlite.conf

%{_fixperms} %{buildroot}

%check
## This seems to fail
#./Build test

prove -b t/*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc TODO README
%config(noreplace) %{httpd_conf_dir}/*.conf
%{httpd_mod_dir}/mod_perlite.so
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Thu Apr 28 2009 David Hrbáč <david@hrbac.cz> - 0.09-0.2.git20090314
- initial rebuild

* Fri Apr 10 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.09-0.2.git20090314
- patch up tarball creation, per review

* Sat Mar 14 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.09-0.1.git20090314
- initial packaging (thanks, mod_perl.spec!)
- based off git a77521aa84ea5b8c5bcc3e387451acd9368292ee
