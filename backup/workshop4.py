# Modified workshop3_1.py with redesigned chime system

import sys
import os
import queue
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QProgressBar
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import logging
from datetime import datetime

# Setup minimal logging for chimes only
def setup_chime_logging():
    """Setup logging configuration for chime events only"""
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(logs_dir, f"chime_log_{timestamp}.log")
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, mode='w'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

# Initialize logger for chime events only
logger = setup_chime_logging()

DEFAULT_CARD_LENGTH = 10
BG_RESOLUTION = (1920, 720)
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "Images")
CHIMES_DIR = os.path.join(os.path.dirname(__file__), "chimes")

# Zone coordinates for telltales
ZONE_COORDINATES = {
    1: {"x": 400, "y": 40},
    2: {"x": 550, "y": 40},
    3: {"x": 700, "y": 40},
    4: {"x": 850, "y": 40},
    5: {"x": 1000, "y": 40},
    6: {"x": 1150, "y": 40},
    7: {"x": 1300, "y": 40}
}

# Redesigned CHIME_CONFIG with chime parameters
CHIME_CONFIG = {
    "blinker": {
        "file": "blinker.mp3",
        "type": "once",
        "duration": 1,
        "priority": "high",  # Special case - can play in parallel
        "volume": 50
    },
    "door_ajar": {
        "file": "door_ajar.mp3",
        "type": "once",
        "duration": 5,
        "priority": "normal",
        "volume": 50
    },
    "parking_brake_engaged": {
        "file": "parking_brake_engaged.mp3",
        "type": "once",
        "duration": 5,
        "priority": "normal",
        "volume": 50
    },
    "engine_check": {
        "file": "engine_check.mp3",
        "type": "twice",
        "duration": 5,
        "priority": "normal",
        "volume": 50
    },
    "low_fuel": {
        "file": "low_fuel.mp3",
        "type": "once",
        "duration": 5,
        "priority": "normal",
        "volume": 50
    },
    "tire_pressure_warning": {
        "file": "tire_pressure_warning.mp3",
        "type": "once",
        "duration": 5,
        "priority": "normal",
        "volume": 50
    },
    "jeep_door_open": {
        "file": "jeep_door_open.mp3",
        "type": "once",
        "duration": 5,
        "priority": "normal",
        "volume": 50
    },
    "jeep_key_left_in_ignition": {
        "file": "jeep_key_left_in_ignition.mp3",
        "type": "once",
        "duration": 5,
        "priority": "normal",
        "volume": 50
    },
    "jeep_seatbelt_alert": {
        "file": "jeep_seatbelt_alert.mp3",
        "type": "continuous",
        "duration": 90,
        "priority": "normal",
        "volume": 50
    }
}

# CHIME_INFO structure for chime details
class ChimeInfo:
    def __init__(self, chime_name, deck_num, card_num, telltale_id=None):
        self.chime_name = chime_name
        self.deck_num = deck_num
        self.card_num = card_num
        self.telltale_id = telltale_id
        self.timestamp = datetime.now()
        self.config = CHIME_CONFIG.get(chime_name, {})
    
    def __str__(self):
        return f"ChimeInfo({self.chime_name}, Deck:{self.deck_num}, Card:{self.card_num}, ID:{self.telltale_id})"

# Global chime event queue for FIFO processing
chime_event_queue = queue.Queue()

