%define name mysql-mmm
%define version 1.1.r186
%define release 1%{dist}

Summary:   MySQL Master Master Replication Manager
Name:      %{name}
Version:   %{version}
Release:   %{release}
License:   GPLv2
Packager:  JL Bond Consulting / Bond Masuda <bond.masuda@jlbond.com>
Group:     Applications/System
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Source:    http://mysql-master-master.googlecode.com/files/mmm-%{version}.tar.bz2
BuildRequires: libnet >= 1.1

# Note about requirements:
#
# mmm requires certain packages, including perl, and a variety of modules.
# Several of these modules are bundled with the base perl package as provided
# by certain distributions (RHEL/CentOS). 
#
# Dependency:				Provided by:
# Perl ithreads				Available with perl RPM in RHEL4/5
# Data::Dumper				Provided by perl RPM in RHEL4/5
# POSIX					Provided by perl RPM in RHEL4/5
# Cwd					Provided by perl RPM in RHEL4/5
# threads				Provided by perl RPM in RHEL4/5
# threads::shared			Provided by perl RPM in RHEL4/5
# Thread::Queue				Provided by perl RPM in RHEL4/5
# Thread::Semaphore			Provided by perl RPM in RHEL4/5
# IO::Socket				Provided by perl RPM in RHEL4/5
# Time::HiRes				Provided by perl RPM in RHEL5 
Requires: perl
Requires: perl(DBD::mysql)
# These dependencies are automatically detected, so we comment out
#Requires: perl(Algorithm::Diff)
#Requires: perl(DBI)
# These dependencies are automatically detected in RHEL5, but not RHEL4
# So, we leave them explicit.
Requires: perl(Proc::Daemon)
Requires: perl(Data::Dumper)
Requires: perl(POSIX)
Requires: perl(Cwd)
Requires: perl(threads)
Requires: perl(Thread::Queue)
Requires: perl(Thread::Semaphore)
Requires: perl(IO::Socket)
Requires: perl(Time::HiRes)

# Remove this requirement for now since we build fping and send_arp
#Requires: iputils, fping
Requires: iproute

%description
MMM (MySQL Master-Master Replication Manager) is a set of flexible scripts to perform monitoring/failover and management of MySQL Master-Master replication configurations (with only one node writable at any time). The toolset also has the ability to read balance standard master/slave configurations with any number of slaves, so you can use it to move virtual IP addresses around a group of servers depending on whether they are behind in replication.

The current version of this software is stable, but the authors would appreciate any comments, suggestions, bug reports about this version to make it even better.

%prep
%setup -q -n mmm-%{version}

%build
# We build binaries for the tools used by MMM
pushd contrib/fping
%configure
make
strip fping
cp -f fping ../../bin/sys/fping
popd

pushd contrib/send_arp
sed -e s/LIBNET_VERSION=1_0/\#LIBNET_VERSION=1_0/ \
	-e s/\#LIBNET_VERSION=1_1/LIBNET_VERSION=1_1/ Makefile > Makefile.new
mv -f Makefile.new Makefile
make
strip send_arp
make install
popd

%install
# We setup the directory structure
rm -rf $RPM_BUILD_ROOT
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/logrotate.d
mkdir -p -m 755 $RPM_BUILD_ROOT/usr/share/man/man1
mkdir -p -m 755 $RPM_BUILD_ROOT/usr/sbin
mkdir -p -m 755 $RPM_BUILD_ROOT/var/log/mmm

# We try to use the install.pl script as provided by the authors of the code. This way,
# any future changes to install.pl are automatically incorporated in this SPEC file.
# We handle the symlinks separately since we're installing in RPM_BUILD_ROOT.
./install.pl --prefix=$RPM_BUILD_ROOT%{_datadir}/mmm --skip-checks --disable-symlinks

ln -s %{_datadir}/mmm/sbin/mmm_clone $RPM_BUILD_ROOT/usr/sbin/mmm_clone
ln -s %{_datadir}/mmm/sbin/mmm_control $RPM_BUILD_ROOT/usr/sbin/mmm_control
ln -s %{_datadir}/mmm/sbin/mmmd_angel $RPM_BUILD_ROOT/usr/sbin/mmmd_angel
ln -s %{_datadir}/mmm/sbin/mmm_backup $RPM_BUILD_ROOT/usr/sbin/mmm_backup
ln -s %{_datadir}/mmm/sbin/mmmd_agent $RPM_BUILD_ROOT/usr/sbin/mmmd_agent
ln -s %{_datadir}/mmm/sbin/mmm_restore $RPM_BUILD_ROOT/usr/sbin/mmm_restore
ln -s %{_datadir}/mmm/sbin/mmm_get_dump $RPM_BUILD_ROOT/usr/sbin/mmm_get_dump

ln -s %{_datadir}/mmm/man/man1/mmmd_agent.1 $RPM_BUILD_ROOT/usr/share/man/man1/mmmd_agent.1
ln -s %{_datadir}/mmm/man/man1/mmmd_mon.1 $RPM_BUILD_ROOT/usr/share/man/man1/mmmd_mon.1
ln -s %{_datadir}/mmm/man/man1/mmm_control.1 $RPM_BUILD_ROOT/usr/share/man/man1/mmm_control.1
ln -s %{_datadir}/mmm/man/man1/mmm_get_dump.1 $RPM_BUILD_ROOT/usr/share/man/man1/mmm_get_dump.1
ln -s %{_datadir}/mmm/man/man1/mmm_restore.1 $RPM_BUILD_ROOT/usr/share/man/man1/mmm_restore.1
ln -s %{_datadir}/mmm/man/man1/mmm_clone.1 $RPM_BUILD_ROOT/usr/share/man/man1/mmm_clone.1
ln -s %{_datadir}/mmm/man/man1/mmm_backup.1 $RPM_BUILD_ROOT/usr/share/man/man1/mmm_backup.1
ln -s %{_datadir}/mmm/man/man1/mmmd_angel.1 $RPM_BUILD_ROOT/usr/share/man/man1/mmmd_angel.1

# we make a few changes to make the installation convenient
ln -s %{_datadir}/mmm/scripts/init.d/mmm_agent $RPM_BUILD_ROOT/etc/rc.d/init.d/mmm_agent
ln -s %{_datadir}/mmm/scripts/init.d/mmm_mon $RPM_BUILD_ROOT/etc/rc.d/init.d/mmm_mon
ln -s %{_datadir}/mmm/scripts/logrotate.d/mmm $RPM_BUILD_ROOT/etc/logrotate.d/mmm
#ln -s %{_datadir}/mmm/etc/mmm_mon.conf $RPM_BUILD_ROOT/etc/mmm/mmm_mon.conf
#ln -s %{_datadir}/mmm/etc/mmm_agent.conf $RPM_BUILD_ROOT/etc/mmm/mmm_agent.conf

# symlink config dir to /etc/mmm
ln -s %{_datadir}/mmm/etc $RPM_BUILD_ROOT/etc/mmm

# we need to correct some paths in various config files
# - correct paths in mmm_agent init script
sed -e s^/usr/local/mmm/var/mmmd_agent.pid^/var/run/mmmd_agent.pid^ \
-e s^MMMD_AGENT_PIDFILE=.*^MMMD_AGENT_PIDFILE=\"/var/run/mmmd_agent.pid\"^ \
-e s^/usr/local/mmm^%{_datadir}/mmm^ \
	$RPM_BUILD_ROOT%{_datadir}/mmm/scripts/init.d/mmm_agent \
	> $RPM_BUILD_ROOT%{_datadir}/mmm/scripts/init.d/mmm_agent.1
mv -f $RPM_BUILD_ROOT%{_datadir}/mmm/scripts/init.d/mmm_agent.1 \
	$RPM_BUILD_ROOT%{_datadir}/mmm/scripts/init.d/mmm_agent

