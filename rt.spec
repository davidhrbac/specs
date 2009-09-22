# This package allows conditional builds
#
# Default values are --with-mysql --with-modperl2.
#
# Read: If neither macro exists, then add the default definition.
%{!?_with_mysql: %{!?_with_Pg: %{!?_with_Informix: %define _with_mysql --with-mysql}}}
%{!?_with_modperl1: %{!?_with_modperl2: %{!?_with_fastcgi: %define _with_modperl2 --with-modperl2}}}

# Webserver setup
%define webusr apache
%define webgrp apache
%define rtname apache
%define rtuid 87
%define rtgid 87

# Database setup
%define dbhost localhost
%{?_with_mysql:    %define dba    root}
%{?_with_Pg:       %define dba    postgres}
%{?_with_Informix: %define dba    informix}
%{?_with_Oracle:   %define dba    system}
%{?_with_DB2:      %define dba    db2inst1}
%define dbname %{rtname}
%define dbuser %{rtname}

# Dependencies related
%define apache_pkgname httpd

%undefine _enable_debug_packages

%define _use_internal_dependency_generator 0
Summary: RT is an enterprise-grade issue tracking system
Name: rt
Version: 3.6.9
Release: 1%{?dist}
Group: Applications/Internet
License: GPL
Url: http://www.bestpractical.com/rt/
Vendor: Best Practical Solutions, LLC
Packager: Paulo Matos <paulo.matos@fct.unl.pt>
Source: http://download.bestpractical.com/pub/rt/release/%{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-root
BuildArch: noarch
#Patch0: %{name}-%{version}-Makefile.in.patch
#Patch1: %{name}-%{version}-rh-layout.patch
Source1: %{name}-%{version}-modperl1-httpd.conf
Source2: %{name}-%{version}-modperl2-httpd.conf
Source3: rt-escalate-tickets.sh
Source10: %{name}-%{version}-filter-depends.sh

#
# Patches to solve bugs
#

# None at the moment.


# mail-dispatcher stuff
Source5: %{name}-mail-dispatcher.tar.gz


%define __find_provides /usr/lib/rpm/find-provides.perl
%define __find_requires %{SOURCE10}


%define siteconfig /etc/%{name}/RT_SiteConfig.pm
%{?_with_modperl1:%define apacheconfig /etc/httpd/conf/rt.conf}
#%{?_with_modperl2:%define apacheconfig /etc/httpd/conf.d/rt.conf}
#assume apache2 with fastcgi
%if %{?_with_modperl2:1}%{?_with_fastcgi:1}0
%define apacheconfig /etc/httpd/conf.d/rt.conf
%endif

