import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QProgressBar
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import queue as pyqueue

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

TELL_TALES = {
    50: {
        0: []        
    },
    51: {
        0: [],
        1: [{"type": "image", "file": "TT001_Low Oil Level_1.png", "zone": 2, "blinking": "NO", "duty_cycle": 0.5, "chime": "engine_check", "chime_type": "twice", "duration": 5}],
        2: [{"type": "image", "file": "TT002_Min Oil Level.png", "zone": 2, "blinking": "YES", "duty_cycle": 0.3, "chime": "engine_check", "chime_type": "once", "duration": 5}]
    },
    52: {
        0: [],
        1: [{"type": "image", "file": "TT003_Airbag_Enabled.png", "zone": 1, "blinking": "NO", "duty_cycle": 0.5, "chime": None, "chime_type": "once", "duration": 5}],
        2: [{"type": "image", "file": "TT004_Airbag_Disabled.png", "zone": 1, "blinking": "NO", "duty_cycle": 0.4, "chime": "jeep_seatbelt_alert", "chime_type": "once", "duration": 5}]
    },
    53: {
        0: [],
        1: [{"type": "image", "file": "TT005_Battery Level Low_1.png", "zone": 2, "blinking": "YES", "duty_cycle": 0.6, "chime": "engine_check", "chime_type": "once", "duration": 5}],
        2: [{"type": "image", "file": "TT006_Battery Level Low_2.png", "zone": 2, "blinking": "NO", "duty_cycle": 0.6, "chime": "engine_check", "chime_type": "twice", "duration": 5}]
    },
    54: {
        0: [],
        1: [{"type": "image", "file": "TT007_Hazard.png", "zone": 4, "blinking": "NO", "duty_cycle": 0.5, "chime": "blinker", "chime_type": "once", "duration": 5}]
    },
    55: {
        0: [],
        1: [{"type": "image", "file": "TT008_SW_1.png", "zone": 1, "blinking": "NO", "duty_cycle": 0.5, "chime": "jeep_seatbelt_alert", "chime_type": "continuous", "duration": 90}],
        2: [{"type": "image", "file": "TT009_SW_2.png", "zone": 1, "blinking": "NO", "duty_cycle": 0.5, "chime": "jeep_seatbelt_alert", "chime_type": "once", "duration": 5}]
    },
    56: {
        0: [],
        1: [{"type": "image", "file": "TT010_Low Fuel Warning.png", "zone": 2, "blinking": "NO", "duty_cycle": 0.7, "chime": "low_fuel", "chime_type": "once", "duration": 5}],
        2: [{"type": "image", "file": "TT011_Water in Fuel.png", "zone": 2, "blinking": "YES", "duty_cycle": 0.5, "chime": "engine_check", "chime_type": "once", "duration": 5}],
        3: [{"type": "image", "file": "TT012_Loose Fuel Cap.png", "zone": 2, "blinking": "YES", "duty_cycle": 0.4, "chime": "engine_check", "chime_type": "once", "duration": 5}],        
    },
    57: {
        0: [],
        1: [{"type": "image", "file": "TT013_Low Beam_1.png", "zone": 7, "blinking": "NO", "duty_cycle": 0.5, "chime": None, "chime_type": "once", "duration": 5}]
    },
    58: {
        0: [],
        1: [{"type": "image", "file": "TT014_High Beam.png", "zone": 6, "blinking": "NO", "duty_cycle": 0.5, "chime": None, "chime_type": "once", "duration": 5}],
        2: [{"type": "image", "file": "TT015_Low Beam_2.png", "zone": 6, "blinking": "NO", "duty_cycle": 0.5, "chime": None, "chime_type": "once", "duration": 5}]
    },
    59: {
        0: [],
        1: [{"type": "image", "file": "TT016_LeftTurn.png", "zone": 3, "blinking": "YES", "duty_cycle": 0.5, "chime": "blinker", "chime_type": "once", "duration": 5}]
    },
    60: {
        0: [],
        1: [{"type": "image", "file": "TT017_RightTurn.png", "zone": 5, "blinking": "YES", "duty_cycle": 0.5, "chime": "blinker", "chime_type": "once", "duration": 5}]
    },
    61: {
        0: [],
        1: [{"type": "image", "file": "TT018_Eng Temp_Low.png", "zone": 2, "blinking": "YES", "duty_cycle": 0.5, "chime": None, "chime_type": "once", "duration": 5}],
        2: [{"type": "image", "file": "TT019_Eng Temp_High_1.png", "zone": 2, "blinking": "NO", "duty_cycle": 0.3, "chime": "engine_check", "chime_type": "twice", "duration": 5}],
        3: [{"type": "image", "file": "TT020_Engine Temp_High_2.png", "zone": 2, "blinking": "NO", "duty_cycle": 0.3, "chime": "engine_check", "chime_type": "twice", "duration": 5}]
    }
}

