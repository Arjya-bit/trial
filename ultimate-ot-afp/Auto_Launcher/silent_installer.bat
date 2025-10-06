@echo off
REM Silent Installer for Windows
REM Installs OT-AFP Platform silently

echo Installing Ultimate OT-AFP Platform...

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting admin privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

REM Create installation directory
set INSTALL_DIR=C:\Program Files\OT-AFP
mkdir "%INSTALL_DIR%" 2>nul

REM Copy files
xcopy /E /I /Y ".\backend" "%INSTALL_DIR%\backend"
xcopy /E /I /Y ".\frontend" "%INSTALL_DIR%\frontend"

REM Install as Windows service (requires NSSM or similar)
echo Installation complete!
pause