class ChimeQueueHandler:
    """Handles chime queue processing in FIFO sequence"""
    
    def __init__(self):
        self.current_player = QMediaPlayer()
        self.current_player.setVolume(50)
        self.current_player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.current_chime_info = None
        self.is_playing = False
        self.play_count = 0
        
        # Timer for managing delays between chimes
        self.delay_timer = QTimer()
        self.delay_timer.setSingleShot(True)
        self.delay_timer.timeout.connect(self.play_next_chime)
        
        # Special blinker player for parallel playback
        self.blinker_player = QMediaPlayer()
        self.blinker_player.setVolume(50)
        
        logger.info("ChimeQueueHandler initialized")
    
    def enqueue_chime(self, chime_info):
        """Add chime request to the queue"""
        if chime_info.chime_name == "blinker":
            # Blinker is special case - play immediately in parallel
            self.play_blinker_chime(chime_info)
            return
        
        # Add to FIFO queue for other chimes
        chime_event_queue.put(chime_info)
        logger.info(f"Chime enqueued: {chime_info}")
        
        # Start processing if not currently playing
        if not self.is_playing:
            self.play_next_chime()
    
    def play_next_chime(self):
        """Play the next chime in the queue"""
        if chime_event_queue.empty() or self.is_playing:
            return
        
        chime_info = chime_event_queue.get()
        self.current_chime_info = chime_info
        self.play_count = 0
        
        config = chime_info.config
        file_path = os.path.join(CHIMES_DIR, config["file"])
        
        if os.path.exists(file_path):
            self.current_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.current_player.setVolume(config.get("volume", 50))
            self.current_player.play()
            self.is_playing = True
            
            logger.info(f"Playing chime: {chime_info}")
        else:
            logger.error(f"Chime file not found: {file_path}")
            self.is_playing = False
            # Continue with next chime
            QTimer.singleShot(100, self.play_next_chime)
    
    def on_media_status_changed(self, status):
        """Handle media status changes for chime playback"""
        if status == QMediaPlayer.EndOfMedia and self.current_chime_info:
            config = self.current_chime_info.config
            chime_type = config.get("type", "once")
            
            if chime_type == "twice" and self.play_count < 1:
                # Play twice - schedule second play
                self.play_count += 1
                QTimer.singleShot(800, self.play_chime_again)
            else:
                # Chime finished - add delay and play next
                delay = config.get("duration", 3) * 1000
                self.is_playing = False
                self.delay_timer.start(delay)
    
    def play_chime_again(self):
        """Play the chime again (for twice type)"""
        if self.current_chime_info:
            self.current_player.play()
            logger.info(f"Playing chime again: {self.current_chime_info}")
    
    def play_blinker_chime(self, chime_info):
        """Play blinker chime in parallel (special case)"""
        config = chime_info.config
        file_path = os.path.join(CHIMES_DIR, config["file"])
        
        if os.path.exists(file_path):
            self.blinker_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.blinker_player.setVolume(config.get("volume", 50))
            self.blinker_player.play()
            logger.info(f"Playing blinker chime: {chime_info}")
        else:
            logger.error(f"Blinker chime file not found: {file_path}")

    def stop_chime(self, chime_name, deck_num, card_num):
        """Stop a specific chime if it is currently playing"""
        # For simplicity, stop the media player if the current chime matches
        if self.current_chime_info and self.current_chime_info.chime_name == chime_name and \
           self.current_chime_info.deck_num == deck_num and self.current_chime_info.card_num == card_num:
            if self.current_player.state() == QMediaPlayer.PlayingState:
                self.current_player.stop()
            self.current_chime_info = None
        # Also stop blinker chimes if needed
        if chime_name == 'blinker' and self.blinker_player.state() == QMediaPlayer.PlayingState:
            self.blinker_player.stop()

# Global chime handler instance
chime_handler = ChimeQueueHandler()

# DECK_GRAPHICS configuration (same as before)
DECK_GRAPHICS = {
    0: {
        0: [],
        1: [{"type": "image", "file": "background.png", "x": 0, "y": 0}]
    },
    1: {
        0: [],
        1: [
            {"type": "image", "file": "guide.png", "x": 928, "y": 31},
            {"type": "image", "file": "Vector 3.png", "x": 526, "y": 39},
            {"type": "image", "file": "Vector 2.png", "x": 956, "y": 39},
            {"type": "image", "file": "Vector 4.png", "x": 768, "y": 45},
            {"type": "image", "file": "Vector 5.png", "x": 960, "y": 45},
            {"type": "image", "file": "road surface.png", "x": 430, "y": 45}
        ]
    },
    2: {
        0: [],
        1: [{"type": "image", "file": "music bgnd.png", "x": 1656, "y": 256}]
    },
    3: {
        0: [],
        1: [{"type": "image", "file": "music cover.png", "x": 1521, "y": 226}]
    },
    4: {
        0: [],
        1: [{"type": "image", "file": "mini car.png", "x": 690, "y": 354}]
    },
    5: {
        0: [],
        1: [{"type": "image", "file": "ECO.png", "x": 1750, "y": 55}]
    },
    6: {
        0: [],
        1: [{"type": "image", "file": "weather icon.png", "x": 1550, "y": 45}]
    },
    7: {
        0: [],
        1: [{"type": "image", "file": "P1.png", "x": 100, "y": 40}],
        2: [{"type": "image", "file": "P2.png", "x": 100, "y": 40}]
    },
    8: {
        0: [],
        1: [{"type": "image", "file": "D1.png", "x": 160, "y": 40}],
        2: [{"type": "image", "file": "D2.png", "x": 160, "y": 40}]
    },
    9: {
        0: [],
        1: [{"type": "image", "file": "N1.png", "x": 220, "y": 40}],
        2: [{"type": "image", "file": "N2.png", "x": 220, "y": 40}]
    },
    10: {
        0: [],
        1: [{"type": "image", "file": "R1.png", "x": 280, "y": 40}],
        2: [{"type": "image", "file": "R2.png", "x": 280, "y": 40}]
    },
    11: {
        0: [],
        1: [{"type": "dynamic_text", "value": "08:30 AM", "x": 1350, "y": 45, "font_family": "HYQiHei", "font_size": 20, "font_color": "#47473F", "opacity": 100}]
    },
    12: {
        0: [],
        1: [{"type": "dynamic_text", "value": "26℃", "x": 1620, "y": 45, "font_family": "HYQiHei", "font_size": 20, "font_color": "#47473F", "opacity": 100}]
    },
    13: {
        0: [],
        1: [
            {"type": "dynamic_text", "value": "85", "x": 100, "y": 275, "font_family": "HFBUBU", "font_size": 80, "font_color": "#47473F", "opacity": 100},
            {"type": "static_text", "value": "km/h", "x": 380, "y": 385, "font_family": "HYQiHei", "font_size": 20, "font_color": "#47473F", "opacity": 80}
        ]
    },
    14: {
        0: [],
        1: [
            {"type": "dynamic_text", "value": "212", "x": 280, "y": 610, "font_family": "HFBUBU", "font_size": 20, "font_color": "#47473F", "opacity": 100},
            {"type": "static_text", "value": "km", "x": 385, "y": 612, "font_family": "HYQiHei", "font_size": 20, "font_color": "#47473F", "opacity": 80},
            {"type": "progress_bar", "x": 106, "y": 626, "fill_color": "#76B047", "outer_bar_color": "#D3D7D2", "w": 160, "h": 16}
        ]
    },
    15: {
        0: [],
        1: [
            {"type": "dynamic_text", "value": "3.2", "x": 929, "y": 190, "font_family": "HFBUBU", "font_size": 25, "font_color": "#47473F", "opacity": 100},
            {"type": "static_text", "value": "km", "x": 1035, "y": 210, "font_family": "HYQiHei", "font_size": 15, "font_color": "#47473F", "opacity": 100},
            {"type": "static_text", "value": "MG Road", "x": 930, "y": 260, "font_family": "HYQiHei", "font_size": 20, "font_color": "#94784D", "opacity": 80}
        ]
    },
    16: {
        0: [],
        1: [{"type": "dynamic_text", "value": "We Don't talk Anymore", "x": 1430, "y": 486, "font_family": "HYQiHei", "font_size": 12, "font_color": "#47473F", "opacity": 100}]
    },
    17: {
        0: [],
        1: [{"type": "dynamic_text", "value": "Charlie Puth", "x": 1564, "y": 525, "font_family": "HYQiHei", "font_size": 10, "font_color": "#94784D", "opacity": 100}]
    },
    18: {
        0: [],
        1: [{"type": "image", "file": "take_right.png", "x": 794, "y": 190}],
        2: [{"type": "image", "file": "take_left.png", "x": 794, "y": 190}],
        3: [{"type": "image", "file": "continue_straight.png", "x": 794, "y": 190}]
    }
}

