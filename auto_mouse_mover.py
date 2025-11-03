#!/usr/bin/env python3
"""
Automatic Mouse Mover
Monitors mouse position and moves it smoothly to a random location if it hasn't moved much.
Useful for keeping system awake or preventing screensaver.
"""
import pyautogui
import time
import math
import random
import signal
import sys
from alarm_manager import AlarmManager

# Disable pyautogui failsafe for smoother operation
pyautogui.FAILSAFE = True  # You can move mouse to top-left corner to stop

class AutoMouseMover:
    """Automatically moves mouse if it hasn't moved much"""
    
    def __init__(self, check_interval_seconds=300, delta_threshold=10, min_distance=100, 
                 max_distance=500, timeout_seconds=1800):
        """
        Initialize the auto mouse mover
        :param check_interval_seconds: Time in seconds between position checks (default: 300 = 5 minutes)
        :param delta_threshold: Maximum pixel difference to consider mouse as "not moved" (default: 10)
        :param min_distance: Minimum distance for random movement (default: 100)
        :param max_distance: Maximum distance for random movement (default: 500)
        :param timeout_seconds: Time in seconds before playing alarm if no manual movement (default: 1800 = 30 minutes)
        """
        self.check_interval = check_interval_seconds
        self.delta_threshold = delta_threshold
        self.min_distance = min_distance
        self.max_distance = max_distance
        self.running = True
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Initialize alarm manager
        self.alarm_manager = AlarmManager(
            timeout_seconds=timeout_seconds,
            check_interval_seconds=check_interval_seconds
        )
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        if sys.platform == 'win32':
            signal.signal(signal.SIGBREAK, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signals (Ctrl+C)"""
        print("\n\nStopping auto mouse mover...")
        self.running = False
    
    def _get_distance(self, pos1, pos2):
        """
        Calculate distance between two positions
        :param pos1: Tuple (x, y)
        :param pos2: Tuple (x, y)
        :return: Distance in pixels
        """
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def _has_moved(self, previous_pos, current_pos):
        """
        Check if mouse has moved significantly
        :param previous_pos: Previous position tuple (x, y)
        :param current_pos: Current position tuple (x, y)
        :return: True if mouse has moved more than threshold, False otherwise
        """
        distance = self._get_distance(previous_pos, current_pos)
        return distance > self.delta_threshold
    
    def _generate_random_position(self, current_pos):
        """
        Generate a random position to move to
        :param current_pos: Current position tuple (x, y)
        :return: Random position tuple (x, y)
        """
        # Generate random angle and distance
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(self.min_distance, self.max_distance)
        
        # Calculate new position
        new_x = int(current_pos[0] + distance * math.cos(angle))
        new_y = int(current_pos[1] + distance * math.sin(angle))
        
        # Ensure position is within screen bounds
        new_x = max(50, min(new_x, self.screen_width - 50))
        new_y = max(50, min(new_y, self.screen_height - 50))
        
        return (new_x, new_y)
    
    def _move_to_random_location(self, current_pos):
        """
        Move mouse smoothly to a random location
        :param current_pos: Current position tuple (x, y)
        """
        target_pos = self._generate_random_position(current_pos)
        distance = self._get_distance(current_pos, target_pos)
        
        # Adjust duration based on distance (smooth movement)
        duration = min(2.0, max(0.5, distance / 200))
        
        try:
            pyautogui.moveTo(target_pos[0], target_pos[1], duration=duration)
            print(f"  ✓ Moved mouse from ({current_pos[0]}, {current_pos[1]}) to ({target_pos[0]}, {target_pos[1]}) "
                  f"[Distance: {int(distance)}px, Duration: {duration:.2f}s]")
        except Exception as e:
            print(f"  ✗ Error moving mouse: {e}")
    
    def start(self):
        """Start monitoring and auto-moving mouse"""
        # Convert seconds to minutes for display
        interval_minutes = self.check_interval / 60
        interval_minutes_str = f"{interval_minutes:.2f}" if interval_minutes < 1 else f"{interval_minutes:.1f}"
        
        # Get status info from alarm manager
        status = self.alarm_manager.get_status_info()
        timeout_minutes_str = status['timeout_minutes']
        timeout_seconds = status['timeout_seconds']
        max_ding_count = status['max_ding_count']
        
        print("=== Auto Mouse Mover Started ===")
        print("Configuration:")
        print(f"  - Check interval: {interval_minutes_str} minutes ({self.check_interval} seconds)")
        print(f"  - Movement threshold: {self.delta_threshold} pixels")
        print(f"  - Random move distance: {self.min_distance}-{self.max_distance} pixels")
        print(f"  - Alarm timeout: {timeout_minutes_str} minutes ({timeout_seconds} seconds)")
        print(f"  - Max ding count per cycle: {max_ding_count} (calculated: min(20, {self.check_interval}s / 1s))")
        print(f"  - Screen size: {self.screen_width}x{self.screen_height}")
        print("\nPress Ctrl+C to stop\n")
        
        # Get initial position
        previous_pos = pyautogui.position()
        print(f"Initial mouse position: ({previous_pos[0]}, {previous_pos[1]})")
        print(f"Monitoring mouse movement every {interval_minutes_str} minutes ({self.check_interval} seconds)...")
        print(f"Alarm will play if no manual movement detected for {timeout_minutes_str} minutes.")
        print(f"Dings will play after each auto-move cycle, increasing by 1 up to {max_ding_count}.\n")
        
        check_count = 0
        
        try:
            while self.running:
                # Wait for check interval
                time.sleep(self.check_interval)
                
                if not self.running:
                    break
                
                # Get current position
                current_pos = pyautogui.position()
                check_count += 1
                
                # Check if mouse has moved
                if self._has_moved(previous_pos, current_pos):
                    # Manual mouse movement detected - reset alarm manager
                    distance = self._get_distance(previous_pos, current_pos)
                    print(f"[Check #{check_count}] Mouse moved: {int(distance)}px "
                          f"({previous_pos[0]}, {previous_pos[1]}) → ({current_pos[0]}, {current_pos[1]})")
                    
                    # Reset alarm manager (resets both alarm and ding counters)
                    self.alarm_manager.on_manual_movement()
                    
                    previous_pos = current_pos
                else:
                    # Mouse hasn't moved much, move it to random location
                    distance = self._get_distance(previous_pos, current_pos)
                    print(f"[Check #{check_count}] Mouse barely moved ({int(distance)}px < {self.delta_threshold}px threshold)")
                    print(f"  Current position: ({current_pos[0]}, {current_pos[1]})")
                    
                    # Perform auto-move
                    self._move_to_random_location(current_pos)
                    
                    # Notify alarm manager of auto-move (plays dings and checks alarm)
                    self.alarm_manager.on_auto_move()
                    
                    # Update previous position to new location
                    previous_pos = pyautogui.position()
        
        except KeyboardInterrupt:
            print("\n\nReceived interrupt signal...")
        
        finally:
            print("\n=== Auto Mouse Mover Stopped ===")
            print(f"Total checks performed: {check_count}")
            status = self.alarm_manager.get_status_info()
            print(f"Final consecutive auto-move count: {status['consecutive_auto_moves']}")


def main():
    """Main function with configurable parameters"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Automatically moves mouse if it has not moved significantly',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Default settings (check every 5 minutes, alarm after 30 minutes)
  python auto_mouse_mover.py
  
  # Check every 10 minutes with 20px threshold
  python auto_mouse_mover.py --interval 10 --threshold 20
  
  # Check every 0.5 minutes (30 seconds), move 200-400 pixels away
  python auto_mouse_mover.py --interval 0.5 --min-distance 200 --max-distance 400
  
  # Check every 0.033 minutes (2 seconds - minimum allowed)
  python auto_mouse_mover.py --interval 0.033
  
  # Set alarm timeout to 15 minutes
  python auto_mouse_mover.py --timeout 15
  
  # Set alarm timeout to 0.5 minutes (30 seconds)
  python auto_mouse_mover.py --timeout 0.5
  
  # Example: Check every 15 seconds, max 15 dings per cycle
  python auto_mouse_mover.py --interval 0.25 --timeout 10
  
  # Example: Check every 1 minute, max 20 dings per cycle (capped at 20)
  python auto_mouse_mover.py --interval 1.0 --timeout 30
        '''
    )
    
    parser.add_argument(
        '--interval', '-i',
        type=float,
        default=5.0,
        help='Time in minutes between position checks (minimum: 0.033 = 2 seconds, default: 5.0)'
    )
    
    parser.add_argument(
        '--threshold', '-t',
        type=int,
        default=10,
        help='Maximum pixel difference to consider mouse as "not moved" (default: 10)'
    )
    
    parser.add_argument(
        '--min-distance', '-min',
        type=int,
        default=100,
        help='Minimum distance in pixels for random movement (default: 100)'
    )
    
    parser.add_argument(
        '--max-distance', '-max',
        type=int,
        default=500,
        help='Maximum distance in pixels for random movement (default: 500)'
    )
    
    parser.add_argument(
        '--timeout', '-to',
        type=float,
        default=30.0,
        help='Time in minutes before playing alarm if no manual movement (minimum: 0.167 = 10 seconds, default: 30.0)'
    )
    
    args = parser.parse_args()
    
    # Convert minutes to seconds and validate minimum
    MIN_INTERVAL_MINUTES = 2.0 / 60.0  # 2 seconds minimum
    if args.interval < MIN_INTERVAL_MINUTES:
        print(f"Error: Interval must be at least {MIN_INTERVAL_MINUTES:.3f} minutes (2 seconds)")
        print(f"       You provided: {args.interval} minutes")
        sys.exit(1)
    
    # Validate timeout minimum (10 seconds = 10/60 minutes)
    MIN_TIMEOUT_MINUTES = 10.0 / 60.0  # 10 seconds minimum
    if args.timeout < MIN_TIMEOUT_MINUTES:
        print(f"Error: Timeout must be at least {MIN_TIMEOUT_MINUTES:.3f} minutes (10 seconds)")
        print(f"       You provided: {args.timeout} minutes")
        sys.exit(1)
    
    # Convert minutes to seconds
    check_interval_seconds = args.interval * 60
    timeout_seconds = args.timeout * 60
    
    # Create and start auto mouse mover
    mover = AutoMouseMover(
        check_interval_seconds=check_interval_seconds,
        delta_threshold=args.threshold,
        min_distance=args.min_distance,
        max_distance=args.max_distance,
        timeout_seconds=timeout_seconds
    )
    
    mover.start()


if __name__ == "__main__":
    main()