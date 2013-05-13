%ifarch x86_64
%define java_arch amd64
%else
%define java_arch %{_arch}
%endif

# Assume not modern. Override if needed.
%global	modern 0

%if 0%{?fedora}
%global modern 1
%endif

%if 0%{?rhel} >= 6
%global	modern 1
%endif

Name: R
Version: 3.0.0
Release: 2%{?dist}
Summary: A language for data analysis and graphics
URL: http://www.r-project.org
Source0: ftp://cran.r-project.org/pub/R/src/base/R-3/R-%{version}.tar.gz
Source1: macros.R
Source2: R-make-search-index.sh
License: GPLv2+
Group: Applications/Engineering
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gcc-gfortran
BuildRequires: gcc-c++, tex(latex), texinfo-tex 
BuildRequires: libpng-devel, libjpeg-devel, readline-devel
BuildRequires: tcl-devel, tk-devel, ncurses-devel
BuildRequires: blas >= 3.0, pcre-devel, zlib-devel
%if %{modern}
BuildRequires: java-1.5.0-gcj
%else
BuildRequires: java-1.4.2-gcj-compat
%endif
BuildRequires: lapack-devel
BuildRequires: libSM-devel, libX11-devel, libICE-devel, libXt-devel
BuildRequires: bzip2-devel, libXmu-devel, cairo-devel, libtiff-devel
BuildRequires: gcc-objc, pango-devel, xz-devel
%if %{modern}
BuildRequires: libicu-devel
%endif
BuildRequires: less
%if 0%{?fedora} >= 18
BuildRequires: tex(inconsolata.sty)
%endif
# R-devel will pull in R-core
Requires: R-devel = %{version}-%{release}
# libRmath-devel will pull in libRmath
Requires: libRmath-devel = %{version}-%{release}
%if %{modern}
# Pull in Java bits (if you don't want this, use R-core)
Requires: R-java = %{version}-%{release}
%endif

%description
This is a metapackage that provides both core R userspace and 
all R development components.

R is a language and environment for statistical computing and graphics. 
R is similar to the award-winning S system, which was developed at 
Bell Laboratories by John Chambers et al. It provides a wide 
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

%package core
Summary: The minimal R components necessary for a functional runtime
Group: Applications/Engineering
Requires: xdg-utils, cups
%if %{modern}
Requires: tex(dvips), vi
%else
Requires: vim-minimal
%endif
Requires: perl, sed, gawk, tex(latex), less

# These are the submodules that R-core provides. Sometimes R modules say they
# depend on one of these submodules rather than just R. These are provided for 
# packager convenience.
Provides: R-base = %{version}
Provides: R-boot = 1.3.9
Provides: R-class = 7.3.7
Provides: R-cluster = 1.14.4
Provides: R-codetools = 0.2.8
Provides: R-datasets = %{version}
Provides: R-foreign = 0.8.53
Provides: R-graphics = %{version}
Provides: R-grDevices = %{version}
Provides: R-grid = %{version}
Provides: R-KernSmooth = 2.23.10
Provides: R-lattice = 0.20.15
Provides: R-MASS = 7.3.26
Provides: R-Matrix = 1.0.12
Obsoletes: R-Matrix < 0.999375-7
Provides: R-methods = %{version}
Provides: R-mgcv = 1.7.22
Provides: R-nlme = 3.1.109
Provides: R-nnet = 7.3.6
Provides: R-parallel = %{version}
Provides: R-rpart = 4.1.1
Provides: R-spatial = 7.3.6
Provides: R-splines = %{version}
Provides: R-stats = %{version}
Provides: R-stats4 = %{version}
Provides: R-survival = 2.37.4
Provides: R-tcltk = %{version}
Provides: R-tools = %{version}
Provides: R-utils = %{version}

%description core
A language and environment for statistical computing and graphics.
R is similar to the award-winning S system, which was developed at
Bell Laboratories by John Chambers et al. It provides a wide
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

%package core-devel
Summary: Core files for development of R packages (no Java)
Group: Applications/Engineering
Requires: R-core = %{version}-%{release}
# You need all the BuildRequires for the development version
Requires: gcc-c++, gcc-gfortran, tex(latex), texinfo-tex
Requires: bzip2-devel, libX11-devel, pcre-devel, zlib-devel
Requires: tcl-devel, tk-devel, pkgconfig
# TeX files needed
%if 0%{?fedora} >= 18
Requires: tex(ecrm1000.tfm)
Requires: tex(inconsolata.sty)
Requires: tex(ptmr8t.tfm)
Requires: tex(ptmb8t.tfm)
Requires: tex(pcrr8t.tfm)
Requires: tex(phvr8t.tfm)
Requires: tex(ptmri8t.tfm)
Requires: tex(ptmro8t.tfm)
Requires: tex(cm-super-ts1.enc)
%endif
Provides: R-Matrix-devel = 1.0.12
Obsoletes: R-Matrix-devel < 0.999375-7

%if %{modern}
%description core-devel
Install R-core-devel if you are going to develop or compile R packages.
This package does not configure the R environment for Java, install
R-java-devel if you want this.
%else
%description core-devel
Install R-core-devel if you are going to develop or compile R packages.
%endif

%package devel
Summary:	Full R development environment metapackage
Group: Applications/Engineering
Requires:	R-core-devel = %{version}-%{release}
%if %{modern}
Requires:	R-java-devel = %{version}-%{release}
%endif

%description devel
This is a metapackage to install a complete (with Java) R development
environment.

%if %{modern}
%package java
Summary: R with Fedora provided Java Runtime Environment
Group: Applications/Engineering
Requires(post): R-core = %{version}-%{release}
Requires(post): java

%description java
A language and environment for statistical computing and graphics.
R is similar to the award-winning S system, which was developed at
Bell Laboratories by John Chambers et al. It provides a wide
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

This package also has an additional dependency on java, as provided by
Fedora's openJDK.

%package java-devel
Summary: Development package for use with Java enabled R components
Group: Applications/Engineering
Requires(post): R-core-devel = %{version}-%{release}
Requires(post): java-devel

%description java-devel
Install R-java-devel if you are going to develop or compile R packages
that assume java is present and configured on the system.
%endif

%package -n libRmath
Summary: Standalone math library from the R project
Group: Development/Libraries

