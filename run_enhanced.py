#!/usr/bin/env python3


import sys
import os
import subprocess
import importlib.util

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = ['cv2', 'mediapipe', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        if package == 'cv2':
            try:
                import cv2
            except ImportError:
                missing_packages.append('opencv-python')
        else:
            try:
                importlib.import_module(package)
            except ImportError:
                missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install them using:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def check_modules():
    """Check if all required modules exist."""
    required_modules = [
        'config.py',
        'hand_tracker.py', 
        'canvas_manager.py',
        'ui_manager.py',
        'virtual_painter_enhanced.py'
    ]
    
    missing_modules = []
    for module in required_modules:
        if not os.path.exists(module):
            missing_modules.append(module)
    
    if missing_modules:
        print("❌ Missing required modules:")
        for module in missing_modules:
            print(f"   - {module}")
        print("\n🔧 Please ensure all files are in the same directory.")
        return False
    
    print("✅ All required modules found!")
    return True

def main():
    """Main launcher function."""
    print("🎨 Enhanced Virtual Painter Launcher")
    print("=" * 40)
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    if not check_dependencies():
        return 1
    
    # Check modules
    print("\n🔍 Checking modules...")
    if not check_modules():
        return 1
    
    print("\n🚀 Starting Enhanced Virtual Painter...")
    print("💡 Press 'H' for help, 'Q' to quit")
    print("=" * 40)
    
    try:
        # Import and run the enhanced virtual painter
        from virtual_painter_enhanced import main as run_painter
        run_painter()
    except KeyboardInterrupt:
        print("\n👋 Application interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error running application: {e}")
        return 1
    
    print("\n👋 Thanks for using Enhanced Virtual Painter!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 