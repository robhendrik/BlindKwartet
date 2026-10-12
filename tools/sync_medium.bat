@echo off
if "%~1"=="" goto usage
if "%~2"=="" goto usage
python "%~dp0sync_medium.py" "%~1" "%~2" %3 %4 %5 %6 %7 %8 %9
exit /b %ERRORLEVEL%
:usage
echo Usage: tools\sync_medium.bat "path\to\article.md" "https://medium.com/..." [options]
echo Options: --model MODEL --dry-run --keep-extracted --verbose
exit /b 2