%description -n libRmath
A standalone library of mathematical and statistical functions derived
from the R project.  This package provides the shared libRmath library.

%package -n libRmath-devel
Summary: Headers from the R Standalone math library
Group: Development/Libraries
Requires: libRmath = %{version}-%{release}, pkgconfig

%description -n libRmath-devel
A standalone library of mathematical and statistical functions derived
from the R project.  This package provides the libRmath header files.

%package -n libRmath-static
Summary: Static R Standalone math library
Group: Development/Libraries
Requires: libRmath-devel = %{version}-%{release}

%description -n libRmath-static
A standalone library of mathematical and statistical functions derived
from the R project.  This package provides the static libRmath library.

%prep
%setup -q

# Filter false positive provides.
cat <<EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} \
| grep -v 'File::Copy::Recursive' | grep -v 'Text::DelimMatch'
EOF
%define __perl_provides %{_builddir}/R-%{version}/%{name}-prov
chmod +x %{__perl_provides}

# Filter unwanted Requires:
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} \
| grep -v 'perl(Text::DelimMatch)'
EOF
%define __perl_requires %{_builddir}/R-%{version}/%{name}-req
chmod +x %{__perl_requires}

%build
# Add PATHS to Renviron for R_LIBS_SITE
echo 'R_LIBS_SITE=${R_LIBS_SITE-'"'/usr/local/lib/R/site-library:/usr/local/lib/R/library:%{_libdir}/R/library:%{_datadir}/R/library'"'}' >> etc/Renviron.in
# No inconsolata on RHEL tex
%if 0%{?rhel}
export R_RD4PDF="times,hyper"
sed -i 's|inconsolata,||g' etc/Renviron.in
%endif
export R_PDFVIEWER="%{_bindir}/xdg-open"
export R_PRINTCMD="lpr"
export R_BROWSER="%{_bindir}/xdg-open"

case "%{_target_cpu}" in
      x86_64|mips64|ppc64|powerpc64|sparc64|s390x)
          export CC="gcc -m64"
          export CXX="g++ -m64"
          export F77="gfortran -m64"
          export FC="gfortran -m64"
      ;;
      ia64|alpha|arm*|sh*)
          export CC="gcc"
          export CXX="g++"
          export F77="gfortran"
          export FC="gfortran"
      ;;
      s390)
          export CC="gcc -m31"
          export CXX="g++ -m31"
          export F77="gfortran -m31"
          export FC="gfortran -m31"
      ;;    
      *)
          export CC="gcc -m32"
          export CXX="g++ -m32"
          export F77="gfortran -m32"
          export FC="gfortran -m32"
      ;;    
esac

export FCFLAGS="%{optflags}"
( %configure \
    --with-system-zlib --with-system-bzlib --with-system-pcre \
    --with-lapack \
    --with-tcl-config=%{_libdir}/tclConfig.sh \
    --with-tk-config=%{_libdir}/tkConfig.sh \
    --enable-R-shlib \
    --enable-prebuilt-html \
    rdocdir=%{_docdir}/R-%{version} \
    rincludedir=%{_includedir}/R \
    rsharedir=%{_datadir}/R) \
 | grep -A30 'R is now' - > CAPABILITIES
make 
(cd src/nmath/standalone; make)
#make check-all
make pdf
make info

# Convert to UTF-8
for i in doc/manual/R-intro.info doc/manual/R-FAQ.info doc/FAQ doc/manual/R-admin.info doc/manual/R-exts.info-1; do
  iconv -f iso-8859-1 -t utf-8 -o $i{.utf8,}
  mv $i{.utf8,}
done

%install
make DESTDIR=${RPM_BUILD_ROOT} install install-info
make DESTDIR=${RPM_BUILD_ROOT} install-pdf

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir.old
install -p CAPABILITIES ${RPM_BUILD_ROOT}%{_docdir}/R-%{version}

#Install libRmath files
(cd src/nmath/standalone; make install DESTDIR=${RPM_BUILD_ROOT})

mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo "%{_libdir}/R/lib" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf

mkdir -p $RPM_BUILD_ROOT%{_datadir}/R/library

# Install rpm helper macros
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm/
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/

# Install rpm helper script
mkdir -p $RPM_BUILD_ROOT/usr/lib/rpm/
install -m0755 %{SOURCE2} $RPM_BUILD_ROOT/usr/lib/rpm/

