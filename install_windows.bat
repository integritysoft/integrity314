@echo off
echo Integrity Assistant 1.0.2 - Windows Installer
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8 or higher.
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Detected Python version: %PYTHON_VERSION%

REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating default configuration file...
    copy .env.template .env
)

REM Create desktop shortcut
echo Creating desktop shortcut...
set DESKTOP=%USERPROFILE%\Desktop
set SHORTCUT=%DESKTOP%\Integrity Assistant.lnk
set SCRIPT_PATH=%CD%\main.py

echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%SHORTCUT%" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "pythonw" >> CreateShortcut.vbs
echo oLink.Arguments = "%SCRIPT_PATH%" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%CD%" >> CreateShortcut.vbs
echo oLink.Description = "Integrity Assistant" >> CreateShortcut.vbs
echo oLink.IconLocation = "%SYSTEMROOT%\System32\SHELL32.dll, 22" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

echo.
echo Installation complete! 
echo.
echo You can now:
echo 1. Run Integrity Assistant from the desktop shortcut
echo 2. Run manually with: python %CD%\main.py
echo.
echo Note: You'll need to create an account on the Integrity website
echo and log in when you first launch the application.
echo.
pause 