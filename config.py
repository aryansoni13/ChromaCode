

# Camera settings
CAMERA_WIDTH = 800
CAMERA_HEIGHT = 600
CAMERA_BRIGHTNESS = 150

# Canvas settings
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CANVAS_BACKGROUND = (0, 0, 0)  # Black background

# UI settings
HEADER_HEIGHT = 80
BUTTON_HEIGHT = 80
SELECTION_BORDER_THICKNESS = 2
SELECTION_BORDER_COLOR = (0, 255, 255)  # Cyan

# Drawing settings
DEFAULT_BRUSH_SIZE = 25
DEFAULT_ERASER_SIZE = 100
DEFAULT_SELECTION_SIZE = 15
BRUSH_SIZES = [5, 10, 15, 25, 35, 50, 75, 100]

# Mode-specific brush sizes
DRAWING_BRUSH_SIZE = 25
ERASER_BRUSH_SIZE = 100
SELECTION_BRUSH_SIZE = 15

# Gesture settings
SELECTION_DELAY = 15  # Frames to wait before allowing new selection
DRAWING_THRESHOLD = 80  # Y-coordinate threshold for drawing mode

# Color palette
COLORS = [
    (255, 255, 255),   # White
    (128, 0, 128),     # Purple
    (255, 0, 0),       # Red
    (0, 255, 0),       # Green
    (0, 255, 255),     # Cyan
    (128, 0, 0),       # Maroon
    (0, 0, 255),       # Blue
    (0, 0, 0),         # Black
    (255, 165, 0),     # Orange
    (255, 192, 203),   # Pink
    (255, 255, 0),     # Yellow
    (128, 128, 128),   # Gray
]

# MediaPipe settings
HAND_DETECTION_CONFIDENCE = 0.7
HAND_TRACKING_CONFIDENCE = 0.5
MAX_NUM_HANDS = 2

# File settings
SAVE_DIRECTORY = "saved_drawings"
DEFAULT_SAVE_FORMAT = "png"

# Performance settings
TARGET_FPS = 30
SHOW_FPS = True
SHOW_MODE_TEXT = True 