# Fix multilib
touch -r NEWS ${RPM_BUILD_ROOT}%{_docdir}/R-%{version}/CAPABILITIES
touch -r NEWS doc/manual/*.pdf
touch -r NEWS $RPM_BUILD_ROOT%{_bindir}/R

# Fix html/packages.html
# We can safely use RHOME here, because all of these are system packages.
sed -i 's|\..\/\..|%{_libdir}/R|g' $RPM_BUILD_ROOT%{_docdir}/R-%{version}/html/packages.html

for i in $RPM_BUILD_ROOT%{_libdir}/R/library/*/html/*.html; do
  sed -i 's|\..\/\..\/..\/doc|%{_docdir}/R-%{version}|g' $i
done

# Fix exec bits
chmod +x $RPM_BUILD_ROOT%{_datadir}/R/sh/echo.sh
chmod -x $RPM_BUILD_ROOT%{_libdir}/R/library/mgcv/CITATION ${RPM_BUILD_ROOT}%{_docdir}/R-%{version}/CAPABILITIES

# Symbolic link for convenience
pushd $RPM_BUILD_ROOT%{_libdir}/R
ln -s ../../include/R include
popd

# Symbolic link for LaTeX
mkdir -p $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex
pushd $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex
ln -s ../../../R/texmf/tex/latex R
popd

%files
# Metapackage

%files core
%defattr(-, root, root, -)
%{_bindir}/R
%{_bindir}/Rscript
%{_datadir}/R/
%{_datadir}/texmf/
# Have to break this out for the translations
%dir %{_libdir}/R/
%{_libdir}/R/bin/
%{_libdir}/R/etc/
%{_libdir}/R/lib/
%dir %{_libdir}/R/library/
%dir %{_libdir}/R/library/translations/
%{_libdir}/R/library/translations/DESCRIPTION
%lang(da) %{_libdir}/R/library/translations/da/
%lang(de) %{_libdir}/R/library/translations/de/
%lang(en) %{_libdir}/R/library/translations/en*/
%lang(es) %{_libdir}/R/library/translations/es/
%lang(fa) %{_libdir}/R/library/translations/fa/
%lang(fr) %{_libdir}/R/library/translations/fr/
%lang(it) %{_libdir}/R/library/translations/it/
%lang(ja) %{_libdir}/R/library/translations/ja/
%lang(ko) %{_libdir}/R/library/translations/ko/
%lang(nn) %{_libdir}/R/library/translations/nn/
%lang(pl) %{_libdir}/R/library/translations/pl/
%lang(pt) %{_libdir}/R/library/translations/pt*/
%lang(ru) %{_libdir}/R/library/translations/ru/
%lang(tr) %{_libdir}/R/library/translations/tr/
%lang(zh) %{_libdir}/R/library/translations/zh*/
# base
%{_libdir}/R/library/base/
# boot
%dir %{_libdir}/R/library/boot/
%{_libdir}/R/library/boot/CITATION
%{_libdir}/R/library/boot/data/
%{_libdir}/R/library/boot/DESCRIPTION
%{_libdir}/R/library/boot/help/
%{_libdir}/R/library/boot/html/
%{_libdir}/R/library/boot/INDEX
%{_libdir}/R/library/boot/Meta/
%{_libdir}/R/library/boot/NAMESPACE
%dir %{_libdir}/R/library/boot/po/
%lang(de) %{_libdir}/R/library/boot/po/de/
%lang(en) %{_libdir}/R/library/boot/po/en*/
%lang(fr) %{_libdir}/R/library/boot/po/fr/
%lang(ko) %{_libdir}/R/library/boot/po/ko/
%lang(pl) %{_libdir}/R/library/boot/po/pl/
%lang(ru) %{_libdir}/R/library/boot/po/ru/
%{_libdir}/R/library/boot/R/
# class
%dir %{_libdir}/R/library/class/
%{_libdir}/R/library/class/CITATION
%{_libdir}/R/library/class/DESCRIPTION
%{_libdir}/R/library/class/help/
%{_libdir}/R/library/class/html/
%{_libdir}/R/library/class/INDEX
%{_libdir}/R/library/class/libs/
%{_libdir}/R/library/class/LICENCE
%{_libdir}/R/library/class/Meta/
%{_libdir}/R/library/class/NAMESPACE
%{_libdir}/R/library/class/NEWS
%dir %{_libdir}/R/library/class/po/
%lang(de) %{_libdir}/R/library/class/po/de/
%lang(en) %{_libdir}/R/library/class/po/en*/
%lang(fr) %{_libdir}/R/library/class/po/fr/
%lang(ko) %{_libdir}/R/library/class/po/ko/
%lang(pl) %{_libdir}/R/library/class/po/pl/
%{_libdir}/R/library/class/R/
# cluster
%dir %{_libdir}/R/library/cluster/
%{_libdir}/R/library/cluster/CITATION
%{_libdir}/R/library/cluster/data/
%{_libdir}/R/library/cluster/DESCRIPTION
%{_libdir}/R/library/cluster/help/
%{_libdir}/R/library/cluster/html/
%{_libdir}/R/library/cluster/INDEX
%{_libdir}/R/library/cluster/libs/
%{_libdir}/R/library/cluster/Meta/
%{_libdir}/R/library/cluster/NAMESPACE
%{_libdir}/R/library/cluster/R/
%dir %{_libdir}/R/library/cluster/po/
%lang(de) %{_libdir}/R/library/cluster/po/de/
%lang(en) %{_libdir}/R/library/cluster/po/en*/
%lang(pl) %{_libdir}/R/library/cluster/po/pl/
# codetools
%dir %{_libdir}/R/library/codetools/
%{_libdir}/R/library/codetools/DESCRIPTION
%{_libdir}/R/library/codetools/help/
%{_libdir}/R/library/codetools/html/
%{_libdir}/R/library/codetools/INDEX
%{_libdir}/R/library/codetools/Meta/
%{_libdir}/R/library/codetools/NAMESPACE
%{_libdir}/R/library/codetools/R/
# compiler
%{_libdir}/R/library/compiler/
# datasets
%{_libdir}/R/library/datasets/
# foreign
%dir %{_libdir}/R/library/foreign/
%{_libdir}/R/library/foreign/COPYRIGHTS
%{_libdir}/R/library/foreign/DESCRIPTION
%{_libdir}/R/library/foreign/files/
%{_libdir}/R/library/foreign/help/
%{_libdir}/R/library/foreign/html/
%{_libdir}/R/library/foreign/INDEX
%{_libdir}/R/library/foreign/libs/
%{_libdir}/R/library/foreign/Meta/
%{_libdir}/R/library/foreign/NAMESPACE
%dir %{_libdir}/R/library/foreign/po/
%lang(de) %{_libdir}/R/library/foreign/po/de/
%lang(en) %{_libdir}/R/library/foreign/po/en*/
%lang(fr) %{_libdir}/R/library/foreign/po/fr/
%lang(pl) %{_libdir}/R/library/foreign/po/pl/
%{_libdir}/R/library/foreign/R/
# graphics
%{_libdir}/R/library/graphics/
# grDevices
%{_libdir}/R/library/grDevices
# grid
%{_libdir}/R/library/grid/
# KernSmooth
%dir %{_libdir}/R/library/KernSmooth/
%{_libdir}/R/library/KernSmooth/DESCRIPTION
%{_libdir}/R/library/KernSmooth/help/
%{_libdir}/R/library/KernSmooth/html/
%{_libdir}/R/library/KernSmooth/INDEX
%{_libdir}/R/library/KernSmooth/libs/
%{_libdir}/R/library/KernSmooth/Meta/
%{_libdir}/R/library/KernSmooth/NAMESPACE
%dir %{_libdir}/R/library/KernSmooth/po/
%lang(de) %{_libdir}/R/library/KernSmooth/po/de/
%lang(en) %{_libdir}/R/library/KernSmooth/po/en*/
%lang(ko) %{_libdir}/R/library/KernSmooth/po/ko/
%lang(pl) %{_libdir}/R/library/KernSmooth/po/pl/
%{_libdir}/R/library/KernSmooth/R/
# lattice
%dir %{_libdir}/R/library/lattice/
%{_libdir}/R/library/lattice/CITATION
%{_libdir}/R/library/lattice/data/
%{_libdir}/R/library/lattice/demo/
%{_libdir}/R/library/lattice/DESCRIPTION
%{_libdir}/R/library/lattice/help/
%{_libdir}/R/library/lattice/html/
%{_libdir}/R/library/lattice/INDEX
%{_libdir}/R/library/lattice/libs/
%{_libdir}/R/library/lattice/Meta/
%{_libdir}/R/library/lattice/NAMESPACE
%{_libdir}/R/library/lattice/NEWS
%dir %{_libdir}/R/library/lattice/po/
%lang(de) %{_libdir}/R/library/lattice/po/de/
%lang(en) %{_libdir}/R/library/lattice/po/en*/
%lang(fr) %{_libdir}/R/library/lattice/po/fr/
%{_libdir}/R/library/lattice/R/
# MASS
%dir %{_libdir}/R/library/MASS/
%{_libdir}/R/library/MASS/CITATION
%{_libdir}/R/library/MASS/data/
%{_libdir}/R/library/MASS/DESCRIPTION
%{_libdir}/R/library/MASS/help/
%{_libdir}/R/library/MASS/html/
%{_libdir}/R/library/MASS/INDEX
%{_libdir}/R/library/MASS/libs/
%{_libdir}/R/library/MASS/LICENCE
%{_libdir}/R/library/MASS/Meta/
%{_libdir}/R/library/MASS/NAMESPACE
%{_libdir}/R/library/MASS/NEWS
%dir %{_libdir}/R/library/MASS/po
%lang(de) %{_libdir}/R/library/MASS/po/de/
%lang(en) %{_libdir}/R/library/MASS/po/en*/
%lang(fr) %{_libdir}/R/library/MASS/po/fr/
%lang(ko) %{_libdir}/R/library/MASS/po/ko/
%lang(pl) %{_libdir}/R/library/MASS/po/pl/
%{_libdir}/R/library/MASS/R/
%{_libdir}/R/library/MASS/scripts/
# Matrix
%dir %{_libdir}/R/library/Matrix/
%{_libdir}/R/library/Matrix/Copyrights
%{_libdir}/R/library/Matrix/data/
%{_libdir}/R/library/Matrix/doc/
%{_libdir}/R/library/Matrix/DESCRIPTION
%{_libdir}/R/library/Matrix/Doxyfile
%{_libdir}/R/library/Matrix/external/
%{_libdir}/R/library/Matrix/help/
%{_libdir}/R/library/Matrix/html/
%{_libdir}/R/library/Matrix/include/
%{_libdir}/R/library/Matrix/INDEX
%{_libdir}/R/library/Matrix/libs/
%{_libdir}/R/library/Matrix/Meta/
%{_libdir}/R/library/Matrix/NAMESPACE
%dir %{_libdir}/R/library/Matrix/po/
%lang(de) %{_libdir}/R/library/Matrix/po/de/
%lang(en) %{_libdir}/R/library/Matrix/po/en*/
%lang(pl) %{_libdir}/R/library/Matrix/po/pl/
%{_libdir}/R/library/Matrix/R/
%{_libdir}/R/library/Matrix/test-tools.R
%{_libdir}/R/library/Matrix/test-tools-1.R
%{_libdir}/R/library/Matrix/test-tools-Matrix.R
# methods
%{_libdir}/R/library/methods/
# mgcv
%{_libdir}/R/library/mgcv/
# nlme
%dir %{_libdir}/R/library/nlme/
%{_libdir}/R/library/nlme/CITATION
%{_libdir}/R/library/nlme/data/
%{_libdir}/R/library/nlme/DESCRIPTION
%{_libdir}/R/library/nlme/help/
%{_libdir}/R/library/nlme/html/
%{_libdir}/R/library/nlme/INDEX
%{_libdir}/R/library/nlme/libs/
%{_libdir}/R/library/nlme/LICENCE
%{_libdir}/R/library/nlme/Meta/
%{_libdir}/R/library/nlme/mlbook/
%{_libdir}/R/library/nlme/NAMESPACE
%dir %{_libdir}/R/library/nlme/po/
%lang(de) %{_libdir}/R/library/nlme/po/de/
%lang(en) %{_libdir}/R/library/nlme/po/en*/
%lang(fr) %{_libdir}/R/library/nlme/po/fr/
%lang(pl) %{_libdir}/R/library/nlme/po/pl/
%{_libdir}/R/library/nlme/R/
%{_libdir}/R/library/nlme/scripts/
# nnet
%dir %{_libdir}/R/library/nnet/
%{_libdir}/R/library/nnet/CITATION
%{_libdir}/R/library/nnet/DESCRIPTION
%{_libdir}/R/library/nnet/help/
%{_libdir}/R/library/nnet/html/
%{_libdir}/R/library/nnet/INDEX
%{_libdir}/R/library/nnet/libs/
%{_libdir}/R/library/nnet/LICENCE
%{_libdir}/R/library/nnet/Meta/
%{_libdir}/R/library/nnet/NAMESPACE
%{_libdir}/R/library/nnet/NEWS
%dir %{_libdir}/R/library/nnet/po
%lang(de) %{_libdir}/R/library/nnet/po/de/
%lang(en) %{_libdir}/R/library/nnet/po/en*/
%lang(fr) %{_libdir}/R/library/nnet/po/fr/
%lang(ko) %{_libdir}/R/library/nnet/po/ko/
%lang(pl) %{_libdir}/R/library/nnet/po/pl/
%{_libdir}/R/library/nnet/R/
# parallel
%{_libdir}/R/library/parallel/
# rpart
%dir %{_libdir}/R/library/rpart/
%{_libdir}/R/library/rpart/data/
%{_libdir}/R/library/rpart/DESCRIPTION
%{_libdir}/R/library/rpart/doc/
%{_libdir}/R/library/rpart/help/
%{_libdir}/R/library/rpart/html/
%{_libdir}/R/library/rpart/INDEX
%{_libdir}/R/library/rpart/libs/
%{_libdir}/R/library/rpart/Meta/
%{_libdir}/R/library/rpart/NAMESPACE
%{_libdir}/R/library/rpart/NEWS.Rd
%dir %{_libdir}/R/library/rpart/po
%lang(de) %{_libdir}/R/library/rpart/po/de/
%lang(en) %{_libdir}/R/library/rpart/po/en*/
%lang(fr) %{_libdir}/R/library/rpart/po/fr/
%lang(ko) %{_libdir}/R/library/rpart/po/ko/
%lang(pl) %{_libdir}/R/library/rpart/po/pl/
%lang(ru) %{_libdir}/R/library/rpart/po/ru/
%{_libdir}/R/library/rpart/R/
# spatial
%dir %{_libdir}/R/library/spatial/
%{_libdir}/R/library/spatial/CITATION
%{_libdir}/R/library/spatial/DESCRIPTION
%{_libdir}/R/library/spatial/help/
%{_libdir}/R/library/spatial/html/
%{_libdir}/R/library/spatial/INDEX
%{_libdir}/R/library/spatial/libs/
%{_libdir}/R/library/spatial/LICENCE
%{_libdir}/R/library/spatial/Meta/
%{_libdir}/R/library/spatial/NAMESPACE
%{_libdir}/R/library/spatial/NEWS
%dir %{_libdir}/R/library/spatial/po
%lang(de) %{_libdir}/R/library/spatial/po/de/
%lang(en) %{_libdir}/R/library/spatial/po/en*/
%lang(fr) %{_libdir}/R/library/spatial/po/fr/
%lang(pl) %{_libdir}/R/library/spatial/po/pl/
%{_libdir}/R/library/spatial/ppdata/
%{_libdir}/R/library/spatial/PP.files
%{_libdir}/R/library/spatial/R/
# splines
%{_libdir}/R/library/splines/
# stats
%{_libdir}/R/library/stats/
# stats4
%{_libdir}/R/library/stats4/
# survival
%{_libdir}/R/library/survival/
# tcltk
%{_libdir}/R/library/tcltk/
# tools
%{_libdir}/R/library/tools/
# utils
%{_libdir}/R/library/utils/
%{_libdir}/R/modules
%{_libdir}/R/COPYING
%{_libdir}/R/NEWS*
%{_libdir}/R/SVN-REVISION
/usr/lib/rpm/R-make-search-index.sh
%{_infodir}/R-*.info*
%{_sysconfdir}/rpm/macros.R
%{_mandir}/man1/*
%{_docdir}/R-%{version}
%docdir %{_docdir}/R-%{version}
/etc/ld.so.conf.d/*

%files core-devel
%defattr(-, root, root, -)
%{_libdir}/pkgconfig/libR.pc
%{_includedir}/R
# Symlink to %{_includedir}/R/
%{_libdir}/R/include

%files devel
# Nothing, all files provided by R-core-devel

%if %{modern}
%files java
# Nothing, all files provided by R-core

%files java-devel
# Nothing, all files provided by R-core-devel
%endif

%files -n libRmath
%defattr(-, root, root, -)
%doc doc/COPYING
%{_libdir}/libRmath.so

%files -n libRmath-devel
%defattr(-, root, root, -)
%{_includedir}/Rmath.h
%{_libdir}/pkgconfig/libRmath.pc

%files -n libRmath-static
%defattr(-, root, root, -)
%{_libdir}/libRmath.a

%clean
rm -rf ${RPM_BUILD_ROOT};

%post core
# Create directory entries for info files
# (optional doc files, so we must check that they are installed)
for doc in admin exts FAQ intro lang; do
   file=%{_infodir}/R-${doc}.info.gz
   if [ -e $file ]; then
      /sbin/install-info ${file} %{_infodir}/dir 2>/dev/null || :
   fi
done
/sbin/ldconfig
R CMD javareconf \
    JAVA_HOME=%{_jvmdir}/jre \
    JAVA_CPPFLAGS='-I%{_jvmdir}/java/include\ -I%{_jvmdir}/java/include/linux' \
    JAVA_LIBS='-L%{_jvmdir}/jre/lib/%{java_arch}/server \
    -L%{_jvmdir}/jre/lib/%{java_arch}\ -L%{_jvmdir}/java/lib/%{java_arch} \
    -L/usr/java/packages/lib/%{java_arch}\ -L/lib\ -L/usr/lib\ -ljvm' \
    JAVA_LD_LIBRARY_PATH=%{_jvmdir}/jre/lib/%{java_arch}/server:%{_jvmdir}/jre/lib/%{java_arch}:%{_jvmdir}/java/lib/%{java_arch}:/usr/java/packages/lib/%{java_arch}:/lib:/usr/lib \
    > /dev/null 2>&1 || exit 0

# With 2.10.0, we no longer need to do any of this.

# Update package indices
# %__cat %{_libdir}/R/library/*/CONTENTS > %{_docdir}/R-%{version}/html/search/index.txt 2>/dev/null
# Don't use .. based paths, substitute RHOME
# sed -i "s!../../..!%{_libdir}/R!g" %{_docdir}/R-%{version}/html/search/index.txt

