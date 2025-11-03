# Auto Mouse Mover

An automatic mouse mover that monitors your mouse position and moves it smoothly to a random location if it hasn't moved much. Perfect for keeping your system awake or preventing screensavers.

## Features

- ✅ Monitors mouse position at configurable intervals
- ✅ Compares current position with previous position
- ✅ Automatically moves mouse smoothly if it hasn't moved (within threshold)
- ✅ Moves to random locations within configurable distance range
- ✅ Graceful shutdown with Ctrl+C
- ✅ Cross-platform (Windows, Mac, Linux)

## Installation

Make sure you have the dependencies installed:
```bash
pip install pyautogui
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage (Default Settings)
```bash
python auto_mouse_mover.py
```

Defaults:
- Interval: 5 minutes (use minutes with decimals)
- Threshold: 10px (manual movement sensitivity)
- Random move distance: 100–500px
- Alarm timeout: 30 minutes

### Custom Configuration

You can configure all parameters via command-line arguments:

```bash
# Interval in minutes (decimals allowed). Example: check every 30 seconds
python auto_mouse_mover.py --interval 0.5

# Higher threshold (require more manual movement to count as moved)
python auto_mouse_mover.py --threshold 20

# Move farther each time
python auto_mouse_mover.py --min-distance 200 --max-distance 600

# Alarm after 15 minutes without manual movement
python auto_mouse_mover.py --timeout 15

# Combined
python auto_mouse_mover.py -i 0.25 -t 15 -min 150 -max 600 --timeout 20
```

### Command Line Arguments

- `--interval` or `-i`: Time in minutes between position checks (minimum: 0.033 = 2 seconds; default: 5.0)
- `--threshold` or `-t`: Maximum pixel difference to consider mouse as "not moved" (default: 10)
- `--min-distance` or `-min`: Minimum distance in pixels for random movement (default: 100)
- `--max-distance` or `-max`: Maximum distance in pixels for random movement (default: 500)
- `--timeout` or `-to`: Time in minutes before alarm if no manual movement (minimum: 0.167 = 10 seconds; default: 30.0)

### Examples

```bash
# Very sensitive - checks every 2 seconds, moves if less than 5 pixels moved
python auto_mouse_mover.py --interval 2 --threshold 5

# Less frequent - checks every 30 seconds, moves if less than 50 pixels moved
python auto_mouse_mover.py --interval 30 --threshold 50 --min-distance 200 --max-distance 800

# Quick movements - small random movements
python auto_mouse_mover.py --min-distance 50 --max-distance 150
```

## How It Works

1. **Initialization**: Records the starting mouse position
2. **Monitoring**: Every N seconds (configurable), checks current mouse position
3. **Comparison**: Compares current position with previous position
4. **Action**: If mouse hasn't moved more than threshold pixels:
   - Calculates a random position within distance range
   - Moves mouse smoothly to that position
5. **Alarm and Dings**
   - Before alarm: No dings are played
   - When timeout is reached (no manual movement for `--timeout`): one-time alarm sound plays
   - After alarm: each auto-move cycle plays dings that increase by 1 each cycle
   - Ding count is capped at `min(20, interval_seconds / 1)` and persists across further alarms
   - Manual movement resets alarm and ding count back to zero (no dings until next alarm)

Example timeline (interval 15s → max 15 dings):

```
Cycle 1..N before timeout: Auto-move → no ding

[After 30 minutes with no manual movement]
🚨 ALARM plays (once)

Cycle N+1: Auto-move → 1 ding
Cycle N+2: Auto-move → 2 dings
...
Cycle N+15: Auto-move → 15 dings (stays at 15 in subsequent cycles)

[Manual movement]
→ reset; start over with no dings until next alarm
```

## Stopping the Program

Press `Ctrl+C` to gracefully stop the program. It will:
- Stop monitoring immediately
- Display final statistics
- Exit cleanly

## Use Cases

- **Keep system awake**: Prevents your computer from going to sleep
- **Prevent screensaver**: Keeps screensaver from activating
- **Stay active on applications**: Useful for applications that require mouse activity
- **Testing**: Test mouse movement and automation

## Platform Notes

- **Windows**: Works out of the box
- **Mac**: May require accessibility permissions:
  - System Preferences → Security & Privacy → Privacy → Accessibility
  - Add Terminal/Python to allowed apps
- **Linux**: Should work without additional permissions

## Troubleshooting

### Mouse moves even when I'm using it
- Increase the `--threshold` value to require more movement
- Increase the `--interval` to check less frequently

### Mouse doesn't move when I want it to
- Decrease the `--threshold` value to be more sensitive
- Decrease the `--interval` to check more frequently

### Movement is too fast/slow
- The movement duration is automatically calculated based on distance
- Larger distances take longer to ensure smooth movement

## License

MIT
