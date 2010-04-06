%define builddir	%{_builddir}/%{name}-%{version}
%define objdir 		objdir
%define hgver		20100111hg

Summary:        Python interface for mozilla XPCOM library
Name:           xulrunner-python
Version:        1.9.2
Release:        3.%{hgver}%{?dist}
URL:            http://developer.mozilla.org/en/PyXPCOM
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
# Get by hg clone http://hg.mozilla.org/pyxpcom pyxpcom/src
Source0:        pyxpcom-%{version}-%{hgver}.tar.bz2

# build patches
Patch0:         xpcom-dynstr.patch

# ---------------------------------------------------

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  gecko-devel >= %{version}
BuildRequires:  autoconf213
BuildRequires:  python-devel
Requires:       gecko-libs >= %{version}

%description
Files needed to run Gecko applications written in python.

%package devel
Summary: Development files for python XPCOM interface
Group: Development/Libraries
Requires: xulrunner-python = %{version}

%description devel
Development files for building Gecko applications written in python.

#---------------------------------------------------------------------

%prep
%setup -q -c
%patch0  -p1 -b .dynstr

mkdir %{objdir}
autoconf-2.13

#---------------------------------------------------------------------

%build
export CFLAGS=$RPM_OPT_FLAGS
export CXXFLAGS=$RPM_OPT_FLAGS

cd %{objdir} 
../configure --with-libxul-sdk=`pkg-config --variable=sdkdir libxul` \
             --with-system-nspr  \
             --prefix=%{_prefix} \
             --libdir=%{_libdir}
make

#---------------------------------------------------------------------

%install
%{__rm} -rf $RPM_BUILD_ROOT

# Some helpers
%define distdir 	objdir/dist/bin
%define includedir 	objdir/dist/include
%define libdir 		objdir/dist/lib
%define idldir 		objdir/dist/idl

function add_files() {
DIRECTORY=$1
TARGET=$2
INSTALL_DIR=$3
%{__mkdir} -p $RPM_BUILD_ROOT/$INSTALL_DIR
if [ -n "$DIRECTORY" ]; then
    %{__cp} -r $DIRECTORY/* $RPM_BUILD_ROOT/$INSTALL_DIR
fi
echo "%dir $INSTALL_DIR" >> %{builddir}/$TARGET
echo "$INSTALL_DIR/*" >> %{builddir}/$TARGET
}

pushd .

# Fix _xpcom.so rights
%{__chmod} 755 %{distdir}/python/xpcom/_xpcom.so

# Install package binaries
echo %defattr\(-,root,root\) > %{builddir}/files.txt
add_files %{distdir} "files.txt" `pkg-config --variable=libdir libxul`

# Install include files for devel package
echo %defattr\(-,root,root\) > %{builddir}/files-devel.txt
add_files  %{includedir} "files-devel.txt" `pkg-config --variable=includedir libxul`/pyxpcom

# Install idl for devel package
add_files  %{idldir} "files-devel.txt" `pkg-config --variable=idldir libxul`

# Install library for devel package
INSTALL_DIR=`pkg-config --variable=sdkdir libxul`/sdk/lib
LIB_DIR=`pkg-config --variable=libdir libxul`

%{__mkdir} -p $RPM_BUILD_ROOT/$INSTALL_DIR
ln -s $LIB_DIR/libpyxpcom.so $RPM_BUILD_ROOT/$INSTALL_DIR

add_files "" "files-devel.txt" $INSTALL_DIR

popd

#---------------------------------------------------------------------

%clean
%{__rm} -rf $RPM_BUILD_ROOT

#---------------------------------------------------------------------

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f files.txt

%files devel -f files-devel.txt

#---------------------------------------------------------------------

%changelog
* Tue Apr 06 2010 David Hrbáč <david@hrbac.cz> - 1.9.2-3.20100111hg
- set CFLAGS and CXXFLAGS variables to $RPM_OPT_FLAGS
* Wed Nov 25 2009 Martin Stransky <stransky@redhat.com> 1.9.2-2.20100111hg
- created as standalone package

