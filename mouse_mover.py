#!/usr/bin/env python3
"""
Basic mouse movement examples for Windows and Mac
"""
import pyautogui
import time
import math
import random

# Disable pyautogui failsafe (optional - remove if you want failsafe enabled)
pyautogui.FAILSAFE = False

class MouseMover:
    """Class for mouse movement operations"""
    
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
    
    def move_to(self, x, y):
        """
        Move mouse to absolute coordinates
        :param x: X coordinate
        :param y: Y coordinate
        """
        try:
            pyautogui.moveTo(x, y)
            print(f"Mouse moved to ({x}, {y})")
        except Exception as e:
            print(f"Error moving mouse: {e}")
    
    def move_relative(self, delta_x, delta_y):
        """
        Move mouse relative to current position
        :param delta_x: Change in X coordinate
        :param delta_y: Change in Y coordinate
        """
        try:
            current_x, current_y = pyautogui.position()
            new_x = current_x + delta_x
            new_y = current_y + delta_y
            pyautogui.moveTo(new_x, new_y)
            print(f"Mouse moved relative by ({delta_x}, {delta_y})")
        except Exception as e:
            print(f"Error moving mouse: {e}")
    
    def smooth_move(self, start_x, start_y, end_x, end_y, steps=50, duration=1.0):
        """
        Move mouse smoothly in a line
        :param start_x: Starting X coordinate
        :param start_y: Starting Y coordinate
        :param end_x: Ending X coordinate
        :param end_y: Ending Y coordinate
        :param steps: Number of steps for smooth movement (optional, duration takes precedence)
        :param duration: Duration of movement in seconds
        """
        try:
            pyautogui.moveTo(start_x, start_y)
            pyautogui.moveTo(end_x, end_y, duration=duration)
            print(f"Smooth move completed from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        except Exception as e:
            print(f"Error in smooth move: {e}")
    
    def move_circle(self, center_x, center_y, radius, steps=36, duration=2.0):
        """
        Move mouse in a circular path
        :param center_x: Center X coordinate
        :param center_y: Center Y coordinate
        :param radius: Radius of the circle
        :param steps: Number of steps to complete the circle
        :param duration: Duration for complete circle in seconds
        """
        try:
            step_duration = duration / steps
            for i in range(steps + 1):
                angle = (i / steps) * 2 * math.pi
                x = int(center_x + radius * math.cos(angle))
                y = int(center_y + radius * math.sin(angle))
                pyautogui.moveTo(x, y, duration=step_duration)
            print(f"Circular move completed around ({center_x}, {center_y}) with radius {radius}")
        except Exception as e:
            print(f"Error in circular move: {e}")
    
    def move_square(self, start_x, start_y, side_length, duration=1.0):
        """
        Move mouse in a square pattern
        :param start_x: Starting X coordinate (top-left)
        :param start_y: Starting Y coordinate (top-left)
        :param side_length: Length of each side
        :param duration: Duration for each side in seconds
        """
        try:
            corners = [
                (start_x, start_y),  # top-left
                (start_x + side_length, start_y),  # top-right
                (start_x + side_length, start_y + side_length),  # bottom-right
                (start_x, start_y + side_length),  # bottom-left
                (start_x, start_y)  # back to start
            ]
            
            for corner in corners:
                pyautogui.moveTo(corner[0], corner[1], duration=duration / 5)
            
            print(f"Square move completed starting at ({start_x}, {start_y}) with side length {side_length}")
        except Exception as e:
            print(f"Error in square move: {e}")
    
    def get_current_position(self):
        """
        Get current mouse position
        :return: Tuple (x, y) of current mouse position
        """
        try:
            x, y = pyautogui.position()
            print(f"Current mouse position: ({x}, {y})")
            return (x, y)
        except Exception as e:
            print(f"Error getting mouse position: {e}")
            return None
    
    def wiggle(self, duration=5, interval=1):
        """
        Wiggle mouse (small random movements) - useful for keeping system awake
        :param duration: Duration in seconds
        :param interval: Interval between movements in seconds
        """
        try:
            start_pos = pyautogui.position()
            start_time = time.time()
            
            while time.time() - start_time < duration:
                delta_x = random.randint(-5, 5)
                delta_y = random.randint(-5, 5)
                new_x = start_pos[0] + delta_x
                new_y = start_pos[1] + delta_y
                pyautogui.moveTo(new_x, new_y, duration=0.1)
                time.sleep(interval)
            
            # Return to original position
            pyautogui.moveTo(start_pos[0], start_pos[1])
            print(f"Wiggle completed for {duration} seconds")
        except Exception as e:
            print(f"Error in wiggle: {e}")


def main():
    """Example usage"""
    mover = MouseMover()
    
    print("=== Mouse Mover Examples ===\n")
    
    # Get current position
    print("1. Getting current mouse position:")
    mover.get_current_position()
    time.sleep(1)
    
    # Move to specific coordinates
    print("\n2. Moving to (500, 300):")
    mover.move_to(500, 300)
    time.sleep(1)
    
    # Move relative
    print("\n3. Moving relative by (100, 50):")
    mover.move_relative(100, 50)
    time.sleep(1)
    
    # Smooth move
    print("\n4. Performing smooth move:")
    current_pos = pyautogui.position()
    mover.smooth_move(current_pos[0], current_pos[1], current_pos[0] + 200, current_pos[1] + 100, duration=1.0)
    time.sleep(1)
    
    # Circle move
    print("\n5. Performing circular move:")
    circle_center = pyautogui.position()
    mover.move_circle(circle_center[0], circle_center[1], 50, steps=36, duration=2.0)
    time.sleep(1)
    
    # Square move
    print("\n6. Performing square move:")
    square_start = pyautogui.position()
    mover.move_square(square_start[0] - 50, square_start[1] - 50, 100, duration=1.0)
    
    print("\n=== All examples completed ===")


if __name__ == "__main__":
    main()
