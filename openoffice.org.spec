%define oootag OOO320
%define ooomilestone 12
%define rh_rpm_release 8

# rhbz#465664 jar-repacking breaks help by reordering META-INF/MANIFEST.MF
%define __jar_repack %{nil}
# undef to get english only and no-langpacks for a faster smoketest build
%define langpacks 1
# undef to revert to the traditional print dialog
%define gtkprintui 0
# whether to use stlport or gcc's stl, we're basically locked to stlport
# for i386 to enable third party built against "vanilla OOo" uno components 
# and add-ons to work with our OOo. We assume there aren't any such for the
# other archs
%ifarch %{ix86}
%define stlport_abi_lockin 1
%else
%define stlport_abi_lockin 0
%endif

%if %{stlport_abi_lockin}
%define stlflags --with-stlport
%else
%define stlflags --without-stlport
%endif

%define jdkflags --with-jdk-home=/usr/lib/jvm/java-1.4.2-gcj
%define jdk_link_ver 1.4.2

%if %{langpacks}
%define langpack_langs af ar bg bn ca cs cy da de dz el en-US es et eu fi fr ga gl gu pa-IN he hi-IN hu hr it ja ko lt ms nb nl nn nr pl pt pt-BR ru sh sk sl sr ss st sv ta th tr ve xh zh-CN zh-TW zu ns tn ts as mr ml or te ur kn uk mai ro
%else
%define langpack_langs en-US
%endif

%define ooo_base_name %{oootag}_m%{ooomilestone}

Summary:        OpenOffice.org comprehensive office suite
Name:           openoffice.org
Version:        3.2.0
Release:        %{ooomilestone}.%{rh_rpm_release}%{?dist}
Epoch:          1
License:        LGPLv3 and LGPLv2+ and MPLv1.1 and BSD
Group:          Applications/Productivity
URL:            http://www.openoffice.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        %{ooo_base_name}.tar.bz2
Source1:        http://cgit.freedesktop.org/ooo-build/ooo-build/plain/src/evolocal.odb
Source2:        http://people.redhat.com/caolanm/templates/Tigert-templates.tar.gz
Source3:        documentation.openoffice.org-templates.tar.gz
Source4:        http://people.redhat.com/caolanm/templates/redhat-templates.tar.gz
Source5:        http://tools.openoffice.org/unowinreg_prebuild/680/unowinreg.dll
Source6:        redhat-registry.tar.gz
Source7:        redhat-langpacks.tar.gz
Source8:        redhat-agreement.xsl
Source9:        openoffice.org-javafilter.desktop
Source10:       http://www.openoffice.org/nonav/issues/showattachment.cgi/65132/acor_ga-IE.dat
Source11:       openoffice.org-multiliblauncher.sh
Source12:       http://www.openoffice.org/nonav/issues/showattachment.cgi/66959/acor_lt.zip
BuildRequires:  zip, findutils, autoconf, flex, bison, icu, gperf, gcc-c++
BuildRequires:  binutils, java-devel, boost-devel, zlib-devel, vigra-devel
BuildRequires:  python-devel, expat-devel, libxml2-devel, libxslt-devel, bc
BuildRequires:  neon-devel, libcurl-devel, libidn-devel, pam-devel, cups-devel
BuildRequires:  libXext-devel, libXt-devel, libICE-devel, libjpeg-devel,
BuildRequires:  gecko-devel, libwpd-devel, hunspell-devel, unixODBC-devel
BuildRequires:  db4-devel, sane-backends-devel, libicu-devel, perl-Archive-Zip
BuildRequires:  freetype-devel, gtk2-devel, desktop-file-utils, hyphen-devel
BuildRequires:  evolution-data-server-devel, libtextcat-devel, nss-devel
BuildRequires:  gstreamer-devel, gstreamer-plugins-base-devel, openssl-devel
BuildRequires:  lpsolve-devel, saxon, hsqldb, bsh, lucene, lucene-contrib
BuildRequires:  mesa-libGLU-devel, redland-devel, ant, ant-apache-regexp
BuildRequires:  jakarta-commons-codec, jakarta-commons-httpclient
BuildRequires:  jakarta-commons-lang, poppler-devel, fontpackages-devel
BuildRequires:  pentaho-reporting-flow-engine, libXinerama-devel

Patch1:  openoffice.org-2.0.1.rhXXXXXX.extensions.defaulttoevo2.patch
Patch2:  openoffice.org-1.9.123.ooo53397.prelinkoptimize.desktop.patch
Patch3:  openoffice.org-2.0.1.ooo58606.sw.pre-edit.patch
Patch4:  openoffice.org-2.0.2.rh188467.printingdefaults.patch
Patch5:  openoffice.org-2.0.4.rhXXXXXX.padmin.nospadmin.patch
Patch6:  workspace.printerpullpages.patch
Patch7:  openoffice.org-2.2.0.ooo74188.sw.cursorinsideglyph.patch
Patch8:  ooo-build.ooo68717.gstreamer.video.patch
Patch9:  openoffice.org-2.2.1.ooo7065.sw.titlepagedialog.patch
Patch10: openoffice.org-2.3.0.ooo76649.httpencoding.patch
Patch11: openoffice.org-2.3.1.ooo83878.unopkg.enablelinking.patch
Patch12: openoffice.org-2.4.0.ooo86080.unopkg.bodge.patch
Patch13: openoffice.org-3.0.0.ooo88341.sc.verticalboxes.patch
Patch14: workspace.fchints01.patch
Patch15: openoffice.org-3.0.0.ooo87970.vcl.samenamesubs.patch
Patch16: openoffice.org-3.0.0.ooo91924.svx.consistentordering.patch
Patch17: openoffice.org-3.0.1.oooXXXXX.fpicker.allformatsonsave.patch
Patch18: openoffice.org-3.1.0.ooo98137.filter.redeclared-variables.patch
Patch19: openoffice.org-2.2.0.gccXXXXX.solenv.javaregistration.patch
Patch20: openoffice.org-3.1.0.oooXXXXX.solenv.allowmissing.patch
Patch21: ooo-build.ooo2497.filter.svg.patch
Patch22: openoffice.org-3.1.0.ooo61927.sw.ww6.unicodefontencoding.patch
Patch23: workspace.slideshow1.patch
Patch24: openoffice.org-3.1.0.ooo101274.opening-a-directory.patch
Patch25: openoffice.org-3.1.0.ooo101354.filter.xhtml.do-not-label-list-headers.patch
Patch26: openoffice.org-3.1.0.ooo101355.filter.no-variables-in-keys.patch
Patch27: openoffice.org-3.1.0.ooo101567.i18npool.mailocaledata.patch
Patch28: openoffice.org-3.1.0.ooo102061.sc.cellanchoring.patch
Patch29: openoffice.org-3.1.0.ooo102142.sd.resleak.patch
Patch30: openoffice.org-2.0.0.ooo46270.svx.search-dialog.no-find-all-in-draw.patch
Patch31: openoffice.org-3.1.0.ooo104280.xmloff.lcl_IsAtEnd.wrong.patch
Patch32: openoffice.org-3.1.1.ooo104329.dbaccess.primarykeys.patch
Patch33: openoffice.org-3.1.1.ooo64671.canvas.add-support-for-font-pitch.patch
Patch34: openoffice.org-3.1.1.ooo109280.sal.justcoredump.patch
Patch35: workspace.vcl106.patch
Patch36: openoffice.org-3.1.1.ooo105784.vcl.sniffscriptforsubs.patch
Patch37: openoffice.org-3.2.0.ooo105827.filter.xpath-on-rtf-not-allowed.patch
Patch38: openoffice.org-3.2.0.ooo106032.linguistic.defaulttoplain.patch
Patch39: workspace.gsminhibit.patch
Patch40: workspace.vcl107.patch
Patch41: workspace.hb33patches1.patch
Patch42: workspace.ause109.patch
Patch43: workspace.cmcfixes67.patch
Patch44: workspace.srb1.patch
Patch45: workspace.thbfixes10.patch
Patch46: openoffice.org-3.3.0.ooo102645.fix.es.patch
Patch47: workspace.vcl108.patch
Patch48: workspace.pythonssldedux.patch
Patch49: openoffice.org-3.2.0.ooo106502.svx.fixspelltimer.patch
Patch50: openoffice.org-3.2.0.ooo47279.sd.objectsave.safe.patch
Patch51: openoffice.org-3.2.0.ooo107834.sw.pseudoattribs.patch
Patch52: workspace.writerfilter07.patch
Patch53: openoffice.org-3.3.0.ooo108246.svx.hide-sql-group-when-inactive.patch
Patch54: workspace.sw33bf02.patch
Patch55: openoffice.org-3.2.0.ooo108330.embeddedobj.outplace.readonly.os.dispatch.patch
Patch56: openoffice.org-3.2.0.ooo96362.filter.nondeterministic.order.patch
Patch57: workspace.cmcfixes70.patch
Patch58: workspace.s390xport02.patch
Patch59: openoffice.org-3.3.0.ooo108637.sfx2.uisavedir.patch
Patch60: openoffice.org-3.2.0.ooo108846.sfx2.qstartfixes.patch
Patch61: openoffice.org-3.2.0.ooo108976.svx.safestyledelete.patch
Patch62: openoffice.org-3.2.0.ooo109009.sc.tooltipcrash.patch
Patch63: workspace.x86_64_bridgefix.patch
Patch64: openoffice.org-3.2.0.ooo109210.sd.allpagesbg.patch
Patch65: openoffice.org-3.2.0.ooo95369.sw.sortedobjs.patch
Patch66: openoffice.org-3.3.0.ooo109406.sdext.pdfimport.escape-newlines-in-pdf-processor.patch
Patch67: workspace.koheicsvimport.patch
Patch68: openoffice.org-3.2.0.ooo108991.redlandfixes.patch
Patch69: openoffice.org-3.2.0.ooo101458.vcl.silencea11y.patch

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%define instdir %{_libdir}
%define baseinstdir %{instdir}/openoffice.org
%define ureinstdir %{baseinstdir}/ure
%define basisinstdir %{baseinstdir}/basis3.2
%define sdkinstdir %{baseinstdir}/basis3.2/sdk
%define oooinstdir %{instdir}/openoffice.org3
%define brinstdir %{instdir}/broffice.org3
%define fontname opensymbol
%define OFFICEUPD 320
%define UPD %nil
%define SOPOST l*

%description
OpenOffice.org is an Open Source, community-developed, multi-platform
office productivity suite.  It includes the key desktop applications,
such as a word processor, spreadsheet, presentation manager, formula
editor and drawing program, with a user interface and feature set
similar to other office suites.  Sophisticated and flexible,
OpenOffice.org also works transparently with a variety of file
formats, including Microsoft Office.

Usage: Simply type "ooffice" to run OpenOffice.org or select the
requested component (Writer, Calc, Impress, etc.) from your
desktop menu. On first start a few files will be installed in the 
user's home, if necessary.

%package core
Summary: Core modules for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-%{fontname}-fonts = %{epoch}:%{version}-%{release}
Requires: %{name}-ure = %{epoch}:%{version}-%{release}
Requires: liberation-sans-fonts >= 1.0, liberation-serif-fonts >= 1.0, liberation-mono-fonts >= 1.0
Requires: dejavu-sans-fonts, dejavu-serif-fonts, dejavu-sans-mono-fonts
Requires: hunspell-en, hyphen-en, hyphen >= 2.4, autocorr-en
Requires: saxon, lucene
Requires(pre):    gtk2 >= 2.9.4
Requires(post):   gtk2 >= 2.9.4
Requires(preun):  gtk2 >= 2.9.4
Requires(postun): gtk2 >= 2.9.4
Obsoletes: openoffice.org < 1.9.0
Obsoletes: openoffice.org-libs < 1.9.0
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-kde < 1.9.0
Obsoletes: openoffice.org-langpack-eo < 1:2.0.0
Obsoletes: openoffice.org2-core < 1:3.0.0

%description core
The shared core libraries and support files for OpenOffice.org.

%package brand
Summary: Core brand for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}

%description brand
The shared core branding files for OpenOffice.org.

%package -n broffice.org-brand
Summary: Core brand for BrOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: %{name}-langpack-pt_BR = %{epoch}:%{version}-%{release}

%description -n broffice.org-brand
The shared core branding files for BrOffice.org

%package pyuno
Summary: Python support for OpenOffice.org
Group: Development/Libraries
Obsoletes: openoffice.org2-pyuno < 1:3.0.0
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: %{name}-ure = %{epoch}:%{version}-%{release}
Requires: python
Requires(pre):    openoffice.org-core
Requires(post):   openoffice.org-core
Requires(preun):  openoffice.org-core
Requires(postun): openoffice.org-core

%description pyuno
Python bindings for the OpenOffice.org UNO component model. Allows scripts both
external to OpenOffice.org and within the internal OpenOffice.org scripting
framework to be written in python.

%package base-core
Summary: Database GUI libraries for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: %{name}-calc-core = %{epoch}:%{version}-%{release}
Requires: %{name}-ure = %{epoch}:%{version}-%{release}
Requires: hsqldb, postgresql-jdbc

%description base-core
GUI database libraries for OpenOffice.org.

%package base
Summary: Database frontend for OpenOffice.org
Group: Applications/Productivity
Obsoletes: openoffice.org2-base < 1:3.0.0
Requires: %{name}-brand = %{epoch}:%{version}-%{release}
Requires: %{name}-base-core = %{epoch}:%{version}-%{release}

%description base
GUI database frontend for OpenOffice.org. Allows creation and management of 
databases through a GUI.

%package -n broffice.org-base
Summary: Database frontend for BrOffice.org
Group: Applications/Productivity
Requires: broffice.org-brand = %{epoch}:%{version}-%{release}
Requires: %{name}-base-core = %{epoch}:%{version}-%{release}

%description -n broffice.org-base
GUI database frontend for BrOffice.org. Allows creation and management of 
databases through a GUI.

%package report-builder
Summary: Create database reports from OpenOffice.org
Group: Applications/Productivity
Requires: pentaho-reporting-flow-engine
Requires: %{name}-base-core = %{epoch}:%{version}-%{release}
Requires(pre):    openoffice.org-core
Requires(post):   openoffice.org-core
Requires(preun):  openoffice.org-core
Requires(postun): openoffice.org-core

%description report-builder
Creates database reports from OpenOffice.org databases. The report builder can
define group and page headers as well as group, page footers and calculation
fields to accomplish complex database reports.

%package bsh
Summary: BeanShell support for OpenOffice.org
Group: Development/Libraries
Requires: bsh
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires(pre):    openoffice.org-core
Requires(post):   openoffice.org-core
Requires(preun):  openoffice.org-core
Requires(postun): openoffice.org-core

%description bsh
Support BeanShell scripts in OpenOffice.org.

%package rhino
Summary: JavaScript support for OpenOffice.org
Group: Development/Libraries
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires(pre):    openoffice.org-core
Requires(post):   openoffice.org-core
Requires(preun):  openoffice.org-core
Requires(postun): openoffice.org-core

%description rhino
Support JavaScript scripts in OpenOffice.org.

%package wiki-publisher
Summary: Create Wiki articles on MediaWiki servers with OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-writer-core = %{epoch}:%{version}-%{release}
Requires: jakarta-commons-codec, jakarta-commons-httpclient
Requires: jakarta-commons-lang, jakarta-commons-logging
Requires(pre):    openoffice.org-core
Requires(post):   openoffice.org-core
Requires(preun):  openoffice.org-core
Requires(postun): openoffice.org-core

%description wiki-publisher
The Wiki Publisher enables you to create Wiki articles on MediaWiki servers
without having to know the syntax of the MediaWiki markup language. Publish
your new and existing documents transparently with writer to a wiki page.

%package ogltrans
Summary: 3D OpenGL slide transitions for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-impress-core = %{epoch}:%{version}-%{release}
Requires(pre):    openoffice.org-core

%description ogltrans
OpenGL Transitions enable 3D slide transitions to be used in OpenOffice.org.
Requires good quality 3D support for your videocard for best
experience.

%package presentation-minimizer
Summary: Shrink OpenOffice.org presentations
Group: Applications/Productivity
Requires: %{name}-impress-core = %{epoch}:%{version}-%{release}
Requires(pre):    openoffice.org-core
Requires(post):   openoffice.org-core
Requires(preun):  openoffice.org-core
Requires(postun): openoffice.org-core

%description presentation-minimizer
The Presentation Minimizer is used to reduce the file size of the current
presentation. Images will be compressed, and data that is no longer needed will
be removed.

%package presenter-screen
Summary: Presenter Screen for OpenOffice.org Presentations
Group: Applications/Productivity
Requires: %{name}-impress-core = %{epoch}:%{version}-%{release}
Requires(pre):    openoffice.org-core
Requires(post):   openoffice.org-core
Requires(preun):  openoffice.org-core
Requires(postun): openoffice.org-core

%description presenter-screen
The Presenter Screen is used to provides information on a second screen, that
typically is not visible to the audience when delivering a presentation. e.g.
slide notes.

%package pdfimport
Summary: PDF Importer for OpenOffice.org Draw
Group: Applications/Productivity
Requires: %{name}-draw-core = %{epoch}:%{version}-%{release}
Requires(pre):    openoffice.org-core
Requires(post):   openoffice.org-core
Requires(preun):  openoffice.org-core
Requires(postun): openoffice.org-core

%description pdfimport
The PDF Importer imports PDF into drawing documents to preserve layout
and enable basic editing of PDF documents.

%package %{fontname}-fonts
Summary: OpenOffice.org dingbats font
Group: User Interface/X
Requires: fontpackages-filesystem
BuildArch: noarch

%description %{fontname}-fonts
A dingbats font, OpenSymbol, suitable for use by OpenOffice.org for bullets and
mathematical symbols. 

%package writer-core
Summary: Word Processor libraries for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: %{name}-ure = %{epoch}:%{version}-%{release}
Requires: libwpd >= 0.8.0

%description writer-core
The wordprocessor libraries of OpenOffice.org.

%package writer
Summary: OpenOffice.org Word Processor Application
Group: Applications/Productivity
Obsoletes: openoffice.org < 1.9.0
Obsoletes: openoffice.org2-writer < 1:3.0.0
Requires: %{name}-brand = %{epoch}:%{version}-%{release}
Requires: %{name}-writer-core = %{epoch}:%{version}-%{release}

%description writer
The OpenOffice.org Word Processor application.

%package -n broffice.org-writer
Summary: BrOffice.org Word Processor Application
Group: Applications/Productivity
Requires: broffice.org-brand = %{epoch}:%{version}-%{release}
Requires: %{name}-writer-core = %{epoch}:%{version}-%{release}

%description -n broffice.org-writer
The BrOffice.org Word Processor application.

%package emailmerge
Summary: Email mail-merge component for OpenOffice.org
Group: Applications/Productivity
Obsoletes: openoffice.org2-emailmerge < 1:3.0.0
Requires: %{name}-writer-core = %{epoch}:%{version}-%{release}
Requires: %{name}-pyuno = %{epoch}:%{version}-%{release}

%description emailmerge
Enables the OpenOffice.org writer module to mail-merge to email.

%package calc-core
Summary: Spreadsheet libraries for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: %{name}-ure = %{epoch}:%{version}-%{release}

%description calc-core
The spreadsheet libraries of OpenOffice.org.

%package calc
Summary: OpenOffice.org Spreadsheet Application
Group: Applications/Productivity
Requires: %{name}-brand = %{epoch}:%{version}-%{release}
Requires: %{name}-calc-core = %{epoch}:%{version}-%{release}

%description calc
The OpenOffice.org Spreadsheet application.

%package -n broffice.org-calc
Summary: BrOffice.org Spreadsheet Application
Group: Applications/Productivity
Requires: broffice.org-brand = %{epoch}:%{version}-%{release}
Requires: %{name}-calc-core = %{epoch}:%{version}-%{release}

%description -n broffice.org-calc
The BrOffice.org Spreadsheet application.

%package draw-core
Summary: Drawing libraries for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: %{name}-ure = %{epoch}:%{version}-%{release}
Requires: %{name}-graphicfilter = %{epoch}:%{version}-%{release}

%description draw-core
The drawing libraries of OpenOffice.org.

%package draw
Summary: OpenOffice.org Drawing Application
Group: Applications/Productivity
Obsoletes: openoffice.org < 1.9.0
Obsoletes: openoffice.org2-draw < 1:3.0.0
Requires: %{name}-draw-core = %{epoch}:%{version}-%{release}
Requires: %{name}-brand = %{epoch}:%{version}-%{release}
Requires: %{name}-pdfimport = %{epoch}:%{version}-%{release}

%description draw
The OpenOffice.org Drawing Application.

%package -n broffice.org-draw
Summary: BrOffice.org Drawing Application
Group: Applications/Productivity
Requires: %{name}-draw-core = %{epoch}:%{version}-%{release}
Requires: broffice.org-brand = %{epoch}:%{version}-%{release}
Requires: %{name}-pdfimport = %{epoch}:%{version}-%{release}

%description -n broffice.org-draw
The BrOffice.org Drawing Application.

%package impress-core
Summary: Presentation libraries for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-ure = %{epoch}:%{version}-%{release}
Requires: %{name}-core = %{epoch}:%{version}-%{release}

%description impress-core
The presentation libraries of OpenOffice.org.

%package impress
Summary: OpenOffice.org Presentation Application
Group: Applications/Productivity
Obsoletes: openoffice.org < 1.9.0
Obsoletes: openoffice.org2-impress < 1:3.0.0
Requires: %{name}-brand = %{epoch}:%{version}-%{release}
Requires: %{name}-impress-core = %{epoch}:%{version}-%{release}
Requires: %{name}-presenter-screen = %{epoch}:%{version}-%{release}

%description impress
The OpenOffice.org Presentation Application.

%package -n broffice.org-impress
Summary: BrOffice.org Presentation Application
Group: Applications/Productivity
Requires: broffice.org-brand = %{epoch}:%{version}-%{release}
Requires: %{name}-impress-core = %{epoch}:%{version}-%{release}
Requires: %{name}-presenter-screen = %{epoch}:%{version}-%{release}

%description -n broffice.org-impress
The BrOffice.org Presentation Application.

%package math-core
Summary: Equation editor libraries for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-ure = %{epoch}:%{version}-%{release}
Requires: %{name}-core = %{epoch}:%{version}-%{release}

%description math-core 
The math editor libraries of OpenOffice.org.

%package math
Summary: OpenOffice.org Equation Editor Application
Group: Applications/Productivity
Obsoletes: openoffice.org < 1.9.0
Obsoletes: openoffice.org2-math < 1:3.0.0
Requires: %{name}-brand = %{epoch}:%{version}-%{release}
Requires: %{name}-math-core = %{epoch}:%{version}-%{release}

%description math 
The OpenOffice.org Equation Editor Application.

%package -n broffice.org-math
Summary: BrOffice.org Equation Editor Application
Group: Applications/Productivity
Requires: broffice.org-brand = %{epoch}:%{version}-%{release}
Requires: %{name}-math-core = %{epoch}:%{version}-%{release}

%description -n broffice.org-math 
The BrOffice.org Equation Editor Application.

%package graphicfilter
Summary: OpenOffice.org Extra Graphic filters
Group: Applications/Productivity
Requires: %{name}-ure = %{epoch}:%{version}-%{release}
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Obsoletes: openoffice.org2-graphicfilter < 1:3.0.0

%description graphicfilter
The graphicfilter module for OpenOffice.org provides graphic filters,
e.g. svg and flash filters.

%package xsltfilter
Summary: Optional xsltfilter module for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Obsoletes: openoffice.org2-xsltfilter < 1:3.0.0

%description xsltfilter
The xsltfilter module for OpenOffice.org, provides additional docbook and
xhtml export transforms. Install this to enable docbook export.

%package javafilter
Summary: Optional javafilter module for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Obsoletes: openoffice.org2-javafilter < 1:3.0.0

%description javafilter
The javafilter module for OpenOffice.org, provides additional AportisDoc,
Pocket Excel and Pocket Word import filters.

%post javafilter
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun javafilter
update-desktop-database %{_datadir}/applications &> /dev/null || :

%package testtools
Summary: Testtools for OpenOffice.org
Group: Development/Libraries
Obsoletes: openoffice.org2-testtools < 1:3.0.0
Requires: %{name}-ure = %{epoch}:%{version}-%{release}
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: %{name}-writer = %{epoch}:%{version}-%{release}
Requires: %{name}-calc = %{epoch}:%{version}-%{release}
Requires: %{name}-draw = %{epoch}:%{version}-%{release}
Requires: %{name}-impress = %{epoch}:%{version}-%{release}
Requires: %{name}-base = %{epoch}:%{version}-%{release}
Requires: %{name}-math = %{epoch}:%{version}-%{release}
Requires: %{name}-bsh = %{epoch}:%{version}-%{release}
Requires: %{name}-rhino = %{epoch}:%{version}-%{release}

%description testtools
QA tools for OpenOffice.org, enables automated testing.

%package ure
Summary: UNO Runtime Environment
Group: Development/Libraries
Requires: unzip, jre >= 1.5.0

%description ure
UNO is the component model of OpenOffice.org. UNO offers interoperability
between programming languages, other components models and hardware
architectures, either in process or over process boundaries, in the Intranet
as well as in the Internet. UNO components may be implemented in and accessed
from any programming language for which a UNO implementation (AKA language
binding) and an appropriate bridge or adapter exists

%package sdk
Summary: Software Development Kit for OpenOffice.org
Group: Development/Libraries
Requires: %{name}-ure = %{epoch}:%{version}-%{release}
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: unzip, java-devel

%description sdk
The OpenOffice.org SDK is an add-on for the OpenOffice.org office suite. It
provides the necessary tools for programming using the OpenOffice.org APIs
and for creating extensions (UNO components) for OpenOffice.org.
To set the build environment for building against the sdk use 
%{sdkinstdir}/setsdkenv_unix.sh.

%package sdk-doc
Summary: Software Development Kit documentation for OpenOffice.org
Group: Documentation
Requires: %{name}-sdk = %{epoch}:%{version}-%{release}

%description sdk-doc
This provides documentation for programming using the OpenOffice.org APIs
and examples of creating extensions (UNO components) for OpenOffice.org.

%package devel
Summary: Development Libraries for OpenOffice.org
Group: Development/Libraries
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: %{name}-sdk = %{epoch}:%{version}-%{release}

%description devel
The OpenOffice.org devel package provides necessary headers for 
development against OpenOffice.org.

%package headless
Summary: OpenOffice.org Headless plugin
Group: Development/Libraries
Requires: %{name}-ure = %{epoch}:%{version}-%{release}
Requires: %{name}-core = %{epoch}:%{version}-%{release}

%description headless
A plugin for OpenOffice.org that enables it to function without an X server. 
It implements the -headless command line option and allows OpenOffice.org to be
used as a backend server for e.g. document conversion.

%package langpack-af_ZA
Summary: Afrikaans language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-af, hyphen-af, autocorr-af
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-af < 1:2.0.3
Obsoletes: openoffice.org2-langpack-af_ZA < 1:3.0.0

%description langpack-af_ZA
Provides additional Afrikaans translations and resources for OpenOffice.org.

%package langpack-ar
Summary: Arabic language pack for OpenOffice.org
Group: Applications/Productivity
Requires: hunspell-ar
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org2-langpack-ar < 1:3.0.0

%description langpack-ar
Provides additional Arabic translations and resources for OpenOffice.org.

%package langpack-bg_BG
Summary: Bulgarian language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-bg, hyphen-bg, mythes-bg, autocorr-bg
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-bg < 1:2.0.3
Obsoletes: openoffice.org2-langpack-bg_BG < 1:3.0.0

%description langpack-bg_BG
Provides additional Bulgarian translations and resources for OpenOffice.org.

%package langpack-bn
Summary: Bengali language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: lohit-bengali-fonts
Requires: hunspell-bn, hyphen-bn
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-bn_IN < 1:2.0.3
Obsoletes: openoffice.org2-langpack-bn < 1:3.0.0

%description langpack-bn
Provides additional Bengali translations and resources for OpenOffice.org.

%package langpack-ca_ES
Summary: Catalan language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-ca, hyphen-ca, mythes-ca
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-ca < 1:2.0.3
Obsoletes: openoffice.org2-langpack-ca_ES < 1:3.0.0

%description langpack-ca_ES
Provides additional Catalan translations and resources for OpenOffice.org.

%package langpack-cs_CZ
Summary: Czech language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-cs, hyphen-cs, mythes-cs, autocorr-cs
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-cs < 1:2.0.3
Obsoletes: openoffice.org2-langpack-cs_CZ < 1:3.0.0

%description langpack-cs_CZ
Provides additional Czech translations and resources for OpenOffice.org.

%package langpack-cy_GB
Summary: Welsh language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-cy, hyphen-cy
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-cy < 1:2.0.3
Obsoletes: openoffice.org2-langpack-cy_GB < 1:3.0.0


%description langpack-cy_GB
Provides additional Welsh translations and resources for OpenOffice.org.

%package langpack-da_DK
Summary: Danish language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-da, hyphen-da, mythes-da, autocorr-da
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-da < 1:2.0.3
Obsoletes: openoffice.org2-langpack-da_DK < 1:3.0.0


%description langpack-da_DK
Provides additional Danish translations and resources for OpenOffice.org.

%package langpack-de
Summary: German language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-de, hyphen-de, mythes-de, autocorr-de
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org2-langpack-de < 1:3.0.0


%description langpack-de
Provides additional German translations and resources for OpenOffice.org.

%package langpack-el_GR
Summary: Greek language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-el, hyphen-el, mythes-el
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-el < 1:2.0.3
Obsoletes: openoffice.org2-langpack-el_GR < 1:3.0.0


%description langpack-el_GR
Provides additional Greek translations and resources for OpenOffice.org.

%package langpack-en
Summary: English language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: mythes-en

%description langpack-en
English thesaurus for OpenOffice.org.

%package langpack-es
Summary: Spanish language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-es, hyphen-es, mythes-es, autocorr-es
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org2-langpack-es < 1:3.0.0

%description langpack-es
Provides additional Spanish translations and resources for OpenOffice.org.

%package langpack-et_EE
Summary: Estonian language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-et, hyphen-et
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-et < 1:2.0.3
Obsoletes: openoffice.org2-langpack-et_EE < 1:3.0.0

%description langpack-et_EE
Provides additional Estonian translations and resources for OpenOffice.org.

%package langpack-eu_ES
Summary: Basque language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-eu, hyphen-eu, autocorr-eu
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-eu < 1:2.0.3
Obsoletes: openoffice.org2-langpack-eu_ES < 1:3.0.0

%description langpack-eu_ES
Provides additional Basque translations and resources for OpenOffice.org.

%package langpack-fi_FI
Summary: Finnish language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: autocorr-fi
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-fi < 1:2.0.3
Obsoletes: openoffice.org2-langpack-fi_FI < 1:3.0.0

%description langpack-fi_FI
Provides additional Finnish translations and resources for OpenOffice.org.

%package langpack-fr
Summary: French language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-fr, hyphen-fr, mythes-fr, autocorr-fr
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org2-langpack-fr < 1:3.0.0

%description langpack-fr
Provides additional French translations and resources for OpenOffice.org.

%package langpack-ga_IE
Summary: Irish language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-ga, hyphen-ga, mythes-ga, autocorr-ga
Obsoletes: openoffice.org2-langpack-ga_IE < 1:3.0.0

%description langpack-ga_IE
Provides additional Irish translations and resources for OpenOffice.org.

%package langpack-gl_ES
Summary: Galician language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-gl, hyphen-gl
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-gl < 1:2.0.3
Obsoletes: openoffice.org2-langpack-gl_ES < 1:3.0.0

%description langpack-gl_ES
Provides additional Galician translations and resources for OpenOffice.org.

%package langpack-gu_IN
Summary: Gujarati language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-gu, hyphen-gu
Requires: lohit-gujarati-fonts
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org2-langpack-gu_IN < 1:3.0.0

%description langpack-gu_IN
Provides additional Gujarati translations and resources for OpenOffice.or.

%package langpack-pa
Summary: Punjabi language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-pa, hyphen-pa
Requires: lohit-punjabi-fonts
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-pa_IN < 1:3.2.0
Obsoletes: openoffice.org2-langpack-pa_IN < 1:3.0.0

%description langpack-pa
Provides additional Punjabi translations and resources for OpenOffice.org.

%package langpack-he_IL
Summary: Hebrew language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-he
Requires: culmus-nachlieli-clm-fonts
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-he < 1:2.0.3
Obsoletes: openoffice.org2-langpack-he_IL < 1:3.0.0

%description langpack-he_IL
Provides additional Hebrew translations and resources for OpenOffice.org.

%package langpack-hi_IN
Summary: Hindi language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-hi, hyphen-hi
Requires: lohit-hindi-fonts
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-hi-IN < 1:2.0.3
Obsoletes: openoffice.org2-langpack-hi_IN < 1:3.0.0

%description langpack-hi_IN
Provides additional Hindi translations and resources for OpenOffice.org.

%package langpack-hu_HU
Summary: Hungarian language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-hu, hyphen-hu, mythes-hu, autocorr-hu
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-hu < 1:2.0.3
Obsoletes: openoffice.org2-langpack-hu_HU < 1:3.0.0

%description langpack-hu_HU
Provides additional Hungarian translations and resources for OpenOffice.org.

%package langpack-hr_HR
Summary: Croatian language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-hr, hyphen-hr
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-hr < 1:2.0.3
Obsoletes: openoffice.org2-langpack-hr_HR < 1:3.0.0

%description langpack-hr_HR
Provides additional Croatian translations and resources for OpenOffice.org.

%package langpack-it
Summary: Italian language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-it, hyphen-it, mythes-it, autocorr-it
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org2-langpack-it < 1:3.0.0

%description langpack-it
Provides additional Italian translations and resources for OpenOffice.org.

%package langpack-ja_JP
Summary: Japanese language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: autocorr-ja
Requires: VLGothic-fonts
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-ja < 1:2.0.3
Obsoletes: openoffice.org2-langpack-ja_JP < 1:3.0.0

%description langpack-ja_JP
Provides additional Japanese translations and resources for OpenOffice.org.

%package langpack-ko_KR
Summary: Korean language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-ko, autocorr-ko
Requires: baekmuk-ttf-gulim-fonts
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-ko < 1:2.0.3
Obsoletes: openoffice.org2-langpack-ko_KR < 1:3.0.0

%description langpack-ko_KR
Provides additional Korean translations and resources for OpenOffice.org.

%package langpack-lt_LT
Summary: Lithuanian language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: autocorr-lt
Requires: hunspell-lt, hyphen-lt
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-lt < 1:2.0.3
Obsoletes: openoffice.org2-langpack-lt_LT < 1:3.0.0

%description langpack-lt_LT
Provides additional Lithuanian translations and resources for OpenOffice.org.

%package langpack-ms_MY
Summary: Malay language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-ms
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-ms < 1:2.0.3
Obsoletes: openoffice.org2-langpack-ms_MY < 1:3.0.0

%description langpack-ms_MY
Provides additional Malay translations and resources for OpenOffice.org.

%package langpack-nb_NO
Summary: Bokmal language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-nb, hyphen-nb, mythes-nb
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-nb < 1:2.0.3
Obsoletes: openoffice.org2-langpack-nb_NO < 1:3.0.0

%description langpack-nb_NO
Provides additional Bokmal translations and resources for OpenOffice.org.

%package langpack-nl
Summary: Dutch language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-nl, hyphen-nl, mythes-nl, autocorr-nl
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org2-langpack-nl < 1:3.0.0

%description langpack-nl
Provides additional Dutch translations and resources for OpenOffice.org.

%package langpack-nn_NO
Summary: Nynorsk language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-nn, hyphen-nn, mythes-nn
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-nn < 1:2.0.3
Obsoletes: openoffice.org2-langpack-nn_NO < 1:3.0.0

%description langpack-nn_NO
Provides additional Nynorsk translations and resources for OpenOffice.org.

%package langpack-nr_ZA
Summary: Southern Ndebele language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-nr

%description langpack-nr_ZA
Provides additional Southern Ndebele translations and resources for 
OpenOffice.org.

%package langpack-pl_PL
Summary: Polish language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-pl, hyphen-pl, mythes-pl, autocorr-pl
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-pl < 1:2.0.3
Obsoletes: openoffice.org2-langpack-pl_PL < 1:3.0.0

%description langpack-pl_PL
Provides additional Polish translations and resources for OpenOffice.org.

%package langpack-pt_PT
Summary: Portuguese language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-pt, hyphen-pt, mythes-pt, autocorr-pt
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-pt < 1:2.0.3
Obsoletes: openoffice.org2-langpack-pt_PT < 1:3.0.0

%description langpack-pt_PT
Provides additional Portuguese translations and resources for OpenOffice.org.

%package langpack-pt_BR
Summary: Brazilian Portuguese language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-pt, hyphen-pt, mythes-pt, autocorr-pt
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-pt-BR < 1:2.0.3
Obsoletes: openoffice.org2-langpack-pt_BR < 1:3.0.0

%description langpack-pt_BR
Provides additional Brazilian Portuguese translations and resources for 
OpenOffice.org.

%package langpack-ru
Summary: Russian language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-ru, hyphen-ru, mythes-ru, autocorr-ru
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org2-langpack-ru < 1:3.0.0

%description langpack-ru
Provides additional Russian translations and resources for OpenOffice.org.

%package langpack-sk_SK
Summary: Slovak language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-sk, hyphen-sk, mythes-sk, autocorr-sk
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-sk < 1:2.0.3
Obsoletes: openoffice.org2-langpack-sk_SK < 1:3.0.0

%description langpack-sk_SK
Provides additional Slovak translations and resources for OpenOffice.org.

%package langpack-sl_SI
Summary: Slovenian language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-sl, hyphen-sl, mythes-sl, autocorr-sl
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-sl < 1:2.0.3
Obsoletes: openoffice.org2-langpack-sl_SI < 1:3.0.0

%description langpack-sl_SI
Provides additional Slovenian translations and resources for OpenOffice.org.

%package langpack-sr
Summary: Serbian language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-sr, hyphen-sr
Obsoletes: openoffice.org-langpack-sr_CS < 1:2.0.3
Obsoletes: openoffice.org2-langpack-sr_CS < 1:3.0.0

%description langpack-sr
Provides additional Serbian translations and resources for OpenOffice.org.

%package langpack-ss_ZA
Summary: Swati language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-ss

%description langpack-ss_ZA
Provides additional Swati translations and resources for OpenOffice.org.