# Updated TELL_TALES with chime configuration using CHIME_INFO structure
TELL_TALES = {
    50: {
        0: []        
    },
    51: {
        0: [],
        1: [{"type": "image", "file": "TT001_Low Oil Level_1.png", "zone": 2, "blinking": "NO", "duty_cycle": 0.5, "chime": "engine_check", "duration": 5}],
        2: [{"type": "image", "file": "TT002_Min Oil Level.png", "zone": 2, "blinking": "YES", "duty_cycle": 0.3, "chime": "engine_check", "duration": 5}]
    },
    52: {
        0: [],
        1: [{"type": "image", "file": "TT003_Airbag_Enabled.png", "zone": 1, "blinking": "NO", "duty_cycle": 0.5, "chime": None, "duration": 5}],
        2: [{"type": "image", "file": "TT004_Airbag_Disabled.png", "zone": 1, "blinking": "NO", "duty_cycle": 0.4, "chime": "jeep_seatbelt_alert", "duration": 5}]
    },
    53: {
        0: [],
        1: [{"type": "image", "file": "TT005_Battery Level Low_1.png", "zone": 2, "blinking": "YES", "duty_cycle": 0.6, "chime": "engine_check", "duration": 5}],
        2: [{"type": "image", "file": "TT006_Battery Level Low_2.png", "zone": 2, "blinking": "NO", "duty_cycle": 0.6, "chime": "engine_check", "duration": 5}]
    },
    54: {
        0: [],
        1: [{"type": "image", "file": "TT007_Hazard.png", "zone": 4, "blinking": "NO", "duty_cycle": 0.5, "chime": "blinker", "duration": 5}]
    },
    55: {
        0: [],
        1: [{"type": "image", "file": "TT008_SW_1.png", "zone": 1, "blinking": "NO", "duty_cycle": 0.5, "chime": "jeep_seatbelt_alert", "duration": 90}],
        2: [{"type": "image", "file": "TT009_SW_2.png", "zone": 1, "blinking": "NO", "duty_cycle": 0.5, "chime": "jeep_seatbelt_alert", "duration": 5}]
    },
    56: {
        0: [],
        1: [{"type": "image", "file": "TT010_Low Fuel Warning.png", "zone": 2, "blinking": "NO", "duty_cycle": 0.7, "chime": "low_fuel", "duration": 5}],
        2: [{"type": "image", "file": "TT011_Water in Fuel.png", "zone": 2, "blinking": "YES", "duty_cycle": 0.5, "chime": "engine_check", "duration": 5}],
        3: [{"type": "image", "file": "TT012_Loose Fuel Cap.png", "zone": 2, "blinking": "YES", "duty_cycle": 0.4, "chime": "engine_check", "duration": 5}],        
    },
    57: {
        0: [],
        1: [{"type": "image", "file": "TT013_Low Beam_1.png", "zone": 7, "blinking": "NO", "duty_cycle": 0.5, "chime": None, "duration": 5}]
    },
    58: {
        0: [],
        1: [{"type": "image", "file": "TT014_High Beam.png", "zone": 6, "blinking": "NO", "duty_cycle": 0.5, "chime": None, "duration": 5}],
        2: [{"type": "image", "file": "TT015_Low Beam_2.png", "zone": 6, "blinking": "NO", "duty_cycle": 0.5, "chime": None, "duration": 5}]
    },
    59: {
        0: [],
        1: [{"type": "image", "file": "TT016_LeftTurn.png", "zone": 3, "blinking": "YES", "duty_cycle": 0.5, "chime": "blinker", "duration": 5}]
    },
    60: {
        0: [],
        1: [{"type": "image", "file": "TT017_RightTurn.png", "zone": 5, "blinking": "YES", "duty_cycle": 0.5, "chime": "blinker", "duration": 5}]
    },
    61: {
        0: [],
        1: [{"type": "image", "file": "TT018_Eng Temp_Low.png", "zone": 2, "blinking": "YES", "duty_cycle": 0.5, "chime": None, "duration": 5}],
        2: [{"type": "image", "file": "TT019_Eng Temp_High_1.png", "zone": 2, "blinking": "NO", "duty_cycle": 0.3, "chime": "engine_check", "duration": 5}],
        3: [{"type": "image", "file": "TT020_Engine Temp_High_2.png", "zone": 2, "blinking": "NO", "duty_cycle": 0.3, "chime": "engine_check", "duration": 5}]
    }
}

