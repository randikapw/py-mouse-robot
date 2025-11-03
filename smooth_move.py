#!/usr/bin/env python3
"""
Smooth mouse move examples
"""
from mouse_mover import MouseMover
import pyautogui
import time

def smooth_move():
    mover = MouseMover()
    
    print("=== Smooth Mouse Move Examples ===\n")
    
    # Get current position
    start_pos = pyautogui.position()
    print(f"Starting position: ({start_pos[0]}, {start_pos[1]})\n")
    
    # Example 1: Smooth horizontal line
    print("1. Smooth horizontal line (200px):")
    mover.smooth_move(start_pos[0], start_pos[1], start_pos[0] + 200, start_pos[1], duration=1.0)
    time.sleep(1)
    
    # Example 2: Smooth vertical line
    print("\n2. Smooth vertical line (200px):")
    pos1 = pyautogui.position()
    mover.smooth_move(pos1[0], pos1[1], pos1[0], pos1[1] + 200, duration=1.0)
    time.sleep(1)
    
    # Example 3: Smooth diagonal line
    print("\n3. Smooth diagonal line:")
    pos2 = pyautogui.position()
    mover.smooth_move(pos2[0], pos2[1], pos2[0] + 300, pos2[1] + 200, duration=1.5)
    time.sleep(1)
    
    # Example 4: Smooth curve (using multiple line segments)
    print("\n4. Smooth curved path (using line segments):")
    pos3 = pyautogui.position()
    segments = [
        (pos3[0] + 100, pos3[1]),
        (pos3[0] + 150, pos3[1] - 50),
        (pos3[0] + 200, pos3[1]),
        (pos3[0] + 250, pos3[1] + 50),
        (pos3[0] + 300, pos3[1])
    ]
    
    for segment in segments:
        current_pos = pyautogui.position()
        mover.smooth_move(current_pos[0], current_pos[1], segment[0], segment[1], duration=0.3)
        time.sleep(0.2)
    
    print("\n=== Smooth move examples completed ===")

if __name__ == "__main__":
    smooth_move()
