%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name HTML_QuickForm

Name:           php-pear-HTML-QuickForm
Version:        3.2.12
Release:        1%{?dist}
Summary:        The PEAR::HTML_QuickForm package provides methods for creating, validating, processing HTML forms

Group:          Development/Libraries
License:        PHP License
URL:            http://pear.php.net/package/HTML_QuickForm
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       php-pear(HTML_Common) >= 1.2.1, php-pear(PEAR) >= 1.4.0

%description
NOTICE: development of HTML_QuickForm version 3 is frozen. Please submit
feature requests for HTML_QuickForm2 package.

The HTML_QuickForm package provides methods to dynamically create,
validate
and render HTML forms.

Features:
* More than 20 ready-to-use form elements.
* XHTML compliant generated code.
* Numerous mixable and extendable validation rules.
* Automatic server-side validation and filtering.
* On request javascript code generation for client-side validation.
* File uploads support.
* Total customization of form rendering.
* Support for external template engines (ITX, Sigma, Flexy, Smarty).
* Pluggable elements, rules and renderers extensions.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml
cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT docdir
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Move documentation
mkdir -p docdir
mv $RPM_BUILD_ROOT%{pear_docdir}/* docdir


# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.php.net/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_name}-%{version}/docdir/%{pear_name}/*


%{pear_xmldir}/%{name}.xml
# Expand this as needed to avoid owning dirs owned by our dependencies
# and to avoid unowned dirs
%{pear_phpdir}/HTML/QuickForm/Renderer/Array.php
%{pear_phpdir}/HTML/QuickForm/Renderer/ArraySmarty.php
%{pear_phpdir}/HTML/QuickForm/Renderer/Default.php
%{pear_phpdir}/HTML/QuickForm/Renderer/ITDynamic.php
%{pear_phpdir}/HTML/QuickForm/Renderer/ITStatic.php
%{pear_phpdir}/HTML/QuickForm/Renderer/Object.php
%{pear_phpdir}/HTML/QuickForm/Renderer/ObjectFlexy.php
%{pear_phpdir}/HTML/QuickForm/Renderer/QuickHtml.php
%{pear_phpdir}/HTML/QuickForm/Rule/Callback.php
%{pear_phpdir}/HTML/QuickForm/Rule/Compare.php
%{pear_phpdir}/HTML/QuickForm/Rule/Email.php
%{pear_phpdir}/HTML/QuickForm/Rule/Range.php
%{pear_phpdir}/HTML/QuickForm/Rule/Regex.php
%{pear_phpdir}/HTML/QuickForm/Rule/Required.php
%{pear_phpdir}/HTML/QuickForm/advcheckbox.php
%{pear_phpdir}/HTML/QuickForm/autocomplete.php
%{pear_phpdir}/HTML/QuickForm/button.php
%{pear_phpdir}/HTML/QuickForm/checkbox.php
%{pear_phpdir}/HTML/QuickForm/date.php
%{pear_phpdir}/HTML/QuickForm/element.php
%{pear_phpdir}/HTML/QuickForm/file.php
%{pear_phpdir}/HTML/QuickForm/group.php
%{pear_phpdir}/HTML/QuickForm/header.php
%{pear_phpdir}/HTML/QuickForm/hidden.php
%{pear_phpdir}/HTML/QuickForm/hiddenselect.php
%{pear_phpdir}/HTML/QuickForm/hierselect.php
%{pear_phpdir}/HTML/QuickForm/html.php
%{pear_phpdir}/HTML/QuickForm/image.php
%{pear_phpdir}/HTML/QuickForm/input.php
%{pear_phpdir}/HTML/QuickForm/link.php
%{pear_phpdir}/HTML/QuickForm/password.php
%{pear_phpdir}/HTML/QuickForm/radio.php
%{pear_phpdir}/HTML/QuickForm/Renderer.php
%{pear_phpdir}/HTML/QuickForm/reset.php
%{pear_phpdir}/HTML/QuickForm/Rule.php
%{pear_phpdir}/HTML/QuickForm/RuleRegistry.php
%{pear_phpdir}/HTML/QuickForm/select.php
%{pear_phpdir}/HTML/QuickForm/static.php
%{pear_phpdir}/HTML/QuickForm/submit.php
%{pear_phpdir}/HTML/QuickForm/text.php
%{pear_phpdir}/HTML/QuickForm/textarea.php
%{pear_phpdir}/HTML/QuickForm/xbutton.php
%{pear_phpdir}/HTML/QuickForm.php




%changelog
* Mon Oct 18 2010 David Hrbáč <david@hrbac.cz> - 3.2.12-1
- initial release