# Ensure every telltale config has a 'chime' entry
for deck, cards in TELL_TALES.items():
    for card, elements in cards.items():
        for elem in elements:
            if elem.get("type") == "image" and "chime" not in elem:
                elem["chime"] = None

class TellTaleWidget(QWidget):
    def __init__(self, deck_num, card_num, elements):
        super().__init__()
        self.deck_num = deck_num
        self.card_num = card_num
        self.setFixedSize(*BG_RESOLUTION)
        self.elements = elements
        self.ui_items = []
        self.blink_timers = []
        self.duration_timer = None
        self.duration = 5  # Default 5 seconds
        self.init_ui()

    def init_ui(self):
        """Initialize the UI for this telltale"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        for elem in self.elements:
            if elem["type"] == "image":
                label = QLabel()
                image_path = os.path.join(IMAGE_DIR, elem["file"])
                if os.path.exists(image_path):
                    pixmap = QPixmap(image_path)
                    label.setPixmap(pixmap)
                    label.setAlignment(Qt.AlignCenter)
                    
                    # Position the label
                    x = elem.get("x", 0)
                    y = elem.get("y", 0)
                    label.move(x, y)
                    label.setFixedSize(pixmap.size())
                    
                    # Setup blinking if specified
                    if elem.get("blinking") == "YES":
                        duty_cycle = elem.get("duty_cycle", 0.5)
                        self.setup_blinking(label, duty_cycle)
                    
                    # Setup chime if specified
                    chime_name = elem.get("chime")
                    if chime_name:
                        self.setup_chime(chime_name, elem.get("duration", 5))
                    
                    self.ui_items.append(label)
                    layout.addWidget(label)
                else:
                    logger.error(f"Image file not found: {image_path}")
            
            elif elem["type"] == "dynamic_text":
                label = QLabel(elem["value"])
                font = QFont(elem.get("font_family", "Arial"), elem.get("font_size", 12))
                label.setFont(font)
                label.setStyleSheet(f"color: {elem.get('font_color', '#000000')};")
                label.setAlignment(Qt.AlignCenter)
                
                # Position the label
                x = elem.get("x", 0)
                y = elem.get("y", 0)
                label.move(x, y)
                
                self.ui_items.append(label)
                layout.addWidget(label)
            
            elif elem["type"] == "static_text":
                label = QLabel(elem["value"])
                font = QFont(elem.get("font_family", "Arial"), elem.get("font_size", 12))
                label.setFont(font)
                label.setStyleSheet(f"color: {elem.get('font_color', '#000000')};")
                label.setAlignment(Qt.AlignCenter)
                
                # Position the label
                x = elem.get("x", 0)
                y = elem.get("y", 0)
                label.move(x, y)
                
                self.ui_items.append(label)
                layout.addWidget(label)
            
            elif elem["type"] == "progress_bar":
                progress_bar = QProgressBar()
                progress_bar.setFixedSize(elem.get("w", 100), elem.get("h", 20))
                progress_bar.setValue(75)  # Default value
                progress_bar.setStyleSheet(f"""
                    QProgressBar {{
                        border: 2px solid {elem.get('outer_bar_color', '#D3D7D2')};
                        border-radius: 5px;
                        text-align: center;
                    }}
                    QProgressBar::chunk {{
                        background-color: {elem.get('fill_color', '#76B047')};
                        border-radius: 3px;
                    }}
                """)
                
                # Position the progress bar
                x = elem.get("x", 0)
                y = elem.get("y", 0)
                progress_bar.move(x, y)
                
                self.ui_items.append(progress_bar)
                layout.addWidget(progress_bar)
        
        self.setLayout(layout)
        
        # Setup duration timer if duration is specified
        for elem in self.elements:
            if "duration" in elem:
                self.duration = elem["duration"]
                break
        self.setup_duration_timer()

    def setup_blinking(self, label, duty_cycle):
        """Setup blinking animation for a label"""
        on_time = int(1000 * duty_cycle)
        off_time = int(1000 * (1 - duty_cycle))
        
        timer = QTimer()
        timer.timeout.connect(lambda: self.toggle_label_visibility(label))
        timer.start(on_time)
        
        self.blink_timers.append((timer, label, on_time, off_time))

    def setup_chime(self, chime_name, duration):
        """Setup chime configuration for this telltale (does not trigger chime automatically)"""
        self.chime_name = chime_name
        self.chime_duration = duration
        logger.info(f"Chime configured - Deck: {self.deck_num}, Card: {self.card_num}, Chime: {chime_name}")

    def trigger_chime(self):
        """Trigger the chime for this telltale"""
        if hasattr(self, 'chime_name') and self.chime_name in CHIME_CONFIG:
            telltale_id = f"{self.deck_num}_{self.card_num}"
            chime_info = ChimeInfo(self.chime_name, self.deck_num, self.card_num, telltale_id)
            chime_handler.enqueue_chime(chime_info)
            logger.info(f"Chime triggered - Deck: {self.deck_num}, Card: {self.card_num}, Chime: {self.chime_name}")
        else:
            logger.warning(f"No chime configured for Deck: {self.deck_num}, Card: {self.card_num}")

    def stop_chime(self):
        """Stop the chime for this telltale if playing"""
        if hasattr(self, 'chime_name') and self.chime_name in CHIME_CONFIG:
            chime_handler.stop_chime(self.chime_name, self.deck_num, self.card_num)
            logger.info(f"Chime stopped - Deck: {self.deck_num}, Card: {self.card_num}, Chime: {self.chime_name}")

    def setup_duration_timer(self):
        """Setup timer for telltale duration"""
        if self.duration > 0:
            self.duration_timer = QTimer()
            self.duration_timer.timeout.connect(self.deactivate_after_duration)
            self.duration_timer.start(self.duration * 1000)  # Convert to milliseconds

    def deactivate_after_duration(self):
        """Deactivate telltale after duration expires"""
        # This would need to be connected to the main window's deactivation system
        # For now, we'll just stop the timers
        logger.info(f"Telltale duration expired - Deck: {self.deck_num}, Card: {self.card_num}")

    def toggle_label_visibility(self, label):
        """Toggle label visibility for blinking effect"""
        label.setVisible(not label.isVisible())

    def clear_ui(self):
        """Clear all UI elements and stop timers"""
        # Stop all blink timers
        for timer, _, _, _ in self.blink_timers:
            timer.stop()
        self.blink_timers.clear()
        
        # Stop duration timer
        if self.duration_timer:
            self.duration_timer.stop()
        
        # Clear UI items
        for item in self.ui_items:
            item.deleteLater()
        self.ui_items.clear()

class TellTaleDeckWidget(QWidget):
    def __init__(self, deck_num, card_length=DEFAULT_CARD_LENGTH):
        super().__init__()
        self.deck_num = deck_num
        self.card_length = card_length
        self.cards = {}
        self.active_card = 0
        self.init_ui()

    def init_ui(self):
        """Initialize the UI for this deck"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create cards for this deck
        for card_num in range(self.card_length):
            elements = TELL_TALES.get(self.deck_num, {}).get(card_num, [])
            card = TellTaleWidget(self.deck_num, card_num, elements)
            self.cards[card_num] = card
            layout.addWidget(card)
            card.hide()  # Initially hide all cards
        
        self.setLayout(layout)

    def show_card(self, card_num):
        """Show a specific card and hide others"""
        # Hide all cards except the specified one
        for num, card in self.cards.items():
            if num == card_num:
                card.show()
            else:
                card.hide()

    def activate_card(self, card_num):
        """Activate a card (show it and make it the active card)"""
        if card_num > 0:
            self.active_card = card_num
            self.show_card(card_num)
            self.show()

    def deactivate_card(self, card_num):
        """Deactivate a card"""
        if card_num == self.active_card:
            self.active_card = 0
            self.hide()