# This could fail if there are no noarch R libraries on the system.
# %__cat %{_datadir}/R/library/*/CONTENTS >> %{_docdir}/R-%{version}/html/search/index.txt 2>/dev/null || exit 0
# Don't use .. based paths, substitute /usr/share/R
# sed -i "s!../../..!/usr/share/R!g" %{_docdir}/R-%{version}/html/search/index.txt


%preun core
if [ $1 = 0 ]; then
   # Delete directory entries for info files (if they were installed)
   for doc in admin exts FAQ intro lang; do
      file=%{_infodir}/R-${doc}.info.gz
      if [ -e ${file} ]; then
         /sbin/install-info --delete R-${doc} %{_infodir}/dir 2>/dev/null || :
      fi
   done
fi

%postun core
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/mktexlsr %{_datadir}/texmf &>/dev/null || :
fi

%posttrans core
/usr/bin/mktexlsr %{_datadir}/texmf &>/dev/null || :

%if %{modern}
%post java
R CMD javareconf \
    JAVA_HOME=%{_jvmdir}/jre \
    JAVA_CPPFLAGS='-I%{_jvmdir}/java/include\ -I%{_jvmdir}/java/include/linux' \
    JAVA_LIBS='-L%{_jvmdir}/jre/lib/%{java_arch}/server \
    -L%{_jvmdir}/jre/lib/%{java_arch}\ -L%{_jvmdir}/java/lib/%{java_arch} \
    -L/usr/java/packages/lib/%{java_arch}\ -L/lib\ -L/usr/lib\ -ljvm' \
    JAVA_LD_LIBRARY_PATH=%{_jvmdir}/jre/lib/%{java_arch}/server:%{_jvmdir}/jre/lib/%{java_arch}:%{_jvmdir}/java/lib/%{java_arch}:/usr/java/packages/lib/%{java_arch}:/lib:/usr/lib \
    > /dev/null 2>&1 || exit 0

