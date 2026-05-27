@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=source
set BUILDDIR=_build

if "%1" == "" goto help

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

REM --- i18n / multi-language targets (zh_CN = source, en = translation) ---
if "%1" == "gettext" (
	%SPHINXBUILD% -b gettext %SOURCEDIR% %BUILDDIR%\gettext %SPHINXOPTS%
	goto end
)
if "%1" == "intl-update" (
	%SPHINXBUILD% -b gettext %SOURCEDIR% %BUILDDIR%\gettext %SPHINXOPTS%
	sphinx-intl update -p %BUILDDIR%\gettext -l en -d %SOURCEDIR%\locale
	goto end
)
if "%1" == "html-cn" (
	%SPHINXBUILD% -b html -D language=zh_CN %SOURCEDIR% %BUILDDIR%\html\zh_CN %SPHINXOPTS%
	goto end
)
if "%1" == "html-en" (
	%SPHINXBUILD% -b html -D language=en %SOURCEDIR% %BUILDDIR%\html\en %SPHINXOPTS%
	goto end
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