class CardWidget(QWidget):
    def __init__(self, deck_num, card_num, elements):
        super().__init__()
        self.deck_num = deck_num
        self.card_num = card_num
        self.setFixedSize(*BG_RESOLUTION)
        self.elements = elements
        self.ui_items = []
        self.init_ui()

    def init_ui(self):
        """Initialize the UI for this card"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        for elem in self.elements:
            if elem["type"] == "image":
                label = QLabel()
                image_path = os.path.join(IMAGE_DIR, elem["file"])
                if os.path.exists(image_path):
                    pixmap = QPixmap(image_path)
                    label.setPixmap(pixmap)
                    label.setAlignment(Qt.AlignCenter)
                    
                    # Position the label
                    x = elem.get("x", 0)
                    y = elem.get("y", 0)
                    label.move(x, y)
                    label.setFixedSize(pixmap.size())
                    
                    self.ui_items.append(label)
                    layout.addWidget(label)
                else:
                    logger.error(f"Image file not found: {image_path}")
            
            elif elem["type"] == "dynamic_text":
                label = QLabel(elem["value"])
                font = QFont(elem.get("font_family", "Arial"), elem.get("font_size", 12))
                label.setFont(font)
                label.setStyleSheet(f"color: {elem.get('font_color', '#000000')};")
                label.setAlignment(Qt.AlignCenter)
                
                # Position the label
                x = elem.get("x", 0)
                y = elem.get("y", 0)
                label.move(x, y)
                
                self.ui_items.append(label)
                layout.addWidget(label)
            
            elif elem["type"] == "static_text":
                label = QLabel(elem["value"])
                font = QFont(elem.get("font_family", "Arial"), elem.get("font_size", 12))
                label.setFont(font)
                label.setStyleSheet(f"color: {elem.get('font_color', '#000000')};")
                label.setAlignment(Qt.AlignCenter)
                
                # Position the label
                x = elem.get("x", 0)
                y = elem.get("y", 0)
                label.move(x, y)
                
                self.ui_items.append(label)
                layout.addWidget(label)
            
            elif elem["type"] == "progress_bar":
                progress_bar = QProgressBar()
                progress_bar.setFixedSize(elem.get("w", 100), elem.get("h", 20))
                progress_bar.setValue(75)  # Default value
                progress_bar.setStyleSheet(f"""
                    QProgressBar {{
                        border: 2px solid {elem.get('outer_bar_color', '#D3D7D2')};
                        border-radius: 5px;
                        text-align: center;
                    }}
                    QProgressBar::chunk {{
                        background-color: {elem.get('fill_color', '#76B047')};
                        border-radius: 3px;
                    }}
                """)
                
                # Position the progress bar
                x = elem.get("x", 0)
                y = elem.get("y", 0)
                progress_bar.move(x, y)
                
                self.ui_items.append(progress_bar)
                layout.addWidget(progress_bar)
        
        self.setLayout(layout)

    def clear_ui(self):
        """Clear all UI elements"""
        for item in self.ui_items:
            item.deleteLater()
        self.ui_items.clear()

class DeckWidget(QWidget):
    def __init__(self, deck_num, card_length=DEFAULT_CARD_LENGTH):
        super().__init__()
        self.deck_num = deck_num
        self.card_length = card_length
        self.cards = {}
        self.active_card = 0
        self.init_ui()

    def init_ui(self):
        """Initialize the UI for this deck"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create cards for this deck
        for card_num in range(self.card_length):
            elements = DECK_GRAPHICS.get(self.deck_num, {}).get(card_num, [])
            card = CardWidget(self.deck_num, card_num, elements)
            self.cards[card_num] = card
            layout.addWidget(card)
            card.hide()  # Initially hide all cards
        
        self.setLayout(layout)

    def show_card(self, card_num):
        """Show a specific card and hide others"""
        # Hide all cards except the specified one
        for num, card in self.cards.items():
            if num == card_num:
                card.show()
            else:
                card.hide()

    def activate_card(self, card_num):
        """Activate a card (show it and make it the active card)"""
        if card_num > 0:
            self.active_card = card_num
            self.show_card(card_num)
            self.show()

    def deactivate_card(self, card_num):
        """Deactivate a card"""
        if card_num == self.active_card:
            self.active_card = 0
            self.hide()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Demo")
        self.setFixedSize(*BG_RESOLUTION)
        
        # Initialize deck widgets
        self.deck_widgets = {}
        self.telltale_decks = []
        
        # Create regular deck widgets (0-18)
        for deck_num in range(19):
            deck = DeckWidget(deck_num)
            self.deck_widgets[deck_num] = deck
        
        # Create telltale deck widgets (50-61)
        for deck_num in range(50, 62):
            telltale_deck = TellTaleDeckWidget(deck_num)
            self.telltale_decks.append(telltale_deck)
        
        # Active telltales tracking
        self.active_telltales = []
        self.zone_telltales = {}
        self.zone_timers = {}
        self.zone_round_robin_data = {}
        
        # Zone display labels
        self.zone_labels = {}
        
        self.init_ui()

    def init_ui(self):
        """Initialize the main UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Add all deck widgets to layout
        for deck in self.deck_widgets.values():
            layout.addWidget(deck)
            deck.hide()  # Initially hide all decks
        
        # Add telltale deck widgets
        for telltale_deck in self.telltale_decks:
            layout.addWidget(telltale_deck)
            telltale_deck.hide()  # Initially hide all telltale decks
        
        # Create zone display labels
        for zone_num in range(1, 8):
            label = QLabel(f"Zone {zone_num}")
            label.setStyleSheet("background-color: rgba(0, 0, 0, 0.7); color: white; padding: 5px; border-radius: 3px;")
            label.setAlignment(Qt.AlignCenter)
            label.hide()
            self.zone_labels[zone_num] = label
            layout.addWidget(label)
        
        self.setLayout(layout)

    def show_deck(self, deck_num):
        """Show a specific deck"""
        if deck_num in self.deck_widgets:
            self.deck_widgets[deck_num].show()

    def hide_deck(self, deck_num):
        """Hide a specific deck"""
        if deck_num in self.deck_widgets:
            self.deck_widgets[deck_num].hide()

    def activate_deck_card(self, deck_num, card_num):
        """Activate a specific card in a deck"""
        if deck_num in self.deck_widgets:
            self.deck_widgets[deck_num].activate_card(card_num)

    def deactivate_deck_card(self, deck_num, card_num):
        """Deactivate a specific card in a deck"""
        if deck_num in self.deck_widgets:
            self.deck_widgets[deck_num].deactivate_card(card_num)

    def activate_telltale(self, deck_num, card_num):
        """Activate a telltale deck/card"""
        if 50 <= deck_num <= max(TELL_TALES.keys()):
            deck_index = deck_num - 50
            if deck_index < len(self.telltale_decks):
                self.telltale_decks[deck_index].activate_card(card_num)
                
                # Add to active telltales list if not empty
                if card_num > 0:
                    self.active_telltales.append((deck_num, card_num))
                    
                    # Get zone for this telltale
                    elements = TELL_TALES.get(deck_num, {}).get(card_num, [])
                    for elem in elements:
                        if elem["type"] == "image":
                            zone = elem.get("zone", 1)
                            if zone not in self.zone_telltales:
                                self.zone_telltales[zone] = []
                            if (deck_num, card_num) not in self.zone_telltales[zone]:
                                self.zone_telltales[zone].append((deck_num, card_num))
                            break
                    
                    self.update_zone_display(zone)
                    
                    # Trigger chime if configured for this telltale
                    card_widget = self.telltale_decks[deck_index].cards[card_num]
                    if hasattr(card_widget, 'chime_name'):
                        card_widget.trigger_chime()

    def deactivate_telltale(self, deck_num, card_num):
        """Deactivate a telltale deck/card"""
        if 50 <= deck_num <= max(TELL_TALES.keys()):
            deck_index = deck_num - 50
            if deck_index < len(self.telltale_decks):
                self.telltale_decks[deck_index].deactivate_card(card_num)
                # Stop chime if active
                card_widget = self.telltale_decks[deck_index].cards[card_num]
                if hasattr(card_widget, 'stop_chime'):
                    card_widget.stop_chime()
                
                # Remove from active telltales list
                if (deck_num, card_num) in self.active_telltales:
                    self.active_telltales.remove((deck_num, card_num))
                    
                # Remove from zone telltales and update affected zones
                affected_zones = []
                for zone in list(self.zone_telltales.keys()):
                    if (deck_num, card_num) in self.zone_telltales[zone]:
                        self.zone_telltales[zone].remove((deck_num, card_num))
                        affected_zones.append(zone)
                        if not self.zone_telltales[zone]:
                            del self.zone_telltales[zone]
                            self.stop_zone_round_robin(zone)
                    
                # Hide deck if no active cards
                if self.telltale_decks[deck_index].active_card == 0:
                    self.telltale_decks[deck_index].hide()
                    
                # Update all affected zones
                for zone in affected_zones:
                    if zone in self.zone_telltales:
                        self.update_zone_display(zone)
                    else:
                        self.stop_zone_round_robin(zone)

    def update_zone_display(self, zone):
        """Update display for a specific zone"""
        if zone not in self.zone_telltales:
            self.stop_zone_round_robin(zone)
            return
            
        telltales = self.zone_telltales[zone]
        
        if len(telltales) > 1:
            # Multiple telltales in same zone - use round-robin based on blinking/duty cycle
            self.start_zone_round_robin(zone, telltales)
        else:
            # Single telltale in zone - show normally (blinking handled by TellTaleWidget)
            self.stop_zone_round_robin(zone)
            deck_num, card_num = telltales[0]
            deck_index = deck_num - 50
            if deck_index < len(self.telltale_decks):
                self.telltale_decks[deck_index].show()

    def start_zone_round_robin(self, zone, telltales):
        """Start round-robin for telltales in the same zone based on blinking/duty cycle"""
        if len(telltales) <= 1:
            self.stop_zone_round_robin(zone)
            return
            
        # Calculate timing based on blinking/duty cycle parameters
        timing_data = self.calculate_zone_timing(zone, telltales)
        
        # Store round-robin data for this zone
        self.zone_round_robin_data[zone] = {
            'telltales': telltales.copy(),
            'current_index': 0,
            'timing_data': timing_data
        }
        
        # Create timer for this zone if it doesn't exist
        if zone not in self.zone_timers:
            timer = QTimer()
            timer.timeout.connect(lambda z=zone: self.cycle_zone_telltales(z))
            self.zone_timers[zone] = timer
        
        # Start the timer with the calculated interval
        interval = timing_data.get('interval', 500)  # Default 0.5 seconds
        self.zone_timers[zone].start(interval)

    def calculate_zone_timing(self, zone, telltales):
        """Calculate timing for zone round-robin based on telltale parameters"""
        timing_data = {
            'interval': 500,  # Default interval
            'telltale_timings': {}
        }
        
        for deck_num, card_num in telltales:
            elements = TELL_TALES.get(deck_num, {}).get(card_num, [])
            for elem in elements:
                if elem["type"] == "image":
                    blinking = elem.get("blinking", "NO")
                    duty_cycle = elem.get("duty_cycle", 0.5)
                    
                    if blinking == "YES":
                        # Calculate timing based on duty cycle
                        on_time = int(1000 * duty_cycle)
                        off_time = int(1000 * (1 - duty_cycle))
                        total_time = on_time + off_time
                        
                        timing_data['telltale_timings'][(deck_num, card_num)] = {
                            'on_time': on_time,
                            'off_time': off_time,
                            'total_time': total_time
                        }
                        
                        # Use the shortest total time as interval
                        if total_time < timing_data['interval']:
                            timing_data['interval'] = total_time
                    break
        
        return timing_data

    def stop_zone_round_robin(self, zone):
        """Stop round-robin for a specific zone"""
        if zone in self.zone_timers:
            self.zone_timers[zone].stop()
        
        if zone in self.zone_round_robin_data:
            del self.zone_round_robin_data[zone]

    def cycle_zone_telltales(self, zone):
        """Cycle through telltales in a zone"""
        if zone not in self.zone_round_robin_data:
            return
        
        data = self.zone_round_robin_data[zone]
        telltales = data['telltales']
        current_index = data['current_index']
        
        # Hide all telltale decks in this zone
        for deck_num, card_num in telltales:
            deck_index = deck_num - 50
            if deck_index < len(self.telltale_decks):
                self.telltale_decks[deck_index].hide()
        
        # Show current telltale
        if telltales:
            deck_num, card_num = telltales[current_index]
            deck_index = deck_num - 50
            if deck_index < len(self.telltale_decks):
                self.telltale_decks[deck_index].show()
        
        # Move to next telltale
        data['current_index'] = (current_index + 1) % len(telltales)

    def show_zone_current_telltale(self, zone):
        """Show the current telltale for a zone"""
        if zone in self.zone_round_robin_data:
            data = self.zone_round_robin_data[zone]
            telltales = data['telltales']
            current_index = data['current_index']
            
            if telltales:
                deck_num, card_num = telltales[current_index]
                deck_index = deck_num - 50
                if deck_index < len(self.telltale_decks):
                    self.telltale_decks[deck_index].show()

class MessageQueue:
    def __init__(self, main_window):
        self.main_window = main_window

    def send_activation(self, deck, card, activation_status):
        """Send activation/deactivation message"""
        if activation_status:
            if deck < 50:
                self.main_window.activate_deck_card(deck, card)
            else:
                self.main_window.activate_telltale(deck, card)
        else:
            if deck < 50:
                self.main_window.deactivate_deck_card(deck, card)
            else:
                self.main_window.deactivate_telltale(deck, card)

    def trigger_chime(self, deck, card):
        """Trigger chime for a specific telltale"""
        if deck >= 50:  # Only telltales have chimes
            deck_index = deck - 50
            if deck_index < len(self.main_window.telltale_decks):
                deck_widget = self.main_window.telltale_decks[deck_index]
                if card in deck_widget.cards:
                    card_widget = deck_widget.cards[card]
                    card_widget.trigger_chime()
                    logger.info(f"Chime triggered via MessageQueue - Deck: {deck}, Card: {card}")
                else:
                    logger.warning(f"Card {card} not found in deck {deck}")
            else:
                logger.warning(f"Deck {deck} not found")
        else:
            logger.warning(f"Deck {deck} is not a telltale deck (no chimes)")

def test_application():
    """Test the redesigned chime system"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    def activate_all():
        """Activate multiple telltales to test chime queue"""
        # Activate telltales with different chimes
        window.activate_telltale(51, 1)  # engine_check (twice)
        window.activate_telltale(52, 2)  # jeep_seatbelt_alert (once)
        window.activate_telltale(56, 1)  # low_fuel (once)
        window.activate_telltale(59, 1)  # blinker (special case)
        window.activate_telltale(60, 1)  # blinker (special case)
        
        logger.info("Test: Activated multiple telltales to test chime queue")
    
    # Schedule the test
    QTimer.singleShot(1000, activate_all)
    
    return app.exec_()

def test_application2():
    """Test blinker chimes in parallel"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    def test_blinkers():
        """Test blinker chimes (should play in parallel)"""
        window.activate_telltale(59, 1)  # Left turn blinker
        window.activate_telltale(60, 1)  # Right turn blinker
        
        logger.info("Test: Activated blinker telltales (should play in parallel)")
    
    # Schedule the test
    QTimer.singleShot(1000, test_blinkers)
    
    return app.exec_()

def test_application3():
    """Test chime queue with different chime types"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    def test_chime_types():
        """Test different chime types in sequence"""
        window.activate_telltale(51, 1)  # engine_check (twice)
        window.activate_telltale(55, 1)  # jeep_seatbelt_alert (continuous)
        window.activate_telltale(56, 1)  # low_fuel (once)
        
        logger.info("Test: Activated telltales with different chime types")
    
    # Schedule the test
    QTimer.singleShot(1000, test_chime_types)
    
    return app.exec_()

def test_chime_functionality():
    """Test the new chime queue functionality"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    def test_chime_queue():
        """Test the FIFO chime queue"""
        # Activate telltales in sequence to test queue
        window.activate_telltale(51, 1)  # First in queue
        window.activate_telltale(52, 2)  # Second in queue
        window.activate_telltale(56, 1)  # Third in queue
        window.activate_telltale(59, 1)  # Blinker (should play immediately)
        
        logger.info("Test: Testing FIFO chime queue with blinker parallel playback")
    
    # Schedule the test
    QTimer.singleShot(1000, test_chime_queue)
    
    return app.exec_()

#if __name__ == "__main__":
    # Run the chime functionality test
    #test_chime_functionality()