%post java-devel
R CMD javareconf \
    JAVA_HOME=%{_jvmdir}/jre \
    JAVA_CPPFLAGS='-I%{_jvmdir}/java/include\ -I%{_jvmdir}/java/include/linux' \
    JAVA_LIBS='-L%{_jvmdir}/jre/lib/%{java_arch}/server \
    -L%{_jvmdir}/jre/lib/%{java_arch}\ -L%{_jvmdir}/java/lib/%{java_arch} \
    -L/usr/java/packages/lib/%{java_arch}\ -L/lib\ -L/usr/lib\ -ljvm' \
    JAVA_LD_LIBRARY_PATH=%{_jvmdir}/jre/lib/%{java_arch}/server:%{_jvmdir}/jre/lib/%{java_arch}:%{_jvmdir}/java/lib/%{java_arch}:/usr/java/packages/lib/%{java_arch}:/lib:/usr/lib \
    > /dev/null 2>&1 || exit 0
%endif

%post -n libRmath -p /sbin/ldconfig

%postun -n libRmath -p /sbin/ldconfig

%changelog
* Thu May 09 2013 David Hrbáč <david@hrbac.cz> - 3.0.0-2
- initial rebuild

* Sat Apr 13 2013 Tom Callaway <spot@fedoraproject.org> - 3.0.0-2
- add Requires: tex(inconsolata.sty) to -core-devel to fix module PDF building

