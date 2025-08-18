import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QTextEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from workshop3_1 import DECK_GRAPHICS, TELL_TALES

class TestToolClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Tool REST Client")
        self.setGeometry(200, 200, 600, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.ip_input = QLineEdit("127.0.0.1")
        self.port_input = QLineEdit("8000")
        self.layout.addWidget(QLabel("Target IP:"))
        self.layout.addWidget(self.ip_input)
        self.layout.addWidget(QLabel("Target Port:"))
        self.layout.addWidget(self.port_input)

        # Type dropdown and editable
        type_layout = QHBoxLayout()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["deck", "card", "telltale", "dynamic_text", "progress_bar"])
        self.type_edit = QLineEdit()
        self.type_edit.setText(self.type_combo.currentText())
        type_layout.addWidget(QLabel("Type:"))
        type_layout.addWidget(self.type_combo)
        type_layout.addWidget(self.type_edit)
        self.layout.addLayout(type_layout)

        # Deck dropdown and editable
        deck_layout = QHBoxLayout()
        self.deck_combo = QComboBox()
        self.deck_edit = QLineEdit()
        deck_layout.addWidget(QLabel("Deck Number:"))
        deck_layout.addWidget(self.deck_combo)
        deck_layout.addWidget(self.deck_edit)
        self.layout.addLayout(deck_layout)

        # Card dropdown and editable
        card_layout = QHBoxLayout()
        self.card_combo = QComboBox()
        self.card_edit = QLineEdit()
        card_layout.addWidget(QLabel("Card Number:"))
        card_layout.addWidget(self.card_combo)
        card_layout.addWidget(self.card_edit)
        self.layout.addLayout(card_layout)

        # Action dropdown and editable
        action_layout = QHBoxLayout()
        self.action_combo = QComboBox()
        self.action_combo.addItems(["activate", "deactivate", "update"])
        self.action_edit = QLineEdit()
        self.action_edit.setText(self.action_combo.currentText())
        action_layout.addWidget(QLabel("Action:"))
        action_layout.addWidget(self.action_combo)
        action_layout.addWidget(self.action_edit)
        self.layout.addLayout(action_layout)

        self.value_input = QLineEdit()
        self.layout.addWidget(QLabel("Value (for dynamic_text):"))
        self.layout.addWidget(self.value_input)

        self.send_btn = QPushButton("Send Command")
        self.layout.addWidget(self.send_btn)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.layout.addWidget(QLabel("Log:"))
        self.layout.addWidget(self.log_box)

        self.activate_all_decks_btn = QPushButton("Activate All Decks")
        self.deactivate_all_decks_btn = QPushButton("Deactivate All Decks")
        self.activate_all_telltales_btn = QPushButton("Activate All Telltales")
        self.deactivate_all_telltales_btn = QPushButton("Deactivate All Telltales")
        self.activate_main_window_btn = QPushButton("Activate Main Window")
        self.layout.addWidget(self.activate_all_decks_btn)
        self.layout.addWidget(self.deactivate_all_decks_btn)
        self.layout.addWidget(self.activate_all_telltales_btn)
        self.layout.addWidget(self.deactivate_all_telltales_btn)
        self.layout.addWidget(self.activate_main_window_btn)
        self.activate_all_decks_btn.clicked.connect(lambda: self.send_bulk_command("activate_all_decks"))
        self.deactivate_all_decks_btn.clicked.connect(lambda: self.send_bulk_command("deactivate_all_decks"))
        self.activate_all_telltales_btn.clicked.connect(lambda: self.send_bulk_command("activate_all_telltales"))
        self.deactivate_all_telltales_btn.clicked.connect(lambda: self.send_bulk_command("deactivate_all_telltales"))
        self.activate_main_window_btn.clicked.connect(lambda: self.send_bulk_command("activate_main_window"))

        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        self.deck_combo.currentTextChanged.connect(self.on_deck_changed)
        self.card_combo.currentTextChanged.connect(self.on_card_changed)
        self.action_combo.currentTextChanged.connect(self.on_action_changed)
        self.send_btn.clicked.connect(self.send_command)

        self.populate_decks()
        self.on_type_changed(self.type_combo.currentText())

    def populate_decks(self):
        self.deck_combo.clear()
        all_decks = set(DECK_GRAPHICS.keys()) | set(TELL_TALES.keys())
        for deck in sorted(all_decks):
            self.deck_combo.addItem(str(deck))
        if self.deck_combo.count() > 0:
            self.deck_combo.setCurrentIndex(0)
            self.deck_edit.setText(self.deck_combo.currentText())

    def on_type_changed(self, value):
        self.type_edit.setText(value)
        self.update_card_combo()

    def on_deck_changed(self, value):
        self.deck_edit.setText(value)
        self.update_card_combo()

    def on_card_changed(self, value):
        self.card_edit.setText(value)

    def on_action_changed(self, value):
        self.action_edit.setText(value)

    def update_card_combo(self):
        typ = self.type_combo.currentText()
        deck = int(self.deck_combo.currentText()) if self.deck_combo.currentText() else 0
        self.card_combo.clear()
        max_card = 0
        if typ in ("deck", "card", "dynamic_text","progress_bar"):
            cards = list(DECK_GRAPHICS.get(deck, {}).keys())
            if cards:
                max_card = max(cards)
        elif typ == "telltale":
            cards = list(TELL_TALES.get(deck, {}).keys())
            if cards:
                max_card = max(cards)
        for card in range(0, max_card + 1):
            self.card_combo.addItem(str(card))
        if self.card_combo.count() > 0:
            self.card_combo.setCurrentIndex(0)
            self.card_edit.setText(self.card_combo.currentText())

    def send_command(self):
        host = self.ip_input.text()
        port = self.port_input.text()
        typ = self.type_edit.text() if self.type_edit.text() else self.type_combo.currentText()
        deck = int(self.deck_edit.text()) if self.deck_edit.text() else int(self.deck_combo.currentText())
        card = int(self.card_edit.text()) if self.card_edit.text() else int(self.card_combo.currentText())
        action = self.action_edit.text() if self.action_edit.text() else self.action_combo.currentText()
        value = self.value_input.text() if typ in ("dynamic_text", "progress_bar") else None
        payload = {
            "type": typ,
            "deck_num": deck,
            "card_num": card,
            "action": action
        }
        if value:
            payload["value"] = value
        url = f"http://{host}:{port}/api/control"
        try:
            resp = requests.post(url, json=payload, timeout=2)
            self.log_box.append(f"Sent: {payload}\nResponse: {resp.text}")
        except Exception as e:
            self.log_box.append(f"Error sending command: {e}")

    def send_bulk_command(self, action):
        host = self.ip_input.text()
        port = self.port_input.text()
        payload = {
            "type": "bulk",
            "action": action
        }
        url = f"http://{host}:{port}/api/control"
        try:
            resp = requests.post(url, json=payload, timeout=2)
            self.log_box.append(f"Sent bulk: {payload}\nResponse: {resp.text}")
        except Exception as e:
            self.log_box.append(f"Error sending bulk command: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = TestToolClient()
    client.show()
    sys.exit(app.exec_())