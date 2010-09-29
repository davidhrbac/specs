Summary:    Eclipse like task list
Name:       vim-plugin-tasklist
Version:    1.0.1
Release:    1%{?dist}
License:    Distributable
Group:      Applications/Editors
URL:        http://www.vim.org/scripts/script.php?script_id=2607
BuildArch:  noarch
#Source0:  http://www.vim.org/scripts/download_script.php?src_id=10388
Source0:    tasklist.vim
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root

%define         _vimdatadir     %{_datadir}/vim/vim70

%description
This script is based on the eclipse Task List. It will search the file
for FIXME, TODO, and XXX (or a custom list) and put them in a handy
list for you to browse which at the same time will update the location
in the document so you can see exactly where the tag is located.
Something like an interactive 'cw'.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_vimdatadir}/plugin
install %{SOURCE0} $RPM_BUILD_ROOT%{_vimdatadir}/plugin/tasklist.vim

%files
%defattr(644,root,root,755)
%{_vimdatadir}/plugin/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Sep 29 2010 David Hrbáč <david@hrbac.cz> - 1.0.1-1
- initial version 
