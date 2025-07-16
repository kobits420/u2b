#!/usr/bin/env python3
"""
Test script for u2b - YouTube Command Line Player
Verifies that all dependencies are properly installed.
"""

import sys
import importlib

def test_imports():
    """Test if all required modules can be imported"""
    required_modules = [
        'yt_dlp',
        'requests',
        'bs4',
        'colorama'
    ]
    
    print("Testing module imports...")
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\nFailed to import: {', '.join(failed_imports)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("✓ All modules imported successfully")
    return True

def test_config():
    """Test if configuration can be loaded"""
    try:
        import config
        print("✓ Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_ffmpeg():
    """Test if FFmpeg is available"""
    import subprocess
    try:
        result = subprocess.run(['ffplay', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✓ FFmpeg detected")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("✗ FFmpeg not found")
    return False

def main():
    """Run all tests"""
    print("u2b - Dependency Test")
    print("=" * 30)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_config),
        ("FFmpeg", test_ffmpeg)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
    
    print(f"\n{'=' * 30}")
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! u2b is ready to use.")
        print("\nRun the application with:")
        print("  python main.py")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 