# Conditional dependencies
%{?_with_modperl1:Requires: %{apache_pkgname} < 2}
%{?_with_modperl2:Requires: %{apache_pkgname} >= 2}
%{?_with_fastcgi:Requires: %{apache_pkgname} >= 2}
%{?_with_modperl1:Requires: mod_perl < 1.99}
%{?_with_modperl2:Requires: mod_perl >= 2.0.0}
%{?_with_fastcgi:Requires: mod_fastcgi >= 2.4.2}
%{?_with_mysql:Requires: mysql}
%{?_with_Pg:Requires: postgresql}
Requires: /usr/bin/perl
Requires: perl >= 5.8.3
# CORE deps
Requires: perl(Digest::base)
Requires: perl(Digest::MD5) >= 2.27
Requires: perl(DBI) >= 1.40
Requires: perl-DBI >= 1.40
Requires: perl(Test::Inline)
Requires: perl(Class::ReturnValue) >= 0.40
Requires: perl(DBIx::SearchBuilder) >= 1.35
#1.38 is the most recommended
Requires: perl(Want) >= 0.09
Requires: perl(Clone)
Requires: perl(capitalization) >= 0.03
Requires: perl(Devel::Symdump)
#Requires: perl(DBIx::DBSchema)
Requires: perl(Class::Accessor)
Requires: perl(DBD::SQLite)
#-- end of extra deps for 1.38
Requires: perl(Text::Template)
Requires: perl(File::Spec) >= 0.8
#Requires: perl(HTML::Entities)
Requires: perl(HTML::Parser) >= 3.35
Requires: perl(HTML::Scrubber) >= 0.08
Requires: perl(Net::Domain)
Requires: perl(Log::Dispatch) >= 2.0
Requires: perl(Locale::Maketext) >= 1.06
Requires: perl(Locale::Maketext::Lexicon) >= 0.32
Requires: perl(Locale::Maketext::Fuzzy)
Requires: perl(MIME::Entity) >= 5.108
Requires: perl(Mail::Mailer) >= 1.57
Requires: perl(Net::SMTP)
Requires: perl(Text::Wrapper)
Requires: perl(Time::ParseDate)
Requires: perl(Time::HiRes)
Requires: perl(File::Temp)
Requires: perl(Term::ReadKey)
Requires: perl(Text::Autoformat)
Requires: perl(Text::Quoted) >= 1.3
Requires: perl(Tree::Simple) >= 1.04
Requires: perl(Scalar::Util)
Requires: perl(Module::Versions::Report)
Requires: perl(Cache::Simple::TimedExpiry) >= 0.21
Requires: perl(XML::Simple)
# MASON deps
Requires: perl(Params::Validate) >= 0.02
Requires: perl(Cache::Cache)
#Requires: perl(Exception::Class) >= 1.14
Requires: perl(Exception::Class)
Requires: perl(HTML::Mason) >= 1.31
Requires: perl(MLDBM)
Requires: perl(Errno)
Requires: perl(FreezeThaw)
Requires: perl(Storable) >= 2.08
#Requires: perl(Apache::Session) >= 1.53
Requires: perl(Apache::Session)
Requires: perl(XML::RSS) >= 1.05
Requires: perl(HTTP::Server::Simple) >= 0.07
Requires: perl(HTTP::Server::Simple::Mason) >= 0.09
Requires: perl(Text::WikiFormat)
# MAILGATE deps
Requires: perl(HTML::TreeBuilder)
Requires: perl(HTML::FormatText)
Requires: perl(Getopt::Long) >= 2.24
Requires: perl(LWP) >= 5.76
#Requires: perl-libwww-perl >= 2:5.76
# DEV deps
Requires: perl(Regexp::Common)
Requires: perl(Apache::Test)
Requires: perl(HTML::Form)
Requires: perl(HTML::TokeParser)
Requires: perl(WWW::Mechanize)
Requires: perl(Test::WWW::Mechanize)
Requires: perl(Module::Refresh) >= 0.03
# Handler deps
#Requires: perl(FCGI) >= 0.67
Requires: perl(CGI) >= 3.11
#Requires: perl-CGI >= 2:2.92 or perl >= 5.8.1
#Requires: perl-CGI >= 2:2.92
Requires: perl(Apache::DBI)
%{?_with_mysql:Requires: perl(DBD::mysql) >= 2.1018}
%{?_with_Pg:Requires: perl(DBD::Pg)}
%{?_with_Informix:Requires: perl(DBD::Informix)}
%{?_with_Oracle:Requires: perl(DBD::Oracle)}
%{?_with_DB2:Requires: perl(DBD::DB2)}
%{?_with_Sybase:Requires: perl(DBD::Sybase)}
#%{?_with_modperl1:BuildRequires: %{apache_pkgname} < 2}
#%{?_with_modperl2:BuildRequires: %{apache_pkgname} >= 2}
#%{?_with_fastcgi:BuildRequires: %{apache_pkgname} >= 2}
#%{?_with_modperl1:BuildRequires: mod_perl < 1.99}
#%{?_with_modperl2:BuildRequires: mod_perl >= 2.0.0}
#%{?_with_fastcgi:BuildRequires: mod_fastcgi >= 2.4.2}
#%{?_with_mysql:BuildRequires: mysql}
#%{?_with_Pg:BuildRequires: postgresql}

%description
RT is an enterprise-grade issue tracking system. It allows
organizations to keep track of their to-do lists, who is working
on which tasks, what's already been done, and when tasks were
completed. It is available under the terms of version 2 of the GNU
General Public License (GPL), so it doesn't cost anything to set
up and use.

Built options:
     %{?_with_mysql}%{?_with_Pg}%{?_with_Informix}
     %{?_with_modperl1}%{?_with_modperl2}%{?_with_fastcgi}
     --with-db-host=%{dbhost}
     --with-db-dba=%{dba} --with-db-rt-user=%{dbuser}
     --with-db-database=%{dbname}
     --with-web-user=%{webusr} --with-web-group=%{webgrp}


%package mail-dispatcher
Vendor: None 
Summary: RT mail dispatcher account
Group: Applications/Internet
Url:     http://www.geert.triple-it.nl/rt_procmail.html
Requires: rt
#, procmail, sendmail

%description mail-dispatcher
This is a setup for a RT mail dispatcher using sendmail and procmail.
It is based on the assumption that you use one domain for all your RT
queues, e.g. @rt.yourdomain.com.

