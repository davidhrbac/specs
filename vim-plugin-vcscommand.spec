Summary:    CVS/SVN/SVK/git integration plugin
Name:       vim-plugin-vcscommand
Version:    1.99.42
Release:    1%{?dist}
License:    Distributable
Group:      Applications/Editors
URL:        http://www.vim.org/scripts/script.php?script_id=90
BuildArch:  noarch
#Source0:  http://www.vim.org/scripts/download_script.php?src_id=11049
Source0:     vcscommand-%{version}.zip
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root

%define         _vimdatadir     %{_datadir}/vim/vim70

%description
VIM 7 plugin useful for manipulating files controlled by CVS, SVN, SVK
and git within VIM, including committing changes and performings diffs
using the vimdiff system.

To enable this plugin define "use_vcscommand" variable somewhere in
your .vimrc file.

%prep
%setup -q -c

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_vimdatadir}/{doc,plugin,syntax}
install -p doc/* $RPM_BUILD_ROOT%{_vimdatadir}/doc
install -p plugin/* $RPM_BUILD_ROOT%{_vimdatadir}/plugin
install -p syntax/* $RPM_BUILD_ROOT%{_vimdatadir}/syntax

%files
%defattr(644,root,root,755)
%doc %{_vimdatadir}/doc/*
%{_vimdatadir}/plugin/*
%{_vimdatadir}/syntax/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Sep 29 2010 David Hrbáč <david@hrbac.cz> - 1.99.42-1
- initial version 
