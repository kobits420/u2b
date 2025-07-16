#!/usr/bin/env python3
"""
Installation script for u2b - YouTube Command Line Player
Checks for dependencies and installs required packages.
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        result = subprocess.run(['ffplay', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✓ FFmpeg detected")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("✗ FFmpeg not found")
    print("\nPlease install FFmpeg:")
    
    system = platform.system().lower()
    if system == "windows":
        print("1. Download from: https://ffmpeg.org/download.html")
        print("2. Extract to C:\\ffmpeg")
        print("3. Add C:\\ffmpeg\\bin to your PATH")
        print("4. Restart your command prompt")
    elif system == "darwin":  # macOS
        print("Run: brew install ffmpeg")
    else:  # Linux
        print("Run: sudo apt update && sudo apt install ffmpeg")
    
    return False

def install_python_packages():
    """Install required Python packages"""
    try:
        print("Installing Python packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Python packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install Python packages: {e}")
        return False

def main():
    """Main installation function"""
    print("u2b - YouTube Command Line Player Installation")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install Python packages
    if not install_python_packages():
        sys.exit(1)
    
    # Check FFmpeg
    if not check_ffmpeg():
        print("\nInstallation incomplete. Please install FFmpeg and run this script again.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✓ Installation completed successfully!")
    print("\nTo run u2b:")
    print("  python main.py")
    print("\nOr on Windows:")
    print("  run.bat")
    print("\nOr on Linux/macOS:")
    print("  ./run.sh")

if __name__ == "__main__":
    main() 