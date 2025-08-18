# Chime System Redesign Summary

## Overview
The chime system has been completely redesigned to implement a queue-based architecture with improved configuration management and special handling for blinker chimes.

## Key Changes

### 1. CHIME_CONFIG (Replaces CHIME_FILES)
- **Old**: Simple file mapping dictionary
- **New**: Comprehensive configuration with chime parameters
```python
CHIME_CONFIG = {
    "blinker": {
        "file": "blinker.mp3",
        "type": "once",
        "duration": 1,
        "priority": "high",  # Special case - can play in parallel
        "volume": 50
    },
    # ... other chimes with full configuration
}
```

### 2. CHIME_INFO Structure
New class to encapsulate chime request information:
```python
class ChimeInfo:
    def __init__(self, chime_name, deck_num, card_num, telltale_id=None):
        self.chime_name = chime_name
        self.deck_num = deck_num
        self.card_num = card_num
        self.telltale_id = telltale_id
        self.timestamp = datetime.now()
        self.config = CHIME_CONFIG.get(chime_name, {})
```

### 3. Event Queue System
- **Global FIFO Queue**: `chime_event_queue = queue.Queue()`
- **Queue Handler**: `ChimeQueueHandler` class manages all chime requests
- **FIFO Processing**: Chimes are played in the order they were requested

### 4. Special Blinker Handling
- **Parallel Playback**: Blinker chimes (TT016, TT017) can play simultaneously with other chimes
- **Immediate Execution**: Blinker requests bypass the queue and play immediately
- **Dedicated Player**: Separate `blinker_player` for parallel audio playback

## Architecture Components

### ChimeQueueHandler Class
```python
class ChimeQueueHandler:
    def __init__(self):
        self.current_player = QMediaPlayer()
        self.blinker_player = QMediaPlayer()  # Special for blinkers
        self.chime_event_queue = queue.Queue()
        self.is_playing = False
    
    def enqueue_chime(self, chime_info):
        # Special handling for blinker
        if chime_info.chime_name == "blinker":
            self.play_blinker_chime(chime_info)
            return
        
        # Add to FIFO queue for other chimes
        chime_event_queue.put(chime_info)
        if not self.is_playing:
            self.play_next_chime()
```

### Updated TellTaleWidget
```python
def setup_chime(self, chime_name, duration):
    """Setup chime for this telltale using the new queue system"""
    if chime_name in CHIME_CONFIG:
        # Create ChimeInfo object
        telltale_id = f"{self.deck_num}_{self.card_num}"
        chime_info = ChimeInfo(chime_name, self.deck_num, self.card_num, telltale_id)
        
        # Enqueue the chime request
        chime_handler.enqueue_chime(chime_info)
```

## Chime Types and Behavior

### 1. Once Chimes
- Play once and wait for duration
- Examples: `door_ajar`, `low_fuel`, `parking_brake_engaged`

### 2. Twice Chimes
- Play twice with 800ms delay between plays
- Example: `engine_check`

### 3. Continuous Chimes
- Play repeatedly every 3 seconds
- Example: `jeep_seatbelt_alert`

### 4. Blinker Chimes (Special)
- Play immediately in parallel
- Can overlap with any other chime
- Examples: TT016 (Left Turn), TT017 (Right Turn)

## Queue Processing Logic

1. **Chime Request**: When a telltale is activated, a `ChimeInfo` object is created
2. **Queue Decision**: 
   - If blinker → play immediately in parallel
   - If other chime → add to FIFO queue
3. **FIFO Processing**: Chimes are played one at a time in request order
4. **Duration Management**: Each chime waits for its configured duration before next chime
5. **Error Handling**: Missing files are logged and queue continues

## Benefits of New Design

1. **Predictable Order**: FIFO ensures chimes play in the order they were triggered
2. **No Audio Conflicts**: Only one non-blinker chime plays at a time
3. **Special Blinker Handling**: Turn signals can play alongside any other chime
4. **Configurable Parameters**: Each chime has its own type, duration, volume, and priority
5. **Better Logging**: Comprehensive logging of chime events and queue status
6. **Extensible**: Easy to add new chime types and parameters

## Test Functions

The redesigned system includes several test functions:

- `test_application()`: Tests multiple chimes in queue
- `test_application2()`: Tests blinker parallel playback
- `test_application3()`: Tests different chime types
- `test_chime_functionality()`: Comprehensive FIFO queue test

## Usage Example

```python
# Activate telltales to test the queue
window.activate_telltale(51, 1)  # engine_check (twice) - first in queue
window.activate_telltale(52, 2)  # jeep_seatbelt_alert (once) - second in queue
window.activate_telltale(59, 1)  # blinker (special) - plays immediately in parallel
```

## File Structure

- `workshop4.py`: Complete redesigned system
- `CHIME_REDESIGN_SUMMARY.md`: This documentation
- `chimes/`: Directory containing all chime audio files
- `logs/`: Generated log files with chime event details

The redesigned system provides a robust, predictable, and extensible chime management solution that handles the special requirements for blinker chimes while maintaining orderly playback for all other chime types. 