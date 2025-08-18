import sys
import os
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

# Available chime files mapping
CHIME_FILES = {
    "blinker"                   : "blinker.mp3",
    "door_ajar"                 : "door_ajar.mp3",
    "parking_brake_engaged"     : "parking_brake_engaged.mp3",
    "engine_check"              : "engine_check.mp3",
    "low_fuel"                  : "low_fuel.mp3",
    "tire_pressure_warning"     : "tire_pressure_warning.mp3",
    "jeep_door_open"            : "jeep_door_open.mp3",
    "jeep_key_left_in_ignition" : "jeep_key_left_in_ignition.mp3",
    "jeep_seatbelt_alert"       : "jeep_seatbelt_alert.mp3"
}




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
            {"type": "dynamic_text", "value": "212", "x": 280, "y": 610, "font_family": "HFBUBU", "font_size": 18, "font_color": "#47473F", "opacity": 100},
            {"type": "static_text", "value": "km", "x": 380, "y": 612, "font_family": "HYQiHei", "font_size": 18, "font_color": "#47473F", "opacity": 80},
            {"type": "progress_bar", "x": 100, "y": 625, "fill_color": "#76B047", "outer_bar_color": "#D3D7D2", "w": 150, "h": 20, "min": 0, "max": 250}
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

TELL_TALES = {
    50: {
        0: []        
    },
    51: {
        0: [],
        1: [{"type": "image", "file": "TT001_Low Oil Level_1.png", "zone": 2, "blinking": "NO", "duty_cycle": 0.5, "chime": "engine_check", "chime_type": "twice", "duration": 0}],
        2: [{"type": "image", "file": "TT002_Min Oil Level.png", "zone": 2, "blinking": "YES", "duty_cycle": 0.3, "chime": "engine_check", "chime_type": "once", "duration": 0}]
    },
    52: {
        0: [],
        1: [{"type": "image", "file": "TT003_Airbag_Enabled.png", "zone": 1, "blinking": "NO", "duty_cycle": 0.5, "chime": None, "chime_type": "once", "duration": 0}],
        2: [{"type": "image", "file": "TT004_Airbag_Disabled.png", "zone": 1, "blinking": "NO", "duty_cycle": 0.4, "chime": "jeep_seatbelt_alert", "chime_type": "once", "duration": 0}]
    },
    53: {
        0: [],
        1: [{"type": "image", "file": "TT005_Battery Level Low_1.png", "zone": 2, "blinking": "YES", "duty_cycle": 0.6, "chime": "engine_check", "chime_type": "once", "duration": 0}],
        2: [{"type": "image", "file": "TT006_Battery Level Low_2.png", "zone": 2, "blinking": "NO", "duty_cycle": 0.6, "chime": "engine_check", "chime_type": "twice", "duration": 0}]
    },
    54: {
        0: [],
        1: [{"type": "image", "file": "TT007_Hazard.png", "zone": 4, "blinking": "NO", "duty_cycle": 0.5, "chime": "blinker", "chime_type": "continuous", "duration": -1}]
    },
    55: {
        0: [],
        1: [{"type": "image", "file": "TT008_SW_1.png", "zone": 1, "blinking": "NO", "duty_cycle": 0.5, "chime": "jeep_seatbelt_alert", "chime_type": "continuous", "duration": 90}],
        2: [{"type": "image", "file": "TT009_SW_2.png", "zone": 1, "blinking": "NO", "duty_cycle": 0.5, "chime": "jeep_seatbelt_alert", "chime_type": "once", "duration": 0}]
    },
    56: {
        0: [],
        1: [{"type": "image", "file": "TT010_Low Fuel Warning.png", "zone": 2, "blinking": "NO", "duty_cycle": 0.7, "chime": "low_fuel", "chime_type": "once", "duration": 0}],
        2: [{"type": "image", "file": "TT011_Water in Fuel.png", "zone": 2, "blinking": "YES", "duty_cycle": 0.5, "chime": "engine_check", "chime_type": "once", "duration": 0}],
        3: [{"type": "image", "file": "TT012_Loose Fuel Cap.png", "zone": 2, "blinking": "YES", "duty_cycle": 0.4, "chime": "engine_check", "chime_type": "once", "duration": 0}],        
    },
    57: {
        0: [],
        1: [{"type": "image", "file": "TT013_Low Beam_1.png", "zone": 7, "blinking": "NO", "duty_cycle": 0.5, "chime": None, "chime_type": "once", "duration": 0}]
    },
    58: {
        0: [],
        1: [{"type": "image", "file": "TT014_High Beam.png", "zone": 6, "blinking": "NO", "duty_cycle": 0.5, "chime": None, "chime_type": "once", "duration": 0}],
        2: [{"type": "image", "file": "TT015_Low Beam_2.png", "zone": 6, "blinking": "NO", "duty_cycle": 0.5, "chime": None, "chime_type": "once", "duration": 0}]
    },
    59: {
        0: [],
        1: [{"type": "image", "file": "TT016_LeftTurn.png", "zone": 3, "blinking": "YES", "duty_cycle": 0.5, "chime": "blinker", "chime_type": "continuous", "duration": -1}]
    },
    60: {
        0: [],
        1: [{"type": "image", "file": "TT017_RightTurn.png", "zone": 5, "blinking": "YES", "duty_cycle": 0.5, "chime": "blinker", "chime_type": "continuous", "duration": -1}]
    },
    61: {
        0: [],
        1: [{"type": "image", "file": "TT018_Eng Temp_Low.png", "zone": 2, "blinking": "YES", "duty_cycle": 0.5, "chime": None, "chime_type": "once", "duration": 0}],
        2: [{"type": "image", "file": "TT019_Eng Temp_High_1.png", "zone": 2, "blinking": "NO", "duty_cycle": 0.3, "chime": "engine_check", "chime_type": "twice", "duration": 0}],
        3: [{"type": "image", "file": "TT020_Engine Temp_High_2.png", "zone": 2, "blinking": "NO", "duty_cycle": 0.3, "chime": "engine_check", "chime_type": "twice", "duration": 0}]
    }
}
'''
# --- Update TELL_TALES durations for chime_type ---
def _patch_telltale_durations():
    for deck, cards in TELL_TALES.items():
        for card, elements in cards.items():
            for elem in elements:
                if elem.get("type") == "image" and elem.get("chime_type"):
                    if elem["chime_type"] in ("once", "twice"):
                        elem["duration"] = 0
                    elif elem["chime_type"] == "continuous":
                        elem["duration"] = -1
_patch_telltale_durations()
'''
class TellTaleWidget(QWidget):
    def __init__(self, deck_num, card_num, elements):
        super().__init__()
        self.deck_num = deck_num
        self.card_num = card_num
        self.setFixedSize(*BG_RESOLUTION)
        self.elements = elements
        self.ui_items = []
        self.blink_timers = []
        self.chime_player = None
        self.chime_timer = None
        self.duration_timer = None
        self.chime_play_count = 0
        self.chime_type = None
        self.duration = 5  # Default 5 seconds
        self.init_ui()

    def init_ui(self):
        for elem in self.elements:
            if elem["type"] == "image":
                img_path = os.path.join(IMAGE_DIR, elem["file"])
                label = QLabel(self)
                if os.path.exists(img_path):
                    pixmap = QPixmap(img_path)
                    # Scale image to half size for telltales
                    scaled_pixmap = pixmap.scaled(pixmap.width() // 2, pixmap.height() // 2, 
                                                 Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    label.setPixmap(scaled_pixmap)
                else:
                    label.setText(f"Missing: {elem['file']}")
                    label.setStyleSheet("color: red; background: white;")
                
                # Use zone coordinates instead of direct x,y
                zone = elem.get("zone", 1)
                zone_coords = ZONE_COORDINATES.get(zone, {"x": 0, "y": 0})
                label.move(zone_coords["x"], zone_coords["y"])
                label.show()
                self.ui_items.append(label)
                
                # Setup blinking if enabled
                blinking = elem.get("blinking", "NO")
                duty_cycle = elem.get("duty_cycle", 0.5)
                if blinking == "YES" and duty_cycle > 0:
                    self.setup_blinking(label, duty_cycle)
                
                # Setup chime if specified
                chime = elem.get("chime", None)
                chime_type = elem.get("chime_type", "once")
                if chime and chime in CHIME_FILES:
                    self.setup_chime(chime, chime_type)
                
                # Setup duration
                duration = elem.get("duration", 5)
                self.duration = duration
                # Only start duration timer if duration > 0
                if duration > 0:  # 0 or -1 means no auto-deactivation
                    self.setup_duration_timer()

    def setup_blinking(self, label, duty_cycle):
        """Setup blinking timer for a label"""
        # Calculate on/off times based on duty cycle
        cycle_time = 1000  # 1 second total cycle
        on_time = int(cycle_time * duty_cycle)
        off_time = cycle_time - on_time
        
        # Create timer for blinking
        timer = QTimer()
        timer.timeout.connect(lambda: self.toggle_label_visibility(label))
        timer.start(on_time)  # Start with on time
        self.blink_timers.append((timer, label, on_time, off_time))

    def setup_chime(self, chime_name, chime_type):
        """Setup chime player for this telltale"""
        chime_file = CHIME_FILES.get(chime_name)
        if chime_file:
            chime_path = os.path.join(CHIMES_DIR, chime_file)
            if os.path.exists(chime_path):
                # Create a new media player for this telltale
                self.chime_player = QMediaPlayer()
                self.chime_player.setMedia(QMediaContent(QUrl.fromLocalFile(chime_path)))
                self.chime_type = chime_type
                self.chime_play_count = 0
                # Connect error handling
                self.chime_player.error.connect(self.on_chime_error)
                self.chime_player.mediaStatusChanged.connect(self.on_chime_status_changed)
                # Set volume to ensure audio is audible
                self.chime_player.setVolume(50)
                # Do NOT play chime here! Only configure.
            else:
                logger.error(f"Chime file not found: {chime_path}")

    def on_chime_error(self, error):
        """Handle chime player errors"""
        error_messages = {
            QMediaPlayer.NoError: "No Error",
            QMediaPlayer.ResourceError: "Resource Error",
            QMediaPlayer.NetworkError: "Network Error",
            QMediaPlayer.FormatError: "Format Error",
            QMediaPlayer.AccessDeniedError: "Access Denied Error"
        }
        error_msg = error_messages.get(error, f"Unknown Error ({error})")
        logger.error(f"Chime player error - Deck: {self.deck_num}, Card: {self.card_num}, Error: {error_msg}")

    def on_chime_status_changed(self, status):
        """Handle chime status changes for twice playback"""
        status_messages = {
            QMediaPlayer.UnknownMediaStatus: "Unknown",
            QMediaPlayer.NoMedia: "No Media",
            QMediaPlayer.LoadingMedia: "Loading",
            QMediaPlayer.LoadedMedia: "Loaded",
            QMediaPlayer.BufferingMedia: "Buffering",
            QMediaPlayer.BufferedMedia: "Buffered",
            QMediaPlayer.StalledMedia: "Stalled",
            QMediaPlayer.EndOfMedia: "End of Media",
            QMediaPlayer.InvalidMedia: "Invalid Media"
        }
        status_msg = status_messages.get(status, f"Unknown Status ({status})")
        logger.debug(f"Chime status changed - Deck: {self.deck_num}, Card: {self.card_num}, Status: {status_msg}")
        
        if status == QMediaPlayer.EndOfMedia and self.chime_type == "twice" and self.chime_play_count < 2:
            self.chime_play_count += 1
            if self.chime_play_count < 2:
                # Add delay before second play
                QTimer.singleShot(800, self.play_chime_twice)
                logger.info(f"Chime second play scheduled - Deck: {self.deck_num}, Card: {self.card_num}, Play Count: {self.chime_play_count}")

    def trigger_chime(self):
        """Explicitly play the chime based on its type. Call this on telltale activation."""
        if not self.chime_player or not self.chime_type:
            return
        # Reset play count for each activation
        self.chime_play_count = 0
        if self.chime_type == "once":
            QTimer.singleShot(200, self.play_chime_once)
            logger.info(f"Chime triggered (once) - Deck: {self.deck_num}, Card: {self.card_num}")
        elif self.chime_type == "twice":
            QTimer.singleShot(200, self.play_chime_twice)
            logger.info(f"Chime triggered (twice) - Deck: {self.deck_num}, Card: {self.card_num}")
        elif self.chime_type == "continuous":
            if self.duration == -1:
                # Indefinite until deactivation
                if not self.chime_timer:
                    self.chime_timer = QTimer()
                    self.chime_timer.timeout.connect(self.play_chime)
                    self.chime_timer.start(3000)  # Play chime every 3 seconds
                QTimer.singleShot(200, self.play_chime)
                logger.info(f"Chime triggered (continuous, infinite) - Deck: {self.deck_num}, Card: {self.card_num}")
            elif self.duration > 0:
                # Play for duration seconds, then stop
                if not self.chime_timer:
                    self.chime_timer = QTimer()
                    self.chime_timer.timeout.connect(self.play_chime)
                    self.chime_timer.start(3000)
                QTimer.singleShot(200, self.play_chime)
                # Start a timer to stop after duration
                if self.duration_timer:
                    self.duration_timer.stop()
                self.duration_timer = QTimer()
                self.duration_timer.setSingleShot(True)
                self.duration_timer.timeout.connect(self.stop_continuous_chime)
                self.duration_timer.start(self.duration * 1000)
                logger.info(f"Chime triggered (continuous, timed {self.duration}s) - Deck: {self.deck_num}, Card: {self.card_num}")

    def play_chime_once(self):
        if self.chime_player:
            self.chime_player.stop()
            self.chime_player.setPosition(0)
            self.chime_player.play()
            logger.info(f"Chime started ONCE - Deck: {self.deck_num}, Card: {self.card_num}")

    def play_chime_twice(self):
        if self.chime_player:
            self.chime_player.stop()
            self.chime_player.setPosition(0)
            self.chime_player.play()
            logger.info(f"Chime started TWICE (first) - Deck: {self.deck_num}, Card: {self.card_num}")
            # Schedule second play after audio ends or fixed delay (e.g., 1s)
            QTimer.singleShot(1200, self._play_chime_twice_second)

    def _play_chime_twice_second(self):
        if self.chime_player:
            self.chime_player.stop()
            self.chime_player.setPosition(0)
            self.chime_player.play()
            logger.info(f"Chime started TWICE (second) - Deck: {self.deck_num}, Card: {self.card_num}")

    def play_chime(self):
        if self.chime_player:
            self.chime_player.stop()
            self.chime_player.setPosition(0)
            self.chime_player.play()
            logger.info(f"Chime started (continuous) - Deck: {self.deck_num}, Card: {self.card_num}")

    def stop_continuous_chime(self):
        if self.chime_timer:
            self.chime_timer.stop()
            self.chime_timer = None
        if self.chime_player:
            self.chime_player.stop()
        logger.info(f"Chime stopped (continuous, timed) - Deck: {self.deck_num}, Card: {self.card_num}")

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
        if self.chime_timer:
            self.chime_timer.stop()
        if self.chime_player:
            self.chime_player.stop()

    def toggle_label_visibility(self, label):
        """Toggle label visibility for blinking effect"""
        for timer, lbl, on_time, off_time in self.blink_timers:
            if lbl == label:
                if label.isVisible():
                    label.hide()
                    timer.setInterval(off_time)
                else:
                    label.show()
                    timer.setInterval(on_time)
                break

    def clear_ui(self):

        # Stop all blink timers
        for timer, _, _, _ in self.blink_timers:
            timer.stop()
        self.blink_timers.clear()
        
        # Stop chime timer if continuous
        if self.chime_timer:
            self.chime_timer.stop()
            self.chime_timer = None
        # Stop duration timer
        if self.duration_timer:
            self.duration_timer.stop()
            self.duration_timer = None
        
        # Stop chime playback
        if self.chime_player:
            self.chime_player.stop()
            logger.info(f"Chime stopped (clear_ui) - Deck: {self.deck_num}, Card: {self.card_num}")
        for item in self.ui_items:
            item.hide()
            item.deleteLater()
        self.ui_items = []

class TellTaleDeckWidget(QWidget):
    def __init__(self, deck_num, card_length=DEFAULT_CARD_LENGTH):
        super().__init__()
        self.deck_num = deck_num
        self.card_length = card_length
        self.setFixedSize(*BG_RESOLUTION)
        self.cards = []
        self.active_card = 0
        for card_num in range(card_length + 1):  # 0 to card_length
            elements = TELL_TALES.get(deck_num, {}).get(card_num, [])
            card = TellTaleWidget(deck_num, card_num, elements)
            card.hide()
            self.cards.append(card)
            card.setParent(self)
        self.show_card(0)

    def show_card(self, card_num):
        # Hide all cards except the highest active one
        for i, card in enumerate(self.cards):
            card.hide()
        self.cards[card_num].show()
        self.active_card = card_num

    def activate_card(self, card_num):
        self.show_card(card_num)

    def deactivate_card(self, card_num):
        # If deactivating the highest active card, show next lower active card
        if self.active_card == card_num:
            for i in range(card_num - 1, -1, -1):
                if self.cards[i].isVisible():
                    self.show_card(i)
                    self.cards[card_num].clear_ui()  # Stop chimes/timers for deactivated card
                    return
            self.show_card(0)
            self.cards[card_num].clear_ui()  # Stop chimes/timers for deactivated card

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
        for elem in self.elements:
            if elem["type"] == "image":
                img_path = os.path.join(IMAGE_DIR, elem["file"])
                label = QLabel(self)
                if os.path.exists(img_path):
                    pixmap = QPixmap(img_path)
                    label.setPixmap(pixmap)
                else:
                    label.setText(f"Missing: {elem['file']}")
                    label.setStyleSheet("color: red; background: white;")
                label.move(elem["x"], elem["y"])
                label.show()
                self.ui_items.append(label)
            elif elem["type"] == "dynamic_text" or elem["type"] == "static_text":
                label = QLabel(self)
                label.setText(elem["value"])
                label.setFont(QFont(elem.get("font_family", "Arial"), elem.get("font_size", 20)))
                label.setStyleSheet(f"color: {elem.get('font_color', '#000')};")
                label.move(elem["x"], elem["y"])
                label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                label.setWindowOpacity(elem.get("opacity", 100) / 100.0)
                label.show()
                self.ui_items.append(label)
            elif elem["type"] == "progress_bar":
                bar = QProgressBar(self)
                bar.setGeometry(elem["x"], elem["y"], elem["w"], elem["h"])
                bar.setMinimum(0)
                bar.setMaximum(250)
                bar.setValue(212)
                bar.setTextVisible(False)  # Hide percentage overlay                
                bar.setStyleSheet(
                    f"""
                    QProgressBar {{
                        border: 1px solid {elem.get('outer_bar_color', '#D3D7D2')};
                        border-radius: 5px;
                        background: {elem.get('outer_bar_color', '#D3D7D2')};
                    }}
                    QProgressBar::chunk {{
                        background-color: {elem.get('fill_color', '#76B047')};
                    }}
                    """
                )
                bar.show()
                self.ui_items.append(bar)

    def clear_ui(self):
        for item in self.ui_items:
            item.hide()
            item.deleteLater()
        self.ui_items = []

class DeckWidget(QWidget):
    def __init__(self, deck_num, card_length=DEFAULT_CARD_LENGTH):
        super().__init__()
        self.deck_num = deck_num
        self.card_length = card_length
        self.setFixedSize(*BG_RESOLUTION)
        self.cards = []
        self.active_card = 0
        for card_num in range(card_length + 1):  # 0 to card_length
            elements = DECK_GRAPHICS.get(deck_num, {}).get(card_num, [])
            card = CardWidget(deck_num, card_num, elements)
            card.hide()
            self.cards.append(card)
            card.setParent(self)
        self.show_card(0)

    def show_card(self, card_num):
        # Hide all cards except the highest active one
        for i, card in enumerate(self.cards):
            card.hide()
        self.cards[card_num].show()
        self.active_card = card_num

    def activate_card(self, card_num):
        self.show_card(card_num)

    def deactivate_card(self, card_num):
        # If deactivating the highest active card, show next lower active card
        if self.active_card == card_num:
            for i in range(card_num - 1, -1, -1):
                if self.cards[i].isVisible():
                    self.show_card(i)
                    return
            self.show_card(0)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Decks and Cards Demo")
        self.setFixedSize(*BG_RESOLUTION)
        self.decks = []
        self.telltale_decks = []
        self.active_telltales = []  # List of (deck_num, card_num) tuples
        self.zone_telltales = {}  # zone: [(deck_num, card_num), ...]
        self.zone_timers = {}  # zone: QTimer for each zone
        self.zone_round_robin_data = {}  # zone: {telltales: [], current_index: 0, timing_data: ...}
        
        # Initialize regular decks
        for deck_num in range(0, max(DECK_GRAPHICS.keys()) + 1):
            deck = DeckWidget(deck_num)
            deck.setParent(self)
            deck.move(0, 0)
            deck.hide()
            self.decks.append(deck)
            
        # Initialize telltale decks
        for deck_num in range(50, max(TELL_TALES.keys()) + 1):
            deck = TellTaleDeckWidget(deck_num)
            deck.setParent(self)
            deck.move(0, 0)
            deck.hide()
            self.telltale_decks.append(deck)

    def show_deck(self, deck_num):
        if deck_num < len(self.decks):
            self.decks[deck_num].show()

    def hide_deck(self, deck_num):
        if deck_num < len(self.decks):
            self.decks[deck_num].hide()

    def activate_deck_card(self, deck_num, card_num):
        if deck_num < len(self.decks):
            self.show_deck(deck_num)
            self.decks[deck_num].activate_card(card_num)

    def deactivate_deck_card(self, deck_num, card_num):
        if deck_num < len(self.decks):
            self.decks[deck_num].deactivate_card(card_num)
            # Optionally hide deck if card 0 is empty
            if self.decks[deck_num].active_card == 0:
                self.hide_deck(deck_num)

    def activate_telltale(self, deck_num, card_num):
        """Activate a telltale deck/card"""
        if 50 <= deck_num <= max(TELL_TALES.keys()):
            deck_index = deck_num - 50
            if deck_index < len(self.telltale_decks):
                self.telltale_decks[deck_index].activate_card(card_num)
                # Trigger chime if card_num > 0
                if card_num > 0:
                    widget = self.telltale_decks[deck_index].cards[card_num]
                    if hasattr(widget, 'trigger_chime'):
                        widget.trigger_chime()
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

    def deactivate_telltale(self, deck_num, card_num):
        """Deactivate a telltale deck/card"""
        if 50 <= deck_num <= max(TELL_TALES.keys()):
            deck_index = deck_num - 50
            if deck_index < len(self.telltale_decks):
                self.telltale_decks[deck_index].deactivate_card(card_num)
                
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
        
        # Show the first telltale
        self.show_zone_current_telltale(zone)

    def calculate_zone_timing(self, zone, telltales):
        """Calculate timing for zone round-robin based on blinking/duty cycle parameters"""
        timing_data = {
            'interval': 500,  # Default 0.5 seconds
            'telltale_timings': {}
        }
        
        # Analyze blinking and duty cycle parameters for all telltales in the zone
        blinking_telltales = []
        non_blinking_telltales = []
        
        for deck_num, card_num in telltales:
            elements = TELL_TALES.get(deck_num, {}).get(card_num, [])
            for elem in elements:
                if elem["type"] == "image":
                    blinking = elem.get("blinking", "NO")
                    duty_cycle = elem.get("duty_cycle", 0.5)
                    
                    if blinking == "YES":
                        blinking_telltales.append((deck_num, card_num, duty_cycle))
                    else:
                        non_blinking_telltales.append((deck_num, card_num))
                    break
        
        # If all telltales are non-blinking, use standard round-robin
        if not blinking_telltales:
            timing_data['interval'] = 500  # 0.5 seconds
        else:
            # If there are blinking telltales, use the fastest duty cycle
            fastest_duty_cycle = min([duty for _, _, duty in blinking_telltales])
            timing_data['interval'] = int(1000 * fastest_duty_cycle)  # Convert to milliseconds
        
        timing_data['blinking_telltales'] = blinking_telltales
        timing_data['non_blinking_telltales'] = non_blinking_telltales
        

        return timing_data

    def stop_zone_round_robin(self, zone):
        """Stop the round-robin cycling for a specific zone"""
        if zone in self.zone_timers:
            self.zone_timers[zone].stop()
    
        
        if zone in self.zone_round_robin_data:
            del self.zone_round_robin_data[zone]

    def cycle_zone_telltales(self, zone):
        """Cycle through telltales for a specific zone"""
        if zone not in self.zone_round_robin_data:
            return
            
        data = self.zone_round_robin_data[zone]
        telltales = data['telltales']
        
        # Hide all telltale decks for this zone
        for deck_num, card_num in telltales:
            deck_index = deck_num - 50
            if 0 <= deck_index < len(self.telltale_decks):
                self.telltale_decks[deck_index].hide()
        
        # Show current telltale for this zone
        self.show_zone_current_telltale(zone)
        
        # Move to next telltale
        data['current_index'] = (data['current_index'] + 1) % len(telltales)

    def show_zone_current_telltale(self, zone):
        """Show the current telltale for a specific zone"""
        if zone not in self.zone_round_robin_data:
            return
            
        data = self.zone_round_robin_data[zone]
        telltales = data['telltales']
        current_index = data['current_index']
        
        if current_index < len(telltales):
            deck_num, card_num = telltales[current_index]
            deck_index = deck_num - 50
            if deck_index < len(self.telltale_decks):
                self.telltale_decks[deck_index].show()

class MessageQueue:
    def __init__(self, main_window):
        self.main_window = main_window

    def send_activation(self, deck, card, activation_status):
        if 50 <= deck <= max(TELL_TALES.keys()):
            # Handle telltales
            if activation_status:
                self.main_window.activate_telltale(deck, card)
            else:
                self.main_window.deactivate_telltale(deck, card)
        else:
            # Handle regular decks
            if activation_status:
                self.main_window.activate_deck_card(deck, card)
            else:
                self.main_window.deactivate_deck_card(deck, card)

    def send_dynamic_text(self, deck, card, text):
        # Update only dynamic text for the given deck/card in the main window
        if deck < len(self.main_window.decks):
            deck_widget = self.main_window.decks[deck]
            card_widget = deck_widget.cards[card]
            for idx, elem in enumerate(DECK_GRAPHICS.get(deck, {}).get(card, [])):
                if elem["type"] == "dynamic_text":
                    # Find corresponding QLabel in ui_items
                    label_count = 0
                    for item in card_widget.ui_items:
                        if isinstance(item, QLabel):
                            # Only update the dynamic_text label (by order)
                            if label_count == idx:
                                item.setText(text)
                            label_count += 1

    def send_progress_bar_old(self, deck, card, value):
        # Update progress bar for the given deck/card in the main window
        if deck < len(self.main_window.decks):
            deck_widget = self.main_window.decks[deck]
            card_widget = deck_widget.cards[card]
            for idx, elem in enumerate(DECK_GRAPHICS.get(deck, {}).get(card, [])):
                if elem["type"] == "progress_bar":
                    # Find corresponding QProgressBar in ui_items
                    bar_count = 0
                    for item in card_widget.ui_items:
                        from PyQt5.QtWidgets import QProgressBar
                        if isinstance(item, QProgressBar):
                            if bar_count == idx:
                                item.setValue(int(value))
                            bar_count += 1
    def send_progress_bar(self, deck, card, value):
        # Update progress bar for the given deck/card in the main window
        if deck < len(self.main_window.decks):
            deck_widget = self.main_window.decks[deck]
            card_widget = deck_widget.cards[card]
            for item in card_widget.ui_items:
                from PyQt5.QtWidgets import QProgressBar
                if isinstance(item, QProgressBar):
                    item.setValue(int(value))
                    break  # Only update the first progress bar

def test_application():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    queue = MessageQueue(main_window)

    # Deactivate all decks/cards (show deck 0, card 0)
    queue.send_activation(0, 0, True)

    # Activate each deck/card as per graphics design
    def activate_all():
        delay = 500
        for deck_num, cards in DECK_GRAPHICS.items():
            for card_num in cards:
                QTimer.singleShot(delay, lambda d=deck_num, c=card_num: queue.send_activation(d, c, True))
                delay += 500

    QTimer.singleShot(1000, activate_all)
    sys.exit(app.exec_())

def test_application2():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    queue = MessageQueue(main_window)

    # Deactivate all decks/cards (show deck 0, card 0)
    queue.send_activation(0, 0, True)

    # Activate last card available in each deck at once (no delay)
    #for deck_num, cards in DECK_GRAPHICS.items():
        #last_card_num = max(cards.keys())
        #queue.send_activation(deck_num, last_card_num, True)

    queue.send_activation(0, 1, True) # bgnd
    queue.send_activation(1, 1, True) # lane graphics
    queue.send_activation(2, 1, True) # music bgnd
    queue.send_activation(3, 1, True) # music cover
    queue.send_activation(4, 1, True) # mini car
    queue.send_activation(5, 1, True) # ECO
    queue.send_activation(6, 1, True) # weather icon

    queue.send_activation(7, 2, True) # P  
    queue.send_activation(8, 1, True) # D
    queue.send_activation(9, 2, True) # N
    queue.send_activation(10, 2, True) # R

    queue.send_activation(11, 1, True) # time
    queue.send_activation(12, 1, True) # temp    
    queue.send_activation(13, 1, True) # speedo
    queue.send_activation(14, 1, True) # range

    sys.exit(app.exec_())

def test_application3():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    queue = MessageQueue(main_window)

    # Activate background
    queue.send_activation(0, 1, True)
    
    # Test different chime types
    
    # Test "once" chime type
    queue.send_activation(51, 2, True)  # TT002 Min Oil Level (once)
    
    # Test "twice" chime type
    queue.send_activation(51, 1, True)  # TT001 Low Oil Level (twice)
    
    # Test "continuous" chime type
    queue.send_activation(55, 1, True)  # TT008_SW_1 (continuous)
    
    # Test telltales without chimes
    queue.send_activation(52, 1, True)  # TT003 Airbag Enabled (no chime)
    
    # Test blinking telltales
    queue.send_activation(54, 1, True)  # TT007 Hazard (blinking)
    queue.send_activation(59, 1, True)  # TT016 LeftTurn (blinking)

    sys.exit(app.exec_())

def test_chime_functionality():
    """Test specific chime functionality"""
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    queue = MessageQueue(main_window)

    # Activate background
    queue.send_activation(0, 1, True)
    
    # Test each chime type systematically
    test_cases = [
        (51, 1, "TT001 - Low Oil Level (twice chime)"),
        (51, 2, "TT002 - Min Oil Level (once chime)"),
        (55, 1, "TT008_SW_1 - Seatbelt Alert (continuous chime)"),
        (55, 2, "TT009_SW_2 - Seatbelt Alert (once chime)"),
        (56, 1, "TT010 - Low Fuel Warning (once chime)"),
        (61, 2, "TT019 - Engine Temp High (twice chime)"),
        (52, 1, "TT003 - Airbag Enabled (no chime)")
    ]
    
    for deck, card, description in test_cases:
        queue.send_activation(deck, card, True)
        # Add delay between tests
        QTimer.singleShot(2000, lambda d=deck, c=card: queue.send_activation(d, c, False))

    sys.exit(app.exec_())

# To run test_application2, replace the main block with:
# if __name__ == "__main__":
#     test_application2()

# To run chime functionality test, replace the main block with:
# if __name__ == "__main__":
#     test_chime_functionality()

#if __name__ == "__main__":
#    test_application3()