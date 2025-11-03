#!/usr/bin/env python3
"""
Sound Notification Module
Cross-platform sound notification functionality
"""
import sys
import platform

class SoundNotifier:
    """Cross-platform sound notification"""
    
    def __init__(self):
        self.platform = platform.system()
    
    def play_notification(self):
        """
        Play a notification sound
        Returns True if sound was played successfully, False otherwise
        """
        try:
            if self.platform == 'Windows':
                self._play_windows_sound()
            elif self.platform == 'Darwin':  # macOS
                self._play_macos_sound()
            else:  # Linux and other Unix-like systems
                self._play_linux_sound()
            return True
        except Exception as e:
            print(f"Warning: Could not play sound: {e}")
            return False
    
    def _play_windows_sound(self):
        """Play sound on Windows"""
        try:
            import winsound
            # Play system default beep
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except (ImportError, AttributeError):
            try:
                # Fallback: try system beep
                import winsound
                winsound.Beep(1000, 500)  # Frequency 1000Hz, duration 500ms
            except (ImportError, Exception):
                # Last resort: ASCII bell
                print('\a', end='', flush=True)
    
    def _play_macos_sound(self):
        """Play sound on macOS"""
        import subprocess
        try:
            # Try using afplay with system sound
            subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'], 
                         check=True, timeout=2, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            try:
                # Fallback: use say command to make a beep sound
                subprocess.run(['say', '-v', 'Samantha', 'beep'], 
                             check=True, timeout=2, capture_output=True)
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                # Last resort: system beep
                print('\a', end='', flush=True)  # ASCII bell character
    
    def _play_linux_sound(self):
        """Play sound on Linux"""
        import subprocess
        import os
        
        # Try different sound commands
        commands = [
            ['aplay', '/usr/share/sounds/alsa/Front_Left.wav'],
            ['paplay', '/usr/share/sounds/freedesktop/stereo/message.oga'],
            ['beep'],  # Requires beep package
        ]
        
        # Also try using Python's print bell as fallback
        for cmd in commands:
            try:
                subprocess.run(cmd, check=True, timeout=2, 
                             capture_output=True, stderr=subprocess.DEVNULL)
                return
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        # Last resort: ASCII bell
        print('\a', end='', flush=True)