%package langpack-st_ZA
Summary: Southern Sotho language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-st

%description langpack-st_ZA
Provides additional Southern Sotho translations and resources for 
OpenOffice.org.

%package langpack-sv
Summary: Swedish language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-sv, hyphen-sv, mythes-sv, autocorr-sv
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org2-langpack-sv < 1:3.0.0

%description langpack-sv
Provides additional Swedish translations and resources for OpenOffice.org.

%package langpack-ta_IN
Summary: Tamil language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires:  hunspell-ta, hyphen-ta
Requires:  lohit-tamil-fonts
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org2-langpack-ta_IN < 1:3.0.0

%description langpack-ta_IN
Provides additional Tamil translations and resources for OpenOffice.org.

%package langpack-th_TH
Summary: Thai language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-th
Requires: thai-scalable-fonts-compat
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-th < 1:2.0.3
Obsoletes: openoffice.org2-langpack-th_TH < 1:3.0.0

%description langpack-th_TH
Provides additional Thai translations and resources for OpenOffice.org.

%package langpack-nso_ZA
Summary: Northern Sotho language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-nso
Obsoletes: openoffice.org2-langpack-nso_ZA < 1:3.0.0

%description langpack-nso_ZA
Provides additional Northern Sotho translations and resources for 
OpenOffice.org.

%package langpack-tn_ZA
Summary: Tswana language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-tn
Obsoletes: openoffice.org-langpack-tn < 1:2.0.3
Obsoletes: openoffice.org2-langpack-tn_ZA < 1:3.0.0

%description langpack-tn_ZA
Provides additional Tswana translations and resources for OpenOffice.org.

%package langpack-ts_ZA
Summary: Tsonga language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-ts
Obsoletes: openoffice.org-langpack-ts < 1:2.0.3
Obsoletes: openoffice.org2-langpack-ts_ZA < 1:3.0.0

%description langpack-ts_ZA
Provides additional Tsonga translations and resources for OpenOffice.org.

%package langpack-tr_TR
Summary: Turkish language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: autocorr-tr
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-tr < 1:2.0.3
Obsoletes: openoffice.org2-langpack-tr < 1:3.0.0

%description langpack-tr_TR
Provides additional Turkish translations and resources for OpenOffice.org.

%package langpack-ve_ZA
Summary: Venda language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-ve

%description langpack-ve_ZA
Provides additional Venda translations and resources for OpenOffice.org.

%package langpack-xh_ZA
Summary: Xhosa language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-xh

%description langpack-xh_ZA
Provides additional Xhosa translations and resources for OpenOffice.org.

%package langpack-zh_CN
Summary: Simplified Chinese language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: autocorr-zh
Requires: cjkuni-uming-fonts
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-zh-CN < 1:2.0.3
Obsoletes: openoffice.org2-langpack-zh_CN < 1:3.0.0

%description langpack-zh_CN
Provides additional Simplified Chinese translations and resources for 
OpenOffice.org.

%package langpack-zh_TW
Summary: Traditional Chinese language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: autocorr-zh
Requires: cjkuni-uming-fonts
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-zh-TW < 1:2.0.3
Obsoletes: openoffice.org2-langpack-zh_TW < 1:3.0.0

%description langpack-zh_TW
Provides additional Traditional Chinese translations and resources for 
OpenOffice.org.

%package langpack-zu_ZA
Summary: Zulu language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-zu, hyphen-zu
Obsoletes: openoffice.org-i18n < 1.9.0
Obsoletes: openoffice.org-langpack-zu < 1:2.0.3
Obsoletes: openoffice.org2-langpack-zu_ZA < 1:3.0.0

%description langpack-zu_ZA
Provides additional Zulu translations and resources for OpenOffice.org.

%package langpack-as_IN
Summary: Assamese language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-as, hyphen-as
Requires: lohit-bengali-fonts
Obsoletes: openoffice.org2-langpack-as_IN < 1:3.0.0

%description langpack-as_IN
Provides additional Assamese translations and resources for OpenOffice.org.

%package langpack-mr_IN
Summary: Marathi language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-mr, hyphen-mr
Requires: lohit-marathi-fonts
Obsoletes: openoffice.org2-langpack-mr_IN < 1:3.0.0

%description langpack-mr_IN
Provides additional Marathi translations and resources for OpenOffice.org.

%package langpack-ml_IN
Summary: Malayalam language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-ml, hyphen-ml
Requires: smc-meera-fonts
Obsoletes: openoffice.org2-langpack-ml_IN < 1:3.0.0

%description langpack-ml_IN
Provides additional Malayalam translations and resources for OpenOffice.org.

%package langpack-or_IN
Summary: Oriya language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-or, hyphen-or
Requires: lohit-oriya-fonts
Obsoletes: openoffice.org2-langpack-or_IN < 1:3.0.0

%description langpack-or_IN
Provides additional Oriya translations and resources for OpenOffice.org.

%package langpack-te_IN
Summary: Telugu language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-te, hyphen-te
Requires: lohit-telugu-fonts
Obsoletes: openoffice.org2-langpack-te_IN < 1:3.0.0

%description langpack-te_IN
Provides additional Telugu translations and resources for OpenOffice.org.

%package langpack-ur
Summary: Urdu language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: paktype-naqsh-fonts, paktype-tehreer-fonts
Requires: hunspell-ur
Obsoletes: openoffice.org2-langpack-ur < 1:3.0.0

%description langpack-ur
Provides additional Urdu translations and resources for OpenOffice.org.

%package langpack-kn_IN
Summary: Kannada language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-kn, hyphen-kn
Requires: lohit-kannada-fonts
Obsoletes: openoffice.org2-langpack-kn_IN < 1:3.0.0

%description langpack-kn_IN
Provides additional Kannada translations and resources for OpenOffice.org.

%package langpack-dz
Summary: Dzongkha language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: jomolhari-fonts

%description langpack-dz
Provides additional Dzongkha translations and resources for OpenOffice.org.

%package langpack-uk
Summary: Ukrainian language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-uk, hyphen-uk, mythes-uk

%description langpack-uk
Provides additional Ukrainian translations and resources for OpenOffice.org.

%package langpack-mai_IN
Summary: Maithili language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: lohit-maithili-fonts
Requires: hunspell-mai

%description langpack-mai_IN
Provides additional Maithili translations and resources for OpenOffice.org.

%package langpack-ro
Summary: Romanian language pack for OpenOffice.org
Group: Applications/Productivity
Requires: %{name}-core = %{epoch}:%{version}-%{release}
Requires: hunspell-ro, hyphen-ro, mythes-ro

%description langpack-ro
Provides additional Romanian translations and resources for OpenOffice.org.

%package -n autocorr-en
Summary: English autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-en
Rules for autocorrecting common English typing errors.

%package -n autocorr-af
Summary: Afrikaans autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-af
Rules for autocorrecting common Afrikaans typing errors.

%package -n autocorr-bg
Summary: Bulgarian autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-bg
Rules for autocorrecting common Bulgarian typing errors.

%package -n autocorr-cs
Summary: Czech autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-cs
Rules for autocorrecting common Czech typing errors.

%package -n autocorr-da
Summary: Danish autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-da
Rules for autocorrecting common Danish typing error.

%package -n autocorr-de
Summary: German autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-de
Rules for autocorrecting common German typing errors.

%package -n autocorr-es
Summary: Spanish autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-es
Rules for autocorrecting common Spanish typing errors.

%package -n autocorr-eu
Summary: Basque autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-eu
Rules for autocorrecting common Basque typing errors.

%package -n autocorr-fa
Summary: Farsi autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-fa
Rules for autocorrecting common Farsi typing errors.

%package -n autocorr-fi
Summary: Finnish autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-fi
Rules for autocorrecting common Finnish typing errors.

%package -n autocorr-fr
Summary: French autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-fr
Rules for autocorrecting common French typing errors.

%package -n autocorr-ga
Summary: Irish autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-ga
Rules for autocorrecting common Irish typing errors.

%package -n autocorr-hu
Summary: Hungarian autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-hu
Rules for autocorrecting common Hungarian typing errors.

%package -n autocorr-it
Summary: Italian autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-it
Rules for autocorrecting common Italian typing errors.

%package -n autocorr-ja
Summary: Japanese autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-ja
Rules for autocorrecting common Japanese typing errors.

%package -n autocorr-ko
Summary: Korean autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-ko
Rules for autocorrecting common Korean typing errors.

%package -n autocorr-lb
Summary: Luxembourgish autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-lb
Rules for autocorrecting common Luxembourgish typing errors.

%package -n autocorr-lt
Summary: Lithuanian autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-lt
Rules for autocorrecting common Lithuanian typing errors.

%package -n autocorr-mn
Summary: Mongolian autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-mn
Rules for autocorrecting common Mongolian typing errors.

%package -n autocorr-nl
Summary: Dutch autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-nl
Rules for autocorrecting common Dutch typing errors.

%package -n autocorr-pl
Summary: Polish autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-pl
Rules for autocorrecting common Polish typing errors.

%package -n autocorr-pt
Summary: Portuguese autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-pt
Rules for autocorrecting common Portuguese typing errors.

%package -n autocorr-ru
Summary: Russian autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-ru
Rules for autocorrecting common Russian typing errors.

%package -n autocorr-sk
Summary: Slovak autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-sk
Rules for autocorrecting common Slovak typing errors.

%package -n autocorr-sl
Summary: Slovenian autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-sl
Rules for autocorrecting common Slovenian typing errors.

%package -n autocorr-sv
Summary: Swedish autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-sv
Rules for autocorrecting common Swedish typing errors.

%package -n autocorr-tr
Summary: Turkish autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-tr
Rules for autocorrecting common Turkish typing errors.

%package -n autocorr-vi
Summary: Vietnamese autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-vi
Rules for autocorrecting common Vietnamese typing errors.

%package -n autocorr-zh
Summary: Chinese autocorrection rules
Group: Applications/Text
BuildArch: noarch

%description -n autocorr-zh
Rules for autocorrecting common Chinese typing errors.

%prep
%setup -q -n %{ooo_base_name}
#Customize Palette to remove Sun colours and add Red Hat colours
(sed -e '/Sun/d' extras/source/palettes/standard.soc | head -n -1 && \
 echo -e ' <draw:color draw:name="Red Hat 1" draw:color="#cc0000"/>
 <draw:color draw:name="Red Hat 2" draw:color="#0093d9"/> 
 <draw:color draw:name="Red Hat 3" draw:color="#ff8d00"/>
 <draw:color draw:name="Red Hat 4" draw:color="#abb400"/>
 <draw:color draw:name="Red Hat 5" draw:color="#4e376b"/>' && \
 tail -n 1 extras/source/palettes/standard.soc) > redhat.soc
mv -f redhat.soc extras/source/palettes/standard.soc
cp -p %{SOURCE1} extras/source/database/evolocal.odb
cp -p %{SOURCE5} external/unowinreg/unowinreg.dll
%patch1  -p1 -b .rhXXXXXX.extensions.defaulttoevo2.patch
%patch2  -p1 -b .ooo53397.prelinkoptimize.desktop.patch
%patch3  -p1 -b .ooo58606.sw.pre-edit.patch
%patch4  -p1
%patch5  -p1 -b .rhXXXXXX.padmin.nospadmin.patch
%patch6  -p0 -b .workspace.printerpullpages.patch
%patch7  -p1 -b .ooo74188.sw.cursorinsideglyph.patch
%patch8  -p0 -b .ooo68717.gstreamer.video.patch
%patch9  -p1 -b .ooo7065.sw.titlepagedialog.patch
%patch10 -p1 -b .ooo76649.httpencoding.patch
%patch11 -p1 -b .ooo83878.unopkg.enablelinking.patch
%patch12 -p1 -b .ooo86080.unopkg.bodge.patch
%patch13 -p1 -b .ooo88341.sc.verticalboxes.patch
%patch14 -p1 -b .workspace.fchints01.patch
%patch15 -p1 -b .ooo87970.vcl.samenamesubs.patch
%patch16 -p1 -b .ooo91924.svx.consistentordering.patch
%patch17 -p1 -b .oooXXXXX.fpicker.allformatsonsave.patch
%patch18 -p0 -b .ooo98137.filter.redeclared-variables.patch
%patch19 -p1 -b .gccXXXXX.solenv.javaregistration.patch
%patch20 -p1 -b .oooXXXXX.solenv.allowmissing.patch
%patch21 -p1 -b .ooo2497.filter.svg.patch
%patch22 -p1 -b .ooo61927.sw.ww6.unicodefontencoding.patch
%patch23 -p2 -b .workspace.slideshow1.patch
%patch24 -p0 -b .ooo101274.opening-a-directory.patch
%patch25 -p0 -b .ooo101354.filter.xhtml.do-not-label-list-headers.patch
%patch26 -p0 -b .ooo101355.filter.no-variables-in-keys.patch
%patch27 -p0 -b .ooo101567.i18npool.mailocaledata.patch
%patch28 -p0 -b .ooo102061.sc.cellanchoring.patch
%patch29 -p0 -b .ooo102142.sd.resleak.patch
%patch30 -p0 -b .ooo46270.svx.search-dialog.no-find-all-in-draw.patch
%patch31 -p0 -b .ooo104280.xmloff.lcl_IsAtEnd.wrong.patch
%patch32 -p0 -b .ooo104329.dbaccess.primarykeys.patch
%patch33 -p0 -b .ooo64671.canvas.add-support-for-font-pitch.patch
%patch34 -p1 -b .ooo109280.sal.justcoredump.patch
%patch35 -p0 -b .workspace.vcl106.patch
%patch36 -p0 -b .ooo105784.vcl.sniffscriptforsubs.patch
%patch37 -p0 -b .ooo105827.filter.xpath-on-rtf-not-allowed.patch
%patch38 -p0 -b .ooo106032.linguistic.defaulttoplain.patch
%patch39 -p1 -b .workspace.gsminhibit.patch
%patch40 -p1 -b .workspace.vcl107.patch
%patch41 -p0 -b .workspace.hb33patches1.patch
%patch42 -p0 -b .workspace.ause109.patch
%patch43 -p1 -b .workspace.cmcfixes67.patch
%patch44 -p1 -b .workspace.srb1.patch
%patch45 -p0 -b .workspace.thbfixes10.patch
%patch46 -p0 -b .ooo102645.fix.es.patch
%patch47 -p0 -b .workspace.vcl108.patch
%patch48 -p1 -b .workspace.pythonssldedux.patch
%patch49 -p1 -b .ooo106502.svx.fixspelltimer.patch
%patch50 -p0 -b .ooo47279.sd.objectsave.safe.patch
%patch51 -p0 -b .ooo107834.sw.pseudoattribs.patch
%patch52 -p1 -b .workspace.writerfilter07.patch
%patch53 -p1 -b .ooo108246.svx.hide-sql-group-when-inactive.patch
%patch54 -p1 -b .workspace.sw33bf02.patch
%patch55 -p0 -b .ooo108330.embeddedobj.outplace.readonly.os.dispatch.patch
%patch56 -p0 -b .ooo96362.filter.nondeterministic.order.patch
%patch57 -p1 -b .workspace.cmcfixes70.patch
%patch58 -p1 -b .workspace.s390xport02.patch
%patch59 -p1 -b .ooo108637.sfx2.uisavedir.patch
%patch60 -p1 -b .ooo108846.sfx2.qstartfixes.patch
%patch61 -p0 -b .ooo108976.svx.safestyledelete.patch
%patch62 -p0 -b .ooo109009.sc.tooltipcrash.patch
%patch63 -p0 -b .workspace.x86_64_bridgefix.patch
%patch64 -p0 -b .ooo109210.sd.allpagesbg.patch
%patch65 -p1 -b .ooo95369.sw.sortedobjs.patch
%patch66 -p1 -b .ooo109406.sdext.pdfimport.escape-newlines-in-pdf-processor.patch
%patch67 -p1 -b .workspace.koheicsvimport.patch
%patch68 -p1 -b .ooo108991.redlandfixes.patch
%patch69 -p0 -b .ooo101458.vcl.silencea11y.patch

%build
echo build start time is `date`, diskspace: `df -h . | tail -n 1`
#don't build localized helps which are poorly translated
POORHELPS=`find l10n/source -name localize.sdf -exec grep 'helpcontent2.*main.*Working With %PRODUCTNAME' {} \; | cut -f 10 | xargs`

#kid translations are broken for the .desktop files at the moment
#See ooo#107407
rm -rf l10n/source/kid

autoconf
%configure \
 --with-build-version="Ver: %{version}-%{release}" --with-unix-wrapper=%{name} \
 --with-use-shell=bash --disable-ldap --disable-epm --disable-qadevooo \
 --disable-fontooo --disable-mathmldtd --disable-Xaw --disable-gnome-vfs \
 --enable-gio --enable-gstreamer --enable-symbols --enable-lockdown \
 --enable-evolution2 --enable-cairo --enable-dbus --enable-opengl \
 --enable-minimizer --enable-presenter-console --enable-pdfimport \
 --enable-wiki-publisher --enable-vba --enable-report-builder \
 --with-system-jfreereport \
 --with-vba-package-format="builtin" --with-system-libs \
 --with-system-headers --with-system-apache-commons \
 --with-system-mozilla --with-system-libtextcat --with-system-redland \
 --with-system-dicts --with-external-dict-dir=/usr/share/myspell \
 --without-myspell-dicts --without-system-mspack --without-fonts \
 --without-agg --without-ppds --without-afms \
 %{stlflags} --with-lang="%{langpack_langs}" \
 --with-poor-help-localizations="$POORHELPS" \
 --disable-graphite # for now

./bootstrap
source ./Linux*Env.Set.sh
#unneccessary to build for both hash types
unset HAVE_LD_HASH_STYLE
#faster build
export nodep=true
export NO_HIDS=true
#Set the "This product has been created by..." in Help->About
export OOO_VENDOR="Red Hat, Inc."
#force linker
export LINK=$CXX
#use the RPM_OPT_FLAGS but remove the OOo overridden ones
for i in $RPM_OPT_FLAGS; do
        case "$i" in
                -O?|-pipe|-Wall|-g|-fexceptions) continue;;
        esac
        ARCH_FLAGS="$ARCH_FLAGS $i"
done
export ARCH_FLAGS

#convert _smp_mflags to dmake equivalent
SMP_MFLAGS=%{?_smp_mflags}
SMP_MFLAGS=$[${SMP_MFLAGS/-j/}]
if [ $SMP_MFLAGS -lt 2 ]; then SMP_MFLAGS=2; fi
DMAKE_SMP_MFLAGS=`dc -e "$SMP_MFLAGS v p"`
BUILD_SMP_MFLAGS=`dc -e "$SMP_MFLAGS $DMAKE_SMP_MFLAGS / p"`
DMAKE_SMP_MFLAGS=-P$DMAKE_SMP_MFLAGS
BUILD_SMP_MFLAGS=-P$BUILD_SMP_MFLAGS
#just in case you have a >16 proc box
export MAXPROCESSLIMIT=65535
#get core dumps
ulimit -c unlimited

#build OOo, on failure make a stab at debugging the crash if any, and
#rebuild un-parallel
cd instsetoo_native/util
if ! build --dlv_switch -link --all $BUILD_SMP_MFLAGS -- $DMAKE_SMP_MFLAGS -s; then
    build --dlv_switch -link --all
fi

#generate the icons and mime type stuff
export DESTDIR=../../../output
export KDEMAINDIR=/usr
export GNOMEDIR=/usr
export GNOME_MIME_THEME=hicolor
cd ../../sysui/unxlng*/misc
%if %{langpacks}
cd broffice.org
./create_tree.sh
cd ..
%endif
cd openoffice.org
./create_tree.sh

echo build end time is `date`, diskspace: `df -h . | tail -n 1`

%install
rm -rf $RPM_BUILD_ROOT
source ./Linux*Env.Set.sh
#figure out the icon version
export `grep "^PRODUCTVERSIONSHORT =" sysui/desktop/productversion.mk | sed -e "s/ //g"`
export `grep "PRODUCTVERSION[ ]*=[ ]*" sysui/desktop/productversion.mk | sed -e "s/ //g"`
unset HAVE_LD_HASH_STYLE
#don't duplicate english helpcontent about the place
unset DEFAULT_TO_ENGLISH_FOR_PACKING
cd instsetoo_native/util
#get an unpackaged raw install
export PKGFORMATSWITCH="-simple $RPM_BUILD_ROOT/%{instdir}"
export CLASSPATH=/usr/share/java/lucene.jar:/usr/share/java/lucene-contrib/lucene-analyzers.jar
%if %{langpacks}
for attempt in 1 2 3 4 5 6 7 8 9 10; do
    echo Attempt $attempt
    if dmake broffice_pt-BR; then
        ok=true
        break
    else
        echo - ---dump log start---
        cat ../unx*.pro/BrOffice/logging/pt-BR/log_*_pt-BR.log
        echo - ---dump log end---
        export _MALLOC_CHECK=0
        ok=false
    fi
done
if [ $ok == "false" ]; then
    exit 1
fi
rm -rf $RPM_BUILD_ROOT/%{ureinstdir}
rm -rf $RPM_BUILD_ROOT/%{basisinstdir}
%endif
for attempt in 1 2 3 4 5 6 7 8 9 10; do
    echo Attempt $attempt
    if dmake openoffice_en-US; then
        ok=true
        break
    else
        echo - ---dump log start---
        cat ../unx*.pro/OpenOffice/logging/en-US/log_*_en-US.log
        echo - ---dump log end---
        export _MALLOC_CHECK=0
        ok=false
    fi
done
if [ $ok == "false" ]; then
    exit 1
fi
chmod -R +w $RPM_BUILD_ROOT/%{baseinstdir} $RPM_BUILD_ROOT/%{oooinstdir}
#provide an owner for these dir
mkdir -p $RPM_BUILD_ROOT/%{baseinstdir}/extensions
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/openoffice.org/extensions
%if %{langpacks}
dmake ooolanguagepack
chmod -R +w $RPM_BUILD_ROOT/%{brinstdir}
%endif
for file in swriter scalc simpress sdraw ; do
    cp -f ../../desktop/$OUTPATH.pro/bin/$file $RPM_BUILD_ROOT/%{oooinstdir}/program/$file.bin
%if %{langpacks}
    cp -f ../../desktop/$OUTPATH.pro/bin/$file $RPM_BUILD_ROOT/%{brinstdir}/program/$file.bin
%endif
done
#share cache between brands, and reuse OOo2 cache
mkdir -p $RPM_BUILD_ROOT/%{baseinstdir}/share/uno_packages/cache
#give a consistent javasettingsunopkginstall.xml
$RPM_BUILD_ROOT/%{oooinstdir}/program/unopkg list --shared || :
rm -rf $RPM_BUILD_ROOT/%{oooinstdir}/share/uno_packages/cache || :
pushd $RPM_BUILD_ROOT/%{oooinstdir}/share/uno_packages
ln -s %{baseinstdir}/share/uno_packages/cache cache
popd
%if %{langpacks}
$RPM_BUILD_ROOT/%{brinstdir}/program/unopkg list --shared || :
rm -rf $RPM_BUILD_ROOT/%{brinstdir}/share/uno_packages/cache || :
pushd $RPM_BUILD_ROOT/%{brinstdir}/share/uno_packages
ln -s %{baseinstdir}/share/uno_packages/cache cache
popd
%endif
export PKGFORMATSWITCH="-simple $RPM_BUILD_ROOT/%{instdir}"
export WITH_LANG="en-US"
dmake sdkoo
cd ../../

# unpack report-builder extension
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/openoffice.org/extensions/sun-report-builder.oxt
unzip solver/%{OFFICEUPD}/unxlng*/bin/sun-report-builder.oxt -d $RPM_BUILD_ROOT%{_datadir}/openoffice.org/extensions/sun-report-builder.oxt

# unpack wiki-publisher extension
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/openoffice.org/extensions/wiki-publisher.oxt
unzip solver/%{OFFICEUPD}/unxlng*/bin/swext/wiki-publisher.oxt -d $RPM_BUILD_ROOT%{_datadir}/openoffice.org/extensions/wiki-publisher.oxt

# unpack presentation-minimizer extension
install -d -m 755 $RPM_BUILD_ROOT%{baseinstdir}/extensions/sun-presentation-minimizer.oxt
unzip solver/%{OFFICEUPD}/unxlng*/bin/minimizer/sun-presentation-minimizer.oxt -d $RPM_BUILD_ROOT%{baseinstdir}/extensions/sun-presentation-minimizer.oxt
chmod -x $RPM_BUILD_ROOT%{baseinstdir}/extensions/sun-presentation-minimizer.oxt/help/component.txt

# unpack presenter screen extension
install -d -m 755 $RPM_BUILD_ROOT%{baseinstdir}/extensions/presenter-screen.oxt
unzip solver/%{OFFICEUPD}/unxlng*/bin/presenter/presenter-screen.oxt -d $RPM_BUILD_ROOT%{baseinstdir}/extensions/presenter-screen.oxt
chmod -x $RPM_BUILD_ROOT%{baseinstdir}/extensions/presenter-screen.oxt/help/component.txt

# unpack pdfimport extension
install -d -m 755 $RPM_BUILD_ROOT%{baseinstdir}/extensions/pdfimport.oxt
unzip solver/%{OFFICEUPD}/unxlng*/bin/pdfimport/pdfimport.oxt -d $RPM_BUILD_ROOT%{baseinstdir}/extensions/pdfimport.oxt
chmod -x $RPM_BUILD_ROOT%{baseinstdir}/extensions/pdfimport.oxt/help/component.txt

# revoke ScriptProviders and make into extensions
pushd $RPM_BUILD_ROOT/%{basisinstdir}/program
../ure-link/bin/regcomp -revoke -r services.rdb -br services.rdb -c "vnd.sun.star.expand:\$OOO_BASE_DIR/program/classes/ScriptProviderForBeanShell.jar"
mkdir $RPM_BUILD_ROOT%{_datadir}/openoffice.org/extensions/ScriptProviderForBeanShell.zip
mv classes/ScriptProviderForBeanShell.jar $RPM_BUILD_ROOT%{_datadir}/openoffice.org/extensions/ScriptProviderForBeanShell.zip
../ure-link/bin/regcomp -revoke -r services.rdb -br services.rdb -c "vnd.sun.star.expand:\$OOO_BASE_DIR/program/classes/ScriptProviderForJavaScript.jar"
mkdir $RPM_BUILD_ROOT%{_datadir}/openoffice.org/extensions/ScriptProviderForJavaScript.zip
mv classes/ScriptProviderForJavaScript.jar $RPM_BUILD_ROOT%{_datadir}/openoffice.org/extensions/ScriptProviderForJavaScript.zip
../ure-link/bin/regcomp -revoke -r services.rdb -br services.rdb -c vnd.openoffice.pymodule:pythonscript
mkdir $RPM_BUILD_ROOT%{_datadir}/openoffice.org/extensions/ScriptProviderForPython.zip
mv pythonscript.py $RPM_BUILD_ROOT%{_datadir}/openoffice.org/extensions/ScriptProviderForPython.zip
popd
#set timestamp so it'll be the same on all archs for multilib
touch -r solenv/inc/minor.mk $RPM_BUILD_ROOT%{_datadir}/openoffice.org/extensions/ScriptProviderForPython.zip/pythonscript.py

# remove force-agrement to extensions licences
find $RPM_BUILD_ROOT/%{_datadir}/openoffice.org/extensions $RPM_BUILD_ROOT/%{baseinstdir}/extensions -name description.xml -exec sh -c 'xsltproc --novalid --nonet -o {}.tmp %{SOURCE8} {} && mv -f {}.tmp {}' \;

#add enough to the sdk to build the kde vcl plug out of tree
cp -r solenv/ $RPM_BUILD_ROOT/%{sdkinstdir}
cp solver/%{OFFICEUPD}/unxlng*/bin/checkdll $RPM_BUILD_ROOT/%{sdkinstdir}/bin
cp -r solver/%{OFFICEUPD}/unxlng*/inc/comphelper/ $RPM_BUILD_ROOT/%{sdkinstdir}/include
cp -r solver/%{OFFICEUPD}/unxlng*/inc/i18npool/ $RPM_BUILD_ROOT/%{sdkinstdir}/include
cp -r solver/%{OFFICEUPD}/unxlng*/inc/svtools $RPM_BUILD_ROOT/%{sdkinstdir}/include
cp -r solver/%{OFFICEUPD}/unxlng*/inc/tools/ $RPM_BUILD_ROOT/%{sdkinstdir}/include
cp -r solver/%{OFFICEUPD}/unxlng*/inc/vos $RPM_BUILD_ROOT/%{sdkinstdir}/include

#configure sdk
pushd $RPM_BUILD_ROOT/%{sdkinstdir}
    for file in setsdkenv_unix.csh setsdkenv_unix.sh ; do
        sed -e "s,@OO_SDK_NAME@,sdk," \
            -e "s,@OO_SDK_HOME@,%{sdkinstdir}," \
            -e "s,@OFFICE_HOME@,%{baseinstdir}," \
            -e "s,@OFFICE_BASE_HOME@,%{basisinstdir}," \
            -e "s,@OO_SDK_URE_HOME@,%{ureinstdir}," \
            -e "s,@OO_SDK_MAKE_HOME@,/usr/bin," \
            -e "s,@OO_SDK_ZIP_HOME@,/usr/bin," \
            -e "s,@OO_SDK_CPP_HOME@,/usr/bin," \
            -e "s,@OO_SDK_CC_55_OR_HIGHER@,," \
            -e "s,@OO_SDK_JAVA_HOME@,$JAVA_HOME," \
            -e "s,@OO_SDK_OUTPUT_DIR@,\$HOME," \
            -e "s,@SDK_AUTO_DEPLOYMENT@,NO," \
            $file.in > $file
        chmod 755 $file
    done
#relocate dmake
    mv solenv/unxlng*/bin/dmake solenv/bin
    rm -rf solenv/unx*
#fix up checkdll
    sed -i -e "s#^checkdll=.*#checkdll=\"%{sdkinstdir}/bin/checkdll\"#g" solenv/bin/checkdll.sh
#fix permissions
    find examples -type f -exec chmod -x {} \;
#make env
    echo export PATH=\$PATH:%{sdkinstdir}/solenv/bin > setdevelenv_unix.sh
    echo export DMAKEROOT=%{sdkinstdir}/solenv/inc/startup >> setdevelenv_unix.sh
    echo export OS="LINUX" >> setdevelenv_unix.sh
    echo export SOLARENV=%{sdkinstdir}/solenv >> setdevelenv_unix.sh
    echo export SOLARVER="\`pwd\`/solver/%{OFFICEUPD}" >> setdevelenv_unix.sh
    echo export SOLARVERSION="\$SOLARVER" >> setdevelenv_unix.sh
    echo export INPATH="$INPATH" >> setdevelenv_unix.sh
    echo export OUTPATH="$OUTPATH" >> setdevelenv_unix.sh
    echo export UPD="$UPD" >> setdevelenv_unix.sh 
    echo export UPDATER="YES" >> setdevelenv_unix.sh
    echo export WORK_STAMP="$WORK_STAMP" >> setdevelenv_unix.sh
    echo export GUI="UNX" >> setdevelenv_unix.sh
    echo export GUIBASE="unx" >> setdevelenv_unix.sh
    echo export PATH_SEPERATOR=":" >> setdevelenv_unix.sh
    echo export COM="GCC" >> setdevelenv_unix.sh
    echo export GLIBC="2REDHAT60" >> setdevelenv_unix.sh
    echo export OS="LINUX" >> setdevelenv_unix.sh
    echo export SHELL="/bin/bash" >> setdevelenv_unix.sh
    echo export USE_SHELL="bash" >> setdevelenv_unix.sh
    echo export CVER="$CVER" >> setdevelenv_unix.sh
    echo export CPU="$CPU" >> setdevelenv_unix.sh
    echo export MAKEDEPEND=makedepend >> setdevelenv_unix.sh
    echo export MKOUT="mkout.pl" >> setdevelenv_unix.sh
    echo export SOLARINC=\"-I%{sdkinstdir}/include/stl -I%{sdkinstdir}/include\" >> setdevelenv_unix.sh
    echo export SOLARLIB=\"-L%{basisinstdir}/program\" >> setdevelenv_unix.sh
    echo export GXX_INCLUDE_PATH="$GXX_INCLUDE_PATH" >> setdevelenv_unix.sh
    echo export EXTERNAL_WARNINGS_NOT_ERRORS="TRUE" >> setdevelenv_unix.sh
    echo export GVER="VCL" >> setdevelenv_unix.sh
    echo export PRODUCT="full" >> setdevelenv_unix.sh
    echo export ISOLANG_MAJOR=1 >> setdevelenv_unix.sh
    echo export COMPHLP_MAJOR=4 >> setdevelenv_unix.sh
    echo export UCBHELPER_MAJOR=4 >> setdevelenv_unix.sh
    echo export VOS_MAJOR=3 >> setdevelenv_unix.sh
popd

#add our custom configuration options
#enable gtk file dialog as the default
rm -rf $RPM_BUILD_ROOT/%{basisinstdir}/share/registry/modules/org/openoffice/Office/Common/Common-UseOOoFileDialogs.xcu
#remove dictooo stuff which we disabled in configure
rm -rf $RPM_BUILD_ROOT/%{basisinstdir}/share/registry/modules/org/openoffice/Office/Common/Common-dicooo.xcu
#don't prompt user to register
sed -i -e "s#>Patch.*# xsi:nil=\"true\"/>#g" $RPM_BUILD_ROOT/%{basisinstdir}/share/registry/data/org/openoffice/Office/Common.xcu
#default autorecovery settings
#don't prompt user to agree to license
#system libtextcat fingerprint location
#rhbz#484055 system autocorr location
#rhbz#451512 set better math print options
tar xzf %{SOURCE6} -C $RPM_BUILD_ROOT/%{basisinstdir}/share

#add the debugging libsalalloc_malloc.so.3 library
cp -f solver/%{OFFICEUPD}/unxlng*.pro/lib/libsalalloc_malloc.so.3 $RPM_BUILD_ROOT/%{ureinstdir}/lib
chmod -x $RPM_BUILD_ROOT/%{basisinstdir}/program/testtoolrc
chmod -x $RPM_BUILD_ROOT/%{basisinstdir}/program/hid.lst

#remove spurious exec bits
chmod -x $RPM_BUILD_ROOT/%{basisinstdir}/program/gengalrc

