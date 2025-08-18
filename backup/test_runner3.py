import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QScrollArea, QMessageBox
)
from workshop3 import MainWindow, MessageQueue, DECK_GRAPHICS

class TestRunnerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deck/Card Activation Test GUI")
        self.setGeometry(100, 100, 800, 600)
        self.main_window = MainWindow()
        self.queue = MessageQueue(self.main_window)
        self.layout = QVBoxLayout(self)

        # Scroll area for deck/card controls
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Build activation buttons and text boxes for each deck/card
        self.text_inputs = {}  # (deck, card): QLineEdit
        for deck_num, cards in DECK_GRAPHICS.items():
            deck_label = QLabel(f"Deck {deck_num}")
            deck_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
            scroll_layout.addWidget(deck_label)
            for card_num, elements in cards.items():
                row = QHBoxLayout()
                btn_activate = QPushButton(f"Activate Deck {deck_num} Card {card_num}")
                btn_deactivate = QPushButton(f"Deactivate")
                btn_activate.setFixedWidth(180)
                btn_deactivate.setFixedWidth(100)
                btn_activate.clicked.connect(lambda _, d=deck_num, c=card_num: self.queue.send_activation(d, c, True))
                btn_deactivate.clicked.connect(lambda _, d=deck_num, c=card_num: self.queue.send_activation(d, c, False))
                row.addWidget(btn_activate)
                row.addWidget(btn_deactivate)

                # Add text boxes for text elements
                for elem in elements:
                    if elem["type"] in ("dynamic_text"):
                        txt = QLineEdit(elem.get("value", ""))
                        txt.setFixedWidth(200)
                        txt.setPlaceholderText("Set text value")
                        self.text_inputs[(deck_num, card_num)] = txt
                        row.addWidget(QLabel(f'Text for card {card_num}:'))
                        row.addWidget(txt)
                        # Button to update text
                        btn_set_text = QPushButton("Set Text")
                        btn_set_text.setFixedWidth(80)
                        btn_set_text.clicked.connect(lambda _, d=deck_num, c=card_num, t=txt: self.set_text(d, c, t.text()))
                        row.addWidget(btn_set_text)
                scroll_layout.addLayout(row)

        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        self.layout.addWidget(scroll)

        # Show main window button
        btn_show_main = QPushButton("Show Main GUI")
        btn_show_main.clicked.connect(self.show_main_window)
        self.layout.addWidget(btn_show_main)

    def show_main_window(self):
        self.main_window.show()

    def set_text(self, deck, card, text):
        # Update only dynamic text for the given deck/card in the main window
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
        QMessageBox.information(self, "Text Updated", f"Dynamic text for Deck {deck} Card {card} updated.")

def main():
    app = QApplication(sys.argv)
    test_gui = TestRunnerWindow()
    test_gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()