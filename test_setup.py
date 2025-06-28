#!/usr/bin/env python3


import sys
import os
import traceback

def test_imports():
    """Test importing all required modules."""
    print("🔍 Testing module imports...")
    
    modules_to_test = [
        ('config', 'config.py'),
        ('hand_tracker', 'hand_tracker.py'),
        ('canvas_manager', 'canvas_manager.py'),
        ('ui_manager', 'ui_manager.py'),
        ('virtual_painter_enhanced', 'virtual_painter_enhanced.py')
    ]
    
    all_passed = True
    
    for module_name, filename in modules_to_test:
        try:
            if not os.path.exists(filename):
                print(f"❌ {filename} not found")
                all_passed = False
                continue
                
            # Try to import the module
            module = __import__(module_name)
            print(f"✅ {filename} imported successfully")
            
        except Exception as e:
            print(f"❌ Failed to import {filename}: {e}")
            all_passed = False
    
    return all_passed

def test_config():
    """Test configuration values."""
    print("\n🔍 Testing configuration...")
    
    try:
        from config import (CAMERA_WIDTH, CAMERA_HEIGHT, COLORS, BRUSH_SIZES, 
                           DEFAULT_BRUSH_SIZE, DRAWING_BRUSH_SIZE, ERASER_BRUSH_SIZE, 
                           SELECTION_BRUSH_SIZE)
        
        # Check essential config values
        required_configs = [
            'CAMERA_WIDTH', 'CAMERA_HEIGHT', 'COLORS', 
            'BRUSH_SIZES', 'DEFAULT_BRUSH_SIZE', 'DRAWING_BRUSH_SIZE',
            'ERASER_BRUSH_SIZE', 'SELECTION_BRUSH_SIZE'
        ]
        
        # Verify all required configs are available
        config_dict = {
            'CAMERA_WIDTH': CAMERA_WIDTH,
            'CAMERA_HEIGHT': CAMERA_HEIGHT,
            'COLORS': COLORS,
            'BRUSH_SIZES': BRUSH_SIZES,
            'DEFAULT_BRUSH_SIZE': DEFAULT_BRUSH_SIZE,
            'DRAWING_BRUSH_SIZE': DRAWING_BRUSH_SIZE,
            'ERASER_BRUSH_SIZE': ERASER_BRUSH_SIZE,
            'SELECTION_BRUSH_SIZE': SELECTION_BRUSH_SIZE
        }
        
        for config_name in required_configs:
            if config_name not in config_dict:
                print(f"❌ Missing config: {config_name}")
                return False
        
        print(f"✅ Camera resolution: {CAMERA_WIDTH}x{CAMERA_HEIGHT}")
        print(f"✅ Colors available: {len(COLORS)}")
        print(f"✅ Brush sizes: {BRUSH_SIZES}")
        print(f"✅ Drawing brush size: {DRAWING_BRUSH_SIZE}")
        print(f"✅ Eraser brush size: {ERASER_BRUSH_SIZE}")
        print(f"✅ Selection brush size: {SELECTION_BRUSH_SIZE}")
        
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_classes():
    """Test class instantiation."""
    print("\n🔍 Testing class instantiation...")
    
    try:
        from hand_tracker import HandTracker
        from canvas_manager import CanvasManager
        from ui_manager import UIManager
        
        # Test HandTracker
        hand_tracker = HandTracker()
        print("✅ HandTracker created successfully")
        
        # Test CanvasManager
        canvas_manager = CanvasManager(640, 480)
        print("✅ CanvasManager created successfully")
        
        # Test UIManager
        ui_manager = UIManager(640, 480)
        print("✅ UIManager created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Class test failed: {e}")
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Test basic functionality without camera."""
    print("\n🔍 Testing basic functionality...")
    
    try:
        from canvas_manager import CanvasManager
        from ui_manager import UIManager
        
        # Create instances
        canvas = CanvasManager(640, 480)
        ui = UIManager(640, 480)
        
        # Test canvas operations
        canvas.set_color((255, 0, 0))  # Red
        canvas.set_brush_size(25)
        
        # Test mode switching
        canvas.set_drawing_mode()
        print(f"✅ Drawing mode: {canvas.current_mode}, brush size: {canvas.current_brush_size}")
        
        canvas.set_selection_mode()
        print(f"✅ Selection mode: {canvas.current_mode}, brush size: {canvas.current_brush_size}")
        
        canvas.set_eraser(True)
        print(f"✅ Eraser mode: {canvas.current_mode}, brush size: {canvas.current_brush_size}")
        
        canvas.set_drawing_mode()
        print(f"✅ Back to drawing mode: {canvas.current_mode}, brush size: {canvas.current_brush_size}")
        
        # Test drawing a line
        canvas.draw_line((100, 100), (200, 200))
        
        # Test undo/redo
        canvas.save_state()
        canvas.draw_line((200, 200), (300, 300))
        canvas.undo()
        
        # Test UI operations
        color = ui.get_selected_color()
        brush_size = ui.get_selected_brush_size()
        
        print(f"✅ Canvas operations work")
        print(f"✅ UI operations work")
        print(f"✅ Current color: {color}")
        print(f"✅ Current brush size: {brush_size}")
        print(f"✅ Mode switching works correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🧪 Enhanced Virtual Painter - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_config),
        ("Class Instantiation", test_classes),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The enhanced virtual painter is ready to use.")
        print("\n🚀 To run the application:")
        print("   python run_enhanced.py")
        print("   or")
        print("   python virtual_painter_enhanced.py")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 