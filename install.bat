@echo off
echo ============================================================
echo 🎨 Düsselbrush - Artist Portfolio Website
echo ============================================================
echo Windows Installation Script
echo ============================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if pip is available
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: pip is not available
    pause
    exit /b 1
)

echo ✅ pip is available

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Error: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Install dependencies
echo 📦 Installing dependencies...
venv\Scripts\pip install -r server\requirements.txt
if errorlevel 1 (
    echo ❌ Error: Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed successfully

REM Create .env file if it doesn't exist
if not exist ".env" (
    if exist "server\env.example" (
        echo 📝 Creating .env file from template...
        copy "server\env.example" ".env" >nul
        echo ✅ .env file created
        echo ⚠️  Please edit .env file with your configuration
    ) else (
        echo 📝 Creating basic .env file...
        (
            echo # Düsselbrush Configuration
            echo ADMIN_PASSWORD=brush2025
            echo SMTP_SERVER=smtp.gmail.com
            echo SMTP_PORT=465
            echo SMTP_USERNAME=roguelife2023@gmail.com
            echo SMTP_PASSWORD=qtfvjxhgtrbsxhue
            echo ADMIN_EMAIL=roguelife2023@gmail.com
        ) > .env
        echo ✅ Basic .env file created
    )
) else (
    echo ✅ .env file already exists
)

REM Create necessary directories
if not exist "server\data" mkdir "server\data"
if not exist "server\uploads" mkdir "server\uploads"
echo ✅ Directories created

echo.
echo ============================================================
echo 🎉 Installation completed successfully!
echo ============================================================
echo.
echo Next steps:
echo 1. Edit .env file with your configuration
echo 2. Activate virtual environment:
echo    venv\Scripts\activate
echo 3. Run the application:
echo    python server\app.py
echo 4. Open your browser and go to:
echo    http://localhost:5000
echo.
echo For more information, see README.md
echo.
pause