This allows you to setup queues in RT, using the following convention
syntax:

correspondence address: queuename@rt.yourdomain.com
comment address:        queuename-comment@rt.yourdomain.com

without having to reconfigure everytime your mail settings.

'postmaster' is reserved to be RFC822 compliant, and should be setup
correctly, defaults to user postmaster. You can always change it to
be a RT queue as well.


%prep
# first let's check out if there are repeated options
#%if %{?_with_modperl1: %{?_with_modperl2:1}}0
#  echo 'both --with modperl1 and --with modperl2 were specified' >&2
#  exit -1;
#%endif

modcount=0
%{?_with_modperl1:modcount=$[ modcount + 1]}
%{?_with_modperl2:modcount=$[ modcount + 1]}
%{?_with_fastcgi:modcount=$[ modcount + 1]}
if [ $modcount != 1 ] ; then
  echo 'only one of --with modperl1, --with modperl2, --with fastcgi must be specifiedr' >&2
  exit -1
fi


bdcount=0
%{?_with_mysql:bdcount=$[ bdcount + 1]}
%{?_with_Pg:bdcount=$[ bdcount + 1]}
%{?_with_Informix:bdcount=$[ bdcount + 1]}
if [ $bdcount != 1 ] ; then
  echo 'only one of --with mysql, --with Pg, --with Informix must be specifiedr' >&2
  exit -1
fi

# now the normal stuff
%setup -q -n %{name}-%{version}
# unpack rt-mail-dispatcher
%setup -D -T -a 5

#patch0 -p1
#patch1 -p1

# bugs
#%patch5 -p1
#%patch6 -p1
#%patch7 -p1
#%patch8 -p1
#%patch9 -p1
# untested (features)
#%patch20 -p1


%build
./configure --prefix=/usr --enable-layout=RH \
            %{?_with_mysql}%{?_with_Pg}%{?_with_Informix} \
            %{?_with_modperl1}%{?_with_modperl2}%{?_with_fastcgi} \
            --with-db-host=%{dbhost} \
            --with-db-dba=%{dba} --with-db-rt-user=%{dbuser} \
            --with-db-database=%{dbname} \
            --with-web-user=%{webusr} --with-web-group=%{webgrp}

#check for compliance
#perl sbin/rt-test-dependencies %{?_with_mysql}%{?_with_Pg}%{?_with_Informix} %{?_with_modperl1}%{?_with_modperl2}%{?_with_fastcgi}
# this would install dependencies... not desired
#perl sbin/rt-test-dependencies %{?_with_mysql}%{?_with_Pg}%{?_with_Informix} %{?_with_modperl1}%{?_with_modperl2}%{?_with_fastcgi}  --install

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/usr/local/rt/{etc,html,po,lib}

# fix permissions
find $RPM_BUILD_ROOT/usr/lib/rt -type d -exec chmod 2755 {} \;
find $RPM_BUILD_ROOT/usr/lib/rt -type f -exec chmod 0644 {} \;
find $RPM_BUILD_ROOT/var/rt/html -type d -exec chmod 2755 {} \;
find $RPM_BUILD_ROOT/var/rt/html -type f -exec chmod 0644 {} \;
find $RPM_BUILD_ROOT/usr/local/rt -type d -exec chmod 2755 {} \;
#this will be /usr/share/docs
find docs -type f -exec chmod 0644 {} \;

mkdir -p $RPM_BUILD_ROOT/var/log/rt
touch $RPM_BUILD_ROOT/var/log/rt/rt.log

# UPGRADE stuff must be copyied as well
mv etc/upgrade $RPM_BUILD_ROOT/etc/rt

%{?_with_modperl1: mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf}
%{?_with_modperl1: cp %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/conf/rt.conf}
#%{?_with_modperl2: mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d}
#%{?_with_modperl2: cp %{SOURCE2} $RPM_BUILD_ROOT/etc/httpd/conf.d/rt.conf}
%if %{?_with_modperl2:1}%{?_with_fastcgi:1}0
   mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
   cp %{SOURCE2} $RPM_BUILD_ROOT/etc/httpd/conf.d/rt.conf
%endif
#should not be done here, moved to %post
#make initialize-database

# rt-escalate-tickets.sh
mkdir -p $RPM_BUILD_ROOT/etc/cron.daily
cp %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.daily


# rt-mail-dispatcher
mkdir -p $RPM_BUILD_ROOT/var/rt/home/
mkdir -p $RPM_BUILD_ROOT/etc/mail

