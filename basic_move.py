#!/usr/bin/env python3
"""
Basic mouse move examples
"""
from mouse_mover import MouseMover
import pyautogui
import time

def basic_move():
    mover = MouseMover()
    
    print("=== Basic Mouse Move Examples ===\n")
    
    # Get screen dimensions
    screen_width, screen_height = pyautogui.size()
    print(f"Screen size: {screen_width}x{screen_height}\n")
    
    # Example 1: Move to center of screen
    print("1. Moving to screen center:")
    mover.move_to(screen_width // 2, screen_height // 2)
    time.sleep(1)
    
    # Example 2: Move to corners
    print("\n2. Moving to top-left corner:")
    mover.move_to(100, 100)
    time.sleep(0.5)
    
    print("3. Moving to top-right corner:")
    mover.move_to(screen_width - 100, 100)
    time.sleep(0.5)
    
    print("4. Moving to bottom-right corner:")
    mover.move_to(screen_width - 100, screen_height - 100)
    time.sleep(0.5)
    
    print("5. Moving to bottom-left corner:")
    mover.move_to(100, screen_height - 100)
    time.sleep(0.5)
    
    # Example 3: Relative movements
    print("\n6. Moving relative (50, 50):")
    mover.move_relative(50, 50)
    time.sleep(0.5)
    
    print("7. Moving relative (-50, -50):")
    mover.move_relative(-50, -50)
    
    print("\n=== Basic examples completed ===")

if __name__ == "__main__":
    basic_move()
