@echo off
REM Copy the built user-manual HTML into the web client's public\manual\ so the
REM in-app manual button works in local dev. Run AFTER building the manual.
REM
REM Usage: docs\copy_manual_to_fe.bat [offline|online]   (default: offline)
REM
REM Release builds perform this copy in Jenkins (Jenkinsfile_aoi_pcb_patch),
REM picking the variant from smt_version -- this script is for local dev only.

setlocal
set "VARIANT=%~1"
if "%VARIANT%"=="" set "VARIANT=offline"
if /I not "%VARIANT%"=="offline" if /I not "%VARIANT%"=="online" (
    echo [ERROR] variant must be 'offline' or 'online' ^(got "%VARIANT%"^).
    exit /b 1
)

set "DOCS_DIR=%~dp0"
set "SRC_EN=%DOCS_DIR%_build\html\%VARIANT%\en"
set "SRC_CN=%DOCS_DIR%_build\html\%VARIANT%\zh_CN"
for %%I in ("%DOCS_DIR%..\..\aoi_pcb_web_client\public\manual") do set "DEST=%%~fI"

if not exist "%SRC_EN%\index.html" (
    echo [ERROR] Built English manual not found at "%SRC_EN%".
    echo         Build it first, e.g. from docs\:  powershell -ExecutionPolicy Bypass -File i18n_build.ps1
    exit /b 1
)
if not exist "%SRC_CN%\index.html" (
    echo [ERROR] Built Chinese manual not found at "%SRC_CN%".
    echo         Build it first, e.g. from docs\:  powershell -ExecutionPolicy Bypass -File i18n_build.ps1
    exit /b 1
)

echo Copying %VARIANT% English manual  -^> "%DEST%\en"
robocopy "%SRC_EN%" "%DEST%\en" /MIR /NFL /NDL /NP
if errorlevel 8 goto :roboerr

echo Copying %VARIANT% Chinese manual  -^> "%DEST%\zh_CN"
robocopy "%SRC_CN%" "%DEST%\zh_CN" /MIR /NFL /NDL /NP
if errorlevel 8 goto :roboerr

echo.
echo Done (%VARIANT%). The web client serves it at /manual/en/ and /manual/zh_CN/.
exit /b 0

:roboerr
echo [ERROR] robocopy failed (exit code %errorlevel%).
exit /b 1