* Fri Apr  5 2013 Tom Callaway <spot@fedoraproject.org> - 3.0.0-1
- update to 3.0.0

* Wed Feb 27 2013 Tom Callaway <spot@fedoraproject.org> - 2.15.2-7
- add BuildRequires: xz-devel (for system xz/lzma support)
- create R-core-devel

* Sat Jan 26 2013 Kevin Fenzi <kevin@scrye.com> - 2.15.2-6
- Rebuild for new icu

* Sun Jan 20 2013 Tom Callaway <spot@fedoraproject.org> - 2.15.2-5
- apply upstream fix for cairo issues (bz 891983)

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.15.2-4
- rebuild due to "jpeg8-ABI" feature drop

* Tue Nov 27 2012 Tom Callaway <spot@fedoraproject.org> - 2.15.2-3
- add Requires: tex(cm-super-ts1.enc) for R-devel

* Tue Nov 27 2012 Tom Callaway <spot@fedoraproject.org> - 2.15.2-2
- add additional TeX font requirements to R-devel for Fedora 18+ (due to new texlive)

* Mon Oct 29 2012 Tom Callaway <spot@fedoraproject.org> - 2.15.2-1
- update to 2.15.2
- R now Requires: R-java (for a more complete base install)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Tom Callaway <spot@fedoraproject.org> - 2.15.1-1
- update to 2.15.1

