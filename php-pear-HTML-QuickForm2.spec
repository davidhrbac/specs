%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name HTML_QuickForm2

Name:           php-pear-HTML-QuickForm2
Version:        0.5.0
Release:        1%{?dist}
Summary:        PHP5 rewrite of HTML_QuickForm package

Group:          Development/Libraries
License:        BSD
URL:            http://pear.php.net/package/HTML_QuickForm2
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       php-pear(HTML_Common2) >= 2.0.0beta1, php-pear(PEAR) >= 1.5.4

%description
PHP5 rewrite of HTML_QuickForm and HTML_QuickForm_Controller packages.
 
 This package provides methods to create, validate and render HTML forms.
 
 Features:
   * Supports all form elements defined by HTML standard
   * Server-side validation, several common rules provided
   * Multipage forms (tabbed forms and wizards)
   * Pluggable elements, rules, renderers and renderer plugins

 Major advantages over PHP4 version:
   * DOM-like API for building the form structure, new streamlined API for

     elements' values handling
   * Default rendering without tables (inspired by
     HTML_QuickForm_Renderer_Tableless)
   * Renderer plugins for elements with complex rendering needs
   * Ability to chain validation rules with 'and' and 'or'

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
%{pear_phpdir}/HTML/QuickForm2.php
%{pear_phpdir}/HTML/QuickForm2/Container.php
%{pear_phpdir}/HTML/QuickForm2/Container/Fieldset.php
%{pear_phpdir}/HTML/QuickForm2/Container/Group.php
%{pear_phpdir}/HTML/QuickForm2/Controller.php
%{pear_phpdir}/HTML/QuickForm2/Controller/Action.php
%{pear_phpdir}/HTML/QuickForm2/Controller/Action/Back.php
%{pear_phpdir}/HTML/QuickForm2/Controller/Action/Direct.php
%{pear_phpdir}/HTML/QuickForm2/Controller/Action/Display.php
%{pear_phpdir}/HTML/QuickForm2/Controller/Action/Jump.php
%{pear_phpdir}/HTML/QuickForm2/Controller/Action/Next.php
%{pear_phpdir}/HTML/QuickForm2/Controller/Action/Submit.php
%{pear_phpdir}/HTML/QuickForm2/Controller/DefaultAction.php
%{pear_phpdir}/HTML/QuickForm2/Controller/Page.php
%{pear_phpdir}/HTML/QuickForm2/Controller/SessionContainer.php
%{pear_phpdir}/HTML/QuickForm2/DataSource.php
%{pear_phpdir}/HTML/QuickForm2/DataSource/Array.php
%{pear_phpdir}/HTML/QuickForm2/DataSource/Session.php
%{pear_phpdir}/HTML/QuickForm2/DataSource/Submit.php
%{pear_phpdir}/HTML/QuickForm2/DataSource/SuperGlobal.php
%{pear_phpdir}/HTML/QuickForm2/Element.php
%{pear_phpdir}/HTML/QuickForm2/Element/Button.php
%{pear_phpdir}/HTML/QuickForm2/Element/Date.php
%{pear_phpdir}/HTML/QuickForm2/Element/Hierselect.php
%{pear_phpdir}/HTML/QuickForm2/Element/Input.php
%{pear_phpdir}/HTML/QuickForm2/Element/InputButton.php
%{pear_phpdir}/HTML/QuickForm2/Element/InputCheckable.php
%{pear_phpdir}/HTML/QuickForm2/Element/InputCheckbox.php
%{pear_phpdir}/HTML/QuickForm2/Element/InputFile.php
%{pear_phpdir}/HTML/QuickForm2/Element/InputHidden.php
%{pear_phpdir}/HTML/QuickForm2/Element/InputImage.php
%{pear_phpdir}/HTML/QuickForm2/Element/InputPassword.php
%{pear_phpdir}/HTML/QuickForm2/Element/InputRadio.php
%{pear_phpdir}/HTML/QuickForm2/Element/InputReset.php
%{pear_phpdir}/HTML/QuickForm2/Element/InputSubmit.php
%{pear_phpdir}/HTML/QuickForm2/Element/InputText.php
%{pear_phpdir}/HTML/QuickForm2/Element/Script.php
%{pear_phpdir}/HTML/QuickForm2/Element/Select.php
%{pear_phpdir}/HTML/QuickForm2/Element/Static.php
%{pear_phpdir}/HTML/QuickForm2/Element/Textarea.php
%{pear_phpdir}/HTML/QuickForm2/Exception.php
%{pear_phpdir}/HTML/QuickForm2/Factory.php
%{pear_phpdir}/HTML/QuickForm2/JavascriptBuilder.php
%{pear_phpdir}/HTML/QuickForm2/Loader.php
%{pear_phpdir}/HTML/QuickForm2/Node.php
%{pear_phpdir}/HTML/QuickForm2/Renderer.php
%{pear_phpdir}/HTML/QuickForm2/Renderer/Array.php
%{pear_phpdir}/HTML/QuickForm2/Renderer/Default.php
%{pear_phpdir}/HTML/QuickForm2/Renderer/Plugin.php
%{pear_phpdir}/HTML/QuickForm2/Renderer/Proxy.php
%{pear_phpdir}/HTML/QuickForm2/Rule.php
%{pear_phpdir}/HTML/QuickForm2/Rule/Callback.php
%{pear_phpdir}/HTML/QuickForm2/Rule/Compare.php
%{pear_phpdir}/HTML/QuickForm2/Rule/Each.php
%{pear_phpdir}/HTML/QuickForm2/Rule/Empty.php
%{pear_phpdir}/HTML/QuickForm2/Rule/Length.php
%{pear_phpdir}/HTML/QuickForm2/Rule/MaxFileSize.php
%{pear_phpdir}/HTML/QuickForm2/Rule/MimeType.php
%{pear_phpdir}/HTML/QuickForm2/Rule/Nonempty.php
%{pear_phpdir}/HTML/QuickForm2/Rule/NotCallback.php
%{pear_phpdir}/HTML/QuickForm2/Rule/NotRegex.php
%{pear_phpdir}/HTML/QuickForm2/Rule/Regex.php
%{pear_phpdir}/HTML/QuickForm2/Rule/Required.php
%{pear_datadir}/HTML_QuickForm2
%{pear_testdir}/HTML_QuickForm2


%changelog
* Wed Dec 15 2010 David Hrbáč <david@hrbac.cz> - 0.5.0-1
- new upstream release

* Mon Oct 18 2010 David Hrbáč <david@hrbac.cz> - 0.4.0-1
- inital release

