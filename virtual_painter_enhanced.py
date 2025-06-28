
import cv2
import time
import os
import sys
from datetime import datetime

# Import our custom modules
from config import *
from hand_tracker import HandTracker
from canvas_manager import CanvasManager
from ui_manager import UIManager

class VirtualPainter:
    def __init__(self):
        """Initialize the Virtual Painter application."""
        self.cap = None
        self.hand_tracker = None
        self.canvas_manager = None
        self.ui_manager = None
        
        # Application state
        self.running = False
        self.selection_cooldown = 0
        self.current_mode = ""
        self.last_fps_time = 0
        self.frame_count = 0
        
        # Initialize components
        self._initialize_camera()
        self._initialize_components()
        
    def _initialize_camera(self):
        """Initialize the camera."""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Error: Could not open camera.")
                sys.exit(1)
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
            self.cap.set(cv2.CAP_PROP_BRIGHTNESS, CAMERA_BRIGHTNESS)
            
            print(f"Camera initialized: {CAMERA_WIDTH}x{CAMERA_HEIGHT}")
            
        except Exception as e:
            print(f"Error initializing camera: {e}")
            sys.exit(1)
    
    def _initialize_components(self):
        """Initialize all application components."""
        try:
            self.hand_tracker = HandTracker()
            self.canvas_manager = CanvasManager(CANVAS_WIDTH, CANVAS_HEIGHT)
            self.ui_manager = UIManager(CANVAS_WIDTH, CANVAS_HEIGHT)
            
            print("All components initialized successfully.")
            
        except Exception as e:
            print(f"Error initializing components: {e}")
            sys.exit(1)
    
    def _handle_keyboard_input(self, key):
        """Handle keyboard input."""
        if key == ord('q'):
            self.running = False
        elif key == ord('c'):
            self.canvas_manager.clear_canvas()
            print("Canvas cleared.")
        elif key == ord('s'):
            filepath = self.canvas_manager.save_drawing()
            if filepath:
                print(f"Drawing saved to: {filepath}")
            else:
                print("Error saving drawing.")
        elif key == ord('l'):
            # For now, just print a message. In a full app, you'd show a file dialog
            print("Load functionality - implement file dialog here.")
        elif key == ord('z'):
            if self.canvas_manager.undo():
                print("Undo performed.")
            else:
                print("Nothing to undo.")
        elif key == ord('y'):
            if self.canvas_manager.redo():
                print("Redo performed.")
            else:
                print("Nothing to redo.")
        elif key == ord('b'):
            self.ui_manager.toggle_brush_sizes()
            print("Brush size panel toggled.")
        elif key == ord('h'):
            self.ui_manager.toggle_help()
        elif key == ord('i'):
            self.ui_manager.toggle_info()
    
    def _process_hand_gestures(self, frame):
        """Process hand gestures and update application state."""
        if not self.hand_tracker.landmarks:
            if self.current_mode != "":
                self.current_mode = ""
                self.canvas_manager.set_idle_mode()
                self.canvas_manager.reset_drawing_state()
            return
        
        # Process first hand (for simplicity)
        landmarks = self.hand_tracker.landmarks[0]
        
        # Get finger positions
        index_tip = self.hand_tracker.get_index_tip(landmarks)
        middle_tip = self.hand_tracker.get_middle_tip(landmarks)
        
        if not index_tip:
            return
        
        x, y = index_tip
        
        # Handle selection mode (index + middle up)
        if (self.hand_tracker.is_selection_gesture(landmarks) and 
            self.selection_cooldown == 0):
            
            # Switch to selection mode
            if self.current_mode != "Selection Mode":
                self.current_mode = "Selection Mode"
                self.canvas_manager.set_selection_mode()
                self.canvas_manager.reset_drawing_state()
                print("Mode: Selection Mode")
            
            # Color selection
            selected_color = self.ui_manager.handle_color_selection(x, y)
            if selected_color:
                self.canvas_manager.set_color(selected_color)
                self.selection_cooldown = SELECTION_DELAY
                print(f"Color selected: {self.ui_manager.get_color_name(self.ui_manager.selected_color_idx)}")
            
            # Brush size selection
            selected_size = self.ui_manager.handle_brush_size_selection(x, y)
            if selected_size:
                self.canvas_manager.set_brush_size(selected_size)
                self.selection_cooldown = SELECTION_DELAY
                print(f"Brush size selected: {selected_size}")
            
            # Visual feedback
            if middle_tip:
                cv2.rectangle(frame, index_tip, middle_tip, 
                             self.canvas_manager.current_color, cv2.FILLED)
        
        # Handle drawing mode (only index up)
        elif self.hand_tracker.is_drawing_gesture(landmarks) and y > DRAWING_THRESHOLD:
            # Switch to drawing mode
            if self.current_mode != "Drawing Mode":
                self.current_mode = "Drawing Mode"
                self.canvas_manager.set_drawing_mode()
                self.canvas_manager.reset_drawing_state()
                print("Mode: Drawing Mode")
            
            self.canvas_manager.update_drawing(index_tip)
        
        # Handle eraser mode (fist)
        elif self.hand_tracker.is_eraser_gesture(landmarks) and y > DRAWING_THRESHOLD:
            # Switch to eraser mode
            if self.current_mode != "Eraser Mode":
                self.current_mode = "Eraser Mode"
                self.canvas_manager.set_eraser(True)
                self.canvas_manager.reset_drawing_state()
                print("Mode: Eraser Mode")
            
            self.canvas_manager.update_drawing(index_tip)
        
        else:
            # No specific gesture detected
            if self.current_mode:
                self.current_mode = ""
                self.canvas_manager.set_idle_mode()
                self.canvas_manager.reset_drawing_state()
        
        # Update cooldown
        if self.selection_cooldown > 0:
            self.selection_cooldown -= 1
    
    def _draw_ui_elements(self, frame):
        """Draw all UI elements on the frame."""
        # Draw header with color selection
        self.ui_manager.draw_header(frame)
        
        # Draw mode status (new detailed mode indicator)
        self.ui_manager.draw_mode_status(frame, self.canvas_manager.get_drawing_info())
        
        # Draw mode text (legacy, can be removed later)
        if SHOW_MODE_TEXT and self.current_mode:
            cv2.putText(frame, self.current_mode, (10, 130), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Draw FPS
        if SHOW_FPS:
            self._draw_fps(frame)
        
        # Draw overlays
        self.ui_manager.draw_help_overlay(frame)
        self.ui_manager.draw_info_overlay(frame, self.canvas_manager.get_drawing_info())
    
    def _draw_fps(self, frame):
        """Draw FPS counter."""
        self.frame_count += 1
        current_time = time.time()
        
        if current_time - self.last_fps_time >= 1.0:
            fps = self.frame_count / (current_time - self.last_fps_time)
            self.frame_count = 0
            self.last_fps_time = current_time
            
            # Store FPS for display
            self.current_fps = int(fps)
        
        # Draw FPS
        cv2.putText(frame, f'FPS: {getattr(self, "current_fps", 0)}', 
                   (self.ui_manager.width - 120, 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    
    def run(self):
        """Main application loop."""
        print("Starting Virtual Painter...")
        print("Press 'H' for help, 'Q' to quit.")
        
        self.running = True
        self.last_fps_time = time.time()
        
        try:
            while self.running:
                # Read frame
                success, frame = self.cap.read()
                if not success:
                    print("Error reading frame.")
                    break
                
                # Process hand tracking
                frame = self.hand_tracker.process_frame(frame)
                
                # Process gestures
                self._process_hand_gestures(frame)
                
                # Apply canvas overlay
                frame = self.canvas_manager.get_canvas_overlay(frame)
                
                # Draw UI elements
                self._draw_ui_elements(frame)
                
                # Show windows
                cv2.imshow('Virtual Painter', frame)
                cv2.imshow('Canvas', self.canvas_manager.get_canvas())
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key != 255:
                    self._handle_keyboard_input(key)
                
                # Control frame rate
                if TARGET_FPS > 0:
                    time.sleep(1.0 / TARGET_FPS)
        
        except KeyboardInterrupt:
            print("\nApplication interrupted by user.")
        
        except Exception as e:
            print(f"Error in main loop: {e}")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        print("Cleaning up...")
        
        if self.cap:
            self.cap.release()
        
        if self.hand_tracker:
            self.hand_tracker.release()
        
        cv2.destroyAllWindows()
        print("Cleanup complete.")

def main():
    """Main entry point."""
    try:
        painter = VirtualPainter()
        painter.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 