# - correct paths in mmm_mon init script
sed -e s^/usr/local/mmm/var/mmmd_mon.pid^/var/run/mmmd_mon.pid^ \
-e s^MMMD_PIDFILE=.*CLUSTER.pid\"^MMMD_PIDFILE=\"/var/run/mmmd-\$CLUSTER.pid\"^ \
-e s^MMMD_PIDFILE=.*mmmd.pid\"^MMMD_PIDFILE=\"/var/run/mmmd.pid\"^ \
-e s^/usr/local/mmm^%{_datadir}/mmm^ \
	$RPM_BUILD_ROOT%{_datadir}/mmm/scripts/init.d/mmm_mon \
	> $RPM_BUILD_ROOT%{_datadir}/mmm/scripts/init.d/mmm_mon.1
mv -f $RPM_BUILD_ROOT%{_datadir}/mmm/scripts/init.d/mmm_mon.1 \
	$RPM_BUILD_ROOT%{_datadir}/mmm/scripts/init.d/mmm_mon

# - correct paths in mmm logrotate config
sed -e s^/opt/mmm/var/.*{^/var/log/mmm/\*.log\ \{^ \
-e /olddir/d \
	$RPM_BUILD_ROOT%{_datadir}/mmm/scripts/logrotate.d/mmm \
	> $RPM_BUILD_ROOT%{_datadir}/mmm/scripts/logrotate.d/mmm.1
mv -f $RPM_BUILD_ROOT%{_datadir}/mmm/scripts/logrotate.d/mmm.1 \
	$RPM_BUILD_ROOT%{_datadir}/mmm/scripts/logrotate.d/mmm

# - correct paths in mmm_common.conf
sed \
-e s^/usr/local/mmm/bin^%{_datadir}/mmm/bin^ \
-e s^/usr/local/mmm/var/mmm-debug.log^/var/log/mmm/mmm-debug.log^ \
-e s^/usr/local/mmm/var/mmm-traps.log^/var/log/mmm/mmm-traps.log^ \
	$RPM_BUILD_ROOT%{_datadir}/mmm/etc/examples/mmm_common.conf.example \
	> $RPM_BUILD_ROOT%{_datadir}/mmm/etc/mmm_common.conf

# - correct paths in mmm_agent.conf
sed -e s^/usr/local/mmm/var/mmmd_agent.pid^/var/run/mmmd_agent.pid^ \
	$RPM_BUILD_ROOT%{_datadir}/mmm/etc/examples/mmm_agent.conf.example \
	> $RPM_BUILD_ROOT%{_datadir}/mmm/etc/mmm_agent.conf

# - correct paths in mmm_mon.conf
sed \
-e s^/usr/local/mmm/var/mmmd.pid^/var/run/mmmd.pid^ \
-e s^/usr/local/mmm/var/mmmd.status^/var/run/mmmd.status^ \
	$RPM_BUILD_ROOT%{_datadir}/mmm/etc/examples/mmm_mon.conf.example \
	> $RPM_BUILD_ROOT%{_datadir}/mmm/etc/mmm_mon.conf

# Now we compress the man pages
gzip -9 $RPM_BUILD_ROOT%{_datadir}/mmm/man/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add mmm_mon
/sbin/chkconfig --add mmm_agent

%preun
/sbin/chkconfig --del mmm_mon
/sbin/chkconfig --del mmm_agent

%files
%defattr(-, root, root, -)
%doc COPYING INSTALL README VERSION
%config %attr(600,root,root) %{_datadir}/mmm/etc/mmm_mon.conf
%config %attr(600,root,root) %{_datadir}/mmm/etc/mmm_agent.conf
%config %attr(600,root,root) %{_datadir}/mmm/etc/mmm_common.conf
/etc/mmm
/etc/rc.d/init.d/*
/etc/logrotate.d/mmm
/var/log/mmm
%{_sbindir}/*
%{_mandir}/man1/*
%{_datadir}/mmm
%attr(755,root,root) %{_datadir}/mmm/scripts/init.d/mmm_mon
%attr(755,root,root) %{_datadir}/mmm/scripts/init.d/mmm_agent

%changelog
* Sun Jan 11 2009 Bond Masuda <bond.masuda@jlbond.com> - 1.1.r186
- Re-package for 1.1 revision 186
* Wed Jan 07 2009 Bond Masuda <bond.masuda@jlbond.com> - 1.0-1
- Initial RPM packaging of MMM for RHEL/CentOS distributions
