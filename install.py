#!/usr/bin/env python3
"""
Düsselbrush Installation Script
Automated setup for the Düsselbrush artist portfolio website
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Print installation banner"""
    print("=" * 60)
    print("🎨 Düsselbrush - Artist Portfolio Website")
    print("=" * 60)
    print("Automated installation script")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_pip():
    """Check if pip is available"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip is available")
    except subprocess.CalledProcessError:
        print("❌ Error: pip is not available")
        sys.exit(1)

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return
    
    print("📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to create virtual environment")
        sys.exit(1)

def get_pip_command():
    """Get the correct pip command for the virtual environment"""
    if os.name == 'nt':  # Windows
        return "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        return "venv/bin/pip"

def install_dependencies():
    """Install Python dependencies"""
    pip_cmd = get_pip_command()
    requirements_file = Path("server/requirements.txt")
    
    if not requirements_file.exists():
        print("❌ Error: requirements.txt not found")
        sys.exit(1)
    
    print("📦 Installing dependencies...")
    try:
        subprocess.run([pip_cmd, "install", "-r", str(requirements_file)], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to install dependencies")
        sys.exit(1)

def create_env_file():
    """Create .env file from template"""
    env_file = Path(".env")
    env_example = Path("server/env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    if env_example.exists():
        print("📝 Creating .env file from template...")
        shutil.copy(env_example, env_file)
        print("✅ .env file created")
        print("⚠️  Please edit .env file with your configuration")
    else:
        print("⚠️  No env.example found, creating basic .env file...")
        with open(env_file, 'w') as f:
            f.write("# Düsselbrush Configuration\n")
            f.write("ADMIN_PASSWORD=brush2025\n")
            f.write("SMTP_SERVER=smtp.gmail.com\n")
            f.write("SMTP_PORT=587\n")
            f.write("SMTP_USERNAME=your-email@gmail.com\n")
            f.write("SMTP_PASSWORD=your-app-password\n")
            f.write("ADMIN_EMAIL=admin@example.com\n")
        print("✅ Basic .env file created")

def create_directories():
    """Create necessary directories"""
    directories = [
        "server/data",
        "server/uploads"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("🎉 Installation completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Edit .env file with your configuration")
    print("2. Activate virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("   source venv/bin/activate")
    print("3. Run the application:")
    print("   python server/app.py")
    print("4. Open your browser and go to:")
    print("   http://localhost:5000")
    print("\nFor more information, see README.md")

def main():
    """Main installation function"""
    print_banner()
    
    # Check prerequisites
    check_python_version()
    check_pip()
    
    # Setup project
    create_virtual_environment()
    install_dependencies()
    create_env_file()
    create_directories()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()