# Patch TELL_TALES to ensure all required fields
for deck, cards in TELL_TALES.items():
    for card, elements in cards.items():
        for elem in elements:
            if elem.get("type") == "image":
                if "zone" not in elem:
                    elem["zone"] = 1
                if "blinking" not in elem:
                    elem["blinking"] = "NO"
                if "duty_cycle" not in elem:
                    elem["duty_cycle"] = 0.5
                if "chime" not in elem or (elem["chime"] is not None and elem["chime"] not in CHIME_CONFIG):
                    elem["chime"] = None

class ChimeRequest:
    def __init__(self, chime_id, deck_num, card_num, duration):
        self.chime_id = chime_id
        self.deck_num = deck_num
        self.card_num = card_num
        self.duration = duration

class ChimeHandler:
    def __init__(self):
        self.queue = pyqueue.Queue()
        self.current_chime = None
        self.player = QMediaPlayer()
        self.blinker_players = []
        self.timer = QTimer()
        self.timer.timeout.connect(self._on_chime_timeout)

    def enqueue(self, chime_req):
        if chime_req.chime_id == "blinker":
            self._play_blinker_chime(chime_req)
        else:
            self.queue.put(chime_req)
            if not self.current_chime:
                self._play_next()

    def _play_next(self):
        if not self.queue.empty():
            chime_req = self.queue.get()
            self.current_chime = chime_req
            chime_info = CHIME_CONFIG[chime_req.chime_id]
            file_path = os.path.join(CHIMES_DIR, chime_info["file"])
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.player.setVolume(chime_info.get("volume", 50))
            self.player.play()
            self.timer.start(chime_info["duration"] * 1000)

    def _on_chime_timeout(self):
        self.player.stop()
        self.current_chime = None
        self.timer.stop()
        self._play_next()

    def _play_blinker_chime(self, chime_req):
        chime_info = CHIME_CONFIG["blinker"]
        file_path = os.path.join(CHIMES_DIR, chime_info["file"])
        player = QMediaPlayer()
        player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        player.setVolume(chime_info.get("volume", 50))
        player.play()
        self.blinker_players.append(player)
        QTimer.singleShot(chime_info["duration"] * 1000, lambda: self._stop_blinker(player))

    def _stop_blinker(self, player):
        player.stop()
        self.blinker_players.remove(player)

    def stop_chime(self, chime_id, deck_num, card_num):
        if self.current_chime and self.current_chime.chime_id == chime_id and \
           self.current_chime.deck_num == deck_num and self.current_chime.card_num == card_num:
            self.player.stop()
            self.current_chime = None
            self.timer.stop()
            self._play_next()
        if chime_id == "blinker":
            for player in self.blinker_players:
                player.stop()
            self.blinker_players.clear()

chime_handler = ChimeHandler()

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
        if 0 <= card_num < len(self.cards):
            for i, card in enumerate(self.cards):
                card.hide()
            self.cards[card_num].show()
            self.active_card = card_num

    def activate_card(self, card_num):
        if 0 <= card_num < len(self.cards):
            self.show_card(card_num)

    def deactivate_card(self, card_num):
        if 0 <= card_num < len(self.cards):
            if self.active_card == card_num:
                for i in range(card_num - 1, -1, -1):
                    if self.cards[i].isVisible():
                        self.show_card(i)
                        return
                self.show_card(0)

# Patch CardWidget to trigger/stop chime on activation/deactivation
old_activate_card = DeckWidget.activate_card
old_deactivate_card = DeckWidget.deactivate_card

