Name:           php-Smarty
Summary:        Template/Presentation Framework for PHP
Version:        2.6.22
Release:        1%{?dist}

Source0:        http://www.smarty.net/distributions/Smarty-%{version}.tar.gz
#Patch0:         %{name}-2.6.20-security.patch
License:        LGPLv2+
URL:            http://www.smarty.net
Group:          Development/Libraries

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       php

%description
Although Smarty is known as a "Template Engine", it would be more accurately
described as a "Template/Presentation Framework." That is, it provides the
programmer and template designer with a wealth of tools to automate tasks
commonly dealt with at the presentation layer of an application. I stress the
word Framework because Smarty is not a simple tag-replacing template engine.
Although it can be used for such a simple purpose, its focus is on quick and
painless development and deployment of your application, while maintaining
high-performance, scalability, security and future growth.


%prep
%setup -qn Smarty-%{version}
iconv -f iso8859-1 -t utf-8 NEWS > NEWS.conv && mv -f NEWS.conv NEWS
iconv -f iso8859-1 -t utf-8 ChangeLog > ChangeLog.conv && mv -f ChangeLog.conv ChangeLog

# install security patch
#%patch0 -p0 -b .security~


%build
# empty build section, nothing required


%install
rm -rf $RPM_BUILD_ROOT

# install smarty libs
install -d $RPM_BUILD_ROOT%{_datadir}/php/Smarty
cp -a libs/* $RPM_BUILD_ROOT%{_datadir}/php/Smarty/

# install icons
install -d $RPM_BUILD_ROOT%{_var}/www/icons
install -pm 644 misc/smarty_icon.gif $RPM_BUILD_ROOT%{_var}/www/icons/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc BUGS ChangeLog COPYING.lib demo FAQ NEWS QUICK_START README
%doc RELEASE_NOTES TODO
%{_datadir}/php/Smarty
%{_var}/www/icons/*


%changelog
* Tue Mar 10 2009 David Hrbáč <david@hrbac.cz> - 2.6.22-1
- New upstream version

* Tue Mar 10 2009 David Hrbáč <david@hrbac.cz> - 2.6.21-1
- New upstream version

* Mon Mar  9 2009 David Hrbáč <david@hrbac.cz> - 2.6.20-3
- Removed requires version

* Sat Dec 20 2008 David Hrbáč <david@hrbac.cz> - 2.6.20-2
- initial rebuild

* Mon Nov 02 2008 Christopher Stone <chris.stone@gmail.com> 2.6.20-2
- Add security patch (bz #469648)
- Add RHL dist tag conditional for Requires

* Mon Oct 13 2008 Christopher Stone <chris.stone@gmail.com> 2.6.20-1
- Upstream sync

* Wed Feb 20 2008 Christopher Stone <chris.stone@gmail.com> 2.6.19-1
- Upstream sync
- Update %%license
- Fix file encoding

* Sun Apr 29 2007 Christopher Stone <chris.stone@gmail.com> 2.6.18-1
- Upstream sync

* Wed Feb 21 2007 Christopher Stone <chris.stone@gmail.com> 2.6.16-2
- Minor spec file changes/cleanups

* Fri Feb 09 2007 Orion Poplawski <orion@cora.nwra.com> 2.6.16-1
- Update to 2.6.16
- Install in /usr/share/php/Smarty
- Update php version requirement

* Tue May 16 2006 Orion Poplawski <orion@cora.nwra.com> 2.6.13-1
- Update to 2.6.13

* Tue Nov  1 2005 Orion Poplawski <orion@cora.nwra.com> 2.6.10-2
- Fix Source0 URL.

* Thu Oct 13 2005 Orion Poplawski <orion@cora.nwra.com> 2.6.10-1
- Initial Fedora Extras version
