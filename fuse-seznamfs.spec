%define real_name seznamfs

Summary: FUSE-Filesystem to access remote filesystems via SSH
Name: fuse-seznamfs
Version: 0.2.0
Release: 1
License: GPL
Group: System Environment/Kernel
URL: http://seznamfs.sourceforge.net/

Source: http://dl.sourceforge.net/sourceforge/seznamfs/seznamfs-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: glib2-devel >= 2.0, fuse-devel >= 2.2
Requires: fuse >= 2.2

Obsoletes: seznamfs <= %{version}-%{release}
Provides: seznamfs = %{version}-%{release}

%description
This is a FUSE-filesystem client based on the SSH File Transfer Protocol.
Since most SSH servers already support this protocol it is very easy to set
up: i.e. on the server side there's nothing to do. On the client side 
mounting the filesystem is as easy as logging into the server with ssh.

%prep
%setup -n %{real_name}-%{version}

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/seznamfs

%changelog
* Tue Dec 18 2007 Dag Wieers <dag@wieers.com> - 1.9-1
- Updated to release 1.9.

* Sat May 12 2007 Dag Wieers <dag@wieers.com> - 1.7-1
- Initial package. (using DAR)