* Mon Jul  2 2012 Jindrich Novy <jnovy@redhat.com> - 2.15.0-4
- fix LaTeX and dvips dependencies (#836817)

* Mon May  7 2012 Tom Callaway <spot@fedoraproject.org> - 2.15.0-3
- rebuild for new libtiff

* Tue Apr 24 2012 Tom Callaway <spot@fedoraproject.org> - 2.15.0-2
- rebuild for new icu

* Fri Mar 30 2012 Tom Callaway <spot@fedoraproject.org> - 2.15.0-1
- Update to 2.15.0

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.14.1-3
- Rebuild against PCRE 8.30

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jan  4 2012 Tom Callaway <spot@fedoraproject.org> - 2.14.1-1
- update to 2.14.1

* Tue Nov  8 2011 Tom Callaway <spot@fedoraproject.org> - 2.14.0-3
- No inconsolata for EL

* Mon Nov  7 2011 Tom Callaway <spot@fedoraproject.org> - 2.14.0-2
- add texinfo-tex to Requires for -devel package

* Wed Nov  2 2011 Tom Callaway <spot@fedoraproject.org> - 2.14.0-1
- update to 2.14.0

* Fri Oct  7 2011 Tom Callaway <spot@fedoraproject.org> - 2.13.2-1
- update to 2.13.2

* Mon Sep 12 2011 Michel Salim <salimma@fedoraproject.org> - 2.13.1-5
- rebuild for libicu 4.8.x

* Tue Aug  9 2011 Tom Callaway <spot@fedoraproject.org> - 2.13.1-4
- fix salimma's scriptlets to be on -core instead of the metapackage

* Tue Aug  9 2011 Michel Salim <salimma@fedoraproject.org> - 2.13.1-3
- Symlink LaTeX files, and rehash on package change when possible (# 630835)

* Mon Aug  8 2011 Tom Callaway <spot@fedoraproject.org> - 2.13.1-2
- add BuildRequires: less

* Mon Jul 11 2011 Tom Callaway <spot@fedoraproject.org> - 2.13.1-1
- update to 2.13.1

* Tue Apr 12 2011 Tom Callaway <spot@fedoraproject.org> - 2.13.0-1
- update to 2.13.0
- add convenience symlink for include directory (bz 688295)

* Mon Mar 07 2011 Caolán McNamara <caolanm@redhat.com> - 2.12.2-2
- rebuild for icu 4.6

* Sun Feb 27 2011 Tom Callaway <spot@fedoraproject.org> - 2.12.2-1
- update to 2.12.2

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Tom Callaway <spot@fedoraproject.org> - 2.12.1-1
- update to 2.12.1

* Wed Oct 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.12.0-1
- update to 2.12.0

* Wed Jul  7 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.11.1-4
- include COPYING in libRmath package

* Wed Jun 30 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.11.1-3
- move libRmath static lib into libRmath-static subpackage

* Thu Jun  3 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.11.1-2
- overload R_LIBS_SITE instead of R_LIBS

* Tue Jun  1 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.11.1-1
- update to 2.11.1

* Thu Apr 22 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.11.0-1
- update to 2.11.0

* Fri Apr 02 2010 Caolán McNamara <caolanm@redhat.com> - 2.10.1-2
- rebuild for icu 4.4

* Mon Dec 21 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10.1-1
- update to 2.10.1
- enable static html pages

* Mon Nov  9 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10.0-2
- get rid of index.txt scriptlet on R-core (bz 533572)
- leave macro in place, but don't call /usr/lib/rpm/R-make-search-index.sh equivalent anymore
- add version check to see if we need to run R-make-search-index.sh guts

* Wed Nov  4 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10.0-1
- update to 2.10.0
- use correct compiler for ARM

* Thu Oct 15 2009 Karsten Hopp <karsten@redhat.com> 2.9.2-2
- s390 (not s390x) needs the -m31 compiler flag

* Mon Aug 24 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.9.2-1
- Update to 2.9.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.9.1-2
- don't try to make the PDFs in rawhide/i586

* Thu Jul  9 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.9.1-1
- update to 2.9.1
- fix versioned provides

* Mon Apr 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.9.0-2
- properly Provide/Obsolete R-Matrix

* Fri Apr 17 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.9.0-1
- update to 2.9.0, change vim dep to vi

* Tue Apr  7 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.1-9
- drop profile.d scripts, they broke more than they fixed
- minimize hard-coded Requires based on Martyn Plummer's analysis

* Sat Mar 28 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.1-8
- fix profile scripts for situation where R_HOME is already defined
  (bugzilla 492706)

* Tue Mar 24 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.1-7
- bump for new tag

* Tue Mar 24 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.1-6
- add profile.d scripts to set R_HOME 
- rpmlint cleanups

* Mon Mar 23 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.1-5
- add R-java and R-java-devel "dummy" packages, so that we can get java dependent R-modules 
  to build/install

* Wed Mar  4 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.1-4
- update post scriptlet (bz 477076)

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan  5 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.8.1-2
- add pango-devel to BuildRequires (thanks to Martyn Plummer and Peter Dalgaard)
- fix libRmath requires to need V-R (thanks to Martyn Plummer)

* Mon Dec 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.8.1-1
- update javareconf call in %%post (bz 477076)
- 2.8.1

* Sun Oct 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.8.0-2
- enable libtiff interface

* Sun Oct 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.8.0-1
- Update to 2.8.0
- New subpackage layout: R-core is functional userspace, R is metapackage 
  requiring everything
- Fix system bzip2 detection

* Thu Oct 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.2-2
- fix sh compile (bz 464055)

* Fri Aug 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.2-1
- update to 2.7.2
- fix spec for alpha compile (bz 458931)
- fix security issue in javareconf script (bz 460658)

* Mon Jul  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.1-1
- update to 2.7.1

* Wed May 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-5
- add cairo-devel to BR/R, so that cairo backend gets built

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-4
- fixup sed invocation added in -3
- make -devel package depend on base R = version-release
- fix bad paths in package html files

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-3
- fix poorly constructed file paths in html/packages.html (bz 442727)

* Tue May 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-2
- add patch from Martyn Plummer to avoid possible bad path hardcoding in 
  /usr/bin/Rscript
- properly handle ia64 case (bz 446181)

* Mon Apr 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-1
- update to 2.70
- rcompgen is no longer a standalone package
- redirect javareconf to /dev/null (bz 442366)

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.2-1
- properly version the items in the VR bundle
- 2.6.2
- don't use setarch for java setup
- fix R post script file

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.1-4
- multilib handling (thanks Martyn Plummer)
- Update indices in the right place.

* Mon Jan  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.1-3
- move INSTALL back into R main package, as it is useful without the 
  other -devel bits (e.g. installing noarch package from CRAN)

* Tue Dec 11 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.1-2
- based on changes from Martyn Plummer <martyn.plummer@r-project.org>
- use configure options rdocdir, rincludedir, rsharedir 
- use DESTDIR at installation
- remove obsolete generation of packages.html
- move header files and INSTALL R-devel package

* Mon Nov 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.1-1
- bump to 2.6.1

* Tue Oct 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.0-3.1
- fix missing perl requires

* Mon Oct 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.0-3
- fix multilib conflicts (bz 343061)

* Mon Oct 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.0-2
- add R CMD javareconf to post (bz 354541)
- don't pickup bogus perl provides (bz 356071)
- use xdg-open, drop requires for firefox/evince (bz 351841)

* Thu Oct  4 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.0-1
- bump to 2.6.0

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.1-3
- fix license tag
- rebuild for ppc32

* Thu Jul  5 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.1-2
- add rpm helper macros, script

* Mon Jul  2 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.1-1
- drop patch, upstream fixed
- bump to 2.5.1

* Mon Apr 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.0-2
- patch from Martyn Plummer fixes .pc files
- add new BR: gcc-objc

* Wed Apr  25 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.0-1
- bump to 2.5.0

* Tue Mar  13 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.1-4
- get rid of termcap related requires, replace with ncurses
- use java-1.5.0-gcj instead of old java-1.4.2
- add /usr/share/R/library as a valid R_LIBS directory for noarch bits

* Sun Feb  25 2007 Jef Spaleta <jspaleta@gmail.com> 2.4.1-3
- rebuild for reverted tcl/tk

* Fri Feb  2 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.1-2
- rebuild for new tcl/tk

* Tue Dec 19 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.1-1
- bump to 2.4.1
- fix install-info invocations in post/preun (bz 219407)

* Fri Nov  3 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.0-2
- sync with patched 2006-11-03 level to fix PR#9339

* Sun Oct 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.0-1
- bump for 2.4.0

* Tue Sep 12 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.1-2
- bump for FC-6

* Fri Jun  2 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.1-1
- bump to 2.3.1

* Tue Apr 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.0-2
- fix ppc build for FC-4 (artificial bump for everyone else)

* Mon Apr 24 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.0-1
- bump to 2.3.0 (also, bump module revisions)

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-5
- now BR is texinfo-tex, not texinfo in rawhide

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-4
- bump for FC-5

* Mon Jan  9 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-3
- fix BR: XFree86-devel for FC-5

* Sat Dec 31 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-2
- missing BR: libXt-devel for FC-5

* Tue Dec 20 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-1
- bump to 2.2.1

* Thu Oct  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.0-2
- use fixed system lapack for FC-4 and devel

* Thu Oct  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.0-1
- bump to 2.2.0

* Mon Jul  4 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.1-2
- fix version numbers on supplemental package provides

* Mon Jun 20 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.1-1
- bugfix update

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.0-51
- proper library handling

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.0-50
- 2.1.0, fc4 version.
- The GNOME GUI is unbundled, now provided as a package on CRAN

* Thu Apr 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-50
- big bump. This is the fc4 package, the fc3 package is 2.0.1-11
- enable gnome gui, add requires as needed

* Thu Apr 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-10
- bump for cvs errors

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-9
- fix URL for Source0

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-8
- spec file cleanup

* Fri Apr  1 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-7
- use evince instead of ggv
- make custom provides for R subfunctions

* Wed Mar 30 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-6
- configure now calls --enable-R-shlib

* Thu Mar 24 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-5
- cleaned up package for Fedora Extras

* Mon Feb 28 2005 Martyn Plummer <plummer@iarc.fr> 0:2.0.1-0.fdr.4
- Fixed file ownership in R-devel and libRmath packages

* Wed Feb 16 2005 Martyn Plummer <plummer@iarc.fr> 0:2.0.1-0.fdr.3
- R-devel package is now a stub package with no files, except a documentation
  file (RPM won't accept sub-packages with no files). R now conflicts
  with earlier (i.e 0:2.0.1-0.fdr.2) versions of R-devel.
- Created libRmath subpackage with shared library.

* Mon Jan 31 2005 Martyn Plummer <plummer@iarc.fr> 0:2.0.1-0.fdr.2
- Created R-devel and libRmath-devel subpackages

* Mon Nov 15 2004 Martyn Plummer <plummer@iarc.fr> 0:2.0.1-0.fdr.1
- Built R 2.0.1

* Wed Nov 10 2004 Martyn Plummer <plummer@iarc.fr> 0:2.0.0-0.fdr.3
- Set R_PRINTCMD at configure times so that by default getOption(printcmd)
  gives "lpr".
- Define macro fcx for all Fedora distributions. This replaces Rinfo

* Tue Oct 12 2004 Martyn Plummer <plummer@iarc.fr> 0:2.0.0-0.fdr.2
- Info support is now conditional on the macro Rinfo, which is only
  defined for Fedora 1 and 2. 

* Thu Oct 7 2004 Martyn Plummer <plummer@iarc.fr> 0:2.0.0-0.fdr.1
- Built R 2.0.0
- There is no longer a BUGS file, so this is not installed as a 
  documentation file.

* Mon Aug  9 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.1-0.fdr.4
- Added gcc-g++ to the list of BuildRequires for all platforms.
  Although a C++ compiler is not necessary to build R, it must
  be present at configure time or R will not be correctly configured
  to build packages containing C++ code.

* Thu Jul  1 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.1-0.fdr.3
- Modified BuildRequires so we can support older Red Hat versions without
  defining any macros.

* Wed Jun 23 2004 Martyn Plummer <plummner@iarc.fr> 0:1.9.1-0.fdr.2
- Added libtermcap-devel as BuildRequires for RH 8.0 and 9. Without
  this we get no readline support.

* Mon Jun 21 2004 Martyn Plummer <plummner@iarc.fr> 0:1.9.1-0.fdr.1
- Build R 1.9.1
- Removed Xorg patch since fix is now in R sources

* Mon Jun 14 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.0-0.fdr.4
- Added XFree86-devel as conditional BuildRequires for rh9, rh80

* Tue Jun 08 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.0-0.fdr.3
- Corrected names for fc1/fc2/el3 when using conditional BuildRequires
- Configure searches for C++ preprocessor and fails if we don't have
  gcc-c++ installed. Added to BuildRequires for FC2.

* Tue Jun 08 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.0-0.fdr.2
- Added patch to overcome problems with X.org headers (backported
  from R 1.9.1; patch supplied by Graeme Ambler)
- Changed permissions of source files to 644 to please rpmlint

* Mon May 03 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.0-0.fdr.1
- R.spec file now has mode 644. Previously it was unreadable by other
  users and this was causing a crash building under mach.
- Changed version number to conform to Fedora conventions. 
- Removed Provides: and Obsoletes: R-base, R-recommended, which are
  now several years old. Nobody should have a copy of R-base on a 
  supported platform.
- Changed buildroot to Fedora standard
- Added Requires(post,preun): info
- Redirect output from postinstall/uninstall scripts to /dev/null
- Added BuildRequires tags necessary to install R with full 
  capabilities on a clean mach buildroot. Conditional buildrequires
  for tcl-devel and tk-devel which were not present on RH9 or earlier.

* Thu Apr 01 2004 Martyn Plummer <plummer@iarc.fr>
- Added patch to set environment variable LANG to C in shell wrapper,
  avoiding warnings about UTF-8 locale not being supported

* Mon Mar 15 2004 Martyn Plummer <plummer@iarc.fr>
- No need to export optimization flags. This is done by %%configure
- Folded info installation into %%makeinstall 
- Check that RPM_BASE_ROOT is not set to "/" before cleaning up

* Tue Feb 03 2004 Martyn Plummer <plummer@iarc.fr>
- Removed tcl-devel from BuildRequires

* Tue Feb 03 2004 Martyn Plummer <plummer@iarc.fr>
- Changes from James Henstridge <james@daa.com.au> to allow building on IA64:
- Added BuildRequires for tcl-devel tk-devel tetex-latex
- Use the %%configure macro to call the configure script
- Pass --with-tcl-config and --with-tk-config arguments to configure
- Set rhome to point to the build root during "make install"

* Wed Jan 07 2004 Martyn Plummer <plummer@iarc.fr>
- Changed obsolete "copyright" field to "license"

* Fri Nov 21 2003 Martyn Plummer <plummer@iarc.fr>
- Built 1.8.1
