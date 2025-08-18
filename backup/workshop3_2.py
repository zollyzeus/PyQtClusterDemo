# Modified workshop3_1.py (integrated into main file)

import sys
import os
import queue
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QProgressBar
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import logging
from datetime import datetime

# Setup logging for chime events
logs_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(logs_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(logs_dir, f"chime_log_{timestamp}.log")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[
    logging.FileHandler(log_file, mode='w'),
    logging.StreamHandler(sys.stdout)
])
logger = logging.getLogger(__name__)

CHIMES_DIR = os.path.join(os.path.dirname(__file__), "chimes")

CHIME_CONFIG = {
    "blinker": {"file": "blinker.mp3", "type": "once", "duration": 1},
    "door_ajar": {"file": "door_ajar.mp3", "type": "once", "duration": 5},
    "parking_brake_engaged": {"file": "parking_brake_engaged.mp3", "type": "once", "duration": 5},
    "engine_check": {"file": "engine_check.mp3", "type": "twice", "duration": 5},
    "low_fuel": {"file": "low_fuel.mp3", "type": "once", "duration": 5},
    "tire_pressure_warning": {"file": "tire_pressure_warning.mp3", "type": "once", "duration": 5},
    "jeep_door_open": {"file": "jeep_door_open.mp3", "type": "once", "duration": 5},
    "jeep_key_left_in_ignition": {"file": "jeep_key_left_in_ignition.mp3", "type": "once", "duration": 5},
    "jeep_seatbelt_alert": {"file": "jeep_seatbelt_alert.mp3", "type": "continuous", "duration": 90}
}

chime_event_queue = queue.Queue()

class ChimeQueueHandler:
    def __init__(self):
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.play_next_chime)
        self.current_player = QMediaPlayer()
        self.current_player.setVolume(50)
        self.current_player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.current_chime_data = None

    def enqueue_chime(self, chime_name):
        if chime_name == "blinker":
            self.play_blinker_chime()
            return
        if chime_name in CHIME_CONFIG:
            chime_event_queue.put(chime_name)
            if not self.timer.isActive():
                self.play_next_chime()

    def play_next_chime(self):
        if chime_event_queue.empty():
            return
        chime_name = chime_event_queue.get()
        config = CHIME_CONFIG.get(chime_name)
        if config:
            file_path = os.path.join(CHIMES_DIR, config["file"])
            self.current_chime_data = (chime_name, config)
            self.current_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.current_player.play()
            logger.info(f"Playing chime: {chime_name}")

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            _, config = self.current_chime_data
            delay = config.get("duration", 3) * 1000
            self.timer.start(delay)

    def play_blinker_chime(self):
        config = CHIME_CONFIG.get("blinker")
        if not config:
            return
        player = QMediaPlayer()
        player.setVolume(50)
        path = os.path.join(CHIMES_DIR, config["file"])
        player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        player.play()
        logger.info("Playing blinker chime")

chime_handler = ChimeQueueHandler()

# In TellTaleWidget.init_ui, replace chime logic:
# Instead of: self.setup_chime(chime, chime_type)
# Use:
# if chime: chime_handler.enqueue_chime(chime)

# Remove methods:
# setup_chime, play_chime, setup_chime_timer, on_chime_status_changed, on_chime_error
# Cleanup chime_player, chime_timer, chime_type, chime_play_count from class attributes
