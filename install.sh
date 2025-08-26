#!/bin/bash

echo "============================================================"
echo "🎨 Düsselbrush - Artist Portfolio Website"
echo "============================================================"
echo "Linux/macOS Installation Script"
echo "============================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.8 or higher is required"
    echo "Current version: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Check if pip is available
if ! python3 -m pip --version &> /dev/null; then
    echo "❌ Error: pip is not available"
    exit 1
fi

echo "✅ pip is available"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Install dependencies
echo "📦 Installing dependencies..."
venv/bin/pip install -r server/requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installed successfully"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f "server/env.example" ]; then
        echo "📝 Creating .env file from template..."
        cp server/env.example .env
        echo "✅ .env file created"
        echo "⚠️  Please edit .env file with your configuration"
    else
        echo "📝 Creating basic .env file..."
        cat > .env << EOF
# Düsselbrush Configuration
ADMIN_PASSWORD=brush2025
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ADMIN_EMAIL=admin@example.com
EOF
        echo "✅ Basic .env file created"
    fi
else
    echo "✅ .env file already exists"
fi

# Create necessary directories
mkdir -p server/data server/uploads
echo "✅ Directories created"

echo
echo "============================================================"
echo "🎉 Installation completed successfully!"
echo "============================================================"
echo
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Activate virtual environment:"
echo "   source venv/bin/activate"
echo "3. Run the application:"
echo "   python server/app.py"
echo "4. Open your browser and go to:"
echo "   http://localhost:5000"
echo
echo "For more information, see README.md"
echo

