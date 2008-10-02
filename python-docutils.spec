%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define srcname docutils

Name:           python-%{srcname}
Version:        0.4
Release:        8%{?dist}
Summary:        A system for processing plaintext documentation

Group:          Development/Languages
# See COPYING.txt for information
License:        Public Domain and MIT and Python and GPLv2
URL:            http://docutils.sourceforge.net
Source0:        http://downloads.sourceforge.net/docutils/%{srcname}-%{version}.tar.gz
Source1:        http://svn.berlios.de/viewcvs/*checkout*/docutils/trunk/docutils/tools/editors/emacs/rst.el?rev=5335
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:       noarch

BuildRequires:  python-devel
%if 0%{?fedora} >= 8
BuildRequires: python-setuptools-devel
%else
BuildRequires: python-setuptools
%endif

Requires: python-imaging
Provides: docutils = %{version}-%{release}
Obsoletes: docutils < %{version}-%{release}

%description
The Docutils project specifies a plaintext markup language, reStructuredText,
which is easy to read and quick to write.  The project includes a python
library to parse rST files and transform them into other useful formats such
as HTML, XML, and TeX as well as commandline tools that give the enduser
access to this functionality.

Currently, the library supports parsing rST that is in standalone files and
PEPs (Python Enhancement Proposals).  Work is underway to parse rST from
Python inline documentation modules and packages.

%prep
%setup -q -n %{srcname}-%{version}

# Remove a shebang from one of the library files
sed -i -e '/#! *\/usr\/bin\/.*python.*/{1D}' docutils/readers/python/pynodes.py

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} -c 'import setuptools; execfile("setup.py")' build


%install
rm -rf %{buildroot}

%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}

for file in %{buildroot}/%{_bindir}/*.py; do
    mv $file `dirname $file`/`basename $file .py`
done

# We want the licenses but don't need this build file
rm -f licenses/docutils.conf

# docutils only installs this if its not already on the system.  Due to the
# possibility that a previous version of docutils may be installed, we install
# it manually here.
file=roman.py
extradest=%{python_sitelib}
fullextradest=%{buildroot}/$extradest
install -D -m 0644 extras/$file $fullextradest/$file

# docutils 0.4 rst.el cannot handle emacs 0.22.  Update to the latest svn
# copy.  This also clarifies the rst.el license.
cp %{SOURCE1} tools/editors/emacs/rst.el
    
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc BUGS.txt COPYING.txt FAQ.txt HISTORY.txt README.txt RELEASE-NOTES.txt 
%doc THANKS.txt licenses docs tools/editors
%{_bindir}/*
%{python_sitelib}/docutils/
%{python_sitelib}/roman.*
%{python_sitelib}/*egg-info/

%changelog
* Thu Sep 25 2008 David Hrbáč <david@hrbac.cz> - 0.4-8
- initial rebuild

* Mon Mar 3 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4-8
- Use regular Requires syntax for python-imaging as missingok is just wrong.

* Thu Sep 27 2007 Toshio Kuratomi <a.badger@gmail.com> 0.4-7
- Build egg info.

* Mon Aug 13 2007 Toshio Kuratomi <a.badger@gmail.com> 0.4-6
- Last version had both the old and new rst.el.  Try again with only
  the new one.

* Sun Aug 12 2007 Toshio Kuratomi <a.badger@gmail.com> 0.4-5
- Make License tag conform to the new Licensing Policy.
- Fix the rst emacs mode (RH BZ 250100)

* Sat Dec 09 2006 Toshio Kuratomi <toshio-tiki-lounge.com> 0.4-4
- Bump and rebuild for python 2.5 in devel.

* Tue Aug 29 2006 Toshio Kuratomi <toshio-tiki-lounge.com> 0.4-3
- Bump for FC6 rebuild.
- Remove python byte compilation as this is handled automatically in FC4+.
- No longer %%ghost .pyo files.
  
* Thu Feb 16 2006 Toshio Kuratomi <toshio-tiki-lounge.com> 0.4-2
- Bump and rebuild for FC5.
  
* Sun Jan 15 2006 Toshio Kuratomi <toshio-tiki-lounge.com> 0.4-1
- Update to 0.4.
- Scripted the listing of files in the python module.
- Add a missingok requirement on python-imaging as docutils can make use of
  it when converting to formats that have images.
  
* Tue Jun 7 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 0.3.9-1
- Update to version 0.3.9.
- Use a dist tag as there aren't any differences between supported fc
  releases (FC3, FC4, devel.)

* Thu May 12 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 0.3.7-7
- Bump version and rebuild to sync across architectures.

* Sun Mar 20 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 0.3.7-6
- Rebuild for FC4t1

* Sat Mar 12 2005 Toshio Kuratomi <toshio.tiki-lounge.com> 0.3.7-5
- Add GPL as a license (mschwendt)
- Use versioned Obsoletes and Provides (mschwendt)

* Fri Mar 04 2005 Toshio Kuratomi <toshio.tiki-lounge.com> 0:0.3.7-4
- Rename to python-docutils per the new packaging guidelines.

* Wed Jan 12 2005 Toshio Kuratomi <toshio.tiki-lounge.com> 0:0.3.7-0.fdr.3
- Really install roman.py and build roman.py[co].  Needed to make sure I have
  docutils installed to test that it builds roman.py fine in that case.

* Tue Jan 11 2005 Toshio Kuratomi <toshio.tiki-lounge.com> 0:0.3.7-0.fdr.2
- Special case roman.py to always install.  This is the behaviour we want
  unless something else provides it.  Will need to watch out for this in
  future Core and Extras packages, but the auto detection code makes it
  possible that builds will not be reproducible if roman.py were installed
  from another package.... Lesser of two evils here.
- Provide python-docutils in case that package were preinstalled from
  another repository.
  
* Fri Dec 31 2004 Toshio Kuratomi <toshio.tiki-lounge.com> 0:0.3.7-0.fdr.1
- Update to 0.3.7
- Rename from python-docutils to docutils.
- Make roman.py optionally a part of the files list.  In FC2, this will be
  included.  In FC3, this won't.
- BuildConflict with self since the docutils build detects the presence
  of roman.py and doesn't reinstall itself.
  
* Mon Aug 9 2004 Toshio Kuratomi <toshio.tiki-lounge.com> 0:0.3.5-0.fdr.1
- Update to 0.3.5.
- Update spec style to latest fedora-rpmdevtools.
- Merge everything into a single package.  There isn't very much space
  advantage to having separate packages in a package this small and in
  this case, the documentation on using docutils as a library is also a
  good example of how to write in ReSructuredText.

* Sat Jan 10 2004 Michel Alexandre Salim <salimma[AT]users.sf.net> 0:0.3-0.fdr.1
- Initial RPM release.
