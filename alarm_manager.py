#!/usr/bin/env python3
"""
Alarm Manager Module
Handles timeout alarm and ding notifications for consecutive auto-move cycles
"""
import time
from sound_notifier import SoundNotifier


class AlarmManager:
    """Manages alarm timeout and ding notifications"""
    
    def __init__(self, timeout_seconds=1800, check_interval_seconds=300, ding_duration=1.0):
        """
        Initialize the alarm manager
        :param timeout_seconds: Time in seconds before playing alarm (default: 1800 = 30 minutes)
        :param check_interval_seconds: Time between position checks in seconds (for max ding calculation)
        :param ding_duration: Duration of each ding in seconds (default: 1.0)
        """
        self.timeout_seconds = timeout_seconds
        self.check_interval_seconds = check_interval_seconds
        self.ding_duration = ding_duration
        self.sound_notifier = SoundNotifier()
        
        # Track time of last manual mouse movement
        self.last_manual_movement_time = time.time()
        
        # Track consecutive auto-move cycles (for ding count) - only after alarm triggers
        self.consecutive_auto_move_count = 0
        
        # Track when last alarm was played
        self.last_alarm_time = 0
        
        # Track if alarm has been triggered (dings only play after alarm)
        self.alarm_triggered = False
        
        # Calculate maximum ding count
        # Max dings = min(20, cycle_interval_seconds / ding_duration)
        # This ensures we don't play more dings than can fit in one cycle
        calculated_max = int(check_interval_seconds / ding_duration)
        self.max_ding_count = min(20, calculated_max)
    
    def reset(self):
        """Reset all counters to initial state"""
        self.last_manual_movement_time = time.time()
        if self.consecutive_auto_move_count > 0 or self.alarm_triggered:
            msg_parts = []
            if self.alarm_triggered:
                msg_parts.append("alarm triggered")
            if self.consecutive_auto_move_count > 0:
                msg_parts.append(f"{self.consecutive_auto_move_count} consecutive auto-moves")
            print(f"   ↻ Resetting alarm counters ({', '.join(msg_parts)})")
        self.consecutive_auto_move_count = 0
        self.last_alarm_time = 0
        self.alarm_triggered = False  # Reset alarm trigger flag
    
    def on_manual_movement(self):
        """Called when manual mouse movement is detected"""
        self.reset()
    
    def on_auto_move(self):
        """Called when auto-move happens"""
        # Check and play alarm if timeout reached (this must happen first)
        alarm_just_triggered = self._check_and_play_alarm()
        
        # Only play dings AFTER alarm has been triggered
        if self.alarm_triggered:
            # Increment consecutive auto-move count (only after alarm)
            self.consecutive_auto_move_count += 1
            
            # Calculate how many dings to play (capped at max)
            # Dings increase: 1st cycle after alarm = 1 ding, 2nd = 2 dings, 3rd = 3 dings, etc.
            ding_count = min(self.consecutive_auto_move_count, self.max_ding_count)
            
            # Play the dings after every auto-move cycle (only after alarm)
            self._play_dings(ding_count)
        elif not alarm_just_triggered:
            # No alarm yet, no dings
            pass
    
    def _play_dings(self, count):
        """
        Play multiple dings with 1 second gap between each
        :param count: Number of dings to play
        """
        if count == 0:
            return
        
        print(f"   🔔 Playing {count} ding(s) after auto-move cycle #{self.consecutive_auto_move_count}...")
        
        all_success = True
        for i in range(count):
            if i > 0:
                # Wait 1 second between dings (except before first ding)
                time.sleep(self.ding_duration)
            
            success = self.sound_notifier.play_notification()
            if not success:
                all_success = False
                print(f"      ✗ Ding #{i+1} failed to play")
            else:
                print(f"      ✓ Ding #{i+1} played")
        
        if all_success:
            print(f"   ✓ All {count} ding(s) played successfully")
    
    def _check_and_play_alarm(self):
        """
        Check if timeout (alarm) is reached and play alarm sound
        Alarm plays once when timeout is reached
        Returns True if alarm was just triggered, False otherwise
        """
        current_time = time.time()
        elapsed_since_manual = current_time - self.last_manual_movement_time
        
        # Check if timeout reached and enough time passed since last alarm
        time_since_last_alarm = current_time - self.last_alarm_time if self.last_alarm_time > 0 else elapsed_since_manual
        
        if elapsed_since_manual >= self.timeout_seconds and time_since_last_alarm >= self.timeout_seconds:
            # Alarm timeout reached
            timeout_minutes = self.timeout_seconds / 60
            timeout_minutes_str = f"{timeout_minutes:.2f}" if timeout_minutes < 1 else f"{timeout_minutes:.1f}"
            elapsed_minutes = elapsed_since_manual / 60
            elapsed_minutes_str = f"{elapsed_minutes:.2f}" if elapsed_minutes < 1 else f"{elapsed_minutes:.1f}"
            
            print(f"\n🚨 ALARM: No manual mouse movement for {elapsed_minutes_str} minutes "
                  f"(timeout: {timeout_minutes_str} minutes)")
            print("   Playing alarm sound...")
            
            success = self.sound_notifier.play_notification()
            if success:
                print("   ✓ Alarm sound played successfully")
            else:
                print("   ✗ Failed to play alarm sound")
            
            # Mark alarm as triggered (this enables dings to start/continue playing)
            # Do NOT reset ding counter here; it must continue increasing up to the cap
            self.alarm_triggered = True
            
            # Update last alarm time (but don't reset manual movement time)
            self.last_alarm_time = current_time
            return True
        
        return False
    
    def get_status_info(self):
        """
        Get status information for display
        :return: Dictionary with status info
        """
        timeout_minutes = self.timeout_seconds / 60
        timeout_minutes_str = f"{timeout_minutes:.2f}" if timeout_minutes < 1 else f"{timeout_minutes:.1f}"
        
        return {
            'timeout_minutes': timeout_minutes_str,
            'timeout_seconds': self.timeout_seconds,
            'max_ding_count': self.max_ding_count,
            'consecutive_auto_moves': self.consecutive_auto_move_count,
            'check_interval_seconds': self.check_interval_seconds
        }
