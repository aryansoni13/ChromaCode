

import cv2
import numpy as np
import os
from datetime import datetime
from config import *

class CanvasManager:
    def __init__(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT):
        """Initialize the canvas manager."""
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width, 3), np.uint8)
        self.canvas.fill(0)  # Black background
        
        # History for undo/redo
        self.history = []
        self.history_index = -1
        self.max_history = 50
        
        # Drawing state
        self.last_point = None
        self.current_color = COLORS[0]  # White
        self.current_brush_size = DRAWING_BRUSH_SIZE
        self.is_erasing = False
        self.current_mode = "idle"  # idle, drawing, erasing, selecting
        
        # Create save directory
        os.makedirs(SAVE_DIRECTORY, exist_ok=True)
    
    def resize_canvas(self, new_width, new_height):
        """Resize the canvas to new dimensions."""
        if new_width != self.width or new_height != self.height:
            # Create new canvas with new dimensions
            new_canvas = np.zeros((new_height, new_width, 3), np.uint8)
            new_canvas.fill(0)
            
            # Copy existing content (if any)
            if self.canvas is not None:
                # Resize existing canvas content to fit new dimensions
                resized_content = cv2.resize(self.canvas, (new_width, new_height))
                new_canvas = resized_content
            
            self.canvas = new_canvas
            self.width = new_width
            self.height = new_height
            print(f"Canvas resized to: {new_width}x{new_height}")
    
    def clear_canvas(self):
        """Clear the canvas and reset history."""
        self.canvas = np.zeros((self.height, self.width, 3), np.uint8)
        self.canvas.fill(0)
        self.history = []
        self.history_index = -1
        self.last_point = None
    
    def save_state(self):
        """Save current canvas state to history."""
        # Remove any states after current index
        self.history = self.history[:self.history_index + 1]
        
        # Add current state
        state = self.canvas.copy()
        self.history.append(state)
        self.history_index += 1
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.history_index -= 1
    
    def undo(self):
        """Undo the last drawing action."""
        if self.history_index > 0 and self.history_index < len(self.history):
            self.history_index -= 1
            self.canvas = self.history[self.history_index].copy()
            return True
        return False
    
    def redo(self):
        """Redo the last undone action."""
        if self.history_index < len(self.history) - 1 and self.history_index >= 0:
            self.history_index += 1
            self.canvas = self.history[self.history_index].copy()
            return True
        return False
    
    def set_color(self, color):
        """Set the current drawing color."""
        self.current_color = color
        self.is_erasing = False
        # Keep current brush size but ensure we're in drawing mode
        if self.current_mode != "erasing":
            self.current_mode = "drawing"
    
    def set_brush_size(self, size):
        """Set the current brush size."""
        self.current_brush_size = size
        # Only update mode if we're not erasing
        if not self.is_erasing:
            self.current_mode = "drawing"
    
    def set_eraser(self, enabled=True):
        """Enable or disable eraser mode."""
        self.is_erasing = enabled
        if enabled:
            self.current_brush_size = ERASER_BRUSH_SIZE
            self.current_mode = "erasing"
        else:
            self.current_brush_size = DRAWING_BRUSH_SIZE
            self.current_mode = "drawing"
    
    def set_drawing_mode(self):
        """Set to drawing mode with appropriate brush size."""
        self.is_erasing = False
        self.current_brush_size = DRAWING_BRUSH_SIZE
        self.current_mode = "drawing"
    
    def set_selection_mode(self):
        """Set to selection mode with appropriate brush size."""
        self.is_erasing = False
        self.current_brush_size = SELECTION_BRUSH_SIZE
        self.current_mode = "selecting"
    
    def set_idle_mode(self):
        """Set to idle mode."""
        self.is_erasing = False
        self.current_mode = "idle"
    
    def draw_line(self, start_point, end_point):
        """Draw a line on the canvas."""
        if start_point is None or end_point is None:
            return
        
        # Save state before drawing
        if self.last_point is None:
            self.save_state()
        
        # Determine color and thickness based on current mode
        if self.is_erasing or self.current_mode == "erasing":
            color = (0, 0, 0)  # Black for erasing
            thickness = ERASER_BRUSH_SIZE
        elif self.current_mode == "selecting":
            color = self.current_color
            thickness = SELECTION_BRUSH_SIZE
        else:  # drawing mode
            color = self.current_color
            thickness = self.current_brush_size
        
        # Draw line
        cv2.line(self.canvas, start_point, end_point, color, thickness, cv2.FILLED)
    
    def update_drawing(self, current_point):
        """Update drawing with current hand position."""
        if current_point is None:
            self.last_point = None
            return
        
        if self.last_point is not None:
            self.draw_line(self.last_point, current_point)
        
        self.last_point = current_point
    
    def reset_drawing_state(self):
        """Reset the drawing state when switching modes."""
        self.last_point = None
    
    def get_canvas_overlay(self, frame):
        """Get the canvas overlay for the frame."""
        # Ensure canvas and frame have the same dimensions
        if self.canvas.shape[:2] != frame.shape[:2]:
            # Resize canvas to match frame (create a copy to avoid modifying original)
            display_canvas = cv2.resize(self.canvas, (frame.shape[1], frame.shape[0]))
        else:
            display_canvas = self.canvas.copy()
        
        # Convert canvas to grayscale for masking
        gray_canvas = cv2.cvtColor(display_canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray_canvas, 1, 255, cv2.THRESH_BINARY)
        
        # Create inverse mask
        mask_inv = cv2.bitwise_not(mask)
        
        # Apply masks
        frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
        canvas_fg = cv2.bitwise_and(display_canvas, display_canvas, mask=mask)
        
        # Combine
        result = cv2.add(frame_bg, canvas_fg)
        return result
    
    def save_drawing(self, filename=None):
        """Save the current drawing to a file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"drawing_{timestamp}.{DEFAULT_SAVE_FORMAT}"
        
        filepath = os.path.join(SAVE_DIRECTORY, filename)
        
        try:
            cv2.imwrite(filepath, self.canvas)
            return filepath
        except Exception as e:
            print(f"Error saving drawing: {e}")
            return None
    
    def load_drawing(self, filepath):
        """Load a drawing from a file."""
        try:
            loaded_canvas = cv2.imread(filepath)
            if loaded_canvas is not None:
                # Resize if necessary
                if loaded_canvas.shape[:2] != (self.height, self.width):
                    loaded_canvas = cv2.resize(loaded_canvas, (self.width, self.height))
                
                self.canvas = loaded_canvas
                self.save_state()
                return True
        except Exception as e:
            print(f"Error loading drawing: {e}")
        
        return False
    
    def get_canvas(self):
        """Get the current canvas."""
        return self.canvas.copy()
    
    def get_drawing_info(self):
        """Get information about the current drawing."""
        # Count non-black pixels
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        non_zero_pixels = cv2.countNonZero(gray)
        total_pixels = self.width * self.height
        
        return {
            'width': self.width,
            'height': self.height,
            'pixels_drawn': non_zero_pixels,
            'coverage_percent': (non_zero_pixels / total_pixels) * 100,
            'history_size': len(self.history),
            'can_undo': self.history_index > 0,
            'can_redo': self.history_index < len(self.history) - 1,
            'current_mode': self.current_mode,
            'current_brush_size': self.current_brush_size,
            'is_erasing': self.is_erasing
        } 