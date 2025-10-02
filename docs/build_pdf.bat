@REM echo off
@REM cd /d "%~dp0"

@REM rem 2) 构建
@REM call make latex

@REM rem 3) 进入输出目录
cd _build\latex

@REM rem 4) 编译两次
@REM lualatex --interaction=nonstopmode --shell-escape daoaipcbaaoiusermanual.tex
@REM lualatex --interaction=nonstopmode --shell-escape daoaipcbaaoiusermanual.tex

for /f %%i in ('wmic os get LocalDateTime ^| find "."') do set "LDT=%%i"
set "TODAY=%LDT:~0,4%-%LDT:~4,2%-%LDT:~6,2%"

rem 6) 重命名（如已存在同名先删）
if exist "DaoAI_PCB_AOI_User_Manual_%TODAY%.pdf" del /f /q "DaoAI_PCB_AOI_User_Manual_%TODAY%.pdf"
ren "daoaipcbaaoiusermanual.pdf" "DaoAI_PCB_AOI_User_Manual_%TODAY%.pdf"

rem 7) 回到原目录（可选）
cd ..\..
