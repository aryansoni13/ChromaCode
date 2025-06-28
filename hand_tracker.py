
import cv2
import mediapipe as mp
import numpy as np
from config import *

class HandTracker:
    def __init__(self):
        """Initialize the hand tracker with MediaPipe."""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_NUM_HANDS,
            min_detection_confidence=HAND_DETECTION_CONFIDENCE,
            min_tracking_confidence=HAND_TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.landmarks = []
        
    def process_frame(self, frame):
        """Process a frame and extract hand landmarks."""
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        self.landmarks = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
                
                # Extract landmark coordinates
                landmarks = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarks.append([id, cx, cy])
                
                self.landmarks.append(landmarks)
        
        return frame
    
    def get_finger_state(self, landmarks):
        """Determine which fingers are up based on landmark positions."""
        if not landmarks:
            return []
            
        tips = [4, 8, 12, 16, 20]  # Finger tip landmark IDs
        fingers = []
        
        # Thumb (special case - compare x coordinates)
        if len(landmarks) > 4:
            fingers.append(1 if landmarks[4][1] > landmarks[3][1] else 0)
        
        # Other fingers (compare y coordinates)
        for i in range(1, 5):
            if len(landmarks) > tips[i]:
                fingers.append(1 if landmarks[tips[i]][2] < landmarks[tips[i]-2][2] else 0)
            else:
                fingers.append(0)
        
        return fingers
    
    def get_hand_center(self, landmarks):
        """Get the center point of the hand."""
        if not landmarks:
            return None
            
        # Use middle finger tip (landmark 12) as center
        if len(landmarks) > 12:
            return (landmarks[12][1], landmarks[12][2])
        return None
    
    def get_index_tip(self, landmarks):
        """Get the index finger tip position."""
        if not landmarks or len(landmarks) < 9:
            return None
        return (landmarks[8][1], landmarks[8][2])
    
    def get_middle_tip(self, landmarks):
        """Get the middle finger tip position."""
        if not landmarks or len(landmarks) < 13:
            return None
        return (landmarks[12][1], landmarks[12][2])
    
    def is_selection_gesture(self, landmarks):
        """Check if the hand is in selection gesture (index and middle up, others down)."""
        if not landmarks:
            return False
            
        fingers = self.get_finger_state(landmarks)
        if len(fingers) >= 5:
            return fingers[1] and fingers[2] and not fingers[3] and not fingers[4]
        return False
    
    def is_drawing_gesture(self, landmarks):
        """Check if the hand is in drawing gesture (only index up)."""
        if not landmarks:
            return False
            
        fingers = self.get_finger_state(landmarks)
        if len(fingers) >= 5:
            return fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]
        return False
    
    def is_eraser_gesture(self, landmarks):
        """Check if the hand is in eraser gesture (fist - all fingers down)."""
        if not landmarks:
            return False
            
        fingers = self.get_finger_state(landmarks)
        if len(fingers) >= 5:
            # Check if all fingers are down (fist gesture)
            # Allow some tolerance for thumb position
            thumb_down = fingers[0] == 0 if len(fingers) > 0 else False
            other_fingers_down = all(finger == 0 for finger in fingers[1:])  # All other fingers down
            
            return thumb_down and other_fingers_down
        return False
    
    def is_eraser_gesture_alternative(self, landmarks):
        """Alternative eraser gesture - thumb and index finger down, others up."""
        if not landmarks:
            return False
            
        fingers = self.get_finger_state(landmarks)
        if len(fingers) >= 5:
            # Thumb and index down, others up
            return (fingers[0] == 0 if len(fingers) > 0 else False and 
                    fingers[1] == 0 if len(fingers) > 1 else False and 
                    fingers[2] == 1 if len(fingers) > 2 else False and 
                    fingers[3] == 1 if len(fingers) > 3 else False and 
                    fingers[4] == 1 if len(fingers) > 4 else False)
        return False
    
    def release(self):
        """Release resources."""
        self.hands.close() 