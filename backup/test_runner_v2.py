import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QScrollArea, QMessageBox, QTabWidget, QGroupBox
)
from workshop_v2 import MainWindow, MessageQueue, DECK_GRAPHICS, TELL_TALES

class TestRunnerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Runner")
        self.setGeometry(100, 100, 900, 700)
        self.main_window = MainWindow()
        self.queue = MessageQueue(self.main_window)
        self.layout = QVBoxLayout(self)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.create_deck_tab()
        self.create_telltale_tab()

        # Show main window button
        btn_show_main = QPushButton("Show Main GUI")
        btn_show_main.clicked.connect(self.show_main_window)
        self.layout.addWidget(btn_show_main)

        # Exit button
        btn_exit = QPushButton("Exit Test Runner")
        btn_exit.setStyleSheet("background-color: #ff4444; color: white; font-weight: bold;")
        btn_exit.clicked.connect(QApplication.quit)
        self.layout.addWidget(btn_exit)

    def create_deck_tab(self):
        deck_tab = QWidget()
        deck_layout = QVBoxLayout(deck_tab)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
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
                scroll_layout.addLayout(row)
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        deck_layout.addWidget(scroll)
        self.tab_widget.addTab(deck_tab, "Deck/Card Activation")

    def create_telltale_tab(self):
        telltale_tab = QWidget()
        telltale_layout = QVBoxLayout(telltale_tab)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        for deck_num, cards in TELL_TALES.items():
            deck_label = QLabel(f"Telltale Deck {deck_num}")
            deck_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
            scroll_layout.addWidget(deck_label)
            for card_num, elements in cards.items():
                row = QHBoxLayout()
                btn_activate = QPushButton(f"Activate Telltale {deck_num} Card {card_num}")
                btn_deactivate = QPushButton(f"Deactivate")
                btn_activate.setFixedWidth(180)
                btn_deactivate.setFixedWidth(100)
                btn_activate.clicked.connect(lambda _, d=deck_num, c=card_num: self.queue.send_activation(d, c, True))
                btn_deactivate.clicked.connect(lambda _, d=deck_num, c=card_num: self.queue.send_activation(d, c, False))
                row.addWidget(btn_activate)
                row.addWidget(btn_deactivate)
                scroll_layout.addLayout(row)
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        telltale_layout.addWidget(scroll)
        self.tab_widget.addTab(telltale_tab, "Telltale Activation")

    def show_main_window(self):
        self.main_window.show()

def main():
    app = QApplication(sys.argv)
    test_gui = TestRunnerWindow()
    test_gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()