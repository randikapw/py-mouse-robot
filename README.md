# Python Mouse Mover

A simple Python script for mouse movement automation that works on both Windows and Mac platforms.

## Features

- Cross-platform mouse control (Windows & Mac)
- Various mouse movement patterns:
  - Absolute position movement
  - Relative movement
  - Smooth linear movements
  - Circular movements
  - Square patterns
  - Wiggle movements (keep system awake)

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install directly:
```bash
pip install pyautogui
```

## Usage

### Run main examples:
```bash
python mouse_mover.py
```

### Run individual examples:
```bash
# Basic movement examples
python basic_move.py

# Smooth movement examples
python smooth_move.py

# Circular movement examples
python circular_move.py
```

### Use in your own code:

```python
from mouse_mover import MouseMover
import time

def my_function():
    mover = MouseMover()
    
    # Move to specific coordinates
    mover.move_to(500, 300)
    
    # Move relative to current position
    mover.move_relative(100, 50)
    
    # Smooth move from point A to point B
    mover.smooth_move(100, 100, 500, 500, duration=1.0)
    
    # Move in a circle
    mover.move_circle(960, 540, 100, steps=36, duration=2.0)
    
    # Move in a square
    mover.move_square(400, 300, 200, duration=1.0)
    
    # Wiggle mouse (keep system awake)
    mover.wiggle(duration=5, interval=1)

if __name__ == "__main__":
    my_function()
```

## API Reference

### `MouseMover` Class

#### Methods

- **`move_to(x, y)`**: Move mouse to absolute coordinates
  - `x`: X coordinate
  - `y`: Y coordinate

- **`move_relative(delta_x, delta_y)`**: Move mouse relative to current position
  - `delta_x`: Change in X coordinate
  - `delta_y`: Change in Y coordinate

- **`smooth_move(start_x, start_y, end_x, end_y, steps, duration)`**: Move mouse smoothly in a line
  - `start_x`: Starting X coordinate
  - `start_y`: Starting Y coordinate
  - `end_x`: Ending X coordinate
  - `end_y`: Ending Y coordinate
  - `steps`: Number of steps (optional, duration takes precedence)
  - `duration`: Duration of movement in seconds (default: 1.0)

- **`move_circle(center_x, center_y, radius, steps, duration)`**: Move mouse in a circular path
  - `center_x`: Center X coordinate
  - `center_y`: Center Y coordinate
  - `radius`: Radius of the circle
  - `steps`: Number of steps to complete the circle (default: 36)
  - `duration`: Duration for complete circle in seconds (default: 2.0)

- **`move_square(start_x, start_y, side_length, duration)`**: Move mouse in a square pattern
  - `start_x`: Starting X coordinate (top-left)
  - `start_y`: Starting Y coordinate (top-left)
  - `side_length`: Length of each side
  - `duration`: Duration for each side in seconds (default: 1.0)

- **`get_current_position()`**: Get current mouse position
  - Returns: Tuple (x, y) of current mouse position

- **`wiggle(duration, interval)`**: Wiggle mouse with small random movements
  - `duration`: Duration in seconds (default: 5)
  - `interval`: Interval between movements in seconds (default: 1)

## Platform Support

- ✅ Windows
- ✅ macOS (Mac)
- ✅ Linux

## Notes

- **Permissions:**
  - On macOS, you may need to grant accessibility permissions:
    - Go to System Preferences → Security & Privacy → Privacy → Accessibility
    - Add Terminal (or Python) to the allowed apps list
  - On Windows, the application should work without additional permissions.

- **Failsafe:** By default, pyautogui has a failsafe that moves your mouse to the top-left corner to stop scripts. In this script, failsafe is disabled for smoother operation. You can press Ctrl+C to stop the script.

## License

MIT