( cd rt-mail-dispatcher ; cp -rp home $RPM_BUILD_ROOT/var/rt/ )
cp rt-mail-dispatcher/virtusertable.rt  $RPM_BUILD_ROOT/etc/mail




%clean
rm -rf $RPM_BUILD_ROOT


%pre
/usr/sbin/groupadd %{?rtgid:-f -g %{rtgid}} -r %{rtname}

%pre mail-dispatcher
/usr/sbin/groupadd %{?rtgid:-f -g %{rtgid}} -r %{rtname}
/usr/sbin/useradd -c 'RT user' %{?rtuid:-u %{rtuid}} %{?rtgid:-g %{rtname}} -r \
                  -d /var/rt/home -n -M  %{rtname}

%post
#check for compliance
perl /usr/sbin/rt-test-dependencies %{?_with_mysql}%{?_with_Pg}%{?_with_Informix} %{?_with_modperl1}%{?_with_modperl2}

#initialize db, should be done by user
#/usr/sbin/rt-setup-database --action init --dba %{dba} \
#                            --prompt-for-dba-password

echo "Congratulations. RT has been installed."
echo ""
echo ""
echo "You must now configure RT by editing %{siteconfig} and"
echo "%{apacheconfig}."
echo ""
echo "(You will definitely need to set RT's database password in"
echo "%{siteconfig} before continuing. Not doing so could be"
echo "very dangerous.)"
echo ""
echo "After that, you need to initialize RT's database by running"
echo ""
echo "/usr/sbin/rt-setup-database --action init \ "
echo "     --dba %{dba} --prompt-for-dba-password"
echo ""
echo "If something goes wrong you can always drop everything, by executing"
echo ""
echo "/usr/sbin/rt-setup-database --action drop \ "
echo "     --dba %{dba} --prompt-for-dba-password"
echo ""

%post mail-dispatcher
echo ""
echo "You must now configure somethings by editing /var/rt/home/.procmailrc,"
echo "please read %{_docdir}/%{name}-%{version}/README.mail-dispatcher."
echo ""


%postun
/usr/sbin/groupdel %{rtname}
# yum removes packages on reverse order
# this will prevent it to fail
R=$?
if [ "$R" == "8" ] ; then exit 0; fi
exit $R

%postun mail-dispatcher
/usr/sbin/userdel %{rtname}
# this causes group to be deleted, so we create
# it again if rt is still installed
if (rpm -q %{name} &> /dev/null) ; then
  /usr/sbin/groupadd %{?rtgid:-f -g %{rtgid}} -r %{rtname}
fi


%files
%defattr(-,root,root)
%doc docs COPYING README README.Oracle UPGRADING
#%doc rt-mail-dispatcher/README.mail-dispatcher
%attr(-,-,rt) /usr/bin/*
/usr/sbin/*
%attr(-,-,rt)/usr/lib/rt
%attr(2775,-,%{webgrp}) %dir /var/log/rt
%attr(0664,-,%{webgrp}) /var/log/rt/rt.log
#/var/rt/{doc,home,html,mason_data,session_data}
%attr(-,-,rt) %dir /var/rt
%attr(-,-,rt)/var/rt/doc
%attr(-,-,rt)/var/rt/html
%attr(-,-,rt)/var/rt/mason_data
%attr(-,-,rt)/var/rt/session_data
#/usr/local/rt/{etc,html,lib,po}
%attr(-,-,rt) %dir /usr/local/rt
%attr(-,-,rt) %dir /usr/local/rt/etc
%attr(-,-,rt) %dir /usr/local/rt/html
%attr(-,-,rt) %dir /usr/local/rt/lib
%attr(-,-,rt) %dir /usr/local/rt/po
%attr(0755,-,rt) %dir /etc/rt
%attr(0644,-,rt) %config /etc/rt/RT*
%attr(0644,-,rt) %config /etc/rt/acl.*
%attr(0644,-,rt) %config /etc/rt/initialdata
%attr(0644,-,rt) %config /etc/rt/schema.*
%attr(-,-,rt) /etc/rt/upgrade
%attr(0644,-,-) %config %{apacheconfig}
%attr(0755,-,-) /etc/cron.daily/*


%files mail-dispatcher
%defattr(-,root,root)
%attr(-,rt,rt)/var/rt/home
%config %attr(-,rt,rt)/var/rt/home/.procmailrc
/etc/mail/virtusertable.rt


%changelog
* Mon Sep 21 2009 David Hrbáč <david@hrbac.cz> - 3.6.9-1
- initial build 
