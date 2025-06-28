
import cv2
import numpy as np
from config import *

class UIManager:
    def __init__(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT):
        """Initialize the UI manager."""
        self.width = width
        self.height = height
        self.num_colors = len(COLORS)
        self.button_width = width // self.num_colors
        self.selected_color_idx = 0
        self.selected_brush_size_idx = 3  # Default brush size index
        
        # UI state
        self.show_brush_sizes = False
        self.show_help = False
        self.show_info = False
        
        # Create color buttons
        self.color_buttons = self._create_color_buttons()
        self.brush_size_buttons = self._create_brush_size_buttons()
    
    def _create_color_buttons(self):
        """Create color button images."""
        buttons = []
        for i, color in enumerate(COLORS):
            # Create button image
            button = np.zeros((BUTTON_HEIGHT, self.button_width, 3), np.uint8)
            button.fill(0)  # Black background
            
            # Fill with color
            cv2.rectangle(button, (0, 0), (self.button_width, BUTTON_HEIGHT), color, -1)
            
            # Add border
            cv2.rectangle(button, (0, 0), (self.button_width, BUTTON_HEIGHT), (255, 255, 255), 2)
            
            # Add color name
            color_names = ['White', 'Purple', 'Red', 'Green', 'Cyan', 'Maroon', 'Blue', 'Black', 
                          'Orange', 'Pink', 'Yellow', 'Gray']
            if i < len(color_names):
                cv2.putText(button, color_names[i], (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.4, (255, 255, 255) if color == (0, 0, 0) else (0, 0, 0), 1)
            
            buttons.append(button)
        
        return buttons
    
    def _create_brush_size_buttons(self):
        """Create brush size button images."""
        buttons = []
        button_height = 40
        button_width = 60
        
        for i, size in enumerate(BRUSH_SIZES):
            button = np.zeros((button_height, button_width, 3), np.uint8)
            button.fill(50)  # Dark gray background
            
            # Draw circle representing brush size
            center = (button_width // 2, button_height // 2)
            radius = min(size // 3, 25)  # Scale down for display
            cv2.circle(button, center, radius, (255, 255, 255), -1)
            
            # Add size text
            cv2.putText(button, str(size), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.4, (255, 255, 255), 1)
            
            buttons.append(button)
        
        return buttons
    
    def draw_header(self, frame):
        """Draw the header with color selection buttons."""
        # Draw color buttons
        for i in range(self.num_colors):
            x1 = i * self.button_width
            x2 = (i + 1) * self.button_width
            
            # Place button image
            frame[0:BUTTON_HEIGHT, x1:x2] = self.color_buttons[i]
            
            # Highlight selected color
            if i == self.selected_color_idx:
                cv2.rectangle(frame, (x1, 0), (x2, BUTTON_HEIGHT), 
                             SELECTION_BORDER_COLOR, SELECTION_BORDER_THICKNESS)
        
        # Draw brush size selector
        if self.show_brush_sizes:
            self._draw_brush_size_selector(frame)
        
        # Draw mode indicator
        self._draw_mode_indicator(frame)
    
    def _draw_brush_size_selector(self, frame):
        """Draw brush size selection panel."""
        panel_width = 150
        panel_height = 40
        x = self.width - panel_width - 10
        y = BUTTON_HEIGHT + 5
        
        # Background
        cv2.rectangle(frame, (x, y), (x + panel_width, y + panel_height), (0, 0, 0), -1)
        cv2.rectangle(frame, (x, y), (x + panel_width, y + panel_height), (255, 255, 255), 1)
        
        # Title
        cv2.putText(frame, "Brush Size:", (x + 5, y + 12), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.4, (255, 255, 255), 1)
        
        # Brush size buttons (show fewer buttons to fit)
        for i, button in enumerate(self.brush_size_buttons[:6]):  # Show only first 6 sizes
            bx = x + 10 + i * 25
            by = y + 15
            # Scale down the button
            small_button = cv2.resize(button, (20, 15))
            frame[by:by+15, bx:bx+20] = small_button
            
            # Highlight selected size
            if i == self.selected_brush_size_idx:
                cv2.rectangle(frame, (bx, by), (bx + 20, by + 15), (0, 255, 255), 1)
    
    def _draw_mode_indicator(self, frame):
        """Draw current mode indicator."""
        mode_text = self._get_current_mode_text()
        if mode_text:
            cv2.putText(frame, mode_text, (10, self.height - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (255, 255, 255), 2)
    
    def _get_current_mode_text(self):
        """Get text for current mode."""
        if self.show_help:
            return "Help Mode - Press 'H' to exit"
        elif self.show_info:
            return "Info Mode - Press 'I' to exit"
        return ""
    
    def draw_help_overlay(self, frame):
        """Draw help overlay."""
        if not self.show_help:
            return frame
        
        # Semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (self.width, self.height), (0, 0, 0), -1)
        frame = cv2.addWeighted(frame, 0.3, overlay, 0.7, 0)
        
        # Help text
        help_text = [
            "VIRTUAL PAINTER - HELP",
            "",
            "GESTURES:",
            "• Index finger up: Draw mode (Brush: 25px)",
            "• Index + Middle up: Selection mode (Brush: 15px)",
            "• Fist (all fingers down): Eraser mode (Brush: 100px)",
            "• Thumb + Index down: Alternative eraser",
            "",
            "MODE-SPECIFIC BRUSH SIZES:",
            "• Drawing Mode: Uses selected brush size (5-100px)",
            "• Selection Mode: Fixed 15px for precise selection",
            "• Eraser Mode: Fixed 100px for easy erasing",
            "",
            "KEYBOARD SHORTCUTS:",
            "• 'C': Clear canvas",
            "• 'S': Save drawing",
            "• 'L': Load drawing",
            "• 'Z': Undo",
            "• 'Y': Redo",
            "• 'B': Toggle brush sizes",
            "• 'E': Toggle eraser mode",
            "• 'H': Toggle help",
            "• 'I': Show info",
            "• 'Q': Quit",
            "",
            "Press 'H' to close help"
        ]
        
        y_start = 60
        for i, text in enumerate(help_text):
            y = y_start + i * 20
            color = (255, 255, 0) if i == 0 else (255, 255, 255)
            thickness = 2 if i == 0 else 1
            cv2.putText(frame, text, (30, y), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.4, color, thickness)
        
        return frame
    
    def draw_info_overlay(self, frame, canvas_info):
        """Draw information overlay."""
        if not self.show_info:
            return frame
        
        # Semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (self.width, self.height), (0, 0, 0), -1)
        frame = cv2.addWeighted(frame, 0.3, overlay, 0.7, 0)
        
        # Info text
        info_text = [
            "DRAWING INFORMATION",
            "",
            f"Canvas Size: {canvas_info['width']} x {canvas_info['height']}",
            f"Pixels Drawn: {canvas_info['pixels_drawn']:,}",
            f"Coverage: {canvas_info['coverage_percent']:.1f}%",
            f"History Size: {canvas_info['history_size']}",
            f"Can Undo: {'Yes' if canvas_info['can_undo'] else 'No'}",
            f"Can Redo: {'Yes' if canvas_info['can_redo'] else 'No'}",
            "",
            f"Current Mode: {canvas_info['current_mode'].title()}",
            f"Current Color: {self.get_color_name(self.selected_color_idx)}",
            f"Current Brush Size: {canvas_info['current_brush_size']}",
            f"Eraser Active: {'Yes' if canvas_info['is_erasing'] else 'No'}",
            "",
            "Press 'I' to close info"
        ]
        
        y_start = 60
        for i, text in enumerate(info_text):
            y = y_start + i * 20
            color = (255, 255, 0) if i == 0 else (255, 255, 255)
            thickness = 2 if i == 0 else 1
            cv2.putText(frame, text, (30, y), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.4, color, thickness)
        
        return frame
    
    def get_color_name(self, index):
        """Get color name by index."""
        color_names = ['White', 'Purple', 'Red', 'Green', 'Cyan', 'Maroon', 'Blue', 'Black', 
                      'Orange', 'Pink', 'Yellow', 'Gray']
        if 0 <= index < len(color_names):
            return color_names[index]
        return f"Color {index}"
    
    def handle_color_selection(self, x, y):
        """Handle color selection based on coordinates."""
        if y < BUTTON_HEIGHT:
            idx = x // self.button_width
            if 0 <= idx < self.num_colors:
                self.selected_color_idx = idx
                return COLORS[idx]
        return None
    
    def handle_brush_size_selection(self, x, y):
        """Handle brush size selection based on coordinates."""
        if not self.show_brush_sizes:
            return None
        
        panel_width = 150
        panel_height = 40
        panel_x = self.width - panel_width - 10
        panel_y = BUTTON_HEIGHT + 5
        
        if (panel_x <= x <= panel_x + panel_width and 
            panel_y <= y <= panel_y + panel_height):
            
            # Check if click is on a brush size button (show only first 6 sizes)
            for i in range(min(6, len(BRUSH_SIZES))):
                bx = panel_x + 10 + i * 25
                by = panel_y + 15
                if (bx <= x <= bx + 20 and by <= y <= by + 15):
                    self.selected_brush_size_idx = i
                    return BRUSH_SIZES[i]
        
        return None
    
    def toggle_brush_sizes(self):
        """Toggle brush size panel visibility."""
        self.show_brush_sizes = not self.show_brush_sizes
    
    def toggle_help(self):
        """Toggle help overlay visibility."""
        self.show_help = not self.show_help
        if self.show_help:
            self.show_info = False
    
    def toggle_info(self):
        """Toggle info overlay visibility."""
        self.show_info = not self.show_info
        if self.show_info:
            self.show_help = False
    
    def get_selected_color(self):
        """Get currently selected color."""
        return COLORS[self.selected_color_idx]
    
    def get_selected_brush_size(self):
        """Get currently selected brush size."""
        if 0 <= self.selected_brush_size_idx < len(BRUSH_SIZES):
            return BRUSH_SIZES[self.selected_brush_size_idx]
        return BRUSH_SIZES[3]  # Default to index 3 if out of bounds
    
    def draw_mode_status(self, frame, canvas_info):
        """Draw detailed mode status information."""
        # Draw mode indicator in top-right corner
        mode = canvas_info.get('current_mode', 'idle').title()
        brush_size = canvas_info.get('current_brush_size', 25)
        is_erasing = canvas_info.get('is_erasing', False)
        
        # Background for mode indicator
        text = f"Mode: {mode}"
        if is_erasing:
            text += " (ERASER)"
        else:
            text += f" (Brush: {brush_size})"
        
        # Get text size for background
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        
        # Draw background rectangle
        x = self.width - text_width - 15
        y = 35
        cv2.rectangle(frame, (x - 8, y - text_height - 8), 
                     (x + text_width + 8, y + 8), (0, 0, 0), -1)
        cv2.rectangle(frame, (x - 8, y - text_height - 8), 
                     (x + text_width + 8, y + 8), (255, 255, 255), 1)
        
        # Draw text with different colors for different modes
        if is_erasing:
            color = (0, 0, 255)  # Red for eraser
            thickness = 2  # Make eraser text bolder
        elif mode == "Drawing":
            color = (0, 255, 0)  # Green for drawing
        elif mode == "Selecting":
            color = (255, 255, 0)  # Yellow for selection
        else:
            color = (255, 255, 255)  # White for idle
        
        cv2.putText(frame, text, (x, y), font, font_scale, color, thickness) 