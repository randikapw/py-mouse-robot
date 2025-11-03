#!/usr/bin/env python3
"""
Circular mouse move examples
"""
from mouse_mover import MouseMover
import pyautogui
import time
import math

def circular_move():
    mover = MouseMover()
    
    print("=== Circular Mouse Move Examples ===\n")
    
    # Get current position to use as center
    center_pos = pyautogui.position()
    print(f"Circle center: ({center_pos[0]}, {center_pos[1]})\n")
    
    # Example 1: Small circle
    print("1. Small circle (radius: 30px):")
    mover.move_circle(center_pos[0], center_pos[1], 30, steps=36, duration=1.5)
    time.sleep(1)
    
    # Example 2: Medium circle
    print("\n2. Medium circle (radius: 60px):")
    mover.move_circle(center_pos[0], center_pos[1], 60, steps=48, duration=2.0)
    time.sleep(1)
    
    # Example 3: Large circle
    print("\n3. Large circle (radius: 100px):")
    mover.move_circle(center_pos[0], center_pos[1], 100, steps=60, duration=2.5)
    time.sleep(1)
    
    # Example 4: Square pattern
    print("\n4. Square pattern:")
    square_pos = pyautogui.position()
    mover.move_square(square_pos[0] - 75, square_pos[1] - 75, 150, duration=1.0)
    time.sleep(1)
    
    # Example 5: Figure-8 pattern (two overlapping circles)
    print("\n5. Figure-8 pattern:")
    fig8_pos = pyautogui.position()
    radius = 50
    
    # First half (top circle)
    for i in range(37):
        angle = (i / 36) * math.pi  # 0 to π (half circle)
        x = int(fig8_pos[0] + radius * math.sin(angle))
        y = int(fig8_pos[1] - radius * math.cos(angle))
        pyautogui.moveTo(x, y, duration=0.03)
    
    # Second half (bottom circle, opposite direction)
    for i in range(37):
        angle = math.pi - (i / 36) * math.pi  # π to 0 (half circle, reverse)
        x = int(fig8_pos[0] + radius * math.sin(angle))
        y = int(fig8_pos[1] + radius * math.cos(angle))
        pyautogui.moveTo(x, y, duration=0.03)
    
    print("\n=== Circular move examples completed ===")

if __name__ == "__main__":
    circular_move()
