@echo off
echo ========================================
echo    Enhanced Virtual Painter Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

echo Python found. Checking dependencies...
echo.

REM Run the launcher script
python run_enhanced.py

REM Pause to show any error messages
if errorlevel 1 (
    echo.
    echo An error occurred. Press any key to exit...
    pause
) 