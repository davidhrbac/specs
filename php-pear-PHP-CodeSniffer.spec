%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name PHP_CodeSniffer

Name:           php-pear-PHP-CodeSniffer
Version:        1.3.0RC1
Release:        1%{?dist}
Summary:        PHP_CodeSniffer tokenises PHP, JavaScript and CSS files and detects violations of a defined set of coding standards

Group:          Development/Libraries
License:        BSD License
URL:            http://pear.php.net/package/PHP_CodeSniffer
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}


%description
PHP_CodeSniffer is a PHP5 script that tokenises and "sniffs" PHP,
JavaScript and CSS files to detect violations of a defined coding
standard. It is an essential development tool that ensures your code
remains clean and consistent. It can also help prevent some common
semantic errors made by developers.

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



%{pear_xmldir}/%{name}.xml
# Expand this as needed to avoid owning dirs owned by our dependencies
# and to avoid unowned dirs
%{pear_phpdir}/PHP/CodeSniffer/CommentParser/AbstractDocElement.php
%{pear_phpdir}/PHP/CodeSniffer/CommentParser/AbstractParser.php
%{pear_phpdir}/PHP/CodeSniffer/CommentParser/ClassCommentParser.php
%{pear_phpdir}/PHP/CodeSniffer/CommentParser/CommentElement.php
%{pear_phpdir}/PHP/CodeSniffer/CommentParser/DocElement.php
%{pear_phpdir}/PHP/CodeSniffer/CommentParser/FunctionCommentParser.php
%{pear_phpdir}/PHP/CodeSniffer/CommentParser/MemberCommentParser.php
%{pear_phpdir}/PHP/CodeSniffer/CommentParser/PairElement.php
%{pear_phpdir}/PHP/CodeSniffer/CommentParser/ParameterElement.php
%{pear_phpdir}/PHP/CodeSniffer/CommentParser/ParserException.php
%{pear_phpdir}/PHP/CodeSniffer/CommentParser/SingleElement.php
%{pear_phpdir}/PHP/CodeSniffer/DocGenerators/Generator.php
%{pear_phpdir}/PHP/CodeSniffer/DocGenerators/HTML.php
%{pear_phpdir}/PHP/CodeSniffer/DocGenerators/Text.php
%{pear_phpdir}/PHP/CodeSniffer/Reports/Checkstyle.php
%{pear_phpdir}/PHP/CodeSniffer/Reports/Csv.php
%{pear_phpdir}/PHP/CodeSniffer/Reports/Emacs.php
%{pear_phpdir}/PHP/CodeSniffer/Reports/Full.php
%{pear_phpdir}/PHP/CodeSniffer/Reports/Gitblame.php
%{pear_phpdir}/PHP/CodeSniffer/Reports/Source.php
%{pear_phpdir}/PHP/CodeSniffer/Reports/Summary.php
%{pear_phpdir}/PHP/CodeSniffer/Reports/Svnblame.php
%{pear_phpdir}/PHP/CodeSniffer/Reports/VersionControl.php
%{pear_phpdir}/PHP/CodeSniffer/Reports/Xml.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Docs/Files/LineLengthStandard.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Docs/Formatting/MultipleStatementAlignmentStandard.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Docs/Functions/OpeningFunctionBraceBsdAllmanStandard.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Docs/Functions/OpeningFunctionBraceKernighanRitchieStandard.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Docs/NamingConventions/UpperCaseConstantNameStandard.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Docs/PHP/DisallowShortOpenTagStandard.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Docs/PHP/LowerCaseConstantStandard.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Docs/PHP/UpperCaseConstantStandard.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/Classes/DuplicateClassNameSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/CodeAnalysis/EmptyStatementSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/CodeAnalysis/ForLoopShouldBeWhileLoopSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/CodeAnalysis/ForLoopWithTestFunctionCallSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/CodeAnalysis/JumbledIncrementerSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/CodeAnalysis/UnconditionalIfStatementSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/CodeAnalysis/UnnecessaryFinalModifierSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/CodeAnalysis/UnusedFunctionParameterSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/CodeAnalysis/UselessOverridingMethodSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/Commenting/TodoSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/ControlStructures/InlineControlStructureSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/Files/LineEndingsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/Files/LineLengthSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/Formatting/DisallowMultipleStatementsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/Formatting/MultipleStatementAlignmentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/Formatting/NoSpaceAfterCastSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/Formatting/SpaceAfterCastSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/Functions/CallTimePassByReferenceSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/Functions/FunctionCallArgumentSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/Functions/OpeningFunctionBraceBsdAllmanSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/Functions/OpeningFunctionBraceKernighanRitchieSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/Metrics/CyclomaticComplexitySniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/Metrics/NestingLevelSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/NamingConventions/ConstructorNameSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/NamingConventions/UpperCaseConstantNameSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/PHP/DeprecatedFunctionsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/PHP/DisallowShortOpenTagSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/PHP/ForbiddenFunctionsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/PHP/LowerCaseConstantSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/PHP/NoSilencedErrorsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/PHP/UpperCaseConstantSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/Strings/UnnecessaryStringConcatSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/VersionControl/SubversionPropertiesSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/WhiteSpace/DisallowTabIndentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/Sniffs/WhiteSpace/ScopeIndentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Generic/ruleset.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/MySource/Sniffs/Channels/ChannelExceptionSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/MySource/Sniffs/Channels/DisallowSelfActionsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/MySource/Sniffs/Channels/IncludeSystemSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/MySource/Sniffs/Channels/UnusedSystemSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/MySource/Sniffs/Commenting/FunctionCommentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/MySource/Sniffs/CSS/BrowserSpecificStylesSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/MySource/Sniffs/Debug/DebugCodeSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/MySource/Sniffs/Debug/FirebugConsoleSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/MySource/Sniffs/Objects/AssignThisSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/MySource/Sniffs/Objects/CreateWidgetTypeCallbackSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/MySource/Sniffs/Objects/DisallowNewWidgetSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/MySource/Sniffs/PHP/GetRequestDataSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/MySource/Sniffs/PHP/EvalObjectFactorySniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/MySource/Sniffs/PHP/ReturnFunctionValueSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/MySource/Sniffs/Strings/JoinStringsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/MySource/ruleset.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Docs/Files/IncludingFileStandard.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Docs/Files/LineLengthStandard.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Docs/Functions/FunctionCallSignatureStandard.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Docs/Functions/ValidDefaultValueStandard.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Docs/NamingConventions/ValidClassNameStandard.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Docs/NamingConventions/ValidFunctionNameStandard.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/Classes/ClassDeclarationSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/Commenting/ClassCommentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/Commenting/FileCommentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/Commenting/FunctionCommentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/Commenting/InlineCommentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/ControlStructures/ControlSignatureSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/ControlStructures/MultiLineConditionSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/Files/IncludingFileSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/Formatting/MultiLineAssignmentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/Functions/FunctionCallSignatureSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/Functions/FunctionDeclarationSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/Functions/ValidDefaultValueSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/NamingConventions/ValidClassNameSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/NamingConventions/ValidFunctionNameSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/NamingConventions/ValidVariableNameSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/WhiteSpace/ObjectOperatorIndentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/WhiteSpace/ScopeClosingBraceSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/Sniffs/WhiteSpace/ScopeIndentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/PEAR/ruleset.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/PHPCS/ruleset.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Docs/Arrays/ArrayDeclarationStandard.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Arrays/ArrayBracketSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Arrays/ArrayDeclarationSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Classes/ClassDeclarationSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Classes/ClassFileNameSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Classes/DuplicatePropertySniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Classes/LowercaseClassKeywordsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Classes/SelfMemberReferenceSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Classes/ValidClassNameSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/CodeAnalysis/EmptyStatementSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Commenting/BlockCommentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Commenting/ClassCommentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Commenting/ClosingDeclarationCommentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Commenting/DocCommentAlignmentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Commenting/EmptyCatchCommentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Commenting/FileCommentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Commenting/FunctionCommentThrowTagSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Commenting/FunctionCommentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Commenting/InlineCommentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Commenting/LongConditionClosingCommentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Commenting/PostStatementCommentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Commenting/VariableCommentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/ControlStructures/ControlSignatureSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/ControlStructures/ElseIfDeclarationSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/ControlStructures/ForEachLoopDeclarationSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/ControlStructures/ForLoopDeclarationSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/ControlStructures/InlineIfDeclarationSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/ControlStructures/LowercaseDeclarationSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/ControlStructures/SwitchDeclarationSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/CSS/ClassDefinitionClosingBraceSpaceSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/CSS/ClassDefinitionNameSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/CSS/ClassDefinitionOpeningBraceSpaceSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/CSS/ColonSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/CSS/ColourDefinitionSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/CSS/DisallowMultipleStyleDefinitionsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/CSS/DuplicateClassDefinitionSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/CSS/DuplicateStyleDefinitionSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/CSS/EmptyClassDefinitionSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/CSS/EmptyStyleDefinitionSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/CSS/IndentationSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/CSS/LowercaseStyleDefinitionSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/CSS/MissingColonSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/CSS/OpacitySniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/CSS/SemicolonSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Debug/JavaScriptLintSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Debug/JSLintSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Files/FileExtensionSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Formatting/OperatorBracketSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Formatting/OutputBufferingIndentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Functions/FunctionDeclarationArgumentSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Functions/FunctionDeclarationSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Functions/FunctionDuplicateArgumentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Functions/GlobalFunctionSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Functions/LowercaseFunctionKeywordsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Functions/MultiLineFunctionDeclarationSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/NamingConventions/ConstantCaseSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/NamingConventions/ValidFunctionNameSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/NamingConventions/ValidVariableNameSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Objects/DisallowObjectStringIndexSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Objects/ObjectInstantiationSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Objects/ObjectMemberCommaSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Operators/ComparisonOperatorUsageSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Operators/IncrementDecrementUsageSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Operators/ValidLogicalOperatorsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/PHP/CommentedOutCodeSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/PHP/DisallowComparisonAssignmentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/PHP/DisallowInlineIfSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/PHP/DisallowMultipleAssignmentsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/PHP/DisallowObEndFlushSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/PHP/DisallowSizeFunctionsInLoopsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/PHP/DiscouragedFunctionsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/PHP/EmbeddedPhpSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/PHP/EvalSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/PHP/ForbiddenFunctionsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/PHP/GlobalKeywordSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/PHP/HeredocSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/PHP/InnerFunctionsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/PHP/LowercasePHPFunctionsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/PHP/NonExecutableCodeSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Scope/MemberVarScopeSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Scope/MethodScopeSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Scope/StaticThisUsageSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Strings/ConcatenationSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Strings/DoubleQuoteUsageSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/Strings/EchoedStringsSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/WhiteSpace/CastSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/WhiteSpace/ControlStructureSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/WhiteSpace/FunctionClosingBraceSpaceSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/WhiteSpace/FunctionOpeningBraceSpaceSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/WhiteSpace/FunctionSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/WhiteSpace/LanguageConstructSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/WhiteSpace/LogicalOperatorSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/WhiteSpace/MemberVarSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/WhiteSpace/ObjectOperatorSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/WhiteSpace/OperatorSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/WhiteSpace/PropertyLabelSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/WhiteSpace/ScopeClosingBraceSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/WhiteSpace/ScopeIndentSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/WhiteSpace/ScopeKeywordSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/WhiteSpace/SemicolonSpacingSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/Sniffs/WhiteSpace/SuperfluousWhitespaceSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Squiz/ruleset.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/Zend/Sniffs/Debug/CodeAnalyzerSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Zend/Sniffs/Files/ClosingTagSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Zend/Sniffs/NamingConventions/ValidVariableNameSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/Zend/ruleset.xml
%{pear_phpdir}/PHP/CodeSniffer/Standards/AbstractPatternSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/AbstractScopeSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/AbstractVariableSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Standards/IncorrectPatternException.php
%{pear_phpdir}/PHP/CodeSniffer/Tokenizers/CSS.php
%{pear_phpdir}/PHP/CodeSniffer/Tokenizers/JS.php
%{pear_phpdir}/PHP/CodeSniffer/Tokenizers/PHP.php
%{pear_phpdir}/PHP/CodeSniffer/CLI.php
%{pear_phpdir}/PHP/CodeSniffer/Exception.php
%{pear_phpdir}/PHP/CodeSniffer/File.php
%{pear_phpdir}/PHP/CodeSniffer/MultiFileSniff.php
%{pear_phpdir}/PHP/CodeSniffer/Report.php
%{pear_phpdir}/PHP/CodeSniffer/Reporting.php
%{pear_phpdir}/PHP/CodeSniffer/Sniff.php
%{pear_phpdir}/PHP/CodeSniffer/Tokens.php
%{pear_phpdir}/PHP/CodeSniffer.php
%{pear_datadir}/PHP_CodeSniffer
%{pear_testdir}/PHP_CodeSniffer
%{_bindir}/phpcs
%{_bindir}/scripts/phpcs-svn-pre-commit

%changelog
* Wed Sep 15 2010 David Hrbáč <david@hrbac.cz> - 1.3.0RC1-1
- initial release