def activate_card_with_chime(self, card_num):
    old_activate_card(self, card_num)
    elements = self.cards[card_num].elements if card_num in self.cards else []
    for elem in elements:
        if elem.get("type") == "image" and elem.get("chime"):
            chime_req = ChimeRequest(elem["chime"], self.deck_num, card_num, elem.get("duration", 5))
            chime_handler.enqueue(chime_req)

def deactivate_card_with_chime(self, card_num):
    old_deactivate_card(self, card_num)
    elements = self.cards[card_num].elements if card_num in self.cards else []
    for elem in elements:
        if elem.get("type") == "image" and elem.get("chime"):
            chime_handler.stop_chime(elem["chime"], self.deck_num, card_num)

DeckWidget.activate_card = activate_card_with_chime
DeckWidget.deactivate_card = deactivate_card_with_chime

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Decks and Cards Demo")
        self.setFixedSize(*BG_RESOLUTION)
        self.decks = []
        for deck_num in range(0, max(DECK_GRAPHICS.keys()) + 1):
            deck = DeckWidget(deck_num)
            deck.setParent(self)
            deck.move(0, 0)
            deck.hide()
            self.decks.append(deck)
        # Create telltale decks
        self.telltale_decks = {}
        for deck_num in TELL_TALES:
            deck = DeckWidget(deck_num)
            deck.setParent(self)
            deck.move(0, 0)
            deck.hide()
            self.telltale_decks[deck_num] = deck

    def show_deck(self, deck_num):
        if 0 <= deck_num < len(self.decks):
            self.decks[deck_num].show()

    def hide_deck(self, deck_num):
        if 0 <= deck_num < len(self.decks):
            self.decks[deck_num].hide()

    def activate_deck_card(self, deck_num, card_num):
        if 0 <= deck_num < len(self.decks):
            self.show_deck(deck_num)
            self.decks[deck_num].activate_card(card_num)

    def deactivate_deck_card(self, deck_num, card_num):
        if 0 <= deck_num < len(self.decks):
            self.decks[deck_num].deactivate_card(card_num)
            if self.decks[deck_num].active_card == 0:
                self.hide_deck(deck_num)

    def activate_telltale(self, deck_num, card_num):
        if deck_num in self.telltale_decks:
            self.telltale_decks[deck_num].show()
            self.telltale_decks[deck_num].activate_card(card_num)

    def deactivate_telltale(self, deck_num, card_num):
        if deck_num in self.telltale_decks:
            self.telltale_decks[deck_num].deactivate_card(card_num)
            if self.telltale_decks[deck_num].active_card == 0:
                self.telltale_decks[deck_num].hide()

class MessageQueue:
    def __init__(self, main_window):
        self.main_window = main_window

    def send_activation(self, deck, card, activation_status):
        if deck in TELL_TALES:
            if activation_status:
                self.main_window.activate_telltale(deck, card)
            else:
                self.main_window.deactivate_telltale(deck, card)
        elif deck in DECK_GRAPHICS:
            if activation_status:
                self.main_window.activate_deck_card(deck, card)
            else:
                self.main_window.deactivate_deck_card(deck, card)
        else:
            print(f"Invalid activation: deck {deck}, card {card}")

# Patch MessageQueue to only allow valid deck/cards and telltales
old_send_activation = MessageQueue.send_activation

def send_activation_guarded(self, deck, card, activation_status):
    if deck in DECK_GRAPHICS and card in DECK_GRAPHICS[deck]:
        old_send_activation(self, deck, card, activation_status)
    elif deck in TELL_TALES and card in TELL_TALES[deck]:
        old_send_activation(self, deck, card, activation_status)
    else:
        print(f"Invalid activation: deck {deck}, card {card}")

MessageQueue.send_activation = send_activation_guarded

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


    sys.exit(app.exec_())

# To run test_application2, replace the main block with:
# if __name__ == "__main__":
#     test_application2()

#if __name__ == "__main__":
#    test_application3()
'''
__all__ = [
    'MainWindow',
    'MessageQueue',
    'DECK_GRAPHICS',
    'TELL_TALES',
    'ZONE_COORDINATES',
    'CHIME_CONFIG'
]
'''