#We don't need to carry around all the letter templates for all the languages 
#in each langpack! In addition, all the bitmaps are the same!
pushd $RPM_BUILD_ROOT/%{basisinstdir}/share/template
mkdir -p wizard
for I in %{langpack_langs}; do
	if [ -d $I/wizard/bitmap ]; then
		cp -afl $I/wizard/bitmap wizard/
		rm -rf $I/wizard/bitmap
		ln -sf ../../wizard/bitmap $I/wizard/bitmap
	fi

	if [ -d $I/wizard/letter/$I ]; then
		mv -f $I/wizard/letter/$I ${I}_wizard_letter_${I}
		rm -rf $I/wizard/letter/*
		mv -f ${I}_wizard_letter_${I} $I/wizard/letter/$I
	else
		rm -rf $I/wizard/letter/*
	fi
done
popd

#Set some aliases to canonical autocorrect language files for locales with matching languages
pushd $RPM_BUILD_ROOT/%{basisinstdir}/share/autocorr

# ooo#105600
cp -p %{SOURCE10} acor_ga-IE.dat
# ooo#108049
cp -p %{SOURCE12} acor_lt-LT.dat

#en-ZA exists and has a good autocorrect file with two or three extras that make sense for South Africa
en_GB_aliases="en-AG en-AU en-BS en-BW en-BZ en-CA en-DK en-GH en-HK en-IE en-IN en-JM en-NG en-NZ en-SG en-TT"
for lang in $en_GB_aliases; do
        ln -sf acor_en-GB.dat acor_$lang.dat
done
en_US_aliases="en-PH"
for lang in $en_US_aliases; do
        ln -sf acor_en-US.dat acor_$lang.dat
done
en_ZA_aliases="en-NA en-ZW"
for lang in $en_ZA_aliases; do
        ln -sf acor_en-ZA.dat acor_$lang.dat
done
%if %{langpacks}
af_ZA_aliases="af-NA"
for lang in $af_ZA_aliases; do
        ln -sf acor_af-ZA.dat acor_$lang.dat
done
de_DE_aliases="de-AT de-BE de-CH de-LI de-LU"
for lang in $de_DE_aliases; do
        ln -sf acor_de-DE.dat acor_$lang.dat
done
es_ES_aliases="es-AR es-BO es-CL es-CO es-CR es-CU es-DO es-EC es-GT es-HN es-MX es-NI es-PA es-PE es-PR es-PY es-SV es-US es-UY es-VE"
for lang in $es_ES_aliases; do
        ln -sf acor_es-ES.dat acor_$lang.dat
done
fr_FR_aliases="fr-BE fr-CA fr-CH fr-LU fr-MC"
for lang in $fr_FR_aliases; do
        ln -sf acor_fr-FR.dat acor_$lang.dat
done
it_IT_aliases="it-CH"
for lang in $it_IT_aliases; do
        ln -sf acor_it-IT.dat acor_$lang.dat
done
nl_NL_aliases="nl-AW nl-BE"
for lang in $nl_NL_aliases; do
        ln -s acor_nl-NL.dat acor_$lang.dat
done
sv_SE_aliases="sv-FI"
for lang in $sv_SE_aliases; do
        ln -s acor_sv-SE.dat acor_$lang.dat
done
%else
rm -f acor_[a-df-z]*.dat acor_e[su]*.dat
%endif
popd
#rhbz#484055 make these shared across multiple applications
mv -f $RPM_BUILD_ROOT/%{basisinstdir}/share/autocorr $RPM_BUILD_ROOT/%{_datadir}/autocorr

%if %{langpacks}

#auto generate the langpack file lists, format is...
#langpack id, has help or not, autocorrection glob, script classification
langpackdetails=\
(\
af	help	western		ar	help	ctl	\
bg	help	western 	bn	help	western	\
ca	help	western 	cs	help	western	\
cy	nohelp	western 	da	help	western	\
de	help	western 	el	help 	western	\
es	help	western 	et	help	western	\
eu	help	western 	fi	help	western	\
fr	help	western 	ga	nohelp	western	\
gl	help	western 	gu	nohelp	ctl	\
pa-IN	help	ctl 		he	nohelp	ctl	\
hi-IN	help	ctl 		hu	help	western	\
hr	nohelp	western 	it	help	western	\
ja	help	cjk		ko	help	cjk	\
lt	help	western 	ms	nohelp	western	\
nb	help	western 	nl	help	western	\
nn	help	western 	pl	help	western	\
pt	help	western 	pt-BR	help	western	\
ru	help	western 	sk	help	western	\
sl	help	western 	sr	help	western	\
sv	help	western 	ta	help	ctl	\
th	help	ctlseqcheck 	tr	help	western	\
zh-CN	help	cjk		zh-TW	help	cjk	\
zu	help	western 	tn	help	western	\
ts	help	western 	as	nohelp	western	\
mr	nohelp	western		ml	nohelp	western	\
or	nohelp	ctl		te	nohelp	western	\
ur	nohelp	western		kn	nohelp	western	\
xh	help	western		ve	help	western \
st	help	western		ss	help	western \
nr	help	western		ns	help	western	\
dz      help    ctl		uk	help	western \
sh	help	western		mai  	help	western \
ro	nohelp	western
)

tar xzf %{SOURCE7}

i=0
while [ $i -lt ${#langpackdetails[@]} ]; do
   lang=${langpackdetails[$i]}
   sed -e "s/LANG/$lang/g" langpacks/openoffice.org.langpack-common.template > $lang.filelist
   i=$[i+1]
   help=${langpackdetails[$i]}
   if [ "$help" = "help" ]; then
     sed -e "s/LANG/$lang/g" langpacks/openoffice.org.langpack-help.template >> $lang.filelist
   fi
   i=$[i+1]
   type=${langpackdetails[$i]}
   if [ "$type" = "cjk" ]; then
     sed -e "s/LANG/$lang/g" langpacks/openoffice.org.langpack-cjk.template >> $lang.filelist
   fi
   #rh217269 upstream made a decision to sequence check all ctl languages
   #I think this is wrong, and only Thai should be sequence checked
   if [ "$type" = "ctlseqcheck" ]; then
     sed -e "s/LANG/$lang/g" langpacks/openoffice.org.langpack-ctl.template >> $lang.filelist
   fi
   if [ "$type" = "ctl" ]; then
     rm -f $RPM_BUILD_ROOT/%{basisinstdir}/share/registry/modules/org/openoffice/Office/Common/Common-ctl_$lang.xcu
   fi
   i=$[i+1]
done

#rhbz#452379 clump serbian translations together
cat sh.filelist >> sr.filelist

%endif

#add in some templates
tar xzf %{SOURCE2} -C $RPM_BUILD_ROOT/%{basisinstdir}/share
tar xzf %{SOURCE3} -C $RPM_BUILD_ROOT/%{basisinstdir}/share
tar xzf %{SOURCE4} -C $RPM_BUILD_ROOT/%{basisinstdir}/share

#remove it in case we didn't build with gcj
rm -f $RPM_BUILD_ROOT/%{basisinstdir}/program/classes/sandbox.jar

#remove pagein stuff
rm -f $RPM_BUILD_ROOT/%{basisinstdir}/program/pagein*

#remove dummy .dat files
rm -f $RPM_BUILD_ROOT/%{basisinstdir}/program/root?.dat

#set standard permissions for rpmlint
find $RPM_BUILD_ROOT/%{baseinstdir} $RPM_BUILD_ROOT/%{basisinstdir} $RPM_BUILD_ROOT/%{oooinstdir} -exec chmod +w {} \;
find $RPM_BUILD_ROOT/%{baseinstdir} $RPM_BUILD_ROOT/%{basisinstdir} $RPM_BUILD_ROOT/%{oooinstdir} -type d -exec chmod 0755 {} \;
%if %{langpacks}
find $RPM_BUILD_ROOT/%{brinstdir} -exec chmod +w {} \;
find $RPM_BUILD_ROOT/%{brinstdir} -type d -exec chmod 0755 {} \;
%endif

# move python bits into site-packages
mkdir -p $RPM_BUILD_ROOT/%{python_sitearch}
pushd $RPM_BUILD_ROOT/%{python_sitearch}
echo "import sys, os" > uno.py
echo "sys.path.append('%{basisinstdir}/program')" >> uno.py
echo "os.putenv('URE_BOOTSTRAP', 'vnd.sun.star.pathname:%{oooinstdir}/program/fundamentalrc')" >> uno.py
cat $RPM_BUILD_ROOT/%{basisinstdir}/program/uno.py >> uno.py
rm -f $RPM_BUILD_ROOT/%{basisinstdir}/program/uno.py*
mv -f $RPM_BUILD_ROOT/%{basisinstdir}/program/unohelper.py* .
popd

# rhbz#477435 package opensymbol separately
pushd $RPM_BUILD_ROOT/%{basisinstdir}/share/fonts/truetype
install -d -m 0755 %{buildroot}%{_fontdir}
install -p -m 0644 *.ttf %{buildroot}%{_fontdir}
popd
rm -rf $RPM_BUILD_ROOT/%{basisinstdir}/share/fonts

#ensure that no sneaky un-prelinkable, un-fpic or non executable shared libs 
#have snuck through
pic=0
executable=0
for foo in `find $RPM_BUILD_ROOT/%{instdir} -name "*" -exec file {} \;| grep ": ELF" | cut -d: -f 1` ; do
	chmod +wx $foo
	ls -asl $foo
        result=`readelf -d $foo | grep TEXTREL` || true
        if [ "$result" != "" ]; then
                echo "TEXTREL Warning: $foo is b0rked (-fpic missing)"
                pic=1
        fi
        result=`readelf -l $foo | grep GNU_STACK | grep RWE` || true
        if [ "$result" != "" ]; then
                echo "GNU_STACK Warning: $foo is b0rked (-noexecstack missing)"
                executable=1
        fi

done
if [ $pic == 1 ]; then false; fi
if [ $executable == 1 ]; then false; fi

#make up some /usr/bin scripts
mkdir -p $RPM_BUILD_ROOT/%{_bindir}

echo \#\!/bin/sh > $RPM_BUILD_ROOT/%{_bindir}/ooffice
echo exec openoffice.org \"\$@\" >> $RPM_BUILD_ROOT/%{_bindir}/ooffice
chmod a+x $RPM_BUILD_ROOT/%{_bindir}/ooffice

echo \#\!/bin/sh > $RPM_BUILD_ROOT/%{_bindir}/ooviewdoc
echo exec openoffice.org -view \"\$@\" >> $RPM_BUILD_ROOT/%{_bindir}/ooviewdoc
chmod a+x $RPM_BUILD_ROOT/%{_bindir}/ooviewdoc

echo \#\!/bin/sh > $RPM_BUILD_ROOT/%{_bindir}/oowriter
echo exec openoffice.org -writer \"\$@\" >> $RPM_BUILD_ROOT/%{_bindir}/oowriter
chmod a+x $RPM_BUILD_ROOT/%{_bindir}/oowriter

echo \#\!/bin/sh > $RPM_BUILD_ROOT/%{_bindir}/oocalc
echo exec openoffice.org -calc \"\$@\" >> $RPM_BUILD_ROOT/%{_bindir}/oocalc
chmod a+x $RPM_BUILD_ROOT/%{_bindir}/oocalc

echo \#\!/bin/sh > $RPM_BUILD_ROOT/%{_bindir}/ooimpress
echo exec openoffice.org -impress \"\$@\" >> $RPM_BUILD_ROOT/%{_bindir}/ooimpress
chmod a+x $RPM_BUILD_ROOT/%{_bindir}/ooimpress

echo \#\!/bin/sh > $RPM_BUILD_ROOT/%{_bindir}/oodraw
echo exec openoffice.org -draw \"\$@\" >> $RPM_BUILD_ROOT/%{_bindir}/oodraw
chmod a+x $RPM_BUILD_ROOT/%{_bindir}/oodraw

echo \#\!/bin/sh > $RPM_BUILD_ROOT/%{_bindir}/oomath
echo exec openoffice.org -math \"\$@\" >> $RPM_BUILD_ROOT/%{_bindir}/oomath
chmod a+x $RPM_BUILD_ROOT/%{_bindir}/oomath

echo \#\!/bin/sh > $RPM_BUILD_ROOT/%{_bindir}/oobase
echo exec openoffice.org -base \"\$@\" >> $RPM_BUILD_ROOT/%{_bindir}/oobase
chmod a+x $RPM_BUILD_ROOT/%{_bindir}/oobase

cp -f %{SOURCE11} $RPM_BUILD_ROOT/%{_bindir}/unopkg
sed -i -e "s/LAUNCHER/unopkg/g" $RPM_BUILD_ROOT/%{_bindir}/unopkg
sed -i -e "s/BRAND/openoffice.org3/g" $RPM_BUILD_ROOT/%{_bindir}/unopkg
chmod a+x $RPM_BUILD_ROOT/%{_bindir}/unopkg

cp -f %{SOURCE11} $RPM_BUILD_ROOT/%{_bindir}/openoffice.org
sed -i -e "s/LAUNCHER/soffice/g" $RPM_BUILD_ROOT/%{_bindir}/openoffice.org
sed -i -e "s/BRAND/openoffice.org3/g" $RPM_BUILD_ROOT/%{_bindir}/openoffice.org
chmod a+x $RPM_BUILD_ROOT/%{_bindir}/openoffice.org

%if %{langpacks}
cp -f %{SOURCE11} $RPM_BUILD_ROOT/%{_bindir}/broffice.org
sed -i -e "s/LAUNCHER/soffice/g" $RPM_BUILD_ROOT/%{_bindir}/broffice.org
sed -i -e "s/BRAND/broffice.org3/g" $RPM_BUILD_ROOT/%{_bindir}/broffice.org
chmod a+x $RPM_BUILD_ROOT/%{_bindir}/broffice.org
%endif

cp $RPM_BUILD_ROOT/%{_bindir}/openoffice.org $RPM_BUILD_ROOT/%{_bindir}/openoffice.org-2.0
cp $RPM_BUILD_ROOT/%{_bindir}/openoffice.org $RPM_BUILD_ROOT/%{_bindir}/openoffice.org-1.9
# rhbz#499474 provide a /usr/bin/soffice for .recently-used.xbel
pushd $RPM_BUILD_ROOT/%{_bindir}
ln -s %{oooinstdir}/program/soffice soffice
popd

pushd $RPM_BUILD_ROOT/%{oooinstdir}/share/xdg/
chmod u+w *.desktop
rm -rf printeradmin.desktop
for file in *.desktop; do
    # rhbz#156677 remove the version from Name=
    sed -i -e "s/$PRODUCTVERSION //g" $file
    # rhbz#156067 don't version the icons
    sed -i -e "s/$PRODUCTVERSIONSHORT//g" $file
    # add X-GIO-NoFuse so we get url:// instead of file://~.gvfs/
    echo X-GIO-NoFuse=true >> $file
done
echo "StartupNotify=true" >> base.desktop
echo "StartupNotify=true" >> calc.desktop
echo "StartupNotify=true" >> impress.desktop
echo "StartupNotify=true" >> writer.desktop
echo "StartupNotify=true" >> math.desktop
echo "StartupNotify=true" >> draw.desktop
echo "TryExec=oobase" >> base.desktop
echo "TryExec=oocalc" >> calc.desktop
echo "TryExec=ooimpress" >> impress.desktop
echo "TryExec=oowriter" >> writer.desktop
echo "TryExec=oomath" >> math.desktop
echo "TryExec=oodraw" >> draw.desktop
# rhbz#156677# / rhbz#186515#
echo "NoDisplay=true" >> math.desktop
# rhbz#491159 temporarily remove NoDisplay=true from qstart.desktop
sed -i -e "/NoDisplay=true/d" qstart.desktop
# relocate the .desktop and icon files
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
cp -p base.desktop $RPM_BUILD_ROOT/%{_datadir}/applications/openoffice.org-base.desktop
cp -p calc.desktop $RPM_BUILD_ROOT/%{_datadir}/applications/openoffice.org-calc.desktop
cp -p impress.desktop $RPM_BUILD_ROOT/%{_datadir}/applications/openoffice.org-impress.desktop
cp -p writer.desktop $RPM_BUILD_ROOT/%{_datadir}/applications/openoffice.org-writer.desktop
cp -p math.desktop $RPM_BUILD_ROOT/%{_datadir}/applications/openoffice.org-math.desktop
cp -p draw.desktop $RPM_BUILD_ROOT/%{_datadir}/applications/openoffice.org-draw.desktop
popd
# rhbz#486062/ooo#109154 create a .desktop file that registers OOo as a handler for the javafilter formats
# iff it is installed
cp -p %{SOURCE9} $RPM_BUILD_ROOT/%{_datadir}/applications/openoffice.org-javafilter.desktop
pushd sysui/output/usr/share/
#get rid of the gnome icons and other unneeded files
rm -rf icons/gnome applications mime application-registry
# rhbz#156067 don't version the icons
find . -name "*.desktop" -exec sed -i -e s/$PRODUCTVERSIONSHORT//g {} \;
find . -name "*officeorg$PRODUCTVERSIONSHORT*" -exec bash -c \
  "mv \$1 \`echo \$1 | sed s/officeorg$PRODUCTVERSIONSHORT/officeorg/\`" -- {} \;
find . -name "*office.org$PRODUCTVERSIONSHORT*" -exec bash -c \
  "mv \$1 \`echo \$1 | sed s/.org$PRODUCTVERSIONSHORT/.org/\`" -- {} \;
find . -type l -print -exec ls -lag '{}' \; | gawk '{q="'\''" ; file=$0 ; \
    getline; \
    split($0, ls, " -> "); \
    link=ls[2]; \
    gsub(ENVIRON["PRODUCTVERSIONSHORT"], "", link) ; \
    if ( link != ls[2] ) system("rm " q file q"; ln -s "q link q" "q file q); \
 }'
sed -i -e s/openofficeorg$PRODUCTVERSIONSHORT/openofficeorg/g \
  ./mime-info/openoffice.org.keys
sed -i -e s/openoffice.org$PRODUCTVERSIONSHORT/openoffice.org/g \
  ./mime-info/openoffice.org.keys
%if %{langpacks}
sed -i -e s/brofficeorg$PRODUCTVERSIONSHORT/brofficeorg/g \
  ./mime-info/broffice.org.keys
sed -i -e s/broffice.org$PRODUCTVERSIONSHORT/broffice.org/g \
  ./mime-info/broffice.org.keys
%endif
#relocate the rest of them
cp -r icons $RPM_BUILD_ROOT/%{_datadir}
cp -r mime-info $RPM_BUILD_ROOT/%{_datadir}
#add our mime-types, e.g. for .oxt extensions
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mime/packages
cp -p ../../../unxlng*.pro/misc/openoffice.org/openoffice.org.xml $RPM_BUILD_ROOT/%{_datadir}/mime/packages
popd

%if %{langpacks}
pushd $RPM_BUILD_ROOT/%{brinstdir}/share/xdg/
chmod u+w *.desktop
rm -rf printeradmin.desktop
for file in *.desktop; do
    # rhbz#156677 remove the version from Name=
    sed -i -e "s/$PRODUCTVERSION //g" $file
    # rhbz#156067 don't version the icons
    sed -i -e "s/$PRODUCTVERSIONSHORT//g" $file
    # use broffice.org launcher
    sed -i -e "s/openoffice/broffice/g" $file
    # add X-GIO-NoFuse so we get url:// instead of file://~.gvfs/
    echo X-GIO-NoFuse=true >> $file
done
echo "StartupNotify=true" >> base.desktop
echo "StartupNotify=true" >> calc.desktop
echo "StartupNotify=true" >> impress.desktop
echo "StartupNotify=true" >> writer.desktop
echo "StartupNotify=true" >> math.desktop
echo "StartupNotify=true" >> draw.desktop
# rhbz#156677# / rhbz#186515#
echo "NoDisplay=true" >> math.desktop
# rhbz#491159 temporarily remove NoDisplay=true from qstart.desktop
sed -i -e "/NoDisplay=true/d" qstart.desktop
# relocate the .desktop and icon files
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
cp -p base.desktop $RPM_BUILD_ROOT/%{_datadir}/applications/broffice.org-base.desktop
cp -p calc.desktop $RPM_BUILD_ROOT/%{_datadir}/applications/broffice.org-calc.desktop
cp -p impress.desktop $RPM_BUILD_ROOT/%{_datadir}/applications/broffice.org-impress.desktop
cp -p writer.desktop $RPM_BUILD_ROOT/%{_datadir}/applications/broffice.org-writer.desktop
cp -p math.desktop $RPM_BUILD_ROOT/%{_datadir}/applications/broffice.org-math.desktop
cp -p draw.desktop $RPM_BUILD_ROOT/%{_datadir}/applications/broffice.org-draw.desktop
popd
%endif

rm -rf $RPM_BUILD_ROOT/%{brinstdir}/readmes
rm -rf $RPM_BUILD_ROOT/%{brinstdir}/licenses
rm -rf $RPM_BUILD_ROOT/%{oooinstdir}/readmes
rm -rf $RPM_BUILD_ROOT/%{oooinstdir}/licenses

mkdir -p $RPM_BUILD_ROOT/%{basisinstdir}/share/psprint/driver
cp -r psprint_config/configuration/ppds/SGENPRT.PS $RPM_BUILD_ROOT/%{basisinstdir}/share/psprint/driver/SGENPRT.PS

# rhbz#452385 to auto have postgres in classpath if subsequently installed
# rhbz#465664 to get lucene working for functional help
sed -i -e "s#URE_MORE_JAVA_CLASSPATH_URLS.*#& file:///usr/share/java/lucene.jar file:///usr/share/java/lucene-contrib/lucene-analyzers.jar file:///usr/share/java/postgresql-jdbc.jar#" $RPM_BUILD_ROOT/%{basisinstdir}/program/fundamentalbasisrc

%clean
rm -rf $RPM_BUILD_ROOT

%if %{langpacks}
%files langpack-af_ZA 	-f af.filelist
%files langpack-ar  	-f ar.filelist
%files langpack-bg_BG 	-f bg.filelist
%files langpack-bn  	-f bn.filelist
%files langpack-ca_ES 	-f ca.filelist
%files langpack-cs_CZ 	-f cs.filelist
%files langpack-cy_GB 	-f cy.filelist
%files langpack-da_DK 	-f da.filelist
%files langpack-de 	-f de.filelist
%files langpack-el_GR 	-f el.filelist
%files langpack-en
%files langpack-es	-f es.filelist
%files langpack-et_EE 	-f et.filelist
%files langpack-eu_ES 	-f eu.filelist
%files langpack-fi_FI 	-f fi.filelist
%files langpack-fr 	-f fr.filelist
%files langpack-ga_IE 	-f ga.filelist
%files langpack-gl_ES	-f gl.filelist
%files langpack-gu_IN	-f gu.filelist
%files langpack-pa	-f pa-IN.filelist
%files langpack-he_IL	-f he.filelist
%files langpack-hi_IN	-f hi-IN.filelist
%files langpack-hu_HU	-f hu.filelist
%files langpack-hr_HR	-f hr.filelist
%files langpack-it	-f it.filelist
%files langpack-ja_JP 	-f ja.filelist
%files langpack-ko_KR	-f ko.filelist
%{oooinstdir}/share/registry/modules/org/openoffice/Office/Common/Common-korea.xcu
%files langpack-lt_LT	-f lt.filelist
%files langpack-ms_MY	-f ms.filelist
%files langpack-nb_NO	-f nb.filelist
%files langpack-nl	-f nl.filelist
%files langpack-nn_NO	-f nn.filelist
%files langpack-pl_PL	-f pl.filelist
%files langpack-pt_PT	-f pt.filelist
%files langpack-pt_BR	-f pt-BR.filelist
%files langpack-ru	-f ru.filelist
%files langpack-sk_SK	-f sk.filelist
%files langpack-sl_SI	-f sl.filelist
%files langpack-sr	-f sr.filelist
%files langpack-sv	-f sv.filelist
%files langpack-ta_IN	-f ta.filelist
%files langpack-th_TH	-f th.filelist
%files langpack-tr_TR	-f tr.filelist
%files langpack-zh_CN	-f zh-CN.filelist
%files langpack-zh_TW	-f zh-TW.filelist
%files langpack-zu_ZA	-f zu.filelist
%files langpack-tn_ZA	-f tn.filelist
%files langpack-ts_ZA	-f ts.filelist
%files langpack-nso_ZA	-f ns.filelist
%files langpack-nr_ZA	-f nr.filelist
%files langpack-ss_ZA	-f ss.filelist
%files langpack-st_ZA	-f st.filelist
%files langpack-ve_ZA	-f ve.filelist
%files langpack-xh_ZA	-f xh.filelist
%files langpack-as_IN	-f as.filelist
%files langpack-mr_IN	-f mr.filelist
%files langpack-ml_IN	-f ml.filelist
%files langpack-or_IN	-f or.filelist
%files langpack-te_IN	-f te.filelist
%files langpack-ur	-f ur.filelist
%files langpack-kn_IN	-f kn.filelist
%files langpack-dz	-f dz.filelist
%files langpack-uk	-f uk.filelist
%files langpack-mai_IN	-f mai.filelist
%files langpack-ro	-f ro.filelist
%endif

%files core
%defattr(-,root,root,-)
%dir %{_datadir}/openoffice.org
%dir %{_datadir}/openoffice.org/extensions
%dir %{baseinstdir}
%dir %{baseinstdir}/share
%dir %{baseinstdir}/share/uno_packages
%{baseinstdir}/share/uno_packages/cache
%dir %{baseinstdir}/extensions
%dir %{basisinstdir}
%dir %{basisinstdir}/help
%docdir %{basisinstdir}/help/en
%dir %{basisinstdir}/help/en
%{basisinstdir}/help/en/default.css
%{basisinstdir}/help/en/err.html
%{basisinstdir}/help/en/highcontrast1.css
%{basisinstdir}/help/en/highcontrast2.css
%{basisinstdir}/help/en/highcontrastblack.css
%{basisinstdir}/help/en/highcontrastwhite.css
%{basisinstdir}/help/en/sbasic.*
%{basisinstdir}/help/en/schart.*
%{basisinstdir}/help/en/shared.*
%{basisinstdir}/help/idxcaption.xsl
%{basisinstdir}/help/idxcontent.xsl
%{basisinstdir}/help/main_transform.xsl
%{basisinstdir}/presets
%dir %{basisinstdir}/program
%{basisinstdir}/program/addin
%{basisinstdir}/program/basprov%{SOPOST}.uno.so
%{basisinstdir}/program/canvasfactory.uno.so
%{basisinstdir}/program/cde-open-url
%dir %{basisinstdir}/program/classes
%{basisinstdir}/program/classes/agenda.jar                
%{basisinstdir}/program/classes/commonwizards.jar
%{basisinstdir}/program/classes/fax.jar
%{basisinstdir}/program/classes/form.jar
%{basisinstdir}/program/classes/query.jar          
%{basisinstdir}/program/classes/letter.jar          
%{basisinstdir}/program/classes/LuceneHelpWrapper.jar
%{basisinstdir}/program/classes/officebean.jar
%{basisinstdir}/program/classes/report.jar
%{basisinstdir}/program/classes/ScriptFramework.jar
%{basisinstdir}/program/classes/ScriptProviderForJava.jar
%{basisinstdir}/program/classes/table.jar
%{basisinstdir}/program/classes/unoil.jar
%{basisinstdir}/program/classes/web.jar
%{basisinstdir}/program/classes/XMergeBridge.jar
%{basisinstdir}/program/classes/xmerge.jar
%{basisinstdir}/program/classes/XSLTFilter.jar
%{basisinstdir}/program/classes/XSLTValidate.jar
%{basisinstdir}/program/cmdmail.uno.so
%{basisinstdir}/program/configmgrrc
%{basisinstdir}/program/deployment%{SOPOST}.uno.so
%{basisinstdir}/program/deploymentgui%{SOPOST}.uno.so
%{basisinstdir}/program/dlgprov%{SOPOST}.uno.so
%{basisinstdir}/program/fastsax.uno.so
%{basisinstdir}/program/fpicker.uno.so
%{basisinstdir}/program/fps_gnome.uno.so
%{basisinstdir}/program/fps_office.uno.so
%{basisinstdir}/program/fundamentalbasisrc
%{basisinstdir}/program/gengal*
%{basisinstdir}/program/gnome-open-url
%{basisinstdir}/program/gnome-open-url.bin
%{basisinstdir}/program/hatchwindowfactory.uno.so
%{basisinstdir}/program/i18nsearch.uno.so
%{basisinstdir}/program/kde-open-url
%{basisinstdir}/program/legacy_binfilters.rdb
%{basisinstdir}/program/libacc%{SOPOST}.so
%{basisinstdir}/program/libadabas%{SOPOST}.so
%{basisinstdir}/program/libavmedia*.so
%{basisinstdir}/program/libbasctl%{SOPOST}.so
%{basisinstdir}/program/libbf_sb%{SOPOST}.so
%{basisinstdir}/program/libbf_frm%{SOPOST}.so
%{basisinstdir}/program/libbf_go%{SOPOST}.so
%{basisinstdir}/program/libbf_migratefilter%{SOPOST}.so
%{basisinstdir}/program/libbf_ofa%{SOPOST}.so
%{basisinstdir}/program/libbf_sch%{SOPOST}.so
%{basisinstdir}/program/libbf_sd%{SOPOST}.so
%{basisinstdir}/program/libbf_so%{SOPOST}.so
%{basisinstdir}/program/libbf_svt%{SOPOST}.so
%{basisinstdir}/program/libbf_svx%{SOPOST}.so
%{basisinstdir}/program/libbf_wrapper%{SOPOST}.so
%{basisinstdir}/program/libbf_xo%{SOPOST}.so
%{basisinstdir}/program/libbib%{SOPOST}.so
%{basisinstdir}/program/libbindet%{SOPOST}.so
%{basisinstdir}/program/libcached1.so
%{basisinstdir}/program/libcanvastools%{SOPOST}.so
%{basisinstdir}/program/libchart*%{SOPOST}.so
%{basisinstdir}/program/libcollator_data.so
%{basisinstdir}/program/libcppcanvas%{SOPOST}.so
%{basisinstdir}/program/libctl%{SOPOST}.so
%{basisinstdir}/program/libcui%{SOPOST}.so
%{basisinstdir}/program/libdba%{SOPOST}.so
%{basisinstdir}/program/libdbacfg%{SOPOST}.so
%{basisinstdir}/program/libdbase%{SOPOST}.so
%{basisinstdir}/program/libdbaxml%{SOPOST}.so
%{basisinstdir}/program/libdbmm%{SOPOST}.so
%{basisinstdir}/program/libdbpool2.so
%{basisinstdir}/program/libdbtools%{SOPOST}.so
%{basisinstdir}/program/libdbu%{SOPOST}.so
%{basisinstdir}/program/libdeploymentmisc%{SOPOST}.so
%{basisinstdir}/program/libdesktop_detector%{SOPOST}.so
%{basisinstdir}/program/libdict_ja.so
%{basisinstdir}/program/libdict_zh.so
%{basisinstdir}/program/libdrawinglayer%{SOPOST}.so
%{basisinstdir}/program/libeggtray%{SOPOST}.so
%{basisinstdir}/program/libembobj.so
%{basisinstdir}/program/libemboleobj.so
%{basisinstdir}/program/libevoab*.so
%{basisinstdir}/program/libevtatt.so
%{basisinstdir}/program/libegi%{SOPOST}.so    
%{basisinstdir}/program/libeme%{SOPOST}.so
%{basisinstdir}/program/libepb%{SOPOST}.so
%{basisinstdir}/program/libepg%{SOPOST}.so    
%{basisinstdir}/program/libepp%{SOPOST}.so
%{basisinstdir}/program/libeps%{SOPOST}.so    
%{basisinstdir}/program/libept%{SOPOST}.so
%{basisinstdir}/program/libera%{SOPOST}.so    
%{basisinstdir}/program/libeti%{SOPOST}.so
%{basisinstdir}/program/libexp%{SOPOST}.so    
%{basisinstdir}/program/libicd%{SOPOST}.so
%{basisinstdir}/program/libicg%{SOPOST}.so
%{basisinstdir}/program/libidx%{SOPOST}.so
%{basisinstdir}/program/libime%{SOPOST}.so
%{basisinstdir}/program/libindex_data.so
%{basisinstdir}/program/libipb%{SOPOST}.so
%{basisinstdir}/program/libipd%{SOPOST}.so
%{basisinstdir}/program/libips%{SOPOST}.so
%{basisinstdir}/program/libipt%{SOPOST}.so
%{basisinstdir}/program/libipx%{SOPOST}.so
%{basisinstdir}/program/libira%{SOPOST}.so
%{basisinstdir}/program/libitg%{SOPOST}.so
%{basisinstdir}/program/libiti%{SOPOST}.so
%{basisinstdir}/program/libofficebean.so
%{basisinstdir}/program/liboooimprovecore%{SOPOST}.so
%{basisinstdir}/program/libfile%{SOPOST}.so
%{basisinstdir}/program/libfilterconfig1.so
%{basisinstdir}/program/libflat%{SOPOST}.so
%{basisinstdir}/program/libfrm%{SOPOST}.so
%{basisinstdir}/program/libguesslang%{SOPOST}.so
%{basisinstdir}/program/libhelplinker%{SOPOST}.so
%{basisinstdir}/program/libhyphen%{SOPOST}.so
%{basisinstdir}/program/libi18nregexpgcc3.so
%{basisinstdir}/program/libjdbc%{SOPOST}.so
%{basisinstdir}/program/liblegacy_binfilters%{SOPOST}.so
%{basisinstdir}/program/liblng%{SOPOST}.so
%{basisinstdir}/program/liblog%{SOPOST}.so
%{basisinstdir}/program/liblocaledata_en.so
%{basisinstdir}/program/liblocaledata_es.so
%{basisinstdir}/program/liblocaledata_euro.so
%{basisinstdir}/program/liblocaledata_others.so
%{basisinstdir}/program/libmcnttype.so
%{basisinstdir}/program/libmozbootstrap.so
%{basisinstdir}/program/libmysql%{SOPOST}.so
%{basisinstdir}/program/libodbc%{SOPOST}.so
%{basisinstdir}/program/libodbcbase%{SOPOST}.so
%{basisinstdir}/program/liboffacc%{SOPOST}.so
%{basisinstdir}/program/liboox%{SOPOST}.so
%{basisinstdir}/program/libpcr%{SOPOST}.so
%{basisinstdir}/program/libpdffilter%{SOPOST}.so
%{basisinstdir}/program/libpl%{SOPOST}.so
%{basisinstdir}/program/libpreload%{SOPOST}.so
%{basisinstdir}/program/libprotocolhandler%{SOPOST}.so
%{basisinstdir}/program/libqstart_gtk%{SOPOST}.so
%{basisinstdir}/program/librecentfile.so
%{basisinstdir}/program/libres%{SOPOST}.so
%{basisinstdir}/program/libsax%{SOPOST}.so
%{basisinstdir}/program/libscn%{SOPOST}.so
%{basisinstdir}/program/libscriptframe.so
%{basisinstdir}/program/libsd%{SOPOST}.so
%{basisinstdir}/program/libsdfilt%{SOPOST}.so
%{basisinstdir}/program/libsdbc2.so
%{basisinstdir}/program/libsdbt%{SOPOST}so
%{basisinstdir}/program/libsdd%{SOPOST}.so
%{basisinstdir}/program/libsdui%{SOPOST}.so
%{basisinstdir}/program/libspa%{SOPOST}.so
%{basisinstdir}/program/libspell%{SOPOST}.so
%{basisinstdir}/program/libsrtrs1.so
%{basisinstdir}/program/libsts%{SOPOST}.so
%{basisinstdir}/program/libsvx%{SOPOST}.so
%{basisinstdir}/program/libsvxcore%{SOPOST}.so
%{basisinstdir}/program/libsvxmsfilter%{SOPOST}.so
%{basisinstdir}/program/libsw%{SOPOST}.so
%{basisinstdir}/program/libtextconv_dict.so
%{basisinstdir}/program/libtextconversiondlgs%{SOPOST}.so
%{basisinstdir}/program/libtfu%{SOPOST}.so
%{basisinstdir}/program/libtvhlp1.so
%{basisinstdir}/program/libucbhelper4gcc3.so
%{basisinstdir}/program/libucpchelp1.so
%{basisinstdir}/program/libucpdav1.so
%{basisinstdir}/program/libucpftp1.so
%{basisinstdir}/program/libucphier1.so
%{basisinstdir}/program/libucppkg1.so
%{basisinstdir}/program/libunordf%{SOPOST}.so
%{basisinstdir}/program/libunopkgapp.so
%{basisinstdir}/program/libunoxml%{SOPOST}.so
%{basisinstdir}/program/libupdchk%{SOPOST}.so
%{basisinstdir}/program/libuui%{SOPOST}.so
%{basisinstdir}/program/libvclplug_gen%{SOPOST}.so
%{basisinstdir}/program/libvclplug_gtk%{SOPOST}.so
%{basisinstdir}/program/libxmlfa%{SOPOST}.so
%{basisinstdir}/program/libxmlfd%{SOPOST}.so
%{basisinstdir}/program/libxmx%{SOPOST}.so
%{basisinstdir}/program/libxof%{SOPOST}.so
%{basisinstdir}/program/libxsec_fw.so
%{basisinstdir}/program/libxsec_xmlsec.so
%{basisinstdir}/program/libxsltdlg%{SOPOST}.so
%{basisinstdir}/program/libxsltfilter%{SOPOST}.so
%{basisinstdir}/program/libxstor.so
%{basisinstdir}/program/migrationoo2.uno.so
%{basisinstdir}/program/nsplugin
%{basisinstdir}/program/open-url
%{basisinstdir}/program/offapi.rdb
%{basisinstdir}/program/passwordcontainer.uno.so
%{basisinstdir}/program/plugin
%{basisinstdir}/program/pluginapp.bin
%{basisinstdir}/program/productregistration.uno.so
%dir %{basisinstdir}/program/resource
%{basisinstdir}/program/resource/avmedia%{UPD}en-US.res
%{basisinstdir}/program/resource/acc%{UPD}en-US.res
%{basisinstdir}/program/resource/basctl%{UPD}en-US.res
%{basisinstdir}/program/resource/bf_frm%{UPD}en-US.res
%{basisinstdir}/program/resource/bf_ofa%{UPD}en-US.res
%{basisinstdir}/program/resource/bf_sch%{UPD}en-US.res
%{basisinstdir}/program/resource/bf_sd%{UPD}en-US.res
%{basisinstdir}/program/resource/bf_svt%{UPD}en-US.res
%{basisinstdir}/program/resource/bf_svx%{UPD}en-US.res
%{basisinstdir}/program/resource/bib%{UPD}en-US.res
%{basisinstdir}/program/resource/cal%{UPD}en-US.res
%{basisinstdir}/program/resource/chartcontroller%{UPD}en-US.res
%{basisinstdir}/program/resource/dba%{UPD}en-US.res
%{basisinstdir}/program/resource/dbmm%{UPD}en-US.res
%{basisinstdir}/program/resource/dbu%{UPD}en-US.res
%{basisinstdir}/program/resource/dbw%{UPD}en-US.res
%{basisinstdir}/program/resource/deployment%{UPD}en-US.res
%{basisinstdir}/program/resource/deploymentgui%{UPD}en-US.res
%{basisinstdir}/program/resource/dkt%{UPD}en-US.res
%{basisinstdir}/program/resource/egi%{UPD}en-US.res
%{basisinstdir}/program/resource/eme%{UPD}en-US.res
%{basisinstdir}/program/resource/epb%{UPD}en-US.res
%{basisinstdir}/program/resource/epg%{UPD}en-US.res
%{basisinstdir}/program/resource/epp%{UPD}en-US.res
%{basisinstdir}/program/resource/eps%{UPD}en-US.res
%{basisinstdir}/program/resource/ept%{UPD}en-US.res
%{basisinstdir}/program/resource/eur%{UPD}en-US.res
%{basisinstdir}/program/resource/fps_office%{UPD}en-US.res
%{basisinstdir}/program/resource/frm%{UPD}en-US.res
%{basisinstdir}/program/resource/fwe%{UPD}en-US.res
%{basisinstdir}/program/resource/gal%{UPD}en-US.res
%{basisinstdir}/program/resource/imp%{UPD}en-US.res
%{basisinstdir}/program/resource/ofa%{UPD}en-US.res
%{basisinstdir}/program/resource/pcr%{UPD}en-US.res
%{basisinstdir}/program/resource/pdffilter%{UPD}en-US.res
%{basisinstdir}/program/resource/preload%{UPD}en-US.res
%{basisinstdir}/program/resource/productregistration%{UPD}en-US.res
%{basisinstdir}/program/resource/san%{UPD}en-US.res
%{basisinstdir}/program/resource/sb%{UPD}en-US.res
%{basisinstdir}/program/resource/sd%{UPD}en-US.res
%{basisinstdir}/program/resource/sfx%{UPD}en-US.res
%{basisinstdir}/program/resource/spa%{UPD}en-US.res
%{basisinstdir}/program/resource/sdbt%{UPD}en-US.res
%{basisinstdir}/program/resource/svs%{UPD}en-US.res
%{basisinstdir}/program/resource/svt%{UPD}en-US.res
%{basisinstdir}/program/resource/svx%{UPD}en-US.res
%{basisinstdir}/program/resource/sw%{UPD}en-US.res
%{basisinstdir}/program/resource/textconversiondlgs%{UPD}en-US.res
%{basisinstdir}/program/resource/tfu%{UPD}en-US.res
%{basisinstdir}/program/resource/tk%{UPD}en-US.res
%{basisinstdir}/program/resource/tpl%{UPD}en-US.res
%{basisinstdir}/program/resource/uui%{UPD}en-US.res
%{basisinstdir}/program/resource/updchk%{UPD}en-US.res
%{basisinstdir}/program/resource/upd%{UPD}en-US.res
%{basisinstdir}/program/resource/vcl%{UPD}en-US.res
%{basisinstdir}/program/resource/wzi%{UPD}en-US.res
%{basisinstdir}/program/resource/xmlsec%{UPD}en-US.res
%{basisinstdir}/program/resource/xsltdlg%{UPD}en-US.res
%{basisinstdir}/program/sax.uno.so
%{basisinstdir}/program/senddoc
%{basisinstdir}/program/services.rdb
%{basisinstdir}/program/simplecanvas.uno.so
%{basisinstdir}/program/slideshow.uno.so
%{basisinstdir}/program/libsofficeapp.so
%{basisinstdir}/program/spadmin.bin
%{basisinstdir}/program/stringresource%{SOPOST}.uno.so
%{basisinstdir}/program/svtmisc.uno.so
%{basisinstdir}/program/syssh.uno.so
%{basisinstdir}/program/ucpexpand1.uno.so
%{basisinstdir}/program/ucptdoc1.uno.so
%{basisinstdir}/program/unorc
%{basisinstdir}/program/updatefeed.uno.so
%{basisinstdir}/ure-link
%{basisinstdir}/program/uri-encode
%{basisinstdir}/program/vclcanvas.uno.so
%{basisinstdir}/program/versionrc
%{basisinstdir}/program/cairocanvas.uno.so
%dir %{basisinstdir}/share
%dir %{basisinstdir}/share/Scripts
%{basisinstdir}/share/Scripts/java
%{basisinstdir}/share/autotext
%{basisinstdir}/share/basic
%dir %{basisinstdir}/share/config
%{basisinstdir}/share/config/images.zip
%{basisinstdir}/share/config/images_classic.zip
%{basisinstdir}/share/config/images_crystal.zip
%{basisinstdir}/share/config/images_hicontrast.zip
%{basisinstdir}/share/config/images_industrial.zip
%{basisinstdir}/share/config/images_tango.zip
%{basisinstdir}/share/config/javasettingsunopkginstall.xml
%{basisinstdir}/share/config/psetup.xpm
%{basisinstdir}/share/config/psetupl.xpm
%dir %{basisinstdir}/share/config/soffice.cfg
%{basisinstdir}/share/config/soffice.cfg/global
%{basisinstdir}/share/config/soffice.cfg/modules
%{basisinstdir}/share/config/symbol
%{basisinstdir}/share/config/webcast
%{basisinstdir}/share/config/wizard
%dir %{basisinstdir}/share/dtd
%{basisinstdir}/share/dtd/officedocument
%{basisinstdir}/share/gallery
%dir %{basisinstdir}/share/psprint
%config %{basisinstdir}/share/psprint/psprint.conf
%{basisinstdir}/share/psprint/driver
%dir %{basisinstdir}/share/registry
%dir %{basisinstdir}/share/registry/data
%dir %{basisinstdir}/share/registry/data/org
%dir %{basisinstdir}/share/registry/data/org/openoffice
%{basisinstdir}/share/registry/data/org/openoffice/FirstStartWizard.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Inet.xcu
%{basisinstdir}/share/registry/data/org/openoffice/LDAP.xcu.sample
%{basisinstdir}/share/registry/data/org/openoffice/Setup.xcu
%dir %{basisinstdir}/share/registry/data/org/openoffice/Office
%{basisinstdir}/share/registry/data/org/openoffice/Office/Accelerators.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/Calc.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/Canvas.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/Common.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/DataAccess.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/Embedding.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/ExtensionManager.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/FormWizard.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/Histories.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/Impress.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/Jobs.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/Labels.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/Logging.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/Math.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/Paths.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/ProtocolHandler.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/SFX.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/Scripting.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/Security.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/TableWizard.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI.xcu
%dir %{basisinstdir}/share/registry/data/org/openoffice/Office/UI
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/BaseWindowState.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/BasicIDECommands.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/BasicIDEWindowState.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/BibliographyCommands.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/ChartCommands.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/ChartWindowState.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/Controller.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/DbBrowserWindowState.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/DbQueryWindowState.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/DbRelationWindowState.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/DbTableDataWindowState.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/DbTableWindowState.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/DbuCommands.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/DrawImpressCommands.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/Factories.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/GenericCategories.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/GenericCommands.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/StartModuleCommands.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/StartModuleWindowState.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/XFormsWindowState.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/Views.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/WebWizard.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/Writer.xcu
%{basisinstdir}/share/registry/data/org/openoffice/TypeDetection
%{basisinstdir}/share/registry/data/org/openoffice/UserProfile.xcu
%{basisinstdir}/share/registry/data/org/openoffice/VCL.xcu
%dir %{basisinstdir}/share/registry/data/org/openoffice/ucb
%{basisinstdir}/share/registry/data/org/openoffice/ucb/Configuration.xcu
%dir %{basisinstdir}/share/registry/ldap
%{basisinstdir}/share/registry/ldap/oo-ad-ldap-attr.map
%{basisinstdir}/share/registry/ldap/oo-ldap-attr.map
%dir %{basisinstdir}/share/registry/modules
%dir %{basisinstdir}/share/registry/modules/org
%dir %{basisinstdir}/share/registry/modules/org/openoffice
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Accelerators
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Embedding
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office/Common
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Common/Common-survey.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Common/Common-unx.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/Office/DataAccess
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office/Linguistic
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Linguistic/Linguistic-lingucomponent-hyphenator.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Linguistic/Linguistic-lingucomponent-spellchecker.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Linguistic/Linguistic-lingucomponent-thesaurus.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office/Paths
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Paths/libtextcat.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Paths/Paths-unxwnt.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Paths/SystemAutoCorrect.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office/Recovery
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Recovery/AutoSaveRecovery.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Setup
%{basisinstdir}/share/registry/modules/org/openoffice/Setup/Langpack-en-US.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/Setup/RegisterAndLicence.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/Setup/Setup-start.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_base_filters.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_chart_filters.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_chart_bf_filters.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/GraphicFilter
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/GraphicFilter/fcfg_internalgraphics_filters.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Misc
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Misc/fcfg_base_others.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Misc/fcfg_chart_others.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_base_types.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_chart_types.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_chart_bf_types.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_internalgraphics_types.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/UISort
%dir %{basisinstdir}/share/registry/modules/org/openoffice/ucb
%dir %{basisinstdir}/share/registry/modules/org/openoffice/ucb/Configuration
%{basisinstdir}/share/registry/modules/org/openoffice/ucb/Configuration/Configuration-gio.xcu
%dir %{basisinstdir}/share/registry/res
%{basisinstdir}/share/registry/res/en-US
%dir %{basisinstdir}/share/registry/schema
%dir %{basisinstdir}/share/registry/schema/org
%dir %{basisinstdir}/share/registry/schema/org/openoffice
%{basisinstdir}/share/registry/schema/org/openoffice/FirstStartWizard.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Inet.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/LDAP.xcs
%dir %{basisinstdir}/share/registry/schema/org/openoffice/Office
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Accelerators.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Addons.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/CalcAddIns.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Calc.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Canvas.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Chart.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Commands.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Common.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Compatibility.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/DataAccess
%{basisinstdir}/share/registry/schema/org/openoffice/Office/DataAccess.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Draw.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Embedding.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/ExtendedColorScheme.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/ExtensionManager.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Events.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/FormWizard.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Histories.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Impress.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Java.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Jobs.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Labels.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Linguistic.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Logging.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Math.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/OptionsDialog.xcs
%dir %{basisinstdir}/share/registry/schema/org/openoffice/Office/OOoImprovement
%{basisinstdir}/share/registry/schema/org/openoffice/Office/OOoImprovement/Settings.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Paths.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/ProtocolHandler.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Recovery.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/SFX.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Scripting.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Security.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Substitution.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/TabBrowse.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/TableWizard.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/TypeDetection.xcs
%dir %{basisinstdir}/share/registry/schema/org/openoffice/Office/UI
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/BaseWindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/BasicIDECommands.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/BasicIDEWindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/BibliographyCommands.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/BibliographyWindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/Category.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/ChartCommands.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/ChartWindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/Commands.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/Controller.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/DbBrowserWindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/DbQueryWindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/DbRelationWindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/DbTableDataWindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/DbTableWindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/DbuCommands.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/DrawImpressCommands.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/Factories.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/GenericCategories.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/GenericCommands.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/GlobalSettings.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/MathWindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/StartModuleCommands.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/StartModuleWindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/WindowContentFactories.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/WindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/XFormsWindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Views.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/WebWizard.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/Writer.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/WriterWeb.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Setup.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/System.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/TypeDetection
%{basisinstdir}/share/registry/schema/org/openoffice/UserProfile.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/VCL.xcs
%dir %{basisinstdir}/share/registry/schema/org/openoffice/ucb
%{basisinstdir}/share/registry/schema/org/openoffice/ucb/Configuration.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/ucb/Hierarchy.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/ucb/InteractionHandler.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/ucb/Store.xcs
%dir %{basisinstdir}/share/template
%{basisinstdir}/share/template/en-US
%{basisinstdir}/share/template/wizard
%{basisinstdir}/share/wordbook
%dir %{basisinstdir}/share/xslt
%{basisinstdir}/share/xslt/common
%dir %{basisinstdir}/share/xslt/export
%{basisinstdir}/share/xslt/export/common
%{basisinstdir}/share/xslt/export/spreadsheetml
%{basisinstdir}/share/xslt/export/wordml
%dir %{basisinstdir}/share/xslt/import
%{basisinstdir}/share/xslt/import/common
%{basisinstdir}/share/xslt/import/spreadsheetml
%{basisinstdir}/share/xslt/import/wordml
%{basisinstdir}/program/liblnth%{SOPOST}.so
%{_bindir}/unopkg
#icons and mime
%{_datadir}/icons/*/*/*/gnome*
%{_datadir}/icons/*/*/*/openoffice*
%{_datadir}/mime-info/openoffice.org.*
%{basisinstdir}/program/libxmlsecurity.so
%{_datadir}/mime/packages/openoffice.org.xml
%{basisinstdir}/program/behelper.uno.so
%{basisinstdir}/program/configmgr2.uno.so
%{basisinstdir}/program/desktopbe1.uno.so
%{basisinstdir}/program/fsstorage.uno.so
%{basisinstdir}/program/gconfbe1.uno.so
%{basisinstdir}/program/i18npool.uno.so
%{basisinstdir}/program/libbasegfx%{SOPOST}.so
%{basisinstdir}/program/libcomphelp4gcc3.so
%{basisinstdir}/program/libfileacc.so
%{basisinstdir}/program/libfwe%{SOPOST}.so
%{basisinstdir}/program/libfwi%{SOPOST}.so
%{basisinstdir}/program/libfwk%{SOPOST}.so
%{basisinstdir}/program/libfwl%{SOPOST}.so
%{basisinstdir}/program/libfwm%{SOPOST}.so
%{basisinstdir}/program/libgo%{SOPOST}.so
%{basisinstdir}/program/libi18nisolang*.so
%{basisinstdir}/program/libi18npaper*.so
%{basisinstdir}/program/libi18nutilgcc3.so
%{basisinstdir}/program/libpackage2.so
%{basisinstdir}/program/libsb%{SOPOST}.so
%{basisinstdir}/program/libsfx%{SOPOST}.so
%{basisinstdir}/program/libsot%{SOPOST}.so
%{basisinstdir}/program/libspl%{SOPOST}.so
%{basisinstdir}/program/libsvl%{SOPOST}.so
%{basisinstdir}/program/libsvt%{SOPOST}.so
%{basisinstdir}/program/libtk%{SOPOST}.so
%{basisinstdir}/program/libtl%{SOPOST}.so
%{basisinstdir}/program/libucb1.so
%{basisinstdir}/program/libucpfile1.so
%{basisinstdir}/program/libutl%{SOPOST}.so
%{basisinstdir}/program/libvcl%{SOPOST}.so
%{basisinstdir}/program/libvos3gcc3.so
%{basisinstdir}/program/libxcr%{SOPOST}.so
%{basisinstdir}/program/libxo%{SOPOST}.so
%{basisinstdir}/program/localebe1.uno.so
%{basisinstdir}/program/sysmgr1.uno.so
%{basisinstdir}/program/ucpgio1.uno.so
#vba
%{basisinstdir}/program/oovbaapi.rdb
#share unopkg
%dir %{oooinstdir}
%{oooinstdir}/basis-link
%dir %{oooinstdir}/share
%{oooinstdir}/share/uno_packages
%dir %{oooinstdir}/program
%{oooinstdir}/program/unopkg
%{oooinstdir}/program/unopkg.bin
%{oooinstdir}/program/bootstraprc
%{oooinstdir}/program/fundamentalrc
%{oooinstdir}/program/setuprc
%{oooinstdir}/program/versionrc

%post core
update-mime-database %{_datadir}/mime &> /dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  for theme in hicolor locolor; do
    if test -d "%{_datadir}/icons/$theme"; then
      if test -f "%{_datadir}/icons/$theme/index.theme"; then
        touch --no-create %{_datadir}/icons/$theme
        gtk-update-icon-cache -q %{_datadir}/icons/$theme
      fi
    fi
  done
fi

%postun core
update-mime-database %{_datadir}/mime &> /dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  for theme in hicolor locolor; do
    if test -d "%{_datadir}/icons/$theme"; then
      if test -f "%{_datadir}/icons/$theme/index.theme"; then
        touch --no-create %{_datadir}/icons/$theme
        gtk-update-icon-cache -q %{_datadir}/icons/$theme
      fi
    fi
  done
fi

%preun core
if [ $1 -eq 0 ]; then
    # not upgrading => remove component cache
    %{__rm} -rf %{baseinstdir}/share/uno_packages/cache/* || :
fi

%files brand
%dir %{oooinstdir}
%doc %{oooinstdir}/LICENSE
%doc %{oooinstdir}/LICENSE.html
%doc %{oooinstdir}/README
%doc %{oooinstdir}/README.html
%doc %{oooinstdir}/THIRDPARTYLICENSEREADME.html
%dir %{oooinstdir}/program
%{oooinstdir}/program/about.bmp
%{oooinstdir}/program/intro.bmp
%dir %{oooinstdir}/program/resource
%{oooinstdir}/program/resource/ooo%{UPD}en-US.res
%{oooinstdir}/program/soffice
%{oooinstdir}/program/soffice.bin
%{oooinstdir}/program/sofficerc
%{oooinstdir}/program/spadmin
%{oooinstdir}/program/unoinfo
%{oooinstdir}/program/libnpsoplugin.so
%dir %{oooinstdir}/share
%dir %{oooinstdir}/share/config
%{oooinstdir}/share/config/images_brand.zip
%docdir %{oooinstdir}/share/readme
%dir %{oooinstdir}/share/readme
%{oooinstdir}/share/readme/LICENSE_en-US
%{oooinstdir}/share/readme/LICENSE_en-US.html
%{oooinstdir}/share/readme/README_en-US
%{oooinstdir}/share/readme/README_en-US.html
%dir %{oooinstdir}/share/registry
%dir %{oooinstdir}/share/registry/data
%dir %{oooinstdir}/share/registry/data/org
%dir %{oooinstdir}/share/registry/data/org/openoffice
%dir %{oooinstdir}/share/registry/data/org/openoffice/Office
%{oooinstdir}/share/registry/data/org/openoffice/Office/Compatibility.xcu
%dir %{oooinstdir}/share/registry/modules
%dir %{oooinstdir}/share/registry/modules/org
%dir %{oooinstdir}/share/registry/modules/org/openoffice
%dir %{oooinstdir}/share/registry/modules/org/openoffice/Office
%dir %{oooinstdir}/share/registry/modules/org/openoffice/Office/Common
%{oooinstdir}/share/registry/modules/org/openoffice/Office/Common/Common-brand.xcu
%dir %{oooinstdir}/share/registry/modules/org/openoffice/Office/UI
%{oooinstdir}/share/registry/modules/org/openoffice/Office/UI/UI-brand.xcu
%dir %{oooinstdir}/share/registry/modules/org/openoffice/Setup
%{oooinstdir}/share/registry/modules/org/openoffice/Setup/Setup-brand.xcu
%{oooinstdir}/share/xdg/
%{oooinstdir}/program/redirectrc
#launchers
%{_bindir}/openoffice.org-1.9
%{_bindir}/openoffice.org-2.0
%{_bindir}/openoffice.org
%{_bindir}/soffice
%{_bindir}/ooffice
%{_bindir}/ooviewdoc

%post brand
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun brand
update-desktop-database %{_datadir}/applications &> /dev/null || :

%if %{langpacks}
%files -n broffice.org-brand
%dir %{brinstdir}
%doc %{brinstdir}/LICENSE
%doc %{brinstdir}/LICENSE.html
%doc %{brinstdir}/README
%doc %{brinstdir}/README.html
%doc %{brinstdir}/THIRDPARTYLICENSEREADME.html
%dir %{brinstdir}/program
%{brinstdir}/program/about.bmp
%{brinstdir}/program/bootstraprc
%{brinstdir}/program/setuprc
%{brinstdir}/program/intro.bmp
%dir %{brinstdir}/program/resource
%{brinstdir}/program/resource/ooo%{UPD}pt-BR.res
%{brinstdir}/program/soffice
%{brinstdir}/program/soffice.bin
%{brinstdir}/program/sofficerc
%{brinstdir}/program/spadmin
%{brinstdir}/program/unoinfo
%{brinstdir}/program/libnpsoplugin.so
%{brinstdir}/program/unopkg
%{brinstdir}/program/unopkg.bin
%{brinstdir}/program/versionrc
%dir %{brinstdir}/share
%dir %{brinstdir}/share/config
%{brinstdir}/share/config/images_brand.zip
%docdir %{brinstdir}/share/readme
%dir %{brinstdir}/share/readme
%{brinstdir}/share/readme/LICENSE_pt-BR
%{brinstdir}/share/readme/LICENSE_pt-BR.html
%{brinstdir}/share/readme/README_pt-BR
%{brinstdir}/share/readme/README_pt-BR.html
%dir %{brinstdir}/share/registry
%dir %{brinstdir}/share/registry/data
%dir %{brinstdir}/share/registry/data/org
%dir %{brinstdir}/share/registry/data/org/openoffice
%dir %{brinstdir}/share/registry/data/org/openoffice/Office
%{brinstdir}/share/registry/data/org/openoffice/Office/Compatibility.xcu
%dir %{brinstdir}/share/registry/modules
%dir %{brinstdir}/share/registry/modules/org
%dir %{brinstdir}/share/registry/modules/org/openoffice
%dir %{brinstdir}/share/registry/modules/org/openoffice/Office
%dir %{brinstdir}/share/registry/modules/org/openoffice/Office/Common
%{brinstdir}/share/registry/modules/org/openoffice/Office/Common/Common-brand.xcu
%dir %{brinstdir}/share/registry/modules/org/openoffice/Office/UI
%{brinstdir}/share/registry/modules/org/openoffice/Office/UI/UI-brand.xcu
%dir %{brinstdir}/share/registry/modules/org/openoffice/Setup
%{brinstdir}/share/registry/modules/org/openoffice/Setup/Setup-brand.xcu
%{brinstdir}/share/uno_packages
%{brinstdir}/share/xdg/
%{brinstdir}/program/fundamentalrc
%{brinstdir}/program/redirectrc
%{brinstdir}/basis-link
%{_datadir}/mime-info/broffice.org.*
%{_datadir}/icons/*/*/*/broffice*
#launchers
%{_bindir}/broffice.org
%endif

%post -n broffice.org-brand
update-desktop-database %{_datadir}/applications &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  for theme in hicolor locolor; do
    if test -d "%{_datadir}/icons/$theme"; then
      if test -f "%{_datadir}/icons/$theme/index.theme"; then
        touch --no-create %{_datadir}/icons/$theme
        gtk-update-icon-cache -q %{_datadir}/icons/$theme
      fi
    fi
  done
fi

%postun -n broffice.org-brand
update-desktop-database %{_datadir}/applications &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  for theme in hicolor locolor; do
    if test -d "%{_datadir}/icons/$theme"; then
      if test -f "%{_datadir}/icons/$theme/index.theme"; then
        touch --no-create %{_datadir}/icons/$theme
        gtk-update-icon-cache -q %{_datadir}/icons/$theme
      fi
    fi
  done
fi


%files base-core
%defattr(-,root,root,-)
%dir %{basisinstdir}
%{basisinstdir}/help/en/sdatabase.*
%dir %{basisinstdir}/program
%dir %{basisinstdir}/program/classes
%{basisinstdir}/program/classes/sdbc_hsqldb.jar
%{basisinstdir}/program/libabp%{SOPOST}.so
%{basisinstdir}/program/libadabasui%{SOPOST}.so
%{basisinstdir}/program/libdbp%{SOPOST}.so
%{basisinstdir}/program/libhsqldb.so
%{basisinstdir}/program/librpt*%{SOPOST}.so
%dir %{basisinstdir}/program/resource
%{basisinstdir}/program/resource/abp%{UPD}en-US.res
%{basisinstdir}/program/resource/adabasui%{UPD}en-US.res
%{basisinstdir}/program/resource/cnr%{UPD}en-US.res
%{basisinstdir}/program/resource/dbp%{UPD}en-US.res
%{basisinstdir}/program/resource/rpt%{UPD}en-US.res
%{basisinstdir}/program/resource/rptui%{UPD}en-US.res
%{basisinstdir}/program/resource/sdbcl%{UPD}en-US.res
%{basisinstdir}/program/resource/sdberr%{UPD}en-US.res
%dir %{basisinstdir}/share/registry
%dir %{basisinstdir}/share/registry/modules
%dir %{basisinstdir}/share/registry/modules/org
%dir %{basisinstdir}/share/registry/modules/org/openoffice
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office/Common
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Common/Common-base.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/Setup/Setup-base.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_database_filters.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Misc
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Misc/fcfg_database_others.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_database_types.xcu

%files base
%defattr(-,root,root,-)
%dir %{oooinstdir}
%dir %{oooinstdir}/program
%{oooinstdir}/program/sbase
%{_datadir}/applications/openoffice.org-base.desktop
%{_bindir}/oobase

%post base
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun base
update-desktop-database %{_datadir}/applications &> /dev/null || :

%if %{langpacks}
%files -n broffice.org-base
%defattr(-,root,root,-)
%dir %{brinstdir}
%dir %{brinstdir}/program
%{brinstdir}/program/sbase
%{_datadir}/applications/broffice.org-base.desktop
%endif

%post -n broffice.org-base
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun -n broffice.org-base
update-desktop-database %{_datadir}/applications &> /dev/null || :

%files report-builder
%defattr(-,root,root,-)
%docdir %{_datadir}/openoffice.org/extensions/sun-report-builder.oxt/help
%{_datadir}/openoffice.org/extensions/sun-report-builder.oxt

%pre report-builder
if [ $1 -gt 1 ]; then
    # Upgrade => deregister old extension
    unopkg remove --shared com.sun.reportdesigner > /dev/null 2>&1 || :
fi

%post report-builder
    # register extension
    unopkg add --shared --force --link %{_datadir}/openoffice.org/extensions/sun-report-builder.oxt > /dev/null 2>&1 || :

%preun report-builder
if [ $1 -eq 0 ]; then
    # not upgrading => deregister
    unopkg remove --shared com.sun.reportdesigner > /dev/null 2>&1 || :
fi

%postun report-builder
    # clear disk cache
    unopkg list --shared > /dev/null 2>&1 || :

%files bsh
%defattr(-,root,root,-)
%{basisinstdir}/share/Scripts/beanshell
%{_datadir}/openoffice.org/extensions/ScriptProviderForBeanShell.zip

%pre bsh
if [ $1 -gt 1 ]; then
    # Upgrade => deregister old extension
    unopkg remove --shared org.openoffice.legacy.ScriptProviderForBeanShell.zip > /dev/null 2>&1 || :
fi

%post bsh
    # register extension
    unopkg add --shared --force --link %{_datadir}/openoffice.org/extensions/ScriptProviderForBeanShell.zip > /dev/null 2>&1 || :

%preun bsh
if [ $1 -eq 0 ]; then
    # not upgrading => deregister
    unopkg remove --shared org.openoffice.legacy.ScriptProviderForBeanShell.zip > /dev/null 2>&1 || :
fi

%postun bsh
    # clear disk cache
    unopkg list --shared > /dev/null 2>&1 || :

%files rhino
%defattr(-,root,root,-)
%{basisinstdir}/program/classes/js.jar
%{basisinstdir}/share/Scripts/javascript
%{_datadir}/openoffice.org/extensions/ScriptProviderForJavaScript.zip

%pre rhino
if [ $1 -gt 1 ]; then
    # Upgrade => deregister old extension
    unopkg remove --shared org.openoffice.legacy.ScriptProviderForJavaScript.zip > /dev/null 2>&1 || :
fi

%post rhino
    # register extension
    unopkg add --shared --force --link %{_datadir}/openoffice.org/extensions/ScriptProviderForJavaScript.zip > /dev/null 2>&1 || :

%preun rhino
if [ $1 -eq 0 ]; then
    # not upgrading => deregister
    unopkg remove --shared org.openoffice.legacy.ScriptProviderForJavaScript.zip > /dev/null 2>&1 || :
fi

%postun rhino
    # clear disk cache
    unopkg list --shared > /dev/null 2>&1 || :

%files wiki-publisher
%defattr(-,root,root,-)
%docdir %{_datadir}/openoffice.org/extensions/wiki-publisher.oxt/license
%{_datadir}/openoffice.org/extensions/wiki-publisher.oxt

%pre wiki-publisher
if [ $1 -gt 1 ]; then
    # Upgrade => deregister old extension
    unopkg remove --shared com.sun.wiki-publisher > /dev/null 2>&1 || :
fi

%post wiki-publisher
    # register extension
    unopkg add --shared --force --link %{_datadir}/openoffice.org/extensions/wiki-publisher.oxt > /dev/null 2>&1 || :

%preun wiki-publisher
if [ $1 -eq 0 ]; then
    # not upgrading => deregister
    unopkg remove --shared com.sun.wiki-publisher > /dev/null 2>&1 || :
fi

%postun wiki-publisher
    # clear disk cache
    unopkg list --shared > /dev/null 2>&1 || :

%files ogltrans
%defattr(-,root,root,-)
%dir %{baseinstdir}
%dir %{basisinstdir}/program
%{basisinstdir}/program/OGLTrans.uno.so
%dir %{basisinstdir}/share/config
%dir %{basisinstdir}/share/config/soffice.cfg
%dir %{basisinstdir}/share/config/soffice.cfg/simpress
%{basisinstdir}/share/config/soffice.cfg/simpress/transitions-ogl.xml
%dir %{basisinstdir}/share/registry
%dir %{basisinstdir}/share/registry/modules
%dir %{basisinstdir}/share/registry/modules/org
%dir %{basisinstdir}/share/registry/modules/org/openoffice
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office/Impress
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Impress/Impress-ogltrans.xcu

%pre ogltrans
# deregister old extension if it is still there
unopkg remove --shared `grep -s identifier %{baseinstdir}/extensions/ogltrans.oxt/description.xml | cut -d '"' -f 2` > /dev/null 2>&1 || :

%files presentation-minimizer
%defattr(-,root,root,-)
%docdir %{baseinstdir}/extensions/sun-presentation-minimizer.oxt/help
%{baseinstdir}/extensions/sun-presentation-minimizer.oxt

%pre presentation-minimizer
if [ $1 -gt 1 ]; then
    # Upgrade => deregister old extension
    unopkg remove --shared `grep -s identifier %{baseinstdir}/extensions/sun-presentation-minimizer.oxt/description.xml | cut -d '"' -f 2` > /dev/null 2>&1 || :
fi

%post presentation-minimizer
    # register extension
    unopkg add --shared --force --link %{baseinstdir}/extensions/sun-presentation-minimizer.oxt > /dev/null 2>&1 || :

%preun presentation-minimizer
if [ $1 -eq 0 ]; then
    # not upgrading => deregister
    unopkg remove --shared `grep -s identifier %{baseinstdir}/extensions/sun-presentation-minimizer.oxt/description.xml | cut -d '"' -f 2` > /dev/null 2>&1 || :
fi

%postun presentation-minimizer
    # clear disk cache
    unopkg list --shared > /dev/null 2>&1 || :

%files presenter-screen
%defattr(-,root,root,-)
%docdir %{baseinstdir}/extensions/presenter-screen.oxt/help
%{baseinstdir}/extensions/presenter-screen.oxt

%pre presenter-screen
if [ $1 -gt 1 ]; then
    # Upgrade => deregister old extension
    unopkg remove --shared `grep -s identifier %{baseinstdir}/extensions/presenter-screen.oxt/description.xml | cut -d '"' -f 2` > /dev/null 2>&1 || :
fi

%post presenter-screen
    # register extension
    unopkg add --shared --force --link %{baseinstdir}/extensions/presenter-screen.oxt > /dev/null 2>&1 || :

%preun presenter-screen
if [ $1 -eq 0 ]; then
    # not upgrading => deregister
    unopkg remove --shared `grep -s identifier %{baseinstdir}/extensions/presenter-screen.oxt/description.xml | cut -d '"' -f 2` > /dev/null 2>&1 || :
fi

%postun presenter-screen
    # clear disk cache
    unopkg list --shared > /dev/null 2>&1 || :

%files pdfimport
%defattr(-,root,root,-)
%docdir %{baseinstdir}/extensions/pdfimport.oxt/help
%{baseinstdir}/extensions/pdfimport.oxt

%pre pdfimport
if [ $1 -gt 1 ]; then
    # Upgrade => deregister old extension
    unopkg remove --shared `grep -s identifier %{baseinstdir}/extensions/pdfimport.oxt/description.xml | cut -d '"' -f 2` > /dev/null 2>&1 || :
fi

%post pdfimport
    # register extension
    unopkg add --shared --force --link %{baseinstdir}/extensions/pdfimport.oxt > /dev/null 2>&1 || :

%preun pdfimport
if [ $1 -eq 0 ]; then
    # not upgrading => deregister
    unopkg remove --shared `grep -s identifier %{baseinstdir}/extensions/pdfimport.oxt/description.xml | cut -d '"' -f 2` > /dev/null 2>&1 || :
fi

%postun pdfimport
    # clear disk cache
    unopkg list --shared > /dev/null 2>&1 || :

%_font_pkg -n %{fontname} opens___.ttf
%dir %{_fontdir}

%files calc-core
%defattr(-,root,root,-)
%dir %{basisinstdir}
%{basisinstdir}/help/en/scalc.*
%dir %{basisinstdir}/program
%{basisinstdir}/program/libanalysis%{SOPOST}.so
%{basisinstdir}/program/libbf_sc%{SOPOST}.so
%{basisinstdir}/program/libcalc%{SOPOST}.so
%{basisinstdir}/program/libdate%{SOPOST}.so
%{basisinstdir}/program/libfor%{SOPOST}.so
%{basisinstdir}/program/libforui%{SOPOST}.so
%{basisinstdir}/program/libsc%{SOPOST}.so
%{basisinstdir}/program/libscd%{SOPOST}.so
%{basisinstdir}/program/libscfilt%{SOPOST}.so
%{basisinstdir}/program/libscui%{SOPOST}.so
%{basisinstdir}/program/libsolver%{SOPOST}.so
%dir %{basisinstdir}/program/resource
%{basisinstdir}/program/resource/analysis%{UPD}en-US.res
%{basisinstdir}/program/resource/bf_sc%{UPD}en-US.res
%{basisinstdir}/program/resource/date%{UPD}en-US.res
%{basisinstdir}/program/resource/for%{UPD}en-US.res
%{basisinstdir}/program/resource/forui%{UPD}en-US.res
%{basisinstdir}/program/resource/sc%{UPD}en-US.res
%{basisinstdir}/program/resource/solver%{UPD}en-US.res
%dir %{basisinstdir}/share/registry
%dir %{basisinstdir}/share/registry/data
%dir %{basisinstdir}/share/registry/data/org
%dir %{basisinstdir}/share/registry/data/org/openoffice
%dir %{basisinstdir}/share/registry/data/org/openoffice/Office
%dir %{basisinstdir}/share/registry/data/org/openoffice/Office/UI
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/CalcCommands.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/CalcWindowState.xcu
%dir %{basisinstdir}/share/registry/modules
%dir %{basisinstdir}/share/registry/modules/org
%dir %{basisinstdir}/share/registry/modules/org/openoffice
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office/Common
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Common/Common-calc.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/Setup/Setup-calc.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_calc_filters.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_calc_bf_filters.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_calc_types.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_calc_bf_types.xcu
%dir %{basisinstdir}/share/registry/schema
%dir %{basisinstdir}/share/registry/schema/org
%dir %{basisinstdir}/share/registry/schema/org/openoffice
%dir %{basisinstdir}/share/registry/schema/org/openoffice/Office
%dir %{basisinstdir}/share/registry/schema/org/openoffice/Office/UI
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/CalcCommands.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/CalcWindowState.xcs
#vba
%{basisinstdir}/program/libvbaobj%{SOPOST}.uno.so

%files calc
%defattr(-,root,root,-)
%dir %{oooinstdir}
%dir %{oooinstdir}/program
%{oooinstdir}/program/scalc
%{oooinstdir}/program/scalc.bin
%{_datadir}/applications/openoffice.org-calc.desktop
%{_bindir}/oocalc

%post calc
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun calc
update-desktop-database %{_datadir}/applications &> /dev/null || :

%if %{langpacks}
%files -n broffice.org-calc
%defattr(-,root,root,-)
%dir %{brinstdir}
%dir %{brinstdir}/program
%{brinstdir}/program/scalc
%{brinstdir}/program/scalc.bin
%{_datadir}/applications/broffice.org-calc.desktop
%endif

%post -n broffice.org-calc
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun -n broffice.org-calc
update-desktop-database %{_datadir}/applications &> /dev/null || :

%files draw-core
%defattr(-,root,root,-)
%dir %{basisinstdir}
%{basisinstdir}/help/en/sdraw.*
%dir %{basisinstdir}/share/registry
%dir %{basisinstdir}/share/registry/data
%dir %dir %{basisinstdir}/share/registry/data/org
%dir %{basisinstdir}/share/registry/data/org/openoffice
%dir %{basisinstdir}/share/registry/data/org/openoffice/Office
%dir %{basisinstdir}/share/registry/data/org/openoffice/Office/UI
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/DrawWindowState.xcu
%dir %{basisinstdir}/share/registry/modules
%dir %{basisinstdir}/share/registry/modules/org
%dir %{basisinstdir}/share/registry/modules/org/openoffice
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office/Common
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Common/Common-draw.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/Setup/Setup-draw.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_draw_filters.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_draw_bf_filters.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_draw_types.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_draw_bf_types.xcu
%dir %{basisinstdir}/share/registry/schema
%dir %{basisinstdir}/share/registry/schema/org
%dir %{basisinstdir}/share/registry/schema/org/openoffice
%dir %{basisinstdir}/share/registry/schema/org/openoffice/Office
%dir %{basisinstdir}/share/registry/schema/org/openoffice/Office/UI
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/DrawWindowState.xcs

%files draw
%defattr(-,root,root,-)
%dir %{oooinstdir}
%dir %{oooinstdir}/program
%{oooinstdir}/program/sdraw
%{oooinstdir}/program/sdraw.bin
%{_datadir}/applications/openoffice.org-draw.desktop
%{_bindir}/oodraw

%post draw
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun draw
update-desktop-database %{_datadir}/applications &> /dev/null || :

%if %{langpacks}
%files -n broffice.org-draw
%defattr(-,root,root,-)
%dir %{brinstdir}
%dir %{brinstdir}/program
%{brinstdir}/program/sdraw
%{brinstdir}/program/sdraw.bin
%{_datadir}/applications/broffice.org-draw.desktop
%endif

%post -n broffice.org-draw
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun -n broffice.org-draw
update-desktop-database %{_datadir}/applications &> /dev/null || :

%files emailmerge
%defattr(-,root,root,-)
%dir %{basisinstdir}
%dir %{basisinstdir}/program
%{basisinstdir}/program/mailmerge.py*
%dir %{basisinstdir}/share/registry
%dir %{basisinstdir}/share/registry/modules
%dir %{basisinstdir}/share/registry/modules/org
%dir %{basisinstdir}/share/registry/modules/org/openoffice
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office/Writer
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Writer/Writer-javamail.xcu

%files writer-core
%defattr(-,root,root,-)
%dir %{basisinstdir}
%{basisinstdir}/help/en/swriter.*
%dir %{basisinstdir}/program
%{basisinstdir}/program/libbf_sw%{SOPOST}.so
%{basisinstdir}/program/libhwp.so
%{basisinstdir}/program/libmsword%{SOPOST}.so
%{basisinstdir}/program/libswd%{SOPOST}.so
%{basisinstdir}/program/libswui%{SOPOST}.so
%{basisinstdir}/program/libt602filter%{SOPOST}.so
%{basisinstdir}/program/libwpft%{SOPOST}.so
%{basisinstdir}/program/libwriterfilter%{SOPOST}.so
%dir %{basisinstdir}/program/resource
%{basisinstdir}/program/resource/bf_sw%{UPD}en-US.res
%{basisinstdir}/program/resource/t602filter%{UPD}en-US.res
%dir %{basisinstdir}/share/registry
%dir %{basisinstdir}/share/registry/data
%dir %{basisinstdir}/share/registry/data/org
%dir %{basisinstdir}/share/registry/data/org/openoffice
%dir %{basisinstdir}/share/registry/data/org/openoffice/Office
%dir %{basisinstdir}/share/registry/data/org/openoffice/Office/UI
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/WriterCommands.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/WriterFormWindowState.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/WriterGlobalWindowState.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/WriterReportWindowState.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/WriterWebWindowState.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/WriterWindowState.xcu
%dir %{basisinstdir}/share/registry/modules
%dir %{basisinstdir}/share/registry/modules/org
%dir %{basisinstdir}/share/registry/modules/org/openoffice
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office/Common
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Common/Common-writer.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/Setup/Setup-writer.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_global_filters.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_global_bf_filters.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_web_filters.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_web_bf_filters.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_writer_filters.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_writer_bf_filters.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_global_types.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_global_bf_types.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_web_types.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_writer_types.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_web_bf_types.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_writer_bf_types.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office/Writer
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Writer/TableNumberRecognition.xcu
%dir %{basisinstdir}/share/registry/schema
%dir %{basisinstdir}/share/registry/schema/org
%dir %{basisinstdir}/share/registry/schema/org/openoffice
%dir %{basisinstdir}/share/registry/schema/org/openoffice/Office
%dir %{basisinstdir}/share/registry/schema/org/openoffice/Office/UI
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/WriterCommands.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/WriterFormWindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/WriterGlobalWindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/WriterReportWindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/WriterWebWindowState.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/WriterWindowState.xcs

%files writer
%defattr(-,root,root,-)
%dir %{oooinstdir}
%dir %{oooinstdir}/program
%{oooinstdir}/program/swriter
%{oooinstdir}/program/swriter.bin
%{_datadir}/applications/openoffice.org-writer.desktop
%{_bindir}/oowriter

%post writer
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun writer
update-desktop-database %{_datadir}/applications &> /dev/null || :

%if %{langpacks}
%files -n broffice.org-writer
%defattr(-,root,root,-)
%{brinstdir}/program/swriter
%{brinstdir}/program/swriter.bin
%{_datadir}/applications/broffice.org-writer.desktop
%endif

%post -n broffice.org-writer
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun -n broffice.org-writer
update-desktop-database %{_datadir}/applications &> /dev/null || :

%files impress-core
%defattr(-,root,root,-)
%dir %{basisinstdir}
%{basisinstdir}/help/en/simpress.*
%dir %{basisinstdir}/program
%{basisinstdir}/program/libanimcore.so
%{basisinstdir}/program/libplaceware*.so
%dir %{basisinstdir}/share/config
%dir %{basisinstdir}/share/config/soffice.cfg
%dir %{basisinstdir}/share/config/soffice.cfg/simpress
%{basisinstdir}/share/config/soffice.cfg/simpress/effects.xml
%{basisinstdir}/share/config/soffice.cfg/simpress/transitions.xml
%dir %{basisinstdir}/share/registry
%dir %{basisinstdir}/share/registry/data
%dir %{basisinstdir}/share/registry/data/org
%dir %{basisinstdir}/share/registry/data/org/openoffice
%dir %{basisinstdir}/share/registry/data/org/openoffice/Office
%dir %{basisinstdir}/share/registry/data/org/openoffice/Office/UI
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/Effects.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/ImpressWindowState.xcu
%dir %{basisinstdir}/share/registry/modules
%dir %{basisinstdir}/share/registry/modules/org
%dir %{basisinstdir}/share/registry/modules/org/openoffice
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office/Common
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Common/Common-impress.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/Setup/Setup-impress.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_impress_filters.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_impress_bf_filters.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_impress_types.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_impress_bf_types.xcu
%dir %{basisinstdir}/share/registry/schema
%dir %{basisinstdir}/share/registry/schema/org
%dir %{basisinstdir}/share/registry/schema/org/openoffice
%dir %{basisinstdir}/share/registry/schema/org/openoffice/Office
%dir %{basisinstdir}/share/registry/schema/org/openoffice/Office/UI
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/Effects.xcs
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/ImpressWindowState.xcs

%files impress
%defattr(-,root,root,-)
%dir %{oooinstdir}
%dir %{oooinstdir}/program
%{oooinstdir}/program/simpress
%{oooinstdir}/program/simpress.bin
%{_datadir}/applications/openoffice.org-impress.desktop
%{_bindir}/ooimpress

%post impress
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun impress
update-desktop-database %{_datadir}/applications &> /dev/null || :

%if %{langpacks}
%files -n broffice.org-impress
%defattr(-,root,root,-)
%dir %{brinstdir}
%dir %{brinstdir}/program
%{brinstdir}/program/simpress
%{brinstdir}/program/simpress.bin
%{_datadir}/applications/broffice.org-impress.desktop
%endif

%post -n broffice.org-impress
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun -n broffice.org-impress
update-desktop-database %{_datadir}/applications &> /dev/null || :

%files math-core
%defattr(-,root,root,-)
%dir %{basisinstdir}
%{basisinstdir}/help/en/smath.*
%dir %{basisinstdir}/program
%{basisinstdir}/program/libbf_sm%{SOPOST}.so
%{basisinstdir}/program/libsm%{SOPOST}.so
%{basisinstdir}/program/libsmd%{SOPOST}.so
%dir %{basisinstdir}/program/resource
%{basisinstdir}/program/resource/bf_sm%{UPD}en-US.res
%{basisinstdir}/program/resource/sm%{UPD}en-US.res
%dir %{basisinstdir}/share/registry
%dir %{basisinstdir}/share/registry/data
%dir %{basisinstdir}/share/registry/data/org
%dir %{basisinstdir}/share/registry/data/org/openoffice
%dir %{basisinstdir}/share/registry/data/org/openoffice/Office
%dir %{basisinstdir}/share/registry/data/org/openoffice/Office/UI
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/MathCommands.xcu
%{basisinstdir}/share/registry/data/org/openoffice/Office/UI/MathWindowState.xcu
%dir %{basisinstdir}/share/registry/modules
%dir %{basisinstdir}/share/registry/modules/org
%dir %{basisinstdir}/share/registry/modules/org/openoffice
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office/Common
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Common/Common-math.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office/Math
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Math/MathPrintOptions.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/Setup/Setup-math.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_math_filters.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_math_bf_filters.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_math_types.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_math_bf_types.xcu
%dir %{basisinstdir}/share/registry/schema
%dir %{basisinstdir}/share/registry/schema/org
%dir %{basisinstdir}/share/registry/schema/org/openoffice
%dir %{basisinstdir}/share/registry/schema/org/openoffice/Office
%dir %{basisinstdir}/share/registry/schema/org/openoffice/Office/UI
%{basisinstdir}/share/registry/schema/org/openoffice/Office/UI/MathCommands.xcs

%files math
%defattr(-,root,root,-)
%dir %{oooinstdir}
%dir %{oooinstdir}/program
%{oooinstdir}/program/smath
%{_datadir}/applications/openoffice.org-math.desktop
%{_bindir}/oomath

%post math
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun math
update-desktop-database %{_datadir}/applications &> /dev/null || :

%if %{langpacks}
%files -n broffice.org-math
%defattr(-,root,root,-)
%dir %{brinstdir}
%dir %{brinstdir}/program
%{brinstdir}/program/smath
%{_datadir}/applications/broffice.org-math.desktop
%endif

%post -n broffice.org-math
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun -n broffice.org-math
update-desktop-database %{_datadir}/applications &> /dev/null || :

%files graphicfilter
%defattr(-,root,root,-)
%dir %{basisinstdir}
%dir %{basisinstdir}/program
%{basisinstdir}/program/libflash%{SOPOST}.so
%{basisinstdir}/program/libsvgfilter%{SOPOST}.so
%dir %{basisinstdir}/share/registry
%dir %{basisinstdir}/share/registry/modules
%dir %{basisinstdir}/share/registry/modules/org
%dir %{basisinstdir}/share/registry/modules/org/openoffice
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_drawgraphics_filters.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_impressgraphics_filters.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_drawgraphics_types.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_impressgraphics_types.xcu

%files xsltfilter
%defattr(-,root,root,-)
%dir %{basisinstdir}
%dir %{basisinstdir}/share/registry
%dir %{basisinstdir}/share/registry/modules
%dir %{basisinstdir}/share/registry/modules/org
%dir %{basisinstdir}/share/registry/modules/org/openoffice
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_xslt_filters.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_xslt_types.xcu
%dir %{basisinstdir}/share/xslt
%{basisinstdir}/share/xslt/docbook
%dir %{basisinstdir}/share/xslt/export
%{basisinstdir}/share/xslt/export/uof
%{basisinstdir}/share/xslt/export/xhtml
%dir %{basisinstdir}/share/xslt/import
%{basisinstdir}/share/xslt/import/uof

%files javafilter
%defattr(-,root,root,-)
%dir %{basisinstdir}
%dir %{basisinstdir}/program
%dir %{basisinstdir}/program/classes
%{basisinstdir}/program/classes/aportisdoc.jar
%{basisinstdir}/program/classes/pexcel.jar
%{basisinstdir}/program/classes/pocketword.jar
%dir %{basisinstdir}/share/registry
%dir %{basisinstdir}/share/registry/modules
%dir %{basisinstdir}/share/registry/modules/org
%dir %{basisinstdir}/share/registry/modules/org/openoffice
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_palm_filters.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_pocketexcel_filters.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Filter/fcfg_pocketword_filters.xcu
%dir %{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_palm_types.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_pocketexcel_types.xcu
%{basisinstdir}/share/registry/modules/org/openoffice/TypeDetection/Types/fcfg_pocketword_types.xcu
%{_datadir}/applications/openoffice.org-javafilter.desktop

%files testtools
%defattr(-,root,root,-)
%dir %{basisinstdir}
%dir %{basisinstdir}/program
%{basisinstdir}/program/hid.lst
%{basisinstdir}/program/libcommuni%{SOPOST}.so
%{ureinstdir}/lib/libsalalloc_malloc.so.3
%{basisinstdir}/program/libsimplecm%{SOPOST}.so
%{basisinstdir}/program/testtoolrc
%{basisinstdir}/program/testtool.bin
%dir %{basisinstdir}/program/resource
%{basisinstdir}/program/resource/stt%{UPD}en-US.res

%files ure
%defattr(-,root,root,-)
%dir %{baseinstdir}
%{ureinstdir}
%exclude %{ureinstdir}/lib/libsalalloc_malloc.so.3

%files sdk
%defattr(-,root,root,-)
%{sdkinstdir}/
%exclude %{sdkinstdir}/setdevelenv_unix.sh
%exclude %{sdkinstdir}/docs/
%exclude %{sdkinstdir}/examples/
%exclude %{sdkinstdir}/include/tools
%exclude %{sdkinstdir}/include/comphelper
%exclude %{sdkinstdir}/include/i18npool
%exclude %{sdkinstdir}/include/vos
%exclude %{sdkinstdir}/solenv
%exclude %{sdkinstdir}/bin/checkdll

%files sdk-doc
%defattr(-,root,root,-)
%docdir %{sdkinstdir}/docs
%{sdkinstdir}/docs/
%{sdkinstdir}/examples/

%files devel
%defattr(-,root,root,-)
%{sdkinstdir}/setdevelenv_unix.sh
%{sdkinstdir}/include/tools
%{sdkinstdir}/include/comphelper
%{sdkinstdir}/include/i18npool
%{sdkinstdir}/include/vos
%{sdkinstdir}/solenv
%{sdkinstdir}/bin/checkdll

%files headless
%defattr(-,root,root,-)
%dir %{basisinstdir}
%dir %{basisinstdir}/program
%{basisinstdir}/program/libbasebmp%{SOPOST}.so
%{basisinstdir}/program/libvclplug_svp%{SOPOST}.so

%files pyuno
%defattr(-,root,root,-)
%dir %{basisinstdir}
%dir %{basisinstdir}/program
%{basisinstdir}/program/libpyuno.so
%{basisinstdir}/program/officehelper.py*
%{basisinstdir}/program/pythonloader.py*
%{basisinstdir}/program/pythonloader.uno.so
%{basisinstdir}/program/pythonloader.unorc
%{basisinstdir}/program/pyuno.so
%dir %{basisinstdir}/share/Scripts
%{basisinstdir}/share/Scripts/python
%dir %{basisinstdir}/share/registry
%dir %{basisinstdir}/share/registry/modules
%dir %{basisinstdir}/share/registry/modules/org
%dir %{basisinstdir}/share/registry/modules/org/openoffice
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office
%dir %{basisinstdir}/share/registry/modules/org/openoffice/Office/Scripting
%{basisinstdir}/share/registry/modules/org/openoffice/Office/Scripting/Scripting-python.xcu
%{python_sitearch}/uno.py*
%{python_sitearch}/unohelper.py*
%{_datadir}/openoffice.org/extensions/ScriptProviderForPython.zip

%pre pyuno
if [ $1 -gt 1 ]; then
    # Upgrade => deregister old extension
    unopkg remove --shared org.openoffice.legacy.ScriptProviderForPython.zip > /dev/null 2>&1 || :
fi

%post pyuno
    # register extension
    unopkg add --shared --force --link %{_datadir}/openoffice.org/extensions/ScriptProviderForPython.zip > /dev/null 2>&1 || :

%preun pyuno
if [ $1 -eq 0 ]; then
    # not upgrading => deregister
    unopkg remove --shared org.openoffice.legacy.ScriptProviderForPython.zip > /dev/null 2>&1 || :
fi

%postun pyuno
    # clear disk cache
    unopkg list --shared > /dev/null 2>&1 || :

%files -n autocorr-en
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_en-*

%if %{langpacks}

%files -n autocorr-af
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_af-*

%files -n autocorr-bg
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_bg-*

%files -n autocorr-cs
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_cs-*

%files -n autocorr-da
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_da-*

%files -n autocorr-de
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_de-*

%files -n autocorr-es
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_es-*

%files -n autocorr-eu
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_eu.dat

%files -n autocorr-fa
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_fa-*

%files -n autocorr-fi
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_fi-*

%files -n autocorr-fr
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_fr-*

%files -n autocorr-ga
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_ga-*

%files -n autocorr-hu
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_hu-*

%files -n autocorr-it
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_it-*

%files -n autocorr-ja
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_ja-*

%files -n autocorr-ko
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_ko-*

%files -n autocorr-lb
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_lb-*

%files -n autocorr-lt
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_lt-*

%files -n autocorr-nl
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_nl-*

%files -n autocorr-mn
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_mn-*

%files -n autocorr-pl
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_pl-*

%files -n autocorr-pt
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_pt-*

%files -n autocorr-ru
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_ru-*

%files -n autocorr-sk
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_sk-*

%files -n autocorr-sl
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_sl-*

%files -n autocorr-sv
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_sv-*

%files -n autocorr-tr
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_tr-*

%files -n autocorr-vi
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_vi-*

%files -n autocorr-zh
%dir %{_datadir}/autocorr
%{_datadir}/autocorr/acor_zh-*

%endif

%changelog
* Thu Feb 25 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-12.8
- Resolves: rhbz#568335 silence a11y warning (caolanm)

* Fri Feb 19 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-12.7
- Resolves: rhbz#564133 [abrt] crash in pdfi::(anonymous
  namespace)::Parser::parseLine (dtardon)
- Resolves: rhbz#566716 It is not possible to redefine default
  separator while doing CSV import (dtardon)
- add openoffice.org-3.2.0.ooo108991.redlandfixes.patch (caolanm)

* Wed Feb 16 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-12.6
- Resolves: rhbz#565519 add openoffice.org-3.2.0.ooo95369.sw.sortedobjs.patch
- Resolves: rhbz#565906 don't crash on bad .svg in add to gallery

* Mon Feb 15 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-12.5
- Resolves: rhbz#565330 abrt in ImplGetGraphics
- Resolves: rhbz#558491 make "yes to all" affect all bgs

* Tue Feb 09 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-12.4
- Resolves: rhbz#445588 improve same name substitution
- backport workspace.x86_64_bridgefix.patch

* Sat Feb 06 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-12.3
- Resolves: rhbz#561989 openoffice.org-3.2.0.ooo109009.sc.tooltipcrash.patch

* Wed Feb 03 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-12.2
- improve pyuno multilib
- Resolves: rhbz#561778 openoffice.org-3.2.0.oooXXXXX.svx.safestyledelete.patch

* Tue Feb 02 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-12.1
- latest milestone
- Resolves: rhbz#560996/rhbz#560353 qstartfixes (caolanm)
- drop integrated openoffice.org-3.2.0.ooo107763.transcrash.patch

* Fri Jan 29 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-11.2
- Resolves: ooo#107763 transparent object crash in impress

* Mon Jan 25 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-11.1
- latest milestone
- Resolves: ooo#108637/rhbz#558253 sfx2 uisavedir

* Mon Jan 18 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-10.2
- improve s390x uno bridge

* Sat Jan 16 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-10.1
- latest milestone

* Thu Jan 14 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-9.5
- Resolves: rbhz#555257 openoffice cannot use JPEG images using CMYK
  colorspace (dtardon)

* Thu Jan 14 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-9.4
- Resolves: rhbz#550043 dispatch outplace objects as ro documents to OS (caolanm)

* Wed Jan 13 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-9.3
- Resolves: rhbz#553929 [abrt] crash in ColorConfigCtrl_Impl::ScrollHdl
  (dtardon)
- Resolves: rhbz#549573 improve document compare (caolanm)

* Mon Jan 11 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-9.2
- Resolves: rhbz#554259 No autocorrect files for Lithuanian (dtardon)
- drop integrated workspace.impress184.patch (caolanm)

* Sun Jan 10 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-9.1
- latest milestone

* Mon Jan 04 2010 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-8.6
- Resolves: rhbz#551983 OpenOffice writer crashes when opening document
  with link in footnote (dtardon)

* Sun Jan 03 2010 Rex Dieter <rdieter@fedoraproject.org> - 1:3.2.0-8.5
- rebuild (rasqal/redland)

* Thu Dec 24 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-8.4
- Resolves: rhbz#489489 enable Romanian translations

* Wed Dec 23 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-8.3
- python bits should be site-arch

* Tue Dec 22 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-8.2
- Resolves: rhbz#545824 bustage in writer with emboldened fonts

* Thu Dec 17 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-8.1
- latest milestone
- drop integrated openoffice.org-3.1.0.ooo90439.sfx2.qstart.hackaround.patch
- drop integrated workspace.fwk132.patch
- drop unnecessary openoffice.org-2.4.0.rh133741.alwaysgtk.vcl.patch
- drop integrated openoffice.org-3.2.0.ooo105988.svx.a11ycrash.patch
- drop integrated openoffice.org-3.2.0.ooo107151.sc.pop-empty-cell.patch

* Tue Dec 15 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-7.3
- Resolves: rhbz#529648 add workspace.fwk132.patch
- Resolves: rhbz#547176 add
  openoffice.org-3.2.0.ooo47279.sd.objectsave.safe.patch

* Wed Dec 09 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-7.2
- Resolves: rhbz#544124 add openoffice.org-3.2.0.ooo106502.svx.fixspelltimer.patch
- Resolves: rhbz#544218 add openoffice.org-3.2.0.ooo107552.vcl.sft.patch

* Thu Dec 03 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-7.1
- latest milestone

* Thu Dec 03 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-6.4
- Resolves: rhbz#543934 drop "kid" pseudo-translations

* Tue Dec 01 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-6.3
- add workspace.pythonssldedux.patch to get CRAM-MD5 working from
  emailmerge

* Fri Nov 27 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-6.2
- Resolves: rhbz#541222 add 
  openoffice.org-3.2.0.ooo107260.vcl.clipboard.shutdown.patch (caolanm)

* Thu Nov 26 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-6.1
- next version
- stick fixups upstream (caolanm)
- add openoffice.org-3.2.0.ooo107151.sc.pop-empty-cell.patch (dtardon)
- Resolves: rhbz#533538 OpenOffice keyboard shortcuts mis-map in the
  Spanish localized version of OOo (caolanm)
- drop post-translations 
  openoffice.org-3.2.0.rhbz521460.svx.revert-paper-sizes-reordering.patch
  (caolanm)
- drop integrated openoffice.org-3.1.0.ooo100273.fix-utf8-hyphenation.patch
  (caolanm)
- drop integrated workspace.fwk125.patch (caolanm)
- drop integrated workspace.impress183.patch (caolanm)

* Mon Nov 23 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-5.2
- Resolves: rhbz#540379/ooo#107131 impress tabledrag crash
- Resolves: rhbz#540231 add openoffice.org-3.2.0.ooo107137.canvas.fixcolorspace.patch

* Thu Nov 19 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-5.1
- next version

* Fri Nov 13 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-4.3
- add openoffice.org-3.2.0.ooo59648.sw.scaling.patch (caolanm)
- Resolves: rhbz#537166 add a version require on hyphen (caolanm)
- Resolves: ooo#101158 parallel build breakage in xmlhelp (caolanm)

* Tue Nov 10 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-4.2
- Resolves: rhbz#533841 ooo#105710 svx loadstorenumbering (caolanm)

* Fri Nov 06 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-4.1
- next milestone
- Resolves: ooo#106523 fix pdf/A export on x86_64 (caolanm)
- drop integrated workspace.impress180.patch
- drop integrated openoffice.org-3.2.0.ooo106596.ww8.exportcrash.patch

* Thu Nov 05 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-3.4
- Resolves: rhbz#533146 calc notes go missing on save (caolanm)

* Wed Nov 04 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-3.3
- Resolves: ooo#106596 ww8 crash on export (caolanm)

* Tue Nov 03 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-3.2
- Resolves: ooo#106497 language marked as providing spellchecking when
  unavailable (caolanm)
- Resolves: rhbz#532330 openoffice impress doesn't recognise .ogv
  files as video (dtardon)

* Fri Oct 30 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-3.1
- Resolves: rhbz#531732 crash in about dialog with unfinished
  accelerator sequence
- drop integrated workspace.impress178.patch
- next milestone

* Wed Oct 28 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-2.5
- Resolves: ooo#103757 custom shape cut and paste (caolanm)
- Resolves: rhbz#529746 crash on exit after loading .ppt (caolanm)
- add workspace.gsminhibit.patch for new g-s-m api-de-jour inhibit (caolanm)

* Mon Oct 19 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-2.4
- Resolves: rhbz#521460 add openoffice.org-3.2.0.ooo106032.linguistic.defaulttoplain.patch (caolanm)
- Related:  rhbz#529521 add openoffice.org-3.2.0.oooXXXXXX.vcl.dontresolve.patch (caolanm)

* Mon Oct 19 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-2.3
- Resolves: rhbz#521460 - wrong page size for A3/A5 (dtardon)

* Sat Oct 17 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-2.2
- Resolves: ooo#105988 a11y crash in impress (caolanm)

* Thu Oct 15 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-2.1
- Resolves: rhbz#529127 [Indic][Various] Default font in oowriter is
  not Language Default (Lohit or Other), but DejaVu Sans (dtardon)
- drop integrated workspace.dba32h.patch (caolanm)

* Wed Oct 14 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-1.2
- don't link against dtrans, not needed anymore (caolanm)

* Tue Oct 13 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.2.0-1.1
- drop integrated autocorrection files (i102567)
- drop integrated workspace.defaultdoclang.patch
- drop integrated workspace.kso32fixes.patch
- drop integrated workspace.sb113.patch
- drop integrated workspace.impress170.patch
- drop integrated workspace.tl66.patch
- drop integrated workspace.mhu17.patch
- drop integrated openoffice.org-3.0.0.ooo95018.sal.fdwarnings.patch
- drop integrated workspace.gtkmenuimages.patch
- drop integrated workspace.calc50.patch
- drop integrated workspace.mav46.patch
- drop integrated workspace.transogl03redux.patch
- drop integrated workspace.cmcfixes63.patch
- drop integrated workspace.cmcfixes54.patch
- drop integrated workspace.fwk103.patch
- drop integrated workspace.hb18.patch
- drop integrated workspace.vcl100.patch
- drop integrated workspace.xmergeclean.patch
- drop integrated workspace.mba32issues02.patch
- drop integrated workspace.impress169.patch
- drop integrated workspace.os130.patch
- drop integrated workspace.cmcfixes57.patch
- drop integrated workspace.hb32bugs01.patch
- drop integrated workspace.vcl101.patch
- drop integrated workspace.impress171.patch
- drop integrated workspace.vcl104.patch
- drop integrated workspace.evoab2def.patch
- drop integrated workspace.cmcfixes59.patch
- drop integrated workspace.impress174.patch
- drop integrated workspace.unifypaper01.patch
- drop integrated workspace.calc51.patch
- drop integrated workspace.locales32.patch
- drop integrated workspace.cmcfixes60.patch
- drop integrated workspace.dr72.patch
- drop integrated workspace.vcl103.patch
- drop integrated workspace.cmcfixes61.patch
- drop integrated workspace.os132.patch
- drop integrated workspace.cmcfixes62.patch
- drop integrated workspace.os131.patch
- drop integrated workspace.vcl102.patch
- drop integrated workspace.dr69.patch
- drop integrated workspace.aw073.patch
- drop integrated openoffice.org-3.1.0.oooXXXXX.gcc44.buildfixes.patch
- drop integrated openoffice.org-3.1.0.ooo99541.sw.reopen.flat.addrbooks.patch
- drop integrated openoffice.org-3.0.1.ooo97488.sw.ww8toc.patch
- drop unneccessary openoffice.org-3.0.1.ooo97088.sd.accel-fallback.patch
- add workspace.dba32h.patch
- Resolves: rhbz#528409 [si_LK] Default font in oowriter is not
  Language Default (LKLUG), but DejaVu Sans (dtardon)
- update openoffice.org-3.1.0.ooo98137.filter.redeclared-variables.patch (dtardon)
- add openoffice.org-3.2.0.ooo105827.filter.xpath-on-rtf-not-allowed.patch (dtardon)

* Thu Oct 08 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-19.11
- merge openoffice.org-3.1.1.ooo104157.svx.crashonencryptparse.patch
  into accepted workspace (caolanm)
- Resolves: rhbz#527177 add workspace.vcl106.patch (caolanm)
- Resolves: rhbz#527719 add 
  openoffice.org-3.1.1.ooo105784.vcl.sniffscriptforsubs.patch

* Wed Sep 30 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-19.10
- Resolves: rhbz#461617 gsub coverage format 2 with greater than 1 ranges (caolanm)

* Wed Sep 23 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-19.9
- Resolves: rhbz#522839 crash on exit after loading .doc (caolanm)

* Tue Sep 15 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-19.8
- disable NumberFormatRecognition from default writer configuration (caolanm)
- Resolves: rhbz#522056 - wrong match of fonts (non-)proportional (dtardon)
- drop custom crash reporter and add
  openoffice.org-3.1.1.oooXXXXXX.sal.justcoredump.patch and use abrt (caolanm)

* Mon Sep 14 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-19.7
- make oo.o buildable without langpacks again (dtardon)
- Resolves: rhbz#523106 [indic] changed names of lohit-* fonts (dtardon)

* Tue Sep 08 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-19.6
- Resolves: ooo#104484 workspace.dr69.patch
- Resolves: rhbz#521460 - wrong page size for A3/A5

* Wed Sep 02 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-19.5
- Resolves: rhbz#520772 copy/paste cockup

* Thu Aug 27 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-19.4
- rebuilt with new openssl
- add openoffice.org-3.1.1.ooo104157.svx.crashonencryptparse.patch

* Wed Aug 26 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-19.3
- backport workspace.vcl102.patch to fix xdg support

* Mon Aug 24 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-19.2
- hyphen-as require
- add workspace.cmcfixes62.patch for 64bit odbc goodness and rebuild
  against now 64bit-safe unixODBC headers

* Fri Aug 21 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-19.1
- latest milestone
- Resolves: rbhz#501141 Images and Frames disappear in sequential
  printing
- Related: rhbz#517822 add hyphen-mr depend
- Resolves: rhbz#514683 add openoffice.org-3.1.1.ooo104329.dbaccess.primarykeys.patch

* Tue Aug 18 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-18.2
- add openoffice.org-3.1.0.ooo104280.xmloff.lcl_IsAtEnd.wrong.patch
- Resolves: rhbz#517843 add openoffice.org-3.1.1.ooo104306.moverecentlyused.patch

* Fri Aug 07 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-18.1
- Resolves: rhbz#516011 keep help .xsl files as non-docs
- latest milestone

* Wed Jul 29 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-17.1
- latest milestone

* Sat Jul 25 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-16.2
- make autocorrect and font subpackages noarch
- add workspace.os132.patch to avoid switch html view overwrite horror

* Wed Jul 22 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-16.1
- next milestone
- drop integrated openoffice.org-3.1.1-ooo102679.sdext.buildfix.patch
- drop integrated workspace.aw073.patch
- Resolves: rhbz#512355 add openoffice.org-3.1.0.ooo103651.canvas.nosubpixel.patch

* Thu Jul 16 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-15.2
- add workspace.vcl103.patch
- mythes-hu available
- Resolves(maybe): rhbz#510327 openoffice.org-3.1.0.oooXXXXX.svx.64bit.patch

* Fri Jul 03 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-15.1
- Resolves: rhbz#506984 openoffice.org-3.1.0.ooo103277.vcl.kwinworkaround.patch
- next milestone

* Sun Jun 28 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-14.1
- implement MSXML decryption, no querying for passwords though, so
  only currently opens "protected" .xlsx documents which are 
  encrypted with excels default password
- drop integrated workspace.sb109.patch
- next milestone

* Mon Jun 22 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-13.3
- add hunspell-ko for Korean
- Resolves: rhbz#506545: openoffice.org-3.1.0.ooo102920.i18npool.utf16bustage.patch
- Resolves: rhbz#506184 workspace.aw073.patch
- Resolves: rhbz#504452 Serial printing: Problems with datasource
  refresh, selection of records when printing to a file

* Mon Jun 15 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-13.2
- add openoffice.org-2.0.0.ooo46270.svx.search-dialog.no-find-all-in-draw.patch
- Related: rhbz#472853 updated openoffice.org-3.1.0.ooo99250.sc.autooutline-reflists.patch
- add hyphen-cy requires for Welsh
- add hyphen-gl requires for Galician
- add hyphen-eu requires for Basque
- Workaround: rhbz#505574 add openoffice.org-3.1.1-rh505574.gccXXXX.patch

* Thu Jun 09 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-13.1
- latest version
- Resolves: rhbz#504419  openoffice.org-3.1.0.ooo102566.sc.less.frenetic.progress.patch
- add openoffice.org-3.1.0.ooo102142.sd.resleak.patch
- Resolves (partially): rhbz#498590 improve svg import
- Resolves: rhbz#504967 openoffice.org-3.1.0.ooo97726.sc.misspelling.repeat.disallowed.patch

* Sat Jun 06 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-12.3
- don't over-write en_ZA auto-correct file
- ooo#102567 update auto-correct files with words that appear in
  dictionary with two initial capital letters

* Fri Jun 05 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-12.2
- Resolves: rhbz#503003 silence warnings on updates
- Resolves: rhbz#451767 get default paper right for all territories
- Resolves: rhbz#430675 ooo102061 new cellanchoring implementation
- add openoffice.org-3.1.0.ooo102473.ww8.fix-restartlinenumbering.patch
- add openoffice.org-3.1.0.ooo102490.sw.ww8.notab_before_nocontent.patch

* Tue May 26 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.1-12.1
- start of 3.1.1 branch

* Mon May 25 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-11.4
- Resolves: ooo#102194 crash export on .doc with unused style in .toc

* Thu May 07 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-11.3
- add in the ia64 and arm fixes for the secondary arch people
- Resolves(partially): rhbz#495901 No default font-width for wmf export
- ooo#101567 add Maithili locale data (some dodgy negative value and
  listseperator though)
- Resolves: rhbz#499474 soffice and .recently-used.xbel

* Tue Apr 27 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-11.2
- Resolves: rhbz#484177 openoffice.org-3.1.0.ooo101354.filter.xhtml.do-not-label-list-headers.patch
- add openoffice.org-3.1.0.ooo101355.filter.no-variables-in-keys.patch
- Resolves: rhbz#491159 openoffice.org-3.1.0.ooo101379.vcl.qstart.SM.patch
- Resolves: rhbz#497882 implement audio/visual looping stub

* Fri Apr 24 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-11.1
- add openoffice.org-3.1.0.ooo90439.sfx2.qstart.hackaround.patch
- add openoffice.org-3.1.0.ooo101159.ww8.export.commentfields.patch
- Resolves: rhbz#473985 - "oocalc this-is-a-dir" finishes immediately
   + add openoffice.org-3.1.0-ooo101274.opening-a-directory.patch
- silence stupid survey dialog

* Sun Apr 19 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-10.2
- Resolves: rhbz#496280 ooo#101184 dynamically detect multiple monitors
- Resolves: rhbz#496276 ooo#98806 disable audio in presenter screen

* Fri Apr 17 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-10.1
- closing in on final

* Fri Apr 17 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-9.4
- workaround rhbz#494817 
- Resolves: rhbz#495840 openoffice.org-3.1.0.ooo101145.vcl.safe.dpi.patch
- Resolves: rhbz#496197 openoffice.org-3.1.0.ooo101152.solenv.kn.patch

* Wed Apr 15 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-9.3
- Resolves: rhbz#495609 openoffice.org-3.1.0.ooo101074.sd.bad.nothrow.patch
- Resolves: rhbz#495868 openoffice.org-3.1.0.ooo101105.sw.reorder.boundscheck.patch

* Thu Apr 09 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-9.2
- Require hyphen-bn, hyphen-te, hyphen-ta, hyphen-pa, hyphen-or, 
  hyphen-ml, hyphen-kn, hyphen-gu, hyphen-hi
- Resolves: rhbz#494643 EMF polypolygons issue
- Resolves: ooo#61927 ww6 unicode font encoding on export
- Revert pythonscript.py part of ooo#95118 for now

* Thu Apr 02 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-9.1
- latest milestone

* Mon Mar 30 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-8.2
- add openoffice.org-3.1.0.ooo100225.comphelper.vis.patch

* Sat Mar 28 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-8.1
- latest version
- add mythes-nl as requires to Dutch langpack
- drop integrated openoffice.org-2.0.0.ooo83140.jvmfwk.retryjvm.patch

* Mon Mar 23 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-7.1
- drop integrated workspace.rptfix06.patch

* Thu Mar 19 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-6.3
- Resolves: rhbz#490924 whacked out handling of tlswg custom token

* Tue Mar 17 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-6.2
- Resolves: ooo#100273 fix utf-8 hyphenation for potential Indic
  hyphenation patterns
- add thb's svg importer

* Tue Mar 17 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-6.1
- drop integrated workspace.cl12.patch

* Mon Mar 16 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-5.2
- re-enable system jfreereport

* Fri Mar 13 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-5.1
- next version
- disable gnome-print-unix dialog
- drop integrated Maithili translations
- drop integrated Finnish translations
- drop integrated Hindi translations
- drop integrated Punjabi translations
- drop integrated Tamil translations
- drop integrated Marathi translations
- drop integrated Telugu translations
- drop integrated Kannada translations
- drop integrated Assamese translations
- drop integrated Malayalam translations
- drop integrated workspace.localization35.patch

* Tue Mar 10 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-4.2
- Resolves: rhbz#481012 workaround incorrect branch/type selection 
  or whatever it is with openoffice.org-3.1.0.gccXXXXX.sw.typeillness.patch

* Fri Mar 06 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-4.1
- report-builder will be broken until rhbz#474391 is resolved
- drop integrated workspace.gfbcrash.patch
- drop integrated workspace.ooo31gsl2.patch
- drop integrated openoffice.org-3.1.0.ooo98465.sw.fix-doctables.patch
- Resolves: rhbz#488688 / ooo#98746 merge Punjabi Translations
- Resolves: rhbz#488700 / ooo#99907 merge Malayalam Translations
- add mythes-sv dependency for Swedish langpack
- Resolves: rhbz#488835 backport workspace.cl12
- Farsi autocorrect files

* Tue Mar 03 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-3.4
- Resolves: rhbz#488228 Assamese Translations
- Resolves: rhbz#488234 Tamil Translations

* Mon Mar 02 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-3.3
- Resolves: rhbz#488021 Kannada Translations
- Resolves: rhbz#488053 Hindi Translations
- backport workspace.localization35.patch for mai_IN
- Maithili Translations and langpack

* Sat Feb 28 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-3.2
- Resolves: rhbz#487664 Marathi Translations
- Resolves: rhbz#487659 Telugu Translations

* Thu Feb 26 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-3.1
- next version
- Resolves: rhbz#487504 / ooo#99658 Oriya translations
- openoffice.org-3.0.1.ooo98909.sfx2.missingplugins.patch merged
  into workspace.fwk103
- replace openoffice.org-1.9.87.rh151357.setlangtolocale.patch 
  with planned.workspace.defaultdoclang.patch to provide a better
  solution to auto-tracking by default the document language from 
  current locale while retaining capability to override by config
- drop integrated workspace.jl115.patch
- add X-GIO-NoFuse to .desktops for future

* Tue Feb 24 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-2.3
- Resolves: rhbz#486958 add openoffice.org-3.1.0.ooo98465.sw.fix-doctables.patch

* Mon Feb 23 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-2.2
- Resolves: rhbz#486807 add openoffice.org-3.1.0.ooo99526.sw.mailmergeup.outofrange.patch
- Resolves: rhbz#486934 add openoffice.org-3.1.0.ooo99529.sw.notrailingnewline.patch
- add openoffice.org-3.1.0.ooo99541.sw.reopen.flat.addrbooks.patch

* Fri Feb 20 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-2.1
- next milestone
- drop integrated workspace.mba31issues01.patch
- drop integrated workspace.fwk102.patch

* Thu Feb 19 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-1.3
- rhbz#486062 add workspace.xmergeclean.patch to ensure functionality
- add Danish thesaurus requires
- Resolves: rhbz#486062
   + add openoffice.org-3.1.0.ooo99407.filter-detectsmalldevicefilters.patch
     to auto-detect AportisDoc and PocketWord documents
   + add openoffice.org-3.1.0.ooo99411.sysui.add.dbf-mimetype.patch
     to register as handler for .dbf files
   + add a openoffice.org-javafilter.desktop to the javafilter subrpm
     to notify existance of handlers for optional importers
- Resolves: rhbz#486362 add openoffice.org-3.1.0.ooo99427.sd.ensure-icons-state.patch
- Resolves: rhbz#486460 unversion (well, don't continue to use the old 1.9 names) .desktop files

* Tue Feb 17 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-1.2
- fix rotated glyphs
- fix refusal to migrate java settings
- fix non-functional forward button

* Mon Feb 16 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.1.0-1.1
- drop integrated workspace.selinux01.patch (finally)
- drop integrated workspace.impressfontsize.patch
- drop integrated workspace.cmcfixes48.patch
- drop integrated workspace.locales31.patch
- drop integrated workspace.fpicker8.patch
- drop integrated workspace.cmcfixes49.patch
- drop integrated workspace.cmcfixes50.patch
- drop integrated workspace.cmcfixes51.patch
- drop integrated workspace.vcl94.patch
- drop integrated workspace.vcl95.patch
- drop integrated workspace.vcl96.patch
- drop integrated workspace.vcl97.patch
- drop integrated workspace.vcl98.patch
- drop integrated workspace.hb12.patch
- drop integrated workspace.fwk92.patch
- drop integrated workspace.sb101.patch
- drop integrated workspace.sw31bf02.patch
- drop integrated workspace.configuretoplevel.patch
- drop integrated workspace.gcc44.patch
- drop integrated workspace.fwk99.patch
- drop integrated workspace.tkr16.patch
- drop integrated workspace.i18n45.patch
- Resolves: rhbz#483487 Updated Finnish translations
- Resolves: rhbz#472853 openoffice.org-3.1.0.ooo99250.sc.autooutline-reflists.patch

* Tue Feb 10 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-15.8
- culmus-fonts => culmus-nachlieli-clm-fonts
- Resolves: rhbz#483890 revert bad change, cure worse than disease
  openoffice.org-3.0.1.ooo99050.sw.htmlload.patch
- Resolves: rhbz#484604 crash in glyph substitution

* Mon Feb 09 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-15.7
- Resolves: rhbz#484055 reusable autocorrection files
- Resolves: rhbz#483931 openoffice.org-3.0.1.ooo98885.sw.safeindex.patch
- Resolves: rhbz#483889 openoffice.org-3.0.1.ooo98909.sfx2.missingplugins.patch
- mythes-bg, hyphen-ca

* Tue Feb 03 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-15.6
- Resolves: rhbz#483223 openoffice.org-3.0.1.ooo98649.svtools.missingUI.patch
- add mythes-pt depend to pt langpack
- add workspace.gcc44.patch for gcc44

* Sat Jan 24 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-15.5
- cjkunifonts-uming -> cjkuni-uming-fonts

* Fri Jan 23 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-15.4
- Resolves: rhbz#480057 add openoffice.org-3.0.1.ooo98288.ucb.neonchange.patch
- cjkunifonts-uming -> cjkuni-uming-fonts

* Tue Jan 20 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-15.3
- Resolves: rhbz#480362 add
  openoffice.org-3.0.1.ooo98240.sc.basicworkaround.patch
- add mythes-it
- rhbz#477435 tweak to get font packaging macros to give a usable
  package

* Mon Jan 19 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-15.2
- Resolves: rhbz#479624 add
  openoffice.org-3.0.1.ooo98024.vcl.emboldenoverlap.patch
- add hyphen-uk, hyphen-pt, mythes-el, mythes-fr dependency
- Resolves: rhbz#479163 add
  openoffice.org-3.0.1.oooXXXXX.fpicker.allformatsonsave.patch
- Resolves: rhbz#480117 workspace.fwk99.patch
- Resolves: rhbz#480121 add
  openoffice.org-3.1.0.ooo98137.filter.redeclared-variables.patch
- merge openoffice.org-3.0.0.ooo96391.sw.prefsalwaysmodified.patch into
  upstream workspace.sw31bf02.patch
- Resolves: rhbz#477435 font making macro changed

* Mon Jan 12 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-15.1
- next milestone
- rename openoffice.org-3.0.0.ooo90072.sw.undo-longtext.patch to 
  upstream workspace.sw31bf02.patch
- Resolves: rhbz#477880 add openoffice.org-3.0.1.ooo97975.bridges.mainalreadyexited.patch

* Wed Jan 07 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-14.4
- add hyphen-el, hyphen-es

* Tue Jan 06 2009 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-14.3
- Resolves: rhbz#476959 openoffice.org-3.0.1.ooo97488.sw.ww8toc.patch

* Tue Dec 23 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-14.2
- Workaround: rhbz#477174 recover metacity workarounds without hanging in
  gdk_x11_get_server_time
- add hyphen-bg
- Resolves: rhbz#477435 package opensymbol in a rpm of its own
- add openoffice.org-3.0.1.oooXXXXX.extensions.npapi.patch for new
  xulrunner headers

* Sat Dec 19 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-14.1
- next milestone
- Resolves: rhbz#475007 openoffice.org-3.0.1.ooo97196.vcl.ensuretheme.whenqttesting.patch
- add ga thesaurus
- add workspace.vcl98.patch, and merge 
  openoffice.org-3.0.1.ooo97064.fpicker.honour-uilang-override.patch
  into it
- Resolves: rhbz#477016 playing video under full-screen presentation went away
- Resolves: rhbz#474719 openoffice.org-3.0.1.ooo97428.config_office.xinerama-on-x86_64.patch
- drop integrated workspace.sjfixes12.patch
- drop integrated workspace.swffixes02.patch
- Workaround: rhbz#477174 where gdk_x11_get_server_time now hangs for us

* Thu Dec 11 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-13.2
- Resolves: rhbz#466680 package OGLTrans 3D OpenGL slide transitions
  as an optional extension.
- Resolves: rhbz#474961 wrong impress accelerators
  openoffice.org-3.0.1.ooo97088.sd.accel-fallback.patch
- Resolves: rhbz#475154 UI Language override doesn't affect system dialogs
  openoffice.org-3.0.1.ooo97064.fpicker.honour-uilang-override.patch
- version the Obsoletes
- Resolves: rhbz#475795 same fallbacks for printing as screen
  workspace.vcl97.patch

* Tue Dec 09 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-13.1
- rhbz#474719 add libXinerama-devel BuildRequires
- merge openoffice.org-3.0.0.ooo91904.sd.wrongindex.patch and
  openoffice.org-2.3.0.ooo80257.sd.textonlystyle to upstream
  workspace.impressfontsize.patch
- rename openoffice.org-3.0.1.ooo96906.ucb.symlinks.and.size.patch to
  upstream workspace.tkr16.patch
- drop integrated workspace.swffixes.patch

* Sat Dec 06 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-12.3
- rebuild for python
- Resolves: rhbz#473390 add workspace.swffixes.patch
- Resolves: rhbz#473390 add openoffice.org-3.0.1.ooo96970.pluginfixups.patch
- add openoffice.org-3.0.1.ooo96906.ucb.symlinks.and.size.patch
- rename openoffice.org-2.4.0.ooo87490.sfx2.allprotocols.urlopen.patch to
  upstream workspace.mba31issues01.patch
- rename openoffice.org-3.0.0.ooo96203.sfx2.3layer-qstart.patch to 
  upstream workspace.cmcfixes51.patch
- rename openoffice.org-3.0.0.ooo90653.pyuno.debugging.spew.patch to
  upstream workspace.sb101.patch
- rename openoffice.org-3.0.0.ooo95533.sw.safertableexport.patch and
  openoffice.org-3.0.0.ooo93949.sw.better_rtf_encodings.patch to 
  upstream workspace.hb12.patch
- rename openoffice.org-3.0.0.ooo94659.sal.magazine.patch to
  upstream workspace.mhu17.patch
- drop integrated openoffice.org-3.0.0.ooo93942.svx.accessibity-loops.patch to
- rename openoffice.org-3.0.0.ooo86142.serbiannumbering.patch to
  upstream workspace.locales31.patch

* Mon Dec 01 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-12.2
- Resolves: rhbz#474058 messy patch
- Resolves: rhbz#473570 Add dejavu requires

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1:3.0.1-12.1.1
- Rebuild for Python 2.6

* Sat Nov 29 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.1-12.1
- Move to 3.0.1 preparation milestones
- Resolves: rhbz#473553 font package splits
- drop integrated workspace.impress163.patch
- drop integrated workspace.dba301a.patch
- drop integrated openoffice.org-3.0.0.ooo95341.cppcanvas.patch

* Thu Nov 27 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-9.12
- Require extra Norwegian hyphenators and thesauri

* Thu Nov 19 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-9.11
- Resolves: rhbz#471103 improve font-settings
- Resolves: ooo#96279 mediawiki proxies problem
- reenable -fasynchronous-unwind-tables for F-11 as gcc#36419 is marked as fixed
- add openoffice.org-3.0.0.ooo96391.sw.prefsalwaysmodified.patch

* Fri Nov 14 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-9.10
- rhbz#248401 extend the title page dialog to create title pages at
  arbitrary positions
- rhbz#470302 g_file_input_stream_query_info doesn't do anything remotely
- window manager hatred
- Resolves: rhbz#471485 openoffice.org-3.0.0.ooo96203.sfx2.3layer-qstart.patch
- Resolves: rhbz#471724 own the share dir too

* Thu Nov 06 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-9.9
- add openoffice.org-3.0.0.ooo95908.pyuno.debugging.spew.patch
- add openoffice.org-3.0.0.ooo90072.sw.undo-longtext.patch

* Tue Nov 04 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-9.8
- Resolves: rhbz#469804 openoffice.org-3.0.0.ooo95793.goodies.met.patch
- Resolves: rhbz#469630 openoffice.org-3.0.0.ooo95834.dontset-nonfunctional-forward.patch

* Wed Oct 29 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-9.7
- Resolves: rhbz#468336 openoffice.org-3.0.0.ooo95533.sw.safertableexport.patch
- workspace.impress163.patch
- Resolves: rhbz#468935 Print to file can have no effect in an edge-case
- openoffice.org-3.0.0.ooo95341.cppcanvas.patch

* Thu Oct 23 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-9.6
- add openoffice.org-3.0.0.ooo95318.system-showicons.patch to honour
  gtk-menu-images setting
- Resolves: rhbz#468288 associate text/csv with oocalc

* Mon Oct 20 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-9.5
- Resolves: rhbz#466603 odd focus troubles with floating toolbars
  "The focus window is an ancestor of the newly mapped
   window which isn't being focused.  Unfocusing the "
   ancestor". Grrr... thanks a bunch.
- add openoffice.org-3.0.0.ooo94659.sal.magazine.patch
- add openoffice.org-3.0.0.ooo95018.sal.fdwarnings.patch

* Thu Oct 16 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-9.4
- Resolves: rhbz#465664 brp-java-repack-jars breaks some of our jars
- Resolves: rhbz#466605 openoffice.org-3.0.0.ooo94936.vcl.nogtkspinwarn.patch
- Resolves: rhbz#466881 openoffice.org-3.0.0.ooo94938.unopkg.handleexception.patch

* Fri Oct 10 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-9.3
- Resolves: rhbz#465664 need lucene for runtime help search

* Sat Oct 04 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-9.2
- Resolves: rhbz#465427 wrong order of seds
- Resolves: rhbz#465515 use --force to avoid any potential problems where
  upgrading a hand-added extension

* Wed Oct 01 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-9.1
- next candidate

* Sun Sep 28 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-8.1
- next candidate
- Resolves: rhbz#463884 openoffice.org-3.0.0.ooo94318.greekmenu.crash
- Resolves: rhbz#464109 lohit-fonts-marathi

* Sun Sep 21 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-7.1
- Tswana, Ukrainian, Urdu spellcheckers
- Resolves: rhbz#462833 openoffice.org-3.0.0.ooo94069.psprint.defconfig.patch
- Resolves: rhbz#463050 rejig desktop-file-utils, shared-mime-info usage

* Tue Sep 16 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-6.1
- next candidate
- use system jfreereport
- Basque, Ndebele, Swati, Southern Sotho, Northern Sotho, Tsonga,
  Venda, Xhosa spellcheckers
- add openoffice.org-3.0.0.ooo93419.svx.accessibity-loops.patch
- add openoffice.org-3.0.0.ooo93949.sw.better_rtf_encodings.patch

* Sun Sep 07 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-5.1
- next candidate

* Thu Sep 04 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-4.2
- Resolves: rhbz#460755 TryExec oowriter on brwriter.desktop etc
- Resolves: rhbz#460883 openoffice.org-3.0.0.ooo93419.svx.ref_deref.before.ctored.patch
- defuzz patches
- add openoffice.org-3.0.0.ooo93366.fpicker_in_main.patch
- add openoffice.org-3.0.0.oooXXXXX.filter.latex.patch
- add openoffice.org-3.0.0.ooo93515.vcl.jrb-frames.patch to get better
  focus for new frames when already running and behind in stacking order

* Fri Aug 29 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-4.1
- next milestone
- writer2latex isn't really core enough to be hard required
- smc-fonts-meera is a far better font than lohit-fonts-malayalam
- Resolves: rhbz#460626 openoffice.org-3.0.0.ooo91924.svx.consistentordering.patch

* Tue Aug 19 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-3.1
- next milestone
- Resolves: rhbz#458681 python requires
- Resolves: rhbz#458739 icon generation sequence
- Resolves: rhbz#441108 fpicker UI lock add workspace.fpicker8.patch
- update to upstream dbaccess a11y solution
- ooo#92920 enable building pdf importer against poppler and activate
  for fedora
- drop integrated workspace.impress152.patch

* Sat Aug 09 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-2.1
- next milestone
- Resolves: rhbz#457938 openoffice.org-3.0.0.ooo92522.sd.brokentemplates.patch
- add openoffice.org-3.0.0.ooo91904.sd.wrongindex.patch
- now moved to saxon instead of xalan

* Tue Aug 05 2008 Caolán McNamara <caolanm@redhat.com> - 1:3.0.0-1.1
- release branch
- drop integrated openoffice.org-3.0.0.ooo90876.connectivity.evoab2.patch

* Sun Aug 03 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.28-2
- Resolves: rhbz#457193 openoffice.org-3.0.0.ooo92253.dbaccess.a11y.crash
- Resolves: rhbz#457529 reset number recognition default in writer back to 
  pre 3.0 settings. Its a stupid feature for a word processor.
- Resolves: rhbz#457600 licences are localized apparently

* Mon Jul 28 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.28-1
- next version
- drop (finally!) integrated ooo#64726 bengali translation fix (April 2006)
- drop integrated workspace.cmcfixes46.patch
- Move hsqldb stuff into database rpm

* Thu Jul 24 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.27-1
- next version
- drop integrated workspace.native172.patch
- drop integrated openoffice.org-3.0.0.ooo82545.np_sdk.x86_64.patch

* Wed Jul 23 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.26-2
- Resolves: rhbz#456292 openoffice.org-3.0.0.ooo92026.sd.disposed_during_disposing.patch
- Resolves: rhbz#451708 ensure root certs are available for document signing
- Resolves: rhbz#456459 3-layer OOo hits the sdk/odk again

* Tue Jul 22 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.26-1
- next version
- drop integrated openoffice.org-3.0.0.ooo90306.sw.wrongprotection.patch
- move some libs out of core into the database module
- Resolves: rhbz#455904 add openoffice.org-3.0.0.ooo91977.sd.holdreference.patch

* Thu Jul 17 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.25-1
- next version
- drop integrated openoffice.org-2.4.0.ooo85448.emptyrpath.patch
- drop inregrated openoffice.org-2.3.0.oooXXXXX.odk.3layer.patch
- add workspace.native172.patch for ScriptFramework extention bustage

* Fri Jul 11 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.24-1
- next version
- drop integrated openoffice.org-3.0.0.ooo6087.sc.sheetnames.patch
- drop integrated openoffice.org-3.0.0.ooo90055.swext.allowadmin.patch
- drop integrated workspace.cairo06.patch
- drop integrated workspace.ab55.patch
- Resolves: rhbz#452385 add postgress-jdbc to default classpath
- Resolves: rhbz#454682 expand macro to get correct name for
  inconsistent, unnecessarily complicated, redundant and nigh universially 
  hated arch-dependant naming scheme for presenter-screen extension 

* Mon Jul 07 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.23-1
- next version
- drop integrated openoffice.org-3.0.0.ooo90612.sd.insertpasswordedfile.patch
- drop integrated openoffice.org-3.0.0.ooo90697.sd.a11ycrash.patch
- drop integrated openoffice.org-2.4.0.ooo85429.sw.a11ycrash.patch
- drop integrated openoffice.org-2.1.0.ooo73201.sw.a11yloadcrash.patch
- Resolves: rhbz#452374 add openoffice.org-3.0.0.ooo86142.serbiannumbering.patch
- split out arcane ScriptProviders out of core into optional extensions 
  => bsh now only required by beanshell ScriptProvider
- extend selinux bodge to m68k

* Tue Jul 01 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.22-1
- next version
- drop integrated pseudoworkspace.valgrind1.patch
- drop integrated openoffice.org-2.2.0.ooo73863.vcl.imcommit.patch
- add workspace.cairo06.patch
- add workspace.ab55.patch
- Resolves: rhbz#453487 some font packages now gone

* Thu Jun 26 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.20-1
- next version
- Resolves: rhbz#450661 openoffice.org-3.0.0.ooo90306.sw.wrongprotection.patch
- Resolves: rhbz#448464 openoffice.org-3.0.0.ooo48400.svx.fixspelling.patch
- Resolves: rhbz#450930 openoffice.org-3.0.0.ooo90697.sd.a11ycrash.patch
- Resolves: rhbz#451512 set better math default print options
- Resolves: rhbz#451708 openoffice.org-3.0.0.oooXXXXX.connectivity.mozprofilefinder.patch
- Resolves: rhbz#452777 Ukranian langpack
- drop integrated openoffice.org-3.0.0.ooo87882.lingucomponent.systemdicts.patch
- drop integrated openoffice.org-3.0.0.ooo87604.fixupsystemhunspell.patch
- drop integrated openoffice.org-3.0.0.ooo90071.chart2.negativecount.patch
- add openoffice.org-3.0.0.ooo90876.connectivity.evoab2.patch

* Wed Jun 11 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.19-1
- next version
- add openoffice.org-3.0.0.ooo90612.sd.insertpasswordedfile.patch

* Mon Jun 09 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.18-1
- next version
- drop integrated openoffice.org-2.4.0.ooo85854.sw.graphicsaveas.patch
- drop integrated openoffice.org-3.0.0.ooo88815.oox.parallel.patch

* Fri Jun 06 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.17-2
- Resolves: rhbz#450212 openoffice.org-3.0.0.ooo82545.np_sdk.x86_64.patch

* Thu Jun 05 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.17-1
- next version 
- drop integrated openoffice.org-2.3.1.ooo84676.ucb.davprotocol.patch

* Thu Jun 05 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.16-2
- still fighting the sdk

* Wed Jun 04 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.16-1
- next version
- add openoffice.org-3.0.0.ooo90178.tools.fixmacro.patch
- add openoffice.org-3.0.0.oooXXXXX.vcl.cairomaxclip.patch
- Resolves: rhbz#449804 fix Requires

* Tue Jun 03 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.15-1
- next version
- add openoffice.org-2.3.0.oooXXXXX.odk.3layer.patch for building against
  3 layer OOo
- drop integrated openoffice.org-3.0.0.ooo88260.decl-defi-mismatch.patch
- drop integrated openoffice.org-3.0.0.ooo89172.filter.string.patch
- filter out -fasynchronous-unwind-tables for the moment until its ok with
  -Os on i386
- Resolves: rhbz#448553 add openoffice.org-3.0.0.ooo90037.vcl.cairotransforms.patch

* Wed May 28 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.14-1
- next version
- Require new hunspell-ml for Malayalam langpack
- drop integrated openoffice.org-2.3.1.ooo84621.sw.insertexcel.patch
- drop integrated openoffice.org-2.4.0.ooo85097.desktop.pagein.patch
- add openoffice.org-3.0.0.ooo89921.oox.parallel.patch
- Resolves: rhbz#445588 add openoffice.org-3.0.0.ooo87970.vcl.samenamesubs.patch
- add openoffice.org-3.0.0.ooo90055.swext.allowadmin.patch

* Mon May 19 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.13-1
- next version
- drop integrated openoffice.org-2.2.0.ooo76424.nonatnum.bn_IN.18npool.patch
- drop integrated openoffice.org-2.4.0.ooo86924.sfx2.iconchanges.patch
- drop integrated openoffice.org-2.4.0.ooo87204.toolkit.64bitevent.patch
- drop integrated openoffice.org-3.0.0.ooo85691.vcl.tooltipcolor.patch
- drop integrated openoffice.org-3.0.0.ooo87991.fpickersafe.patch
- drop integrated workspace.ucpgio1.patch
- drop integrated openoffice.org-3.0.0.ooo88584.sdext.extraqual.patch

* Fri May 16 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.12.2
- I misspelled the damn Requires

* Fri May 09 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.12.1
- next version
- re-add openoffice.org-2.2.0.gccXXXXX.solenv.javaregistration.patch

* Fri May 09 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.11.1
- next version
- drop integrated workspace.cmcfixes43.patch
- drop integrated openoffice.org-3.0.0.ooo88375.filter.disablepdf.patch
- drop integrated openoffice.org-3.0.0.ooo88319.setup_native.missing.patch
- drop redundant openoffice.org-2.0.4.ooo69051.vcl.singlekeypress.patch
- drop openoffice.org-2.0.4.rh217065.syncbackspace.patch as reported fixed
- add openoffice.org-3.0.0.ooo89002.vcl.symbolfonts.patch
- add openoffice.org-3.0.0.ooo89172.filter.string.patch
- enable presentation-minimizer
- enable presenter-screen
- tidy configure line through --with-system-libs --with-system-headers
- drop sequence check patch and use .xcu configuration

* Wed Apr 30 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.10.1
- next version
- drop integrated openoffice.org-2.3.0.ooo82966.svx.missing3d.patch
- drop integrated openoffice.org-2.2.1.ooo79481.sw.rowordcount.patch
- drop openoffice.org-2.4.0.gccXXXXX.wizards.patch
- drop openoffice.org-2.1.0.oooXXXXX.vcl.dontsortglyphs.patch
- drop openoffice.org-2.2.1.ooo78971.xmloff.outofrange.patch
- drop openoffice.org-2.4.0.ooo85054.stlport.noorigs.patch
- drop openoffice.org-2.2.0.rh232389.tango.patch
- Resolves: rhbz#444571 add openoffice.org-3.0.0.ooo88090.chart2.negativecount.patch
- add workspace.ucpgio1.patch and disable gnome-vfs

* Mon Apr 21 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.9.1
- Resolves: rhbz#358021 enable BrOffice.org brand
- add openoffice.org-3.0.0.ooo88375.filter.disablepdf.patch
- add openoffice.org-3.0.0.ooo6087.sc.sheetnames.patch
- add openoffice.org-2.4.0.gccXXXXX.wizards.patch to try and build

* Wed Apr 16 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.7.1
- next version
- drop integrated openoffice.org-2.3.0.ooo86882.vcl.unsigned_int_to_long.patch
- extend selinux bodge to s390x
- add openoffice.org-3.0.0.ooo88260.decl-defi-mismatch.patch
- add openoffice.org-3.0.0.ooo88303.vcl.dynamicfontoptions.patch
- disable pdfimport for now
- add openoffice.org-3.0.0.ooo88319.setup_native.missing.patch
- add openoffice.org-3.0.0.ooo88341.sc.verticalboxes.patch

* Wed Apr 09 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.5.4
- Resolves: rhbz#441128 openoffice.org-3.0.0.ooo88033.svx.a11ycrash.patch
- migrate system extensions automatically
- Resolves: rhbz#358021 split up into brand layers and add BrOffice.org
- try and share unopkg and make a broffice.org launcher to allow both to
  be installed at the same time

* Mon Apr 07 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.5.3
- Resolves: rhbz#441112 openoffice.org-3.0.0.ooo85691.vcl.tooltipcolor.patch
- Resolves: rhbz#441108 openoffice.org-3.0.0.ooo87991.fpickersafe.patch

* Fri Apr 04 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.5.2
- reenable dicts

* Mon Mar 31 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.5.1
- drop integrated workspace.cairotext01.patch
- fix up launchers
- fix up configuration settings without using configimport
- extend selinux bodge to arm, mips and s390
- add openoffice.org-3.0.0.ooo87604.fixupsystemhunspell.patch

* Tue Mar 27 2008 Caolan McNamara <caolanm@redhat.com> - 1:3.0.0-0.4.1
- extend selinux bodge to ia64 
- drop integrated workspace.notes2.patch
- drop integrated openoffice.org-2.3.1.ooo84770.svx.eventsmismatch.patch
- drop integrated openoffice.org-2.4.0.ooo85385.svtools.a11ycrash.patch
- drop integrated workspace.gcc430two.patch
- drop integrated openoffice.org-2.4.0.ooo85931.svx.getentrypos.patch
- drop integrated openoffice.org-2.4.0.ooo86123.ucb.newneon.patch
- drop subsumed openoffice.org-2.4.0.ooo86670.config_office.xpcomasxul.patch
- drop integrated workspace.unifysound01.patch
- drop openoffice.org-2.3.0.ooo81321.cppu.silencewarnings.patch
- drop integrated openoffice.org-1.9.114.rh161886.rpath.desktop.patch
- drop integrated openoffice.org-2.3.1.ooo81307.sw.word2.patch
- libsoffice partially integrated into head
- add workspace.cmcfixes43.patch
- add the report-builder

* Wed Mar 19 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-12.2
- add openoffice.org-2.4.0.ooo87204.toolkit.64bitevent.patch
- add openoffice.org-2.4.0.ooo87490.sfx2.allprotocols.urlopen.patch

* Sun Mar 16 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-12.1
- yet another release candidate

* Thu Mar 13 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-11.1
- next release candidate
- Resolves: rhbz#429632 add openoffice.org-2.3.0.ooo86882.vcl.unsigned_int_to_long.patch
- Resolves: rhbz#435590 add openoffice.org-2.4.0.ooo86924.sfx2.iconchanges.patch

* Sun Mar 09 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-10.1
- next release candidate
- rhbz#293791 Restore draw back to the menus and revert to upstream app names
- drop integrated openoffice.org-2.4.0.ooo86268.desktop.visibilitycockup.patch
- Resolves: rhbz#436518 add openoffice.org-2.3.0.ooo86866.embeddedobj.plusequalsoperator.patch

* Sun Mar 09 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-10.1
- next release candidate
- rhbz#293791 Restore draw back to the menus and revert to upstream app names
- drop integrated openoffice.org-2.4.0.ooo86268.desktop.visibilitycockup.patch
- Resolves: rhbz#436518 add openoffice.org-2.3.0.ooo86866.embeddedobj.plusequalsoperator.patch

* Thu Mar 06 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-9.1
- next release candidate

* Thu Feb 28 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-8.1
- next release candidate
- add openoffice.org-2.4.0.ooo86268.desktop.visibilitycockup.patch
- add openoffice.org-2.4.0.oooXXXXX.psprint.debugcups.patch to debug
  rhbz#434803

* Sun Feb 17 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-7.3
- accidentally included scratch uno_packages cache, i.e. trashed your
  shared extensions

* Thu Feb 14 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-7.2
- some multilib helping
- Resolves: rhbz#432654 add openoffice.org-2.4.0.ooo86080.unopkg.bodge.patch

* Wed Feb 13 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-7.1
- Resolves: rhbz#432368 parallel build is err... "a little" aggressive
- next milestone
- drop integrated openoffice.org-2.4.0.ooo85624.sw.headerfooters.patch

* Tue Feb 12 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-6.3
- Resolves: rhbz#431805 openoffice.org-2.4.0.ooo85931.svx.getentrypos.patch
- Resolves: rhbz#431620 presentation problems
- add openoffice.org-2.4.0.ooo85624.sw.headerfooters.patch from fridrich
- add openoffice.org-2.4.0.oooXXXXX.ucb.newneon.patch for new neon

* Tue Feb 05 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-6.2
- fix problem with mixed fontsizes with same font face
- resync workspace.notes2.patch
- Resolves: ooo#84209 make letter wizard work with gstreamer changes
- Resolves: rhbz#431606 require jre not java
- Resolves: rhbz#431620/ooo#85909 depth mismatch for text
- ooo#85914 work around trouble with deleting multiple notes
- add openoffice.org-2.4.0.ooo85921.sd.editmasterundermouse.patch for jrb

* Mon Feb 04 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-6.1
- next milestone
- Resolves: rhbz#422661 support n-up printing of rotated landscape
  slides in a human-expectation direction
- drop integrated openoffice.org-2.4.0.ooo84684.vcl.fixfontconfig.patch
- drop openoffice.org.2.0.3-ooo66018.cppuhelper.dangerousvisibility.patch
  now that we have gcc 4.3.0
- drop integrated openoffice.org-2.4.0.ooo85321.vcl.pixmapleak.patch
- add workspace.gcc430two.patch for some newly needed includes
- add openoffice.org-2.4.0.ooo85854.sw.graphicsaveas.patch for riel

* Mon Jan 28 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-5.1
- next milestone
- replace cairotext with workspace.cairotext01.patch, not use
  SAL_DISABLE_CAIROTEXT=1 to disable as cairo text rendering is now
  default
- add openoffice.org-2.4.0.ooo85643.psprint.helppreviewers.patch to 
  help gv/evince rotate landscape pages when previewing
- drop integrated workspace.sw24bf02.patch
- drop integrated openoffice.org-2.4.0.ooo85055.psprint.linetoolong.patch
- drop integrated openoffice.org-2.4.0.ooo85487.evoconnectivity.patch

* Thu Jan 23 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-4.1
- next milestone
- drop integrated openoffice.org-2.4.0.ooo83410.solenv.renameserbian.patch
- drop integrated openoffice.org-2.3.1.ooo83877.sal.allowsoftlinkdelete.patch
- drop integrated workspace.sw8u10bf04.patch
- drop integrated workspace.impress132.patch
- add openoffice.org-2.4.0.ooo85487.evoconnectivity.patch to make evoab2 build
- new finnish autocorrect file
- Resolves: rhbz#429897 one click print with lpr-only backend fix
- Resolves: rhbz#426295 openoffice.org-2.4.0.ooo85470.vcl.cairotext.patch
  use export SAL_ENABLE_CAIROTEXT=1 to enable

* Mon Jan 21 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-3.3
- fix openoffice.org-2.4.0.ooo85321.vcl.pixmapleak.patch for warren
- fix openoffice.org-2.4.0.ooo85429.sw.a11ycrash.patch
- Resolves: rhbz#428574 add workspace.sw24bf02.patch
- Resolves: problem in rhbz#429550 openoffice.org-2.4.0.ooo85448.emptyrpath.patch

* Sat Jan 19 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-3.2
- Resolves: rhbz#429258 openoffice.org-2.4.0.ooo85385.svtools.a11ycrash.patch

* Wed Jan 16 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-3.1
- Resolves: rhbz#428655 workspace.sw8u10bf04.patch
- Resolves: rhbz#428655 workspace.impress132.patch
- fix word2 import
- Lithuanian help content

* Tue Jan 15 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-2.2
- fix hyphenation

* Tue Jan 15 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-2.1
- drop integrated openoffice.org-2.3.0.ooo74751.bean.mawt.patch
- drop integrated openoffice.org-1.9.88.rhXXXXXX.noxfonts.desktop.patch
- next candidate

* Mon Jan 14 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-1.3
- fix broken requires

* Fri Jan 11 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-1.2
- add openoffice.org-2.4.0.ooo92086.solenv.paths.patch to fix up -devel Requires
- add openoffice.org-2.4.0.rh133741.alwaysgtk.vcl.patch
- Resolves: rhbz#425701/ooo#83410 try and fix serbian translations

* Sat Jan 06 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.4.0-1.1
- first OOH680_m1
- remove redundant entries from configure
- drop integrated openoffice.org-2.3.0.ooo77885.stoc.stocmerge.patch
- drop integrated openoffice.org-1.9.129.ooo54603.fontconfig.patch
- drop integrated workspace.as6.patch
- drop integrated openoffice.org-2.0.3.ooo68048.vcl.imsurroundtext.patch
- drop integrated openoffice.org-2.1.0.ooo72129.vcl.fontglyphindex.patch
- drop integrated workspace.configrefactor01.patch
- drop integrated openoffice.org-2.2.1.ooo80424.vcl.honourwidthtype.patch
- drop integrated workspace.npower7.patch
- drop integrated openoffice.org-2.3.0.ooo80721.reportdesign.stlportism.patch
- drop integrated openoffice.org-2.3.0.ooo80735.cppu.map.patch
- drop integrated openoffice.org-2.3.0.ooo80967.ucb.neon27.patch
- drop integrated openoffice.org-2.3.0.ooo81112.reportdesign.parallel.patch
- drop integrated openoffice.org-2.3.0.ooo81936.sc.maketypesagree.patch
- drop integrated workspace.fpicker7.patch
- drop integrated openoffice.org-2.3.0.ooo83591.vcl.checkboxes.patch
- drop integrated openoffice.org-2.3.1.ooo82911.sd.insertbackground.patch
- drop integrated workspace.sw8u10bf02.patch
- drop integrated openoffice.org-2.3.1.ooo83930.sw.flushanchors.patch
- drop integrated workspace.cmcfixes39.patch
- drop integrated workspace.gcc430.patch
- drop integrated workspace.locales24.patch
- drop integrated openoffice.org-2.3.0.ooo81314.i18npool.crash.patch
- drop openoffice.org-2.3.1.ooo84001.slideshow.gccisaprick.patch
- drop openoffice.org-2.2.0.ooo53397.linkopt.patch
- replace openoffice.org-2.1.0.ooo78148.lingucomponent.systemhunspell.patch with
  openoffice.org-2.1.0.oooXXXXX.lingucomponent.systemdicts.patch
- add openoffice.org-2.4.0.ooo84684.vcl.fixfontconfig.patch
- add Requires for indic hunspell dictionaries
- Resolves: rhbz#427757 add openoffice.org-2.4.0.ooo85054.stlport.noorigs.patch
- Resolves: rhbz#426876 add openoffice.org-2.4.0.ooo85055.psprint.linetoolong.patch
- add openoffice.org-2.4.0.oooXXXXX.config_office.xpcomasxul.patch to build
- add openoffice.org-2.4.0.ooo85097.desktop.pagein.patch

* Wed Jan 03 2008 Caolan McNamara <caolanm@redhat.com> - 1:2.3.1-9.11
- Resolves: rhbz#427071 openoffice.org-2.3.0.ooo81314.i18npool.crash.patch

* Thu Dec 20 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.1-9.10
- Resolves: rhbz#425701 add workspace.locales24.patch
- Resolves: rhbz#423371 openoffice.org-2.3.1.ooo84621.sw.insertexcel.patch
- add workspace.gcc430.patch for gcc 4.3.0
- add openoffice.org-2.3.1.ooo84770.svx.eventsmismatch.patch

* Sun Dec 09 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.1-9.9
- oops

* Sat Dec 08 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.1-9.8
- Resolves: rhbz#384401 attempt to allow davs:// to work

* Mon Dec 03 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.1-9.7
- Resolves: rhbz#206400 add long awaited workspace.notes2.patch
    + drop openoffice.org-2.3.0.ooo53885.raiseannotationpriority.sw.patch
    integrated
- add openoffice.org-2.3.1.oooXXXXX.ucb.davprotocol.patch for dav:// and davs://

* Sat Dec 01 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.1-9.6
- add workspace.cmcfixes39.patch for ooo#83751 and use system writer2latex

* Thu Nov 29 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.1-9.5
- split out thesauri
- move autocorrect files into langpacks and make appropiate aliases
- allow "import uno" to just work out of the box

* Sat Nov 24 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.1-9.4
- Resolves: rhbz#384391 add openoffice.org-2.3.1.ooo83930.sw.flushanchors.patch
- split out libhyphen and hyphenators
- add openoffice.org-2.3.1.ooo84001.slideshow.gccisaprick.patch coz gcc hates us
- drop openoffice.org-2.3.1.83876.unopkg.avoida11y.patch coz upstream won't do it

* Thu Nov 22 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.1-9.3
- Resolves: rhbz#247634 add openoffice.org-2.3.1.ooo82911.sd.insertbackground.patch (jnavrati)
- Resolves: rhbz#386371 add workspace.sw8u10bf02.patch (caolanm)
- add openoffice.org-2.3.1.83876.unopkg.avoida11y.patch to avoid unopkg
  crapping out on first run with a11y enabled and no X (caolanm)
- add openoffice.org-2.3.1.ooo83877.sal.allowsoftlinkdelete.patch to allow
  sal to delete softlinks (caolanm)
- add openoffice.org-2.3.1.ooo83878.unopkg.enablelinking.patch to enable
  linking to unpacked extensions already on the fs when registering (caolanm)
==> makes extension rpm packaging non-wasteful and safe

* Thu Nov 15 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.1-9.2
- move from firefox to xulrunner

* Wed Nov 14 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.1-9.1
- 2.3.1 pre-release candidate m9
- tweak mime information and desktop files to support .oxt extensions
- add openoffice.org-2.3.1.ooo81307.sw.word2.patch
- add openoffice.org-2.3.0.ooo83591.vcl.checkboxes.patch
- drop integrated openoffice.org-2.3.0.ooo77672.boost.use.end_p.patch
- drop integrated openoffice.org-2.3.0.ooo81323.svtools.sixtyfour.patch
- drop integrated openoffice.org.ooo82608.vcl.gtkbadfree.patch
- drop integrated openoffice.org-2.3.0.ooo83169.colordialog.crash.patch

* Fri Nov 09 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.0-6.7
- rebuild for hunspell

* Wed Oct 24 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.0-6.6
- Resolves: rhbz#338701 fix openoffice.org.ooo82608.vcl.gtkbadfree.patch
- Resolves: rhbz#213213 openoffice.org-2.3.0.ooo76649.httpencoding.patch
- add openoffice.org-2.3.0.ooo82966.svx.missing3d.patch
- Resolves: rhbz#360461 fix openoffice.org-2.3.0.ooo83169.colordialog.crash.patch

* Thu Oct 19 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.0-6.5
- Resolves: rhbz#338701 fix openoffice.org.ooo82608.vcl.gtkbadfree.patch

* Tue Oct 16 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.0-6.4
- Resolves: rhbz#333201 dangling symlinks
- Resolves: rhbz#334841 fix "all files" glob in in mail merge picker
- Resolves: ooo#82671 print crash

* Fri Oct 12 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.0-6.3
- reenable prelink-optimized launchers
- rhbz#326161 make code compiled with icedtea compatible with 1.5.0 so libgcj
  can still be selected as a jvm
- add openoffice.org-2.3.0.ooo53885.raiseannotationpriority.sw.patch

* Sun Oct 07 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.0-6.2
- reenable visibility again now that guard visibility is sane again

* Thu Oct 04 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.0-6.1
- Resolves: rhbz#299391 Serbian langpack name update
- Resolves: rhbz#286221 allow custom printing commands
- Resolves: rhbz#303431 some printing problems
- add openoffice.org-2.3.0.ooo81936.sc.maketypesagree.patch

* Mon Sep 17 2007 Jan Navratil <jnavrati@redhat.com> - 1:2.3.0-5.1
- release candidate

* Thu Sep 06 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.0-4.1
- next version
- ooo#77672 fix ::boost::spirit::parse to use ::boost::spirit::end_p to
  make drawing shapes work properly again with new boost 1.34
- add openoffice.org-2.3.0.ooo81321.cppu.silencewarnings.patch
- add openoffice.org-2.3.0.ooo81323.svtools.sixtyfour.patch
- disable custom launchers, it breaks icedtea for some reason I haven't time to
  figure out
- disable visibility for now, seems screwed up.

* Tue Sep 04 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.0-3.2
- rebuild against icu
- rebuild against icedtea
- add openoffice.org-2.3.0.ooo74751.bean.mawt.patch to allow build against icedtea
- don't prefer gcj over icedtea when both installed
- add ooo#81253 connectivity uninit fix
- add ooo#81258 sw uninit fix
- package sandbox.jar where available

* Sat Sep 01 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.0-3.1
- release candidate
- drop integrated openoffice.org-1.9.130.ooo67740.doublefree.xmlhelp.patch
- drop integrated openoffice.org-2.2.0.ooo75790.sc.pa-IN.translate.patch
- drop integrated openoffice.org-2.3.0.ooo80944.sd.sixtyfour.patch
- drop integrated workspace.dba23e.patch
- drop integrated openoffice.org-2.3.0.ooo80931.sysui.genericname.patch

* Wed Aug 29 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.0-2.4
- add openoffice.org-2.3.0.ooo81112.reportdesign.parallel.patch

* Mon Aug 27 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.0-2.3
- drop integrated openoffice.org-2.1.0.ooo61812.svx.a11ycrash.patch
- drop openoffice.org-1.9.85.rh151356.usetwodotzeropath.patch and do
  it differently
- allow -fasynchronous-unwind-tables to be passed to ARCH_FLAGS
- oovbaapi.rdb needs be in core package

* Wed Aug 22 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.0-2.2
- move vba stuff into calc package
- add workspace.dba23e.patch
- no longer need openoffice.org-2.0.4.oooXXXXX.vcl.x86_64.impressatk.patch
- add openoffice.org-2.3.0.ooo80967.ucb.neon27.patch and reenable neon
- drop openoffice.org-1.9.97.rh156067.noversionedsysui.patch and do it
  differently
- add openoffice.org-2.3.0.ooo80931.sysui.genericname.patch

* Wed Aug 22 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.3.0-2.1
- Resolves: rhbz#251896 count from start of ctl sequence, not start of
  string when doing range test
- first 2.3.0 prerelease candidate
  + disable neon until 0.26 series is in fedora
  + unset HAVE_LD_HASH_STYLE because both is enabled despite constantly
    saying that was a stupid idea to hardcode
  + large file support upstreamed
  + add libtextcat.xcu -> reuse libtextcat fingerprints
  + add workspace.npower7.patch for build failure
  + add openoffice.org-2.3.0.oooXXXXX.reportdesign.stlportism.patch for build failure
  + add openoffice.org-2.3.0.ooo80735.cppu.map.patch for ppc64
  + add openoffice.org-2.3.0.ooo80944.sd.sixtyfour.patch
  + add openoffice.org-2.2.0.gccXXXXX.solenv.javaregistration.patch for pesky ppc64 
    install failure
  + replace openoffice.org-1.9.121.rh156677.cripplemenus.sysui.patch
    with integrated GenericName support
  + drop integrated workspace.libxslt02.patch
  + drop integrated workspace.ppc64one.patch
  + drop integrated openoffice.org-2.0.3.rh187919.gtkunderkde.patch
  + drop integrated ooobuild.VBAObjects.patch and use --enable-vba
  + drop integrated openoffice.org-2.0.4.ooo70155.fasterhelplinking.patch
  + drop integrated workspace.thbpp6.patch
  + drop integrated openoffice.org-2.1.0.ooo72014.officecfg.malayammenu.patch
  + drop integrated openoffice.org-2.1.0.ooo73481.svx.longnotint32.patch
  + drop integrated openoffice.org-2.2.0.ooo73866.javaunohelper.parallel.patch
  + drop integrated openoffice.org-2.2.0.ooo73974.bridges.doublereturn.patch
  + drop integrated openoffice.org-2.2.0.ooo74451.sw.typemismatch.patch
  + drop integrated workspace.sixtyfour11.patch
  + drop integrated openoffice.org-2.2.0.ooo75167.framework.workspacerestore.patch
  + drop integrated openoffice.org-2.2.0.ooo75190.shell.newrecentlyused.patch
  + drop integrated openoffice.org-2.2.0.ooo75329.xdguserdir.patch
  + drop integrated openoffice.org-2.2.0.oooXXXXX.shell.reduceglobals.patch
  + drop integrated workspace.cmcfixes34.patch
  + drop integrated openoffice.org-2.2.0.ooo77470.docexport.liberation.to.ms.patch
  + drop integrated openoffice.org-2.2.1.ooo73728.desktop.mapped_type.patch
  + drop integrated openoffice.org-2.2.1.ooo78392.sixtyfour.tools.patch
  + drop integrated openoffice.org-2.2.1.ooo78383.vcl.printxerror.patch
  + drop integrated openoffice.org-2.2.1.ooo78392.sixtyfour.tools.patch
  + drop integrated workspace.glyphadv.patch
  + drop integrated openoffice.org-2.2.1.ooo78921.sw.embedded.patch
  + drop integrated openoffice.org.ooo79953.dbusinhibitscreensaver.patch
  + drop integrated openoffice.org-2.2.0.ooo74401.basctl.boost.patch

* Fri Aug 03 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.1-18.8
- clarify licenses is use in OOo
- rebuild for new icu
- add workspace.unifysound01,
  + unify all our sound under gstreamer
  + add play button to sound selection fpicker
  + fix type detection for .wavs so they don't open as text files(!)
  + drop openoffice.org-2.0.3.rhXXXXXX.vcl.annoyingbeeps.patch
- add --with-ant-home=/usr/share/ant because something changed and I
  need it now

* Tue Jul 24 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.1-18.7
- Resolves: ooo#79953 inhibit screensaver during presentations
- Resolves: rhbz#249196 propogate font width types up from the font ooo#79878
- Resolves: rhbz#249568 empty line in autocorrect options
- Resolves: rhbz#247632 new text only impress layout

* Thu Jul 19 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.1-18.6
- FC-8 Test 1 Candidate
- Resolves: rhbz#247781 openoffice.org-2.2.1.ooo79481.sw.rowordcount.patch
- better page counting for titlepage dialog

* Mon Jul 10 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.1-18.5
- Resolves: rhbz#245729 openoffice.org-2.2.1.ooo78921.sw.embedded.patch
- update setlangtolocale for prettier fonts when appropiate langpack is missing
- add openoffice.org-2.2.1.oooXXXXX.sw.titlepagedialog.patch

* Tue Jun 26 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.1-18.4
- require new hunspell-ar for arabic langpack
- Resolves: rhbz#244656 overlapping glyphs in pdf export

* Mon Jun 18 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.1-18.3
- add ppc64 uno bridge (workspace.ppc64one.patch)
- Resolves: rhbz#241875 get script detection right for range vs point
  in drawing objects ooo#72349
- Resolves: rhbz#242692 openoffice.org-2.2.1.oooXXXXX.xmloff.outofrange.patch
- Resolves: rhbz#243305 missing xdg file for quickstart restart
- Resolves: rhbz#243904 add openoffice.org-2.2.1.ooo78383.vcl.printxerror.patch
- update stocmerge patch
- add openoffice.org-2.2.1.ooo78392.sixtyfour.tools.patch
- extend selinux patch for ppc64 and sparc

* Sat Jun 15 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.1-18.2
- ppc64 test

* Thu May 31 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.1-18.1
- next 2.2.1 release candidate
- add Jan's stocmerge.all.patch

* Wed May 23 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.1-17.2
- remove LD_LIBRARY_PATH again, the third party extension requiring it 
  links against the wrong libraries
- try and re-disable stlport for selected platforms
- add openoffice.org-2.2.1.ooo73728.desktop.mapped_type.patch fix

* Tue May 22 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.1-17.1
- next 2.2.1 release candidate
- add workspace.cmcfixes34.patch for int(0) not being promoted to long
  NULL in ellipsed methods
- ooo#77470 Because Liberation fonts will be included in >= FC-7 we need
  to set the ms font equivalents as their fallbacks in exported to 
  msoffice format documents so things work out right for ms users

* Fri May 18 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.1-16.1
- 2.2.1 release candidate
- Resolves: rhbz#216332 use cups for all duplex and printer features
- Resolves: rhbz#237110 Dzongkha langpack
- drop integrated workspace.cmcfixes32.patch
- drop integrated openoffice.org-2.2.0.ooo74255.vcl.depth.mismatch.patch
- require Liberation fonts
- enable link optimizations

* Thu May 17 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-14.9
- ooo#77470 Because Liberation fonts will be included in FC-7 we need
  to set the ms font equivalents as their fallbacks in exported to 
  msoffice format documents.
 
* Fri May 04 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-14.8
- Resolves: rhbz#203495 add some magic to allow native and OOo dialogs to
  interleave and keep parent child transient logic correct

* Tue Apr 24 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-14.7
- remove gnome icons seeing as they are redundant
- Resolves: rhbz#231924 Add the hunspell dictionaries requires
- Resolves: rhbz#231924 add remove NatNum1 from bn_IN.xml

* Tue Apr 17 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-14.6
- merge openoffice.org-2.0.2.ooo59127.vcl.honourcairofont.patch
- Resolves: rhbz#235834 update font subpixel logic
- add dynamicsection patch for better offline debugging
- Resolves: rhbz#236671 backup ldmerge

* Wed Apr 11 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-14.5
- Resolves: rhbz#235828 INIFILE optimization breaks addins
- Resolves: rhbz#235325 crash on launch of x86_64 soffice.bin
- finish ld reordering -> apparent 0.4 warm launch improvement
  http://people.redhat.com/caolanm/speed/ldreorder.ods

* Fri Apr 06 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-14.4
- Resolves: rhbz#235341 pdf overlapping characters
- Resolves: rhbz#223190 make a final fallback to a font with a known
  working notdef glyph
- remove openoffice.org-2.2.0.gccXXXXX.solenv.javaregistration.patch
  because gcc 4.1.2-8 should allow our java components to work again.
- add a handful of valgrind fixes

* Tue Mar 27 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-14.3
- Resolves: rhbz#233944 openoffice.org-2.2.0.ooo75790.sc.pa-IN.translate.patch
- add aliases for the english autocorrect files
- drop old themes to save space and need for translations of their names
- combine more DSOs, the speed improvement is not immediately compelling but
  is at least startup time neutral and saves a meg in size for just 
  core + writer
  + http://people.redhat.com/caolanm/speed/CombinedDSO.ods

* Sun Mar 25 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-14.1
- RC4
- follow up on drepper's suggestion of combining startup DSOs into libsoffice
  + http://people.redhat.com/caolanm/speed/CombinedDSO.ods

* Tue Mar 20 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-13.1
- add tango to the themes UI
- yet another rc

* Thu Mar 15 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-12.1
- Resolves: rhbz#232389 enable tango theme
- support xdguserdir translated user dirs
- add alloc debugging library to testtools
- next release candidate

* Mon Mar 12 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-11.2
- Resolves: rhbz#231788 openoffice.org-2.2.0.ooo75301.svtools.eventmismatch.patch

* Wed Mar 07 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-11.1
- yet another release candidate

* Wed Mar 07 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-10.2
- rhbz#206268/ooo#75167 session restore back to the right workspace
- -fno-threadsafe-statics seeing as we're already double locked
  http://people.redhat.com/caolanm/speed/threadsafe-statics.ods
- drop openoffice.org-2.2.0.oooXXXXX.atkthreads.atexit.patch, atk fixed
- add openoffice.org-2.2.0.ooo75190.shell.newrecentlyused.patch, the
  ~/.recently-used location and format changed

* Sun Mar 04 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-10.1
- next release candidate
- drop d_type patch, no perceptable difference in performance 
  http://people.redhat.com/caolanm/speed/d_type.ods

* Wed Mar 02 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-9.2
- jumped the run on requiring extras from a core package, back out for now
- -finline-limit=64 http://blogs.linux.ie/caolan/2007/03/02/finline-limit-and-ooo

* Mon Feb 26 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-9.1
- next release candidate
- add openoffice.org-2.2.0.gccXXXXX.solenv.javaregistration.patch to workaround strange
  gcj component registration problem
- a better fix for the persistant visibility markup problem

* Wed Feb 21 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-8.3
- add workspace.configrefactor01.patch and knock .1 sec off warm start
  http://people.redhat.com/caolanm/speed/configmgr.refactor.ods

* Tue Feb 20 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-8.2
- ooo#74692 64bit form controls

* Mon Feb 19 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-8.1
- next version

* Wed Feb 14 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-7.2
- Resolves: rhbz#228629 mistranslation for properties in or-IN
- drop dictionaries, they're in hunspell-?? now

* Tue Feb 13 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-7.1
- Resolves: rhbz#228254 crash on print to pdf after print to ps
- Resolves: rhbz#227897 long/sal_Int32 mismatch
- need openoffice.org-2.2.0.ooo74401.basctl.boost.patch to build

* Fri Feb 09 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-6.3
- spec cleanups

* Wed Feb 06 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-6.2
- Resolves: rhbz#221214 openoffice.org-2.2.0.ooo74255.vcl.depth.mismatch.patch
- Resolves: rhbz#227224 package the sdk

* Tue Feb 06 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-6.1
- next candidate
- drop integrated openoffice.org-2.2.0.ooo73295.basctl.extraqual.patch
- extra gl and pa-IN help translations

* Mon Feb 05 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-5.2
- Resolves: rhbz#227245 add openoffice.org-2.2.0.oooXXXXX.atkthreads.atexit.patch
- Resolves: rhbz#226737 add openoffice.org-2.2.0.ooo74188.sw.cursorinsideglyph.patch

* Thu Feb 01 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-5.1
- next candidate
- workspace.npower5 integrated
- some valgrind fixes integrated
- Resolves: rhbz#158538 page breaks in calc problem
- pair of build fixes

* Mon Jan 29 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-4.3
- Resolves: rhbz#225061 openoffice.org-2.2.0.ooo73974.bridges.doublereturn.patch
- Resolves: rhbz#225097 library path problems for extensions
- Resolves: rhbz#225143 detect newly added printers

* Sun Jan 28 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-4.2
- fix CUPSManager::initialize

* Sat Jan 27 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-4.1
- next candidate

* Fri Jan 26 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.2.0-3.1
- Resolves: rhbz#224230 mark sofficerc as config file
- Resolves: rhbz#223190 openoffice.org-2.1.0.oooXXXXX.vcl.makenotdefglyph.patch
- Resolves: rhbz#222779 openoffice.org-2.2.0.ooo73863.vcl.imcommit.patch
- start of release candidate
- drop integrated workspace.icuupgrade.patch
- drop integrated workspace.cmcfixes29.patch
- drop integrated workspace.sixtyfour09.patch
- drop integrated workspace.sixtyfour10.patch
- drop integrated workspace.vcl69.patch
- drop integrated workspace.vcl70.patch
- drop integrated workspace.vcl71.patch
- drop integrated workspace.os89.patch
- drop integrated workspace.dr51.patch
- drop integrated workspace.fwk59.patch
- drop integrated workspace.aw024.patch
- drop integrated workspace.dba22b.patch
- drop integrated workspace.impress115.patch
- drop integrated workspace.inplaceobjects.patch
- drop integrated openoffice.org-2.0.4.rh213710.vba.patch
- drop integrated openoffice.org-2.0.4.ooo70779.vcl.setprgname.patch
- drop integrated openoffice.org-2.1.0.ooo73485.vcl.filterzwatrender.patch
- add openoffice.org-2.2.0.ooo73866.javaunohelper.parallel.patch
- add openoffice.org-2.2.0.oooXXXXX.extensions.noxaw.patch
- xt.jar no longer distributed
- some new .sos

* Wed Jan 17 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-6.14
- Resolves: rhbz#222817 openoffice.org-2.1.0.oooXXXXX.vcl.dontsortglyphs.patch

* Mon Jan 15 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-6.13
- Resolves: rhbz#222426 add openoffice.org-2.1.0.ooo73481.svx.longnotint32.patch
- Resolves: rhbz#222423 openoffice.org-2.1.0.ooo73485.vcl.filterzwatrender.patch
- Resolves: rhbz#222420 DejaVu font has two plausible english names

* Thu Jan 11 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-6.12
- Resolves: rhbz#216089 if there is no font at all to handle something

* Sat Jan 06 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-6.11
- Resolves: rhbz#221491 openoffice.org-2.1.0.ooo73201.sw.a11yloadcrash.patch

* Wed Jan 03 2007 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-6.10
- Resolves: rhbz#216094 add workspace.impress115.patch

* Wed Dec 20 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-6.9
- still need openoffice.org-2.1.0.gccXXXXX.basegfx.crash.patch for rh#199870#
- experiment and drop -fno-threadsafe-statics

* Mon Dec 18 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-6.8
- rename and appropiately merge commited patches as their respective workspaces
- drop rh200118.filter.xalanbroken.patch
- try and drop
	+ openoffice.org-2.0.3.gccXXXXX.basegfx.crash.patch
	+ openoffice.org-2.0.4.gccXXXXX.svtools.fsstorage.patch

* Wed Dec 13 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-6.7
- split out english dictionaries into hunspell-en

* Tue Dec 12 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-6.6
- Resolves: rhbz#219161 openoffice.org-2.1.0.ooo72505.vcl.wrongrole.patch

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1:2.1.0-6.5
- rebuild for python2.5

* Tue Dec 07 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-6.4
- Resolves: rhbz#216094 openoffice.org-2.1.0.ooo72349.svx.scriptrange.patch
- Resolves: rhbz#216094 openoffice.org-2.1.0.ooo72350.svx.showsizes.patch

* Tue Dec 05 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-6.3
- Resolves: rhbz#218412 crash on cancel from search view of file chooser

* Sun Dec 03 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-6.2
- hazard some educated guesses as to dictionaries might be acceptable to
  speakers of the same language in neighbouring countries
- Resolves: rhbz#218253 openoffice.org-2.1.0.oooXXXXX.vcl.filterzwatrender.patch

* Fri Dec 01 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-6.1
- next version
- Resolves: rhbz#217813 openoffice.org-2.1.0.ooo72129.vcl.fontglyphindex.patch
- relocate dictionaries

* Wed Nov 29 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-5.5
- Resolves: rhbz#217269/rhbz#190515/rhbz#212134 disable sequence by default

* Tue Nov 28 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-5.4
- drop unneeded openoffice.org-2.0.4.oooXXXXX.solenv.warnnoterror.patch
- Resolves: rhbz#217521 extend grapheme cluster on ranges \u0c01-\u0c03 \u0c41-\u0c44
- use system hunspell

* Tue Nov 28 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-5.3
- rhbz#217361 wrong libjvm on ppc32/ppc64 multiarch installed libgcj's
- rhbz#217490/ooo#72058 don't add underline to preedit if not necessary
- visibility.warning.patch

* Mon Nov 27 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-5.2
- Resolves: rhbz#217321 openoffice.org-2.1.0.ooo72014.officecfg.malayammenu.patch
- Resolves: rhbz#217234 visibility and inline local static data

* Thu Nov 23 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-5.1
- next one
- Resolves: rhbz#217047 i.e.
  replace openoffice.org-2.0.4.ooo.vcl.im_yield.patch with 
  openoffice.org-2.0.4.ooo69992.sw.syncbackspace.patch

* Tue Nov 21 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-4.2
- Resolves: rhbz#216347 openoffice.org-2.1.0.ooo71815.bridges.x86_64.patch
- Resolves: rhbz#216662 stick to a single .desktop launcher name

* Thu Nov 15 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-4.1
- Resolves: rhbz#215511 can't print brochure on landscape mode
- Resolves: rhbz#216089 zoom affecting cjk substitution
- add openoffice.org-2.1.0.ooo71662.dbaccess.noasync.patch

* Wed Nov 15 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-3.1
- next version
- Resolves: rhbz#215694 add openoffice.org-2.0.4.ooo71562.svx.64bitcrash.patch
- Resolves: rhbz#215582 add openoffice.org-2.0.4.ooo71570.psprint.noonecopy.patch
- pt help translated
- ta-IN help translated

* Fri Nov 10 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-2.4
- Resolves: rhbz#214889
- drop using agg
- rebuild for new db4

* Fri Nov 10 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-2.3
- Resolves: rhbz#214896 pt/pt_BR translations
- Resolves: rhbz#214887 pt/pt_BR translations
- Resolves: rhbz#214973 collate print setting

* Tue Nov 07 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-2.2
- Resolves: rhbz#213996 openoffice.org-2.1.0.ooo65491.psprint.enablenups.patch
- Resolves: rhbz#213996 distinguish properly between ppd and cups option
- Resolves: rhbz#213996 openoffice.org-2.1.0.ooo71379.psprint.endfeatureonnewline.patch
- Resolves: rhbz#214773 openoffice.org-2.1.0.ooo61812.svx.a11ycrash.patch

* Tue Nov 07 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-2.1
- next upstream
- drop upstreamed openoffice.org-2.0.3.ooo67976.svx.macroscrash.patch
- drop upstreamed openoffice.org-2.0.3.ooo68018.svx.classpathdialog.patch
- drop upstreamed openoffice.org-2.0.4.ooo70601.sd.sal_uInt32_aslong.patch
- drop upstreamed openoffice.org-2.1.0.ooo71111.sfx2.x86_64.patch
- drop upstreamed workspace.gtkquickstart2.patch

* Mon Nov 06 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-1.2
- Resolves: rhbz#213710 additional application.version vba support
- Resolves: rhbz#214187 openoffice.org-2.0.4.ooo71285.tools.ulongmax.patch

* Thu Nov 02 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.1.0-1.1
- start of 2.1.0
- setlang patch partially upstreamed
- drop upstreamed workspace.vcl66 upstreamed
- drop upstreamed openoffice.org-2.0.4.ooo69325.cairocanvas.slowfills.patch
- drop upstreamed workspace.sixtyfour08.patch
- drop upstreamed openoffice.org-2.0.3.ooo67781.sc.reloadhiddenrows.patch
- drop upstreamed openoffice.org-2.0.3.ooo68047.vcl.zwj.patch
- drop upstreamed workspace.cmcfixes26.patch
- drop upstreamed workspace.vcl65.patch
- drop upstreamed openoffice.org-2.0.4.ooo68851.framework.disablemenuifempty.patch
- drop upstreamed openoffice.org-2.0.4.ooo68919.sc.atk.patch
- drop upstreamed openoffice.org-2.0.4.ooo69068.parallelxslt.patch
- drop upstreamed workspace.cairofixes02.patch
- drop upstreamed openoffice.org-2.0.4.ooo69530.sd.crash.patch
- drop upstreamed workspace.cmcfixes28.patch
- drop upstreamed openoffice.org-2.0.4.ooo69236.slideshow.esccrash.patch
- drop upstreamed workspace.calc39.patch
- drop upstreamed openoffice.org-2.0.4.ooo70361.vcl.atkfilechooser.patch
- drop upstreamed openoffice.org-2.0.4.ooo69620.vcl.atkcombo.patch
- drop upstreamed workspace.fwk53.patch
- drop upstreamed workspace.opensymbol01.patch
- add openoffice.org-2.1.0.ooo71111.sfx2.x86_64.patch
- add workspace.gtkquickstart2.patch
- add workspace.gtkquickstart2.patch
- add openoffice.org-1.9.129.ooo54603.fontconfig.part4.patch for localized
  fontnames
- Estonian dictionaries added

* Wed Nov 01 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.4-5.7
- Resolves: rhbz#213203 openoffice.org.2.0.4.oooXXXXX.i18npool.extendgrapheme.patch
- Resolves: rhbz#212988 try /tmp if /home fails, and abort with a message instead of segv
- Resolves: rhbz#213329 "." from numeric keypad not converted to "," in appropiate locales
- Resolves: (partial) rhbz#213371 openoffice.org.2.0.4.oooXXXXX.i18npool.extendgrapheme.patch
- Resolves: rhbz#212814 openoffice.org-2.0.4.ooo71076.dtrans.64bitdragdrop.patch
- add openoffice.org-2.0.4.ooo71039.svx.purevirtual.patch for bad pure virtual
- add openoffice.org-2.0.4.ooo71077.sc.purevirtual.patch for bad pure virtual
- rebuild for curl

* Mon Oct 23 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.4-5.6
- add openoffice.org-2.0.4.ooo70601.sd.sal_uInt32_aslong.patch
- Resolves: rhbz#211741 add additional de .desktop translations
- Resolves: rhbz#210435 openoffice.org-2.0.4.ooo69620.vcl.atkcombo.patch
- Resolves: rhbz#211949 replace openoffice.org-2.0.4.ooo70388.vcl.setprgname.patch with 
  openoffice.org-2.0.4.ooo70779.vcl.setprgname.patch
- Resolves: rhbz#211969 add openoffice.org-2.0.4.ooo70782.secondaryfpicker.atk.patch
- Resolves: rhbz#212009 add workspace.fwk53.patch
- Resolves: rhbz#212141 add openoffice.org-2.0.4.ooo70835.vcl.minimizealerts.patch
- add my experimental openoffice.org-2.0.4.ooo70155.fasterhelplinking.patch to knock 
  a few hours of the build, might result in wrong help indexing

* Thu Oct 12 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.4-5.4
- add openoffice.org-2.0.4.ooo70361.vcl.atkfilechooser.patch for rh#210440#
- add openoffice.org-2.0.4.ooo70388.vcl.setprgname.patch for rh#210441#

* Fri Oct 06 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.4-5.3
- add openoffice.org-2.0.4.ooo69992.vcl.im_yield.patch for rh#208537#
- add workspace.cmcfixes28.patch for rh#208966#
- add openoffice.org-2.0.4.ooo70064.sc.crashonalignment.patch for rh#208888#

* Thu Sep 28 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.4-5.1
- add openoffice.org-2.0.4.ooo69780.goodies.hugetile.patch for rh#207226#
- add openoffice.org-2.0.4.ooo69530.sd.crash.patch for stupid crash in
  impress wizard
- rh#206615# supporting trailing ZWJ in fallback blocks
- rh#207856# .ppt import line spacing fix ooo#69841#
- rh#206177# cancelling slideshow transistion crash ooo#69236#
- add openoffice.org-2.0.4.ooo69905.sd.casting.patch

* Tue Sep 19 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.4-4.2
- add openoffice.org-2.0.4.gccXXXXX.svtools.fsstorage.patch to work
  around fsstorage crash apparently triggered by gcc -Os change

* Fri Sep 15 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.4-4.1
- ooo#69585# x86_64 svtools database crasher
- fix rh#206264# 16bit .ppt load crash
- ooo#69653# 64bitscaling chart2 display fix

* Tue Sep 04 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.4-3.1
- add workspace.cairofixes02.patch for some cairocanvas fixing
- add openoffice.org-2.0.4.ooo69325.cairocanvas.slowfills.patch to
  fix the real real slow cairo canvas on my laptop
- rh#203872# -> openoffice.org-2.0.4.ooo69051.vcl.singlekeypress.patch
- add pseudoworkspace.valgrind1.patch with various valgrinded leaks

* Mon Aug 28 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.4-2.2
- rh#203063# Glyph replacement work when single run has multiple fonts
- rh#204173# Crash on Glyph replacement when single run has single glyph
  for multiple character positions

* Fri Aug 25 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.4-2.1
- fix openoffice.org-2.0.4.ooo68369.dtrans.crash.patch
- fix openoffice.org-2.0.4.ooo68805.sw.ww8size.patch
- fix openoffice.org-2.0.4.ooo68822.sw.recursiveim.patch
- fix potential out of bounds in xmlhelp
- drop openoffice.org-2.0.3.oooXXXXX.atkbroken.vcl.patch, fixed in gnome now
- rh#203497# -> openoffice.org-2.0.4.ooo68851.framework.disablemenuifempty.patch
- rh#203439# -> openoffice.org-2.0.4.oooXXXXX.vcl.x86_64.impressatk.patch
- rh#203063# -> openoffice.org-1.9.129.ooo54603.fontconfig.part3.patch

* Thu Aug 10 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.4-1.1
- rh#201447# -> openoffice.org-2.0.3.ooo68339.vcl.maskingtoomanybytes.patch
- rh#201305# -> openoffice.org-1.9.115.ooo51931.fixxmlsec.patch
- add openoffice.org-2.0.3.ooo68383.evo28support.patch for new evo
- clear font customization as fontconfig now has it's defaults the way we need
- clear gengal rdb removal, ooo#65361# fixed
- drop integrated workspace.targetedaot
- drop integrated workspace.bfsixtyfour
- drop integrated workspace.thbpp4
- drop integrated workspace.vcl59
- drop integrated workspace.vcl60
- drop integrated workspace.fwk40
- drop integrated workspace.sixtyfour06
- drop integrated workspace.kendy10
- drop integrated workspace.impress96
- drop integrated workspace.gcjsix
- drop integrated workspace.vcl63
- drop integrated workspace.os84
- drop integrated workspace.configure18
- drop integrated ooo65327.builddep.writerperfect.patch
- drop integrated ooo67337.sfx2.dontshowbuttons.patch
- add openoffice.org-2.0.4.ooo68665.x86_64gcj.jvm.patch

* Tue Aug 08 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-7.9
- icu settext ownership of string data changed silently

* Mon Jul 31 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-7.8
- add openoffice.org-1.9.129.ooo54603.fontconfig.part2.patch
- rh#200703# -> openoffice.org-2.0.3.ooo67976.svx.macroscrash.patch
- rh#200874# -> openoffice.org-2.0.3.ooo68018.svx.classpathdialog.patch
- rh#200728# ->
	+ openoffice.org-2.0.3.ooo68047.vcl.zwj, don't drop zero width joiner
	+ openoffice.org-2.0.3.ooo68048.vcl.imsurroundtext, a bizarre, but
	perfectly functional input method surrounding text implementation
	based on the ATK bridge
- rh#200805# replace ooo58663 missing glyph patch -> workspace.icuupgrade
- rh#201143# more Indian langpacks
- rh#201305# digital signature compile flags mismatch
- 2.0.4+ accepted
	+ ooo#66510# recentlyused fix -> workspace.kendy10
	+ ooo#66067# embeddedobj crash -> workspace.fwk40
	+ ooo#65519# samba printing ->> workspace.fwk40
	+ ooo#59997# defaultbullets -> workspace.opensymbol01
	+ ooo#65081# switch layout -> workspace.os84
	+ ooo#65308# notes paste -> workspace.impress96
	+ ooo#19976# nofocussteal -> workspace.inplaceobjects
	+ ooo#65318# agg24 -> workspace.thbpp4.patch
	+ ooo#65767# menu key -> workspace.vcl60.patch
	+ ooo#66851# x86_64 i18npool ->> workspace.sixtyfour06
	+ ooo#67656# tabdialogs minimize -> workspace.vcl63
	+ ooo#67750# dont expand title -> workspace.pb17
	+ ooo#67750# dont expand title ->> workspace.pb17

* Wed Jul 26 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-7.7
- rh#200207# -> openoffice.org-2.0.3.ooo67779.svx.toolbarcrash.patch
- rh#200194# -> openoffice.org-2.0.3.ooo67793.sw.stickymenu.patch
- rh#199056# -> openoffice.org-2.0.3.ooo67829.dtrans.64bitpaste.patch
- rh#200042# -> openoffice.org-2.0.3.ooo65081.sw.layout.patch
- rh#200193# -> openoffice.org-2.0.3.ooo67781.sc.reloadhiddenrows.patch
- rh#200369# help build glitch
- drop openoffice.org-2.0.3.oooXXXXX.all.ODR.anonymousmembers.patch
- drop openoffice.org-2.0.3.oooXXXXX.sal.importvisibilityasexported.patch
- require dejavu-lgc-fonts, Greek coverage problems begone
- rh#200512# South African translations
- move to firefox-devel instead of mozilla-devel, --with-firefox
	+ add workspace.configure18.patch

* Thu Jul 20 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-7.6
- rh#199535# presentation templates duplicated in zh-CN
- rh#199664# -> openoffice.org-2.0.3.ooo67644.sw.spacing.patch, dialog spacing
- rh#199659# -> openoffice.org-2.0.3.ooo67656.vcl.tabdialogsminimize.patch
- rh#199665# -> openoffice.org-2.0.3.ooo67658.sfx2.reloadcrash.patch
- rh#199894# -> openoffice.org-2.0.3.ooo67716.svx.overflow.patch
- rh#199870# ->openoffice.org-2.0.3.gccXXXXX.basegfx.crash.patch
- rh#199907# -> openoffice.org-2.0.3.ooo67740.xmlhelp.doublefree.patch
- rh#200059# -> openoffice.org-2.0.3.ooo67337.sfx2.dontshowbuttons.patch
- rh#200055# -> openoffice.org-2.0.3.ooo67750.sfx2.dontexpandtitle.patch
- drop openoffice.org.2.0.3-gcc28409.anonymousexternc.patch
- drop openoffice.org-2.0.3.gccXXXXX.svtools.R_X86_64_PC32.patch
- add openoffice.org-2.0.3.oooXXXXX.jvmfwk.futureproof.patch to preempt new libjvm for gcj
- see if we can drop openoffice.org-2.0.3.gccXXXXX.svtools.R_X86_64_PC32.patch
- reenable visibility support
- add openoffice.org-2.0.3.rh200118.filter.xalanbroken.patch to work around the new
  xalan problem

* Wed Jul 17 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-7.5
- add openoffice.org.2.0.3.ooo66510.shell.recentlyused.patch
- add openoffice.org-2.0.3.rh187919.gtkunderkde.patch
- add openoffice.org-2.0.3.ooo67186.sw.eventisULONG.patch
- add ooobuild.VBAObjects.patch for VBA macro support
- fix use of freetype headers for new freetype
- rebuild for new tasty linker hash/new compiler
    + add openoffice.org.2.0.3.gcc28370.statics.patch to workaround gcc28370
	-> drop with 4.1.1-8
    + add openoffice.org.2.0.3.gccXXXXX.anonymousexternc.patch for namespace { extern "C" ... }
    + add openoffice.org-2.0.3.oooXXXXX.all.ODR.anonymousmembers.patch to 
        workaround strict gcc ODR anon namespace handling
    + what gcc "visibility" means has changed significantly, futile to update OOo to work with 
      it anymore, most unfortunate :-(
    + add openoffice.org-2.0.3.oooXXXXX.sal.importvisibilityasexported.patch to import
    visibility the same as exported anyway

* Thu Jun 28 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-7.4
- final 2.0.3 version
- rh#196123# add openoffice.org-2.0.3.ooo66851.i18npool.x86_64.patch
- add openoffice.org.2.0.3-ooo66018.cppuhelper.dangerousvisibility.patch as visibility(?)
  workaround
- add openoffice.org-2.0.3.rhXXXXXXvcl.annoyingbeeps.patch to *SHUT UP* the
  damn needy msgboxes before I loose control and go kill something cute and fluffy
- from the gtk print dialog, when printing to pdf, pick some defaults and just do
  it, don't use the pdf options dialog.

* Tue Jun 27 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-7.1
- next milestone
- track down vor and sdw crashes to some gcc problem with static initializers, 
	failed to be able to find a standalone testcase though :-( => workaround
- add workspace.sixtyfour06.patch for x86_64 stability

* Thu Jun 22 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-6.1
- next milestone
- drop hack and use new gtk_print_unix_dialog_set_manual_capabilities api instead
- readjust printing stuff for new "print to file" mechanism

* Wed Jun 07 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-5.3
- rh#185806# update croatian dictionaries, and add spanish, norwegian thesaruses
(thesari?) etc
- rh#193918# add openoffice.org.2.0.3.ooo66067.embeddedobj.crash.patch
- rh#193776# add openoffice.org.2.0.3.ooo66018.linguistic.vorcrash.patch

* Fri Jun 02 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-5.2
- fontcache problem

* Mon May 29 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-5.1
- 2.0.3 RC5

* Mon May 29 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-4.1
- 2.0.3 RC4
- add openoffice.org-2.0.3.ooo65852.vcl.a11ywizard.patch for rh#193246#

* Wed May 24 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-3.2
- enable lockdown functionality, fix crash on ESC on right click submenus
- re-enable "Reverse" on print dialog, it's a cups option

* Tue May 23 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-3.1
- 2.0.3 RC3
- rh#191650# add openoffice.org-2.0.2.oooXXXXX.vcl.honourcairofont.patch
- rh#192588# don't use the cairo canvas by default

* Fri May 19 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-2.1
- 2.0.3 RC2
- drop rvpapi module
- experimental new gtk print dialog

* Thu May 18 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-1.2
- 2.0.3 RC1
- rh#191689# well fine so!, anonymous EXEC mapping is verboten altogether,
  reimplement three UNO bridges arch with the double file mmap pattern
- add openoffice.org-2.0.3.oooXXXXX.vcl.removemenukey.patch for rh#192172#

* Mon May 15 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-0.169.5
- rh#191689# re-add openoffice.org-2.0.3.oooXXXXX.selinux.bridges.patch 
  the upstreamed replacement alloc/mprotect pattern still leaves writable 
  executable mem

* Mon May 15 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-0.169.4
- ooo#65361# remove gengal.rdb
- ooo#61767# remove oo_product.bmp
- add workspace.vcl59.patch
    + openoffice.org-2.0.3.ooo65304.sn.vcl.patch merged into vcl59
- add openoffice.org-2.0.3.oooXXXXX.atkbroken.vcl.patch for rh#191621#
    + upstream atk version check doesn't seen to work

* Fri May 12 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-0.169.2
- ta_IN translations integrated
- add openoffice.org-2.0.3.ooo65327.builddep.writerperfect.patch
- add openoffice.org-2.0.3.ooo65330.samba.fpicker.patch

* Fri May 12 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-0.169.1
- add openoffice.org-2.0.3.ooo65304.sn.vcl.patch for rh#191155#
- add openoffice.org-2.0.3.ooo65308.notespaste.sd.patch for rh#191333#
- drop integrated openoffice.org-2.0.3.ooo65052.bridges.makeasmpic.patch

* Fri Apr 28 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.3-0.168.1
- 2.0.3 preview builds
- enable cairo canvas
- disable useless ldap backend
- drop integrated workspace.jaxpapi.patch
- drop integrated workspace.evo2fixes.patch
- drop integrated workspace.dmake43p01.patch
- drop integrated workspace.systemjava
- drop integrated workspace.atkbridge.patch
- drop integrated openoffice.org-2.0.1-ooo59675.sysui.rtfmimetype.patch
- drop integrated openoffice.org-2.0.2.ooo34909.dbaccess.patch
- drop integrated openoffice.org-2.0.2.ooo61875.sd.compile.patch
- drop integrated openoffice.org-2.0.2-ooo61841.vcl.honourfontconfigoverrides.patch
- drop integrated openoffice.org-2.0.2.ooo62030.solenv._version.patch
- drop integrated openoffice.org-2.0.2.oooXXXXX.config_office.noppds.patch
- drop integrated openoffice.org-2.0.2.ooo63155.sfx2.badscript.patch
- drop integrated openoffice.org-1.9.120.ooo52428.execshield.bridges.patch
- drop integrated openoffice.org-1.9.130.ooo54959.negativeindent.sw.patch
- drop integrated openoffice.org-2.0.2.ooo64743.vcl.adjustonlevel1.patch
- drop some integrated dictionary components
- add workspace.bfsixtyfour.patch
- add openoffice.org-2.0.3.gccXXXXX.svtools.R_X86_64_PC32.patch workaround
- add openoffice.org-2.0.3.ooo65052.bridges.makeasmpic.patch

* Thu Apr 27 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.2-5.13
- rh#189630# lfs trouble

* Tue Apr 25 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.2-5.12
- ooo#64743# continuing my epic battle with CJK and Indic glyph
  fallback (rh#189760#)
- ooo#64726# "untranslate" bengali keyboard shortcuts (rh#189760#)

* Mon Apr 24 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.2-5.11
- ooo#64063# Finally 2.0.X Tamil translation updates

* Tue Apr 18 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.2-5.10
- ooo#64463# don't require Xaw for the use mozilla plugins (e.g flash)
  in OOo feature
- ooo#64508#/rh#189061# honour fontconfig hinting settings

* Wed Apr 12 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.2-5.9
- rh#187939# not detecting changes to CUPS printers during execution
- rh#188467# set printer font-handling defaults
- ooo#59997# opensymbol font metrics changed
- rh#161530# new South African locales exist in glibc now

* Mon Apr 10 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.2-5.8
- rh#188053# more a11y fixes
- ooo#63583# committed to workspace.atkbridge

* Wed Mar 29 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.2-5.7
- rh#186747# TTF conts converted to Type 1 in print to file ps

* Tue Mar 28 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.2-5.6
- more rh#186215#/ooo#63583# accessibility fixes
- better fallback to english if help is missing

* Fri Mar 24 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.2-5.5
- rh#186515# Keep draw and math launchers for mimetypes
- rh#186215#/ooo#63583# accessibility crasher in impress

* Mon Mar 13 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.2-5.4
- ooo#59997# replacement opens___.ttf updated
- drop integrated openoffice.org-2.0.0.ooo56651.sw.rtfcrash.patch
- drop integrated openoffice.org-1.9.114.ooo51718.rpath.patch
- add openoffice.org-2.0.2.ooo63155.sfx2.badscript.patch for rh#185390#
- rh#181900# rename Bengali langpack
- drop pagein swappiness foo
- drop nearly 9 megs of afms and ppds

* Fri Mar 10 2006 Bill Nottingham <notting@redhat.com> - 1:2.0.2-5.2
- rebuild for PPC TLS issue (#184446)

* Sat Feb 25 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.2-5.1
- hunspell replaces myspell
- Catalan help documentation available
- add sestatus details to crash_reporter
- nl_NL dictionaries upstreamed
- hu_HU dictionaries upstreamed
- workspace.epspreview.patch integrated
- workspace.dbwizardpp1.patch integrated
- workspace.cmcfixes20.patch integrated
- workspace.cmcfixes21.patch integrated
- workspace.cmcfixes22.patch integrated
- workspace.cmcfixes23.patch integrated
- workspace.gcc41.patch integrated
- workspace.sb41.patch integrated
- workspace.systemagg.patch integrated
- workspace.hro02.patch integrated
- openoffice.org-1.9.96.ooo35641.noxfonts.vcl.patch integrated
- openoffice.org-2.0.1.ooo58618.sfx2.interactionhandler.patch integrated
- openoffice.org-2.0.1.ooo58798.parallel.patch integrated
- openoffice.org-2.0.1.ooo59537.config_office.nss.patch integrated
- openoffice.org-2.0.1.ooo59666.vcl.animatedtheme.patch integrated
- openoffice.org-1.9.125.ooo54040.savecrash.svtools.patch integrated
- openoffice.org-2.0.1.ooo61098.vcl.readonlyentry.patch integrated
- openoffice.org-2.0.2.ooo61178.ucb.neon25.patch integrated
- drop openoffice.org-1.9.125.ooo54586.nfslock.sal.patch
- drop openoffice.org-1.9.112.ooo50857.gtkslowunderkde.vcl.patch
- drop openoffice.org-1.9.88.NONE.gcc3gcj4.patch
- drop empty sandbox.jar
- deliver link flag syntax changed
- new workspace.jaxpapi.patch
- replace fasterhelpcontent2.patch with workspace.targetedaot.patch
- replace ooo52974.systemhsqldbbeanshell.patch and oooXXXXX.systemxalan.patch 
  with workspace.systemjava.patch
- rh#178670# drop PROT_EXEC
- add openoffice.org-2.0.2-ooo61841.vcl.honourfontconfigoverrides.patch for rh#179692#
- add openoffice.org-2.0.2.ooo62030.solenv._version.patch
- rh#181876# update workspace.atkbridge.patch
- update and split evo patches to match upstream segmentation
- ooo#62318# mozab not available with system mozilla

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:2.0.1.1-11.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:2.0.1.1-11.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 06 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1.1-11
- rh#180125# unnecessary gnome mime files

* Thu Feb 02 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1.1-10
- reshuffle bridge patch
- reimplement lang from locale patch

* Fri Jan 27 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1.1-9
- add openoffice.org-2.0.2.ooo61178.ucb.neon25.patch for neon 0.25.X
- missing defattr(-,root,root)
- rh#179256# if java fails (i.e. was configured to use libgcj.so.6) reconfigure
  to pick up libgcj.so.7
- rh#177205# add some templates, including a fedora themed presentation

* Thu Jan 26 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1.1-8
- rh#178971# defer exec mem until bridge code

* Tue Jan 17 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1.1-7
- rh#177933# add Serbian sr_CS language pack
- rh#178002# af_ZA dictionary in wrong encoding

* Fri Jan 13 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1.1-6
- rh#177669# icons s/test -f/test -d/ :-)

* Wed Jan 04 2006 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1.1-5
- spinbutton factory needs to be uneditable as well as combobox
- add openoffice.org-2.0.1-ooo19976.framework.nofocussteal.patch for jrb

* Thu Dec 22 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1.1-4
- add openoffice.org-2.0.1-ooo59997.sw.defaultbullets.patch for rh#176779#

* Thu Dec 22 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1.1-3
- gcc#25426# fixed
    + reenabled workspace.jaxpapi.patch
    + reenabled fasterhelpcontent2.patch
- add openoffice.org-2.0.1-ooo59675.sysui.rtfmimetype.patch for rh#176259#
- gcc#19870# still busted, accesser hack returns

* Wed Dec 21 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1.1-2
- add openoffice.org-2.0.1.oooXXXXX.vcl.animatedtheme.patch for animated
  theme problem

* Thu Dec 15 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1.1-1
- gcc#25199# fixed, drop bitfield patch
- gcc#25389# fixed, drop jurt.nullpointer.patch
- gcc#25426# identified, crash with jaxpapi patch
- addressbooks
	a) evo1 addressbook removed, as only evo2 required
	b) mozilla addressbook removed, utterly useless
	c) evo2 ldap addressbook added to give some sort of ldap access
	d) patch wizard UI to show available addressbook backends
- add openoffice.org-2.0.1.oooXXXXX.config_office.nss.patch
- upstream cocks up their numbering

* Tue Dec 13 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1-145.3
- system agg

* Fri Dec 08 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1-145.2
- gcc 4.1 rebuild
- disable workspace.jaxpapi.patch for now
- disable fasterhelpcontent2.patch for now
- rh#175272# openoffice.org-2.0.1.ooo59129.vcl.readonlyentry.patch
- gcc#25389# File(new URI("file:./")) regression

* Thu Dec 08 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1-145.1
- next version

* Thu Dec 08 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1-144.1
- openoffice.org-2.0.1.rh175242.connectivity.mozab.patch, provide mozilla
  address backend despite http://bugzilla.mozilla.org/show_bug.cgi?id=135137

* Mon Dec 05 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1-143.3
- default to evo2 as address book
- add workspace.sb41.patch for gcc 4.1 support
- add libgcj.so.7 to jvm providing jvmfwk lib list (workspace.cmcfixes23)

* Fri Dec 02 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1-143.2
- subtle build breakage

* Fri Dec 02 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1-143.1
- 2.0.1 RC2

* Thu Dec 01 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1-0.142.4
- rh#174664# right click spellcheck came unstuck

* Tue Nov 29 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1-0.142.3
- workaround for illadvised last minute "interaction handler" workspace merge

* Tue Nov 29 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1-0.142.2
- rh#174147# openoffice.org-2.0.1.oooXXXXX.vcl.missingglyph.patch
- rh#174148# openoffice.org-2.0.1.ooo58606.sw.pre-edit.patch
- openoffice.org-1.9.87.warnnoterroronmissing.patch not going to be upstreamed

* Thu Nov 17 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1-0.142.1
- next version
- rh#173775# crash on help under some circumstances

* Thu Nov 17 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1-0.141.1
- next version
- hi-IN translations upstreamed
- loads of translated help

* Tue Nov 15 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1-0.140.1
- drop integrated workspace.oooemailmerge.patch
- drop integrated workspace.javapatch.patch
- drop integrated workspace.systemlibxmlfix.patch

* Wed Nov 08 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1-0.139.1
- drop integrated openoffice.org-1.9.108.ooo47323.binfilter.stupiddetect.patch
- openoffice.org-1.9.97.ooo48600.rtfparseerror.svx.patch -> javapatch
- drop integrated openoffice.org-1.9.112.ooo53025.exception.package.patch
- gcc#22132# fixed
	+ drop openoffice.org-1.9.84.ooo44843.sdcasting.patch
	+ drop openoffice.org-1.9.84.ooo44846.svxcasting.patch
	+ drop openoffice.org-1.9.84.ooo45162.svxcasting2.patch
- workaround deprecated openldap api usage
- add industrial set of icons

* Wed Nov 08 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1-0.138.3
- fix problem with icu rule searching with null locale

* Fri Nov 04 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.1-0.138.1
- drop integrated openoffice.org-1.9.74.ooo41875.mktemp.patch
- drop integrated openoffice.org-1.9.89.ooo35627.parallel.cppumaker.patch
- drop integrated openoffice.org-1.9.97.ooo48610.searchalltemplates.wizards.patch
- drop integrated openoffice.org-1.9.106.ooo50172.icu.tamilvowelslikepango.patch
- drop integrated workspace.vcl39.patch
	- CACHE_MAGIC of rh2 changed back to default 2. No broken caches of "2" 
        should exist to cause ambiguity
- drop integrated openoffice.org-1.9.108.ooo48814.solenv.nostripwithsimpleinstall.patch
- drop integrated openoffice.org-1.9.122.ooo52626.workspacerestore.vcl.patch
- drop integrated workspace.impress57.patch
- drop integrated workspace.gslpatches6.patch
- drop integrated workspace.emblock1.patch
- drop integrated workspace.cmcfixes18.patch
- drop integrated workspace.cmcfixes19.patch
- add workspace.systemlibxmlfix.patch
- additional hungarian help

* Fri Oct 28 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.0-3.8
- ooo#53397# SEGV signal installation needs to be extended to include 
  custom application launcher names
- reenable faster helpcontent2 building

* Fri Oct 28 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.0-3.7
- rh#171918# wrong LDAP stuff gets launched from wizard
- upstream patches as cmcfixes20
- rh#171844# make another stab at the klipper problem
- ooo#57107# updated hindi translation
- rh#171692# be less of a gcj bigot
- rh#172149# need more stuff in the classpath for macro creating

* Fri Oct 14 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.0-3.6
- rh#171425#/ooo#56536# weird SwTxtNode is not a SwTxtNode problem

* Fri Oct 14 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.0-3.5
- get RPM_OPT_FLAGS in operation minus -fasynchronous-unwind-tables

* Fri Oct 14 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.0-3.1
- release candidate 3
- alias en_US thesasurus for other en varients
- can crash on empty thesasurus rh#170091#/ooo#55603#
- drop thesaruses not in new format

* Thu Oct 06 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.0-2.1
- release candidate 2
- workspace.cmcfixes17 integrated

* Thu Sep 29 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.0-1.2
- add mmeeks workspace.atkbridge for rh#169323# acessibility

* Mon Sep 26 2005 Caolan McNamara <caolanm@redhat.com> - 1:2.0.0-1.1
- release candidate 1

* Thu Sep 22 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.130-2
- add openoffice.org-1.9.130.ooo54959.negativeindent.sw.patch
- add openoffice.org-1.9.130.ooo54708.sc.patch
- workaround for gcc#22132# for rh#168537#
- alternative parallel cppumaker problem fix
- build against system db4 
      -> java api is different, fix that
- build against system xalan
      -> that's as small as OOo gets until gcc#19664# get fixed
      or someone figures out how to use system rhino
- add workspace.cmcfixes19.patch
- remove dictooo wizards menus which aren't actually available

* Thu Sep 14 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.130-1
- next version
- drop integrated .ooo53699.unzipunused.postprocess.patch
- add openoffice.org-1.9.130.ooo54692.fasterhelpcontent2.patch

* Wed Sep 14 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.129-3
- track nfs bug id change
- ooo#54514# save as .doc self-inflicted failure

* Tue Sep 13 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.129-2
- fix icu usage

* Tue Sep 13 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.129-1
- next version
- build against external icu

* Thu Sep 08 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.128-2
- busted translation
- force gcj as java solution, that's the only JVM I want to support
- openoffice.org-1.9.112.ooo51724.gcc21020.testtools.patch fixed in gcc
- make a different stab at fixing klipper related embedded object hang 
  for rh#166950#

* Wed Sep 07 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.128-1
- next version
- SISSL is retired, now LGPL only
- swap workspace.cmcfixes17.patch for .rhXXXXXX.noexpandfpicker.desktop.patch
  as upstream agrees on rh default for fpicker
- drop integrated openoffice.org-1.9.114.oooXXXXX.nostlport.patch
- more translated help documentation
- new langpack
- add mutexhang patch for rh#166950#

* Wed Aug 31 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.127-1
- bump to next version
- ooo#53956# thai dictionary
- remove unslightly warning from gnomeprint
- replace sablot with libxslt i.e. help application
- add workspace.impress57.patch for rh#167130#
- add plausible .ooo54040.savecrash.svtools.patch fix for rh#167178#
- drop integrated workspace.cmcfixes15.patch
- drop integrated workspace.cmcfixes16.patch
- split and upstream font additions
- add openoffice.org-1.9.127.gcc23691.slideshow.patch boost workaround

* Sat Aug 27 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.126-1
- next version
- drop integrated workspace.gslpatches4.patch
- build with FORTIFY_SOURCE

* Fri Aug 26 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.125-5
- parallel langpack installing

* Thu Aug 25 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.125-4
- add workspace.cmcfixes16.patch for export dialog problem
- rh#166812# crash on keyboard customization save

* Tue Aug 23 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.125-3
- use only underlying toolkit startup notification
- use proper nfslock fix
- workspace.cmcfixes15.patch, no MathMLDTD or msfontextract foo
- openoffice.org-1.9.125.oooXXXXX.bulletexport.vcl.patch

* Mon Aug 22 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.125-2
- rh#166432# add README to he_IL dictionary
- rh#166290# print range not properly available in gnomeprintui
- flr moves inhalt patch into javafilter workspace

* Wed Aug 17 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.125-1
- beta2
- drop integrated workspace.cmcfixes14.patch
- drop integrated ooo46585.sunmiscisnotstandard.filter.patch
- drop integrated ooo30133.lingucomponent.ukrainean.patch
- drop integrated ooo53026.selinux-pipegiveup.desktop.patch

* Wed Aug 17 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.124-3
- rh#166102# pspfontcache format problem hang on start
- rebuild for new cairo

* Mon Aug 15 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.124-2
- experiment with jakub's suggestion for prelink based optimization
  intermediate library and binaries

* Mon Aug 15 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.124-1
- drop integrated workspace.fpicandrpath.patch

* Wed Aug 10 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.123-3
- recombine into workspace.cmcfixes14.patch
- use configimport rather than patches for customization

* Mon Aug 08 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.123-1
- use system beanshell
- drop integrated workspace.cmcfixes12
- drop integrated ooo51736.xsltproc.evenwithjava.patch
- drop integrated ooo51745.cpputools.patch
- drop integrated ooo51755.scp2.parallel.patch
- drop integrated ooo51774.rsc.parallel.patch

* Fri Aug 05 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.122-4
- session management and workspace restore corrections
- add openoffice.org-1.9.112.oooXXXXX.exception.package.patch for rh#165197#

* Wed Aug 03 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.122-3
- ooo#52626# sessionmanagement and vclplug problem
- ooo#52786# czech 8bit msword doc import problem
- disable internal hsqldb 1.80.1 and use the rawhide system one now
  that it has been bumped to that version

* Tue Aug 02 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.122-1
- next version

* Tue Aug 02 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.121-4
- return of ppc

* Wed Jul 27 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.121-3
- add rh#164310# pipe giveup
- add openoffice.org-1.9.121.ooo52542.emptyrtfframes.sw.patch for rh#161313#

* Tue Jul 26 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.121-2
- rh#127576# add libgnomeprintui 
- make database front end into pseudo subpackage
- replace patches with combined workspace.gslpatches4
- add rh#156677# menu changes

* Mon Jul 25 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.121-1
- next version

* Sat Jul 23 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.120-3
- add openoffice.org-1.9.120.rh158977.execshield.bridges.patch
- workaround gcj accessor problem on a global basis

* Sat Jul 23 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.120-2
- try and reenable ppc building

* Thu Jul 20 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.120-1
- drop redundant workspace.dummywebwizard.patch

* Thu Jul 20 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.119-2
- re-experiment with execshield GNU_STACK non X

* Wed Jul 20 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.119-1
- experiment with security flags
- drop integrated cmcfixes11.workspace
- drop integrated openoffice.org-1.9.113.ooo51385.bridges.stack.patch
- drop integrated openoffice.org-1.9.118.ooo52061.recursive.animations.patch

* Sat Jul 16 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.118-1
- add experiemental rh150643.fontconfigalwayssystemfont.vcl.patch
- drop integrated workspace.impress63.patch
- drop integrated workspace.mh19104.patch
- rh#163554# due to #i41296# missing FormWizard stuff

* Fri Jul 15 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.117-2
- add openoffice.org-1.9.117.ooo52023.evoadb2.nognuconst.patch to
  fix evoab2
- add openoffice.org-1.9.117.ooo52048.inhalt.sw.patch as minor .doc
  export regression fix for rh#158252#
- split email mailmerge stuff into a subpackage to avoid python
  dependancy on writer

* Wed Jul 13 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.117-1
- bump to next version and drop the integrated (finally) fpicker patch
- back to using stlport for now because I'm dubious
- rh#162984# fallbacks from en_AU to en_GB for wizards
- rh#160783# set a targetname for font when it's found
- add openoffice.org-1.9.117.rh163147.thorndale.fontconfig.patch
- add openoffice.org-1.9.117.ooo51912.nullpointer.wizards.patch for
  rh#161173#

* Mon Jul 11 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.116-3
- enable evo addressbook in addressbook wizard
- rh#162875# extra leading / from file picker
- update fpicker stuff
- add workspace.impress63.patch for rh#162158#
- add openoffice.org-1.9.116.rh162935.gccXXXXX.weirdcrash.patch as a temporary
  workaround until I figure out just what the hell is wrong

* Mon Jul 11 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.116-2
- add openoffice.org-1.9.116.ooo51774.rsc.parallel.patch

* Sat Jul 09 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.116-1
- bump to new version, Hamburg burning the midnight oil apparently
- add openoffice.org-1.9.115.ooo51755.scp2.parallel.patch
- drop integrated openoffice.org-1.9.111.ooo51091.exportgcjsymbolname.jvmaccess.patch

* Fri Jul 08 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.115-3
- in rawhide we should be able to use system-xmlsec1 now with 
  system-xmlsec patch

* Thu Jul 07 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.115-2
- add openoffice.org-1.9.115.oooXXXXX.audio.withoutnas.patch
  and disable worthless nas/portaudio/sndfile stuff
- add openoffice.org-1.9.115.oooXXXXX.xsltproc.evenwithjava.patch
  and see if we can build faster with xsltproc

* Thu Jul 07 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.115-1
- bump to next version
- add openoffice.org-1.9.115.ooo51673.printing.checkerror.patch
- rpath of ORIGIN complete, enable failure on regression
- drop integrated openoffice.org-1.9.114.ooo50745.cruxcrash.vcl.patch

* Mon Jul 04 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.114-2
- further split langpacks
- modify test for $ORIGIN rpaths
- rh#161886# 
    + openoffice.org-1.9.114.oooXXXXX.rpath.patch
    + openoffice.org-1.9.114.rh161886.rpath.desktop.patch
- add openoffice.org-1.9.114.ooo50745.cruxcrash.vcl.patch for rh#160293#
- add openoffice.org-1.9.114.ooo51637.solenv.pyuno.patch to workaround
  multiple pyuno registering failures
- add openoffice.org-1.9.114.ooo51638.mailmerge.patch to provide email
  support for maill merge
- add openoffice.org-1.9.114.oooXXXXX.nostlport.patch and not build
  stlport

* Mon Jul 04 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.114-1
- bump to next version

* Thu Jun 30 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.113-1
- bump to new version
- translations merged, drop translation sources
- hsqldb bumped to version with working build.xml, drop sources
- add patch to work around notorious gcc19870 for hsqldb
- indic font fallbacks now in upstream
- openoffice.org-1.9.92.oooXXXXX.addindic.patch integrated

* Wed Jun 29 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.112-2
- wrong userdir
- allow fallbacks for translations with partial support file coverage
- rh#160301# tweak fontconfig patch to ignore opensymbol/starsymbol

* Mon Jun 27 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.112-1
- bump to next version
- add openoffice.org-1.9.112.ooo50875.gtkslowunderkde.vcl.patch for rh#157158#

* Tue Jun 21 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.111-1
- bump to next version
- drop integrated openoffice.org-1.9.87.ooo50575.fragments.patch
- add openoffice.org-1.9.111.ooo51091.exportgcjsymbolname.jvmaccess.patch
  to export differently named symbols under gcj
- try to workaround hsqldb problems with itself and with gcj

* Thu Jun 16 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.110-1
- bump to next version
- drop integrated workspace.gcc4fwdecl.patch
- need a openoffice.org-1.9.110.oooXXXXX.psprintfriend.patch

* Wed Jun 14 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.109-6
- drop unnecessary Require
- rh#160302# skip fontconfig for symbol font processing

* Tue Jun 14 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.109-5
- drop unnecessary openoffice.org-1.9.103.oooXXXXX.installation.disable-epm.fix.patch
- add simple crash report output, not that there are any crashs you understand

* Tue Jun 14 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.109-4
- add Bengali langpack
- make a stable /usr/lib/openoffice.org2.0 dir
- make openoffice.org-1.9.108.ooo9290.goodies.epstoepdf.patch paranoid
- enable failure on rpmbuild test for executable stack
- drop integrated openoffice.org-1.9.89.ooo46912.setjmpoutsidenamespace.binfilter.patch

* Tue Jun 14 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.109-3
- add openoffice.org-1.9.108.oooXXXXX.pyuno.pushrpath.patch
- rejig build to use current splashscreen
- readd openoffice.org-1.9.88.NONE.gcc3gcj4.patch
- add openoffice.org-1.9.108.ooo9290.goodies.epstoepdf.patch for rh#142535#

* Mon Jun 13 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.109-2
- rh#159169# crash due to dodgy casting when save to legacy impress format
- ooo#50571#/rh#157813# add workspace.gslpatches2.patch to fix bizarre 
  lohit combining characters rendering bug

* Fri Jun 10 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.109-1
- rh#158943# Require some fonts
- bump to next version
- drop integrated ooo46528.stillnotpic.icu.patch
- drop integrated ooo48816.instsetoo_native.systempython.patch

* Fri Jun 10 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.108-4
- ooo#50556# Filetype-label doesn't support special char

* Thu Jun 09 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.108-3
- rh#159930# use us english thesaurus for australia as well
- add openoffice.org-1.9.108.ooo47323.binfilter.stupiddetect.patch for
  rh#159851#/ooo#47323#

* Thu Jun 09 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.108-2
- add openoffice.org-1.9.108.ooo30133.lingucomponent.ukrainean.patch
- rh#158923# korean not identified as CJK font by userinstall module
- add openoffice.org-1.9.108.oooXXXXX.solenv.nostipwithsimpleinstall.patch
  to fix rh#157254# useless debuginfo rpm
- shrink buildtime space requirements

* Wed Jun 08 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.108-1
- bump to latest version
- add workspace.vcl39.patch for rh#156176#
- drop integrated openoffice.org-1.9.106.ooo50107.briges.noexecstack.patch
- drop integrated openoffice.org-1.9.106.ooo45298.psprint.pspfontcache.patch
- drop integrated workspace.gcj5.patch

* Fri Jun 03 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.106-2
- add openoffice.org-1.9.106.ooo50172.icu.tamilvowelslikepango.patch to fix (?) 
  rh#157815#

* Tue May 31 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.106-1
- bump to latest version
- drop gcc#20629# workaround
- add openoffice.org-1.9.106.ooo50107.briges.noexecstack.patch
- add workspace.gcc4fwdecl.patch to workaround new gcc pickiness
- add openoffice.org-1.9.106.ooo45298.psprint.pspfontcache.patch
- upstream openoffice.org-1.9.104-gcjawt.patch as part of gcj5
- add GSI_ru.sdf for rh#158539#
- add workspace-fpicker4.patch
- add openoffice.org-1.9.106.ooo44627.sal.brokencondition.patch to
  fix rh#158489#

* Wed May 24 2005 Dan Williams <dcbw@redhat.com> - 1:1.9.104-3
- Remove openoffice.org-1.9.104.oooXXXXX.indic-font-fallbacks.patch
- Add openoffice.org-1.9.104-use-fontconfig-everywhere.patch, which
    uses Fontconfig for all font substituion and glyph fallback

* Tue May 24 2005 Dan Williams <dcbw@redhat.com> - 1:1.9.104-2
- Add -IN glyph fallbacks for Hindi, Gujarati, Bengali, Punjabi, and Tamil
    (penoffice.org-1.9.104.oooXXXXX.indic-font-fallbacks.patch)
- Add Croatian 'hr' langpack
- Package libportaudio and libsndfile libraries in -core package
- drop workspace-db4.patch and workspace-db4-2.patch since it appears we can use
    db4 with gcc again
- add openoffice.org-1.9.104-gcjawt.patch to deal with gcj AWT library change
    to libgcjawt.so
- add openoffice.org-1.9.104-berkeleydb-jni-casting-misuse.patch to fix grievous
    misuse of C casting in berkeleydb's JNI glue

* Thu May 19 2005 Dan Williams <dcbw@redhat.com> - 1:1.9.104-1
- update to m104
- drop integrated openoffice.org-1.9.88.rh150650.gcjneedstoresolveallrequirements.patch
    (#rh150650)

* Tue May 17 2005 Dan Williams <dcbw@redhat.com> - 1:1.9.103-1
- m103 now builds 'hr' language
- add openoffice.org-1.9.101.ooo48816.instsetoo_native.systempython.patch
- add openoffice.org-1.9.103.oooXXXXX.installation.disable-epm.fix.patch
- drop integrated openoffice.org-1.9.97.ooo48362.checkzipresult.sc.patch
- updated to m103
- updated Gujarati translation

* Wed May 04 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.100-1
- bump to next version
- drop finally integrated openoffice.org-1.9.75.ooo41904.singleton.patch

* Tue May 03 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.99-2
- add openoffice.org-1.9.99.gcc19870.gcjaccessproblem.filter.patch for gcj bug workaround
- add openoffice.org-1.9.97.ooo48610.searchalltemplates.wizards.patch
- help documentation for cs and et has landed
- add openoffice.org-1.9.99.gcc19870.gcjaccessproblem.wizards.patch
   -> wizards work!

* Tue May 03 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.99-1
- add openoffice.org-1.9.97.ooo48600.rtfparseerror.svx.patch
- drop openoffice.org-1.9.95.gcc21233.noquotesonjavaver.patch as of
  gcc 4.0.0-2

* Fri Apr 29 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.98-1
- bump to next version
- drop integrated workspace.mhu06.patch
- a better idea for the rh#156039# provides problem along the valgrind.spec
  pattern
- add openoffice.org-1.9.97.rh156067.noversionedicons.patch

* Fri Apr 29 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.97-3
- respin and try out an alternative hack

* Wed Apr 27 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.97-1
- bump to next version
- rh#156039# problems with the autoprovides apparently
- drop integrated openoffice.org-1.9.89.ooo46228.parallel.solenv.patch
- drop integrated openoffice.org-1.9.89.ooo46316.parallel.vcl.patch
- rh#156064# namespace .desktop files
- rh#156066# shorten menu entry name with
  openoffice.org-1.9.97.ooo48256.nolongname.sysui.patch
- drop integrated openoffice.org-1.9.89.ooo46389.parallel.framework.patch
- drop integrated openoffice.org-1.9.89.ooo46481.parallel.svx.patch
- rh#156065# use alternative gnome icons
- add export SAL_ENABLE_FILE_LOCKING=1 for concurrent cppumakers collision
experimentation
- add openoffice.org-1.9.97.ooo48362.checkzipresult.sc.patch

* Tue Apr 26 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.96-2
- just for havoc add openoffice.org-1.9.96.ooo35641.noxfonts.vcl.patch

* Tue Apr 26 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.96-1
- bump to next version
- drop unnecessary openoffice.org-1.9.74.ArchiveZip.patch
- drop integrated openoffice.org-1.9.82.ooo45628.noznow.patch
- drop integrated openoffice.org-1.9.92.ooo47641.pptmimetype.patch
- package new files

* Thu Apr 21 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.95-1
- bump to next version
- drop integrated openoffice.org-1.9.89.oooXXXXX.systemjpeg.tools.patch
- drop integrated openoffice.org-1.9.89.ooo46998.changeppclinkflags.solenv.patch
- drop integrated openoffice.org-1.9.91.ooo46539.sleep.vcl.patch
- drop integrated openoffice.org-1.9.91.ooo46388.unsigned.sot.patch
- pointless to ship partial translated kn_IN without fonts which can
  even display them
- backport workspace.mhu06 to bring back the gnome filedialog that got whacked
- add openoffice.org-1.9.95.dbXXXXX.configureerror.berkleydb.patch to
  try and move to db4 with latest gcc4, but gcc 4.0.0-1 is still broken wrt to db4
  so back to db3 again

* Thu Apr 21 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.93-1
- bump to next version
- drop integrated openoffice.org-1.9.85.ooo45146.mandrakelicence.patch
- try doing without reverting the db4 change
- add openoffice.org-1.9.92.ooo47641.pptmimetype.patch
- Fix GTK combo box button sizes (dcbw)

* Wed Apr 13 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.92-3
- rh#153229# add multiple Obsoletes

* Mon Apr 11 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.92-2
- add some indic translations, but leave disabled for now
- push ooo#46388# sot fix
- drop perl-Archive-Zip buildtime copy

* Mon Apr 11 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.92-1
- bump to next version
- drop integrated workspace-gcj4.patch
- drop openoffice.org-1.9.80.ooo43466.wmclass.patch 
  g_set_application() name called multiple times
- drop integrated openoffice.org-1.9.91.ooo46603.boost.sd.patch

* Mon Apr 11 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.91-2
- scripting framework builds with gcj now

* Fri Apr 8 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.91-1
- bump to latest version
- have to reverse move to db4 because of rh#153231#
- drop integrated workspace-systemmozilla
- drop integrated workspace-gccfour
- add backport of spurious sleep prototype removal
- add our font fallbacks
- stl stuff integrated now
- happy birthday to me
- add openoffice.org-1.9.90.ooo46585.sunmiscisnotstandard.filter.patch

* Wed Apr 5 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.89-5
- ooo#46850# libscui680* apparently in the wrong subpackage
- upstream patches to hsqldb b0rk gcj

* Tue Apr 5 2005 Caolan McNamara <caolanm@redhat.com> - 1:1.9.89-4
- rh#153129# Requires won't work for x86_64
- rh#152269# Reported problems with nfs file locking
- add openoffice.org-1.9.89.oooXXXXX.upstreamhatesthefp.officecfg.patch
- drop redundant patches

* Mon Apr 4 2005 Elliot Lee <sopwith@redhat.com> - 1:1.9.89-3
- Slim down the langpacks

* Sat Apr 2 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.89-2
- package the wizard jars (doh!)
- fix the fpic icudata issue properly
- enthused by parallized build success try parallized build.pl as well as dmake
- some problems during langpack creation -> maxprocess issues ?
- damn ppc gives illegal instruction on sysui mandrake menus which it didn't
  in the last build. I couldn't be bothered wasting my time figuring out why

* Thu Mar 31 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.89-1
- bump to 1.9.89
- drop integrated openoffice.org-1.9.83.ooo43995.wptypedetect.patch
- drop hsqldb backport from 1.9.89 now
- add more parallel build patches as we go along

* Tue Mar 29 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.88-5
- new wzi.res
- ooo#46217# allow fallback to en_US from other english, i.e. en_IE, en_GB etc
- replace openoffice.org-1.9.87.NONE.wizards.broken.patch with
  openoffice.org-1.9.88.rh150650.gcjneedstoresolveallrequirements.patch
  as a workaround to get the wizards registered
- give parallel building a go with 
        openoffice.org-1.9.89.ooo46228.parallel.solenv.patch
        openoffice.org-1.9.89.ooo46316.parallel.vcl.patch
        openoffice.org-1.9.89.ooo46389.parallel.framework.patch
	openoffice.org-1.9.89.ooo35627.parallel.cppumaker.patch
	openoffice.org-1.9.89.oooXXXXX.parallel.sysui.patch

* Mon Mar 28 2005 Christopher Aillon <caillon@redhat.com>
- rebuilt

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com> 1:1.9.88-2
- Update the GTK+ theme icon cache on (un)install

* Tue Mar 22 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.88-1
- bump to 1.9.88
- submit openoffice.org-1.9.84.ooo45725.lingucomponent.contribdict.patch upstream
- drop integrated openoffice.org-1.9.87.ooo43538.sfx2.patch
- openoffice.org-1.9.87.oooXXXXX.fragments.patch build problem of some kind
- add a check for non -fpic libs
- allow switching spec to build with gcc3 and gcj4, kudos Fridrich Strba
- jump to hsqldb 1.8.0RC9 in advance of 1.9.89 to fix our hsqldb issues

* Tue Mar 22 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.87-2
- unpackaged libraries
- try out more lenient LOCALE acceptence for rh#151357#

* Sat Mar 19 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.87-1
- bump to latest version
- rh#151356# stick to 2.0 pathname to keep user settings during pre-release cycle
- drop integrated workspace-gcj3.patch
- drop integrated openoffice.org-1.9.83.ooo44377.icunotusingfpic.patch
- add openoffice.org-1.9.87.gccXXXXX.bean.patch to temporariy work around spurious gcj symbol
- drop unnecessary openoffice.org-1.9.82.NONE.qadevOOogcj.patch
- merge patches that skip boring modules
- scboost issue now part of gccfour workspace
- openoffice.org-1.9.87.NONE.wizards.broken.patch wizards build with gcj, but don't register
- reshuffle direct install to a simple warn not error on missing files, and hijack PKGFORMAT to
  transport direct install flags
- libxmlsec name changed
- java-filter subpackage like upstream now that they build with gcj
- backport openoffice.org-1.9.87.ooo43538.sfx2.patch for rh#151594#
- add requires on appropiate fonts for some langpacks

* Tue Mar 15 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.85-1
- bump to latest version
- add the contrib non-core dictionaries, and allow them to be split up 
  between the languagepacks
- use gcj-dbtool during build

* Wed Mar 09 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.84-1
- bump to 1.9.84
- describe what language is in which langpack, drop some unsupported ones
- ppc should build hsqldb now
- disable qadevOOo for now until gcj3 workspace is fully integrated
- gcc20465 breaks ooo build

* Fri Mar 04 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.83-1
- bump to 1.9.83
- drop integrated workspace.gcj2
- add Requires for libwpd which is now pulled in from the system
- add openoffice.org-1.9.83.ooo43995.wptypedetect.patch
- add openoffice.org-1.9.83.ooo44377.icunotusingfpic.patch because icudata isn't being compiled with -fpic

* Fri Mar 04 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.82-1
- bump to 1.9.82
- drop integrated openoffice.org-1.9.75.ooo42251.copyright.patch
- drop integrated workspace-systempython2.patch
- drop integrated openoffice.org-1.9.77.ooo41026.unxlngi6.patch
- drop integrated openoffice.org-1.9.77.ooo42457.ppclink.patch
- add openoffice.org-1.9.82.NONE.noznow.patch no -z now under ppc

* Wed Mar 02 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.81-1
- bump to 1.9.81
- drop integrated openoffice.org-1.9.77.ooo42152.gnomevfs.patch
- with --with-system-stdlibs
	rm -f $RPM_BUILD_ROOT/instdir/program/libgcc_s.so.*
	rm -f $RPM_BUILD_ROOT/instdir/program/libstdc++.so.*
  becomes redundant
- --with-system-icu & --with-system-db3 no longer in --with-system-libs
- sc needs another file in exceptions because of system-boost
- drop integrated ooo#43297#

* Wed Mar 02 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.80-1
- move to openoffice.org
- gcc4 patch

* Tue Mar 01 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.80-4
- new ms-langpack
- bump from libgcj4 to libgcj >= 4.0.0
- so drop fc4uselibgcj_fc4 patch

* Mon Feb 28 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.80-3
- reenable langpacks
- ignore missing localized files, rather than copying the english version

* Mon Feb 28 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.80-2
- disable langpacks
- hsqldb is apparently buildable with gcj4 now (except under ppc!)

* Thu Feb 25 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.80-1
- bump to latest release
- drop integrated rpath workspace
- slideshow gcc internal error worked around elsewhere
- drop integrated ppc visibility patch
- drop integrated pyunofixes1 workspace
- add ooo#43297# chart2 build fix

* Mon Feb 21 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.77-3
- add extra langpacks

* Fri Feb 11 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.77-2
- add new installed but unpackaged files
- haul in the .desktops and icons

* Tue Feb 8 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.77-1
- drop integrated ooo#40937# doublefree patch
- drop redundant gcj awt without display patch
- drop redundant missingapp patch
- seperate pyuno package with all the goodies from pyunofixes1 and systempython2

* Thu Feb 3 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.75-2
- gcc ppc visibility and inlines are not working correctly

* Wed Feb 2 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.75-1
- bump to next version
- drop integrated gcj1 workspace
- drop integrated systempython workspace

* Wed Feb 2 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.73-2
- crash on exit, correct options for oofoo2 scripts

* Wed Jan 26 2005 Caolan McNamara <caolanm@redhat.com> 1:1.9.73-1
- initial import of the levithan
