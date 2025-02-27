@echo off
echo Opening project in VSCode Dev Container

REM Check if VS Code is installed
where code >nul 2>&1
if %errorlevel% neq 0 (
  echo VSCode is not installed. Please install it and the Remote Containers extension.
  pause
  exit /b 1
)

REM Open VSCode in current dir
code .

echo When prompted, choose to open in Dev Container.
pause

