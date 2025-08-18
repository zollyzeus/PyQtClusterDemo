import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QProgressBar
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

DEFAULT_CARD_LENGTH = 10
BG_RESOLUTION = (1920, 720)
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "Images")

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
        1: [{"type": "image", "file": "music cover.png", "x": 1521, "y": 226}],
        2: [{"type": "dynamic_text", "value": "We Don't talk Anymore", "x": 1482, "y": 486, "font_family": "HYQiHei", "font_size": 28, "font_color": "#47473F", "opacity": 100}],
        3: [{"type": "dynamic_text", "value": "Charlie Puth", "x": 1564, "y": 525, "font_family": "HYQiHei", "font_size": 24, "font_color": "#47473F", "opacity": 40}]
    },
    4: {
        0: [],
        1: [{"type": "image", "file": "mini car.png", "x": 690, "y": 354}]
    },
    5: {
        0: [],
        1: [{"type": "image", "file": "ECO.png", "x": 1750, "y": 45}]
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
        1: [{"type": "dynamic_text", "value": "08:30", "x": 1420, "y": 45, "font_family": "HYQiHei", "font_size": 32, "font_color": "#47473F", "opacity": 100}]
    },
    12: {
        0: [],
        1: [{"type": "dynamic_text", "value": "26℃", "x": 1620, "y": 45, "font_family": "HYQiHei", "font_size": 32, "font_color": "#47473F", "opacity": 100}]
    },
    13: {
        0: [],
        1: [
            {"type": "dynamic_text", "value": "85", "x": 100, "y": 275, "font_family": "HFBUBU", "font_size": 180, "font_color": "#47473F", "opacity": 100},
            {"type": "static_text", "value": "km/h", "x": 380, "y": 385, "font_family": "HYQiHei", "font_size": 32, "font_color": "#47473F", "opacity": 80}
        ]
    },
    14: {
        0: [],
        1: [
            {"type": "dynamic_text", "value": "212", "x": 282, "y": 616, "font_family": "HFBUBU", "font_size": 32, "font_color": "#47473F", "opacity": 100},
            {"type": "static_text", "value": "km", "x": 361, "y": 612, "font_family": "HYQiHei", "font_size": 28, "font_color": "#47473F", "opacity": 80},
            {"type": "progress_bar", "x": 106, "y": 626, "fill_color": "#76B047", "outer_bar_color": "#D3D7D2", "w": 160, "h": 16}
        ]
    }
}

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
                label.setFont(QFont(elem.get("font_family", "Arial"), elem.get("font_size", 24)))
                label.setStyleSheet(f"color: {elem.get('font_color', '#000')};")
                label.setGeometry(elem["x"], elem["y"], elem.get("w", 100), elem.get("h", 40))
                label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                label.setWindowOpacity(elem.get("opacity", 100) / 100.0)
                label.show()
                self.ui_items.append(label)
            elif elem["type"] == "progress_bar":
                bar = QProgressBar(self)
                bar.setGeometry(elem["x"], elem["y"], elem["w"], elem["h"])
                bar.setValue(70)
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
        # Use absolute positioning for all decks
        for deck_num in range(0, max(DECK_GRAPHICS.keys()) + 1):
            deck = DeckWidget(deck_num)
            deck.setParent(self)
            deck.move(0, 0)
            deck.hide()
            self.decks.append(deck)
        # No single active_deck, all decks can be visible

    def show_deck(self, deck_num):
        self.decks[deck_num].show()

    def hide_deck(self, deck_num):
        self.decks[deck_num].hide()

    def activate_deck_card(self, deck_num, card_num):
        self.show_deck(deck_num)
        self.decks[deck_num].activate_card(card_num)

    def deactivate_deck_card(self, deck_num, card_num):
        self.decks[deck_num].deactivate_card(card_num)
        # Optionally hide deck if card 0 is active (empty)
        if self.decks[deck_num].active_card == 0:
            self.hide_deck(deck_num)

class MessageQueue:
    def __init__(self, main_window):
        self.main_window = main_window

    def send_activation(self, deck, card, activation_status):
        if activation_status:
            self.main_window.activate_deck_card(deck, card)
        else:
            self.main_window.deactivate_deck_card(deck, card)

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

    queue.send_activation(7, 1, True) # P  
    queue.send_activation(8, 2, True) # D
    queue.send_activation(9, 2, True) # N
    queue.send_activation(10, 2, True) # R

    queue.send_activation(11, 1, True) # time
    queue.send_activation(12, 1, True) # temp    
    queue.send_activation(13, 1, True) # speedo
    queue.send_activation(14, 1, True) # range

    sys.exit(app.exec_())

# To run test_application2, replace the main block with:
# if __name__ == "__main__":
#     test_application2()

if __name__ == "__main__":
    test_application2()