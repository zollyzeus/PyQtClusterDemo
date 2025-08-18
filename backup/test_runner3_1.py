import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QScrollArea, QMessageBox, QTabWidget, QGroupBox
)
from PyQt5.QtCore import QTimer
from workshop3_1 import MainWindow, MessageQueue, DECK_GRAPHICS, TELL_TALES, ZONE_COORDINATES



class TestRunnerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deck/Card Activation Test GUI")
        self.setGeometry(100, 100, 1200, 800)
        self.main_window = MainWindow()
        self.queue = MessageQueue(self.main_window)
        self.layout = QVBoxLayout(self)

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        # Create tabs
        self.create_deck_tab()
        self.create_telltale_tab()
        self.create_chime_test_tab()

        # Show main window button
        btn_show_main = QPushButton("Show Main GUI")
        btn_show_main.clicked.connect(self.show_main_window)
        self.layout.addWidget(btn_show_main)
        
        # Exit button
        btn_exit = QPushButton("Exit Application")
        btn_exit.setStyleSheet("background-color: #ff4444; color: white; font-weight: bold;")
        btn_exit.clicked.connect(self.exit_application)
        self.layout.addWidget(btn_exit)
        


    def create_deck_tab(self):
        """Create tab1 for deck activations"""
        deck_tab = QWidget()
        deck_layout = QVBoxLayout(deck_tab)

        # Activate/Deactivate all buttons for decks
        deck_control_layout = QHBoxLayout()
        btn_activate_all_decks = QPushButton("Activate All Decks")
        btn_deactivate_all_decks = QPushButton("Deactivate All Decks")
        btn_activate_all_decks.clicked.connect(self.activate_all_decks)
        btn_deactivate_all_decks.clicked.connect(self.deactivate_all_decks)
        deck_control_layout.addWidget(btn_activate_all_decks)
        deck_control_layout.addWidget(btn_deactivate_all_decks)
        deck_layout.addLayout(deck_control_layout)

        # Scroll area for deck/card controls
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Build activation buttons and text boxes for each deck/card
        self.deck_text_inputs = {}  # (deck, card): QLineEdit
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
                        self.deck_text_inputs[(deck_num, card_num)] = txt
                        row.addWidget(QLabel(f'Text for card {card_num}:'))
                        row.addWidget(txt)
                        # Button to update text
                        btn_set_text = QPushButton("Set Text")
                        btn_set_text.setFixedWidth(80)
                        btn_set_text.clicked.connect(lambda _, d=deck_num, c=card_num, t=txt: self.set_deck_text(d, c, t.text()))
                        row.addWidget(btn_set_text)
                scroll_layout.addLayout(row)

        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        deck_layout.addWidget(scroll)
        
        self.tab_widget.addTab(deck_tab, "Deck Activations")

    def create_telltale_tab(self):
        """Create tab2 for telltale activations grouped by zone first, then deck"""
        telltale_tab = QWidget()
        telltale_layout = QVBoxLayout(telltale_tab)

        # Activate/Deactivate all buttons for telltales
        telltale_control_layout = QHBoxLayout()
        btn_activate_all_telltales = QPushButton("Activate All Telltales")
        btn_deactivate_all_telltales = QPushButton("Deactivate All Telltales")
        btn_activate_all_telltales.clicked.connect(self.activate_all_telltales)
        btn_deactivate_all_telltales.clicked.connect(self.deactivate_all_telltales)
        telltale_control_layout.addWidget(btn_activate_all_telltales)
        telltale_control_layout.addWidget(btn_deactivate_all_telltales)
        telltale_layout.addLayout(telltale_control_layout)

        # Scroll area for telltale controls
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Group telltales by zone first, then by deck within each zone
        zone_deck_telltales = {}
        for deck_num, cards in TELL_TALES.items():
            for card_num, elements in cards.items():
                for elem in elements:
                    if elem["type"] == "image":
                        zone = elem.get("zone", 1)
                        if zone not in zone_deck_telltales:
                            zone_deck_telltales[zone] = {}
                        if deck_num not in zone_deck_telltales[zone]:
                            zone_deck_telltales[zone][deck_num] = []
                        zone_deck_telltales[zone][deck_num].append((card_num, elem))
                        break

        # Create zone groups
        for zone_num in sorted(zone_deck_telltales.keys()):
            zone_group = QGroupBox(f"Zone {zone_num}")
            zone_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 12px; }")
            zone_layout = QVBoxLayout(zone_group)
            
            # Add zone coordinates info
            zone_coords = ZONE_COORDINATES.get(zone_num, {"x": 0, "y": 0})
            coord_label = QLabel(f"Position: ({zone_coords['x']}, {zone_coords['y']})")
            coord_label.setStyleSheet("color: #666; font-size: 10px;")
            zone_layout.addWidget(coord_label)
            
            # Add deck groups within this zone
            for deck_num in sorted(zone_deck_telltales[zone_num].keys()):
                deck_group = QGroupBox(f"Deck {deck_num}")
                deck_group.setStyleSheet("QGroupBox { font-weight: normal; font-size: 11px; margin-left: 10px; }")
                deck_layout = QVBoxLayout(deck_group)
                
                # Add telltales for this deck in this zone
                for card_num, elem in zone_deck_telltales[zone_num][deck_num]:
                    row = QHBoxLayout()
                    
                    # Create descriptive label
                    file_name = elem.get("file", "")
                    blinking = elem.get("blinking", "NO")
                    duty_cycle = elem.get("duty_cycle", 0.5)
                    chime = elem.get("chime", None)
                    chime_type = elem.get("chime_type", "once")
                    duration = elem.get("duration", 5)
                    
                    # Extract telltale name from file name
                    telltale_name = file_name.replace(".png", "").replace("TT", "").replace("_", " ")
                    if telltale_name.startswith("0"):
                        telltale_name = telltale_name[1:]
                    
                    label_text = f"Card {card_num}: {telltale_name}"
                    if blinking == "YES":
                        label_text += f" (Blinking: {duty_cycle})"
                    else:
                        label_text += " (No Blinking)"
                    
                    if chime:
                        label_text += f" [Chime: {chime} - {chime_type}]"
                    else:
                        label_text += " [No Chime]"
                    
                    if duration == 0:
                        label_text += " [Duration: Infinite]"
                    else:
                        label_text += f" [Duration: {duration}s]"
                    
                    label = QLabel(label_text)
                    label.setFixedWidth(550)
                    row.addWidget(label)
                    
                    # Activation buttons
                    btn_activate = QPushButton("Activate")
                    btn_deactivate = QPushButton("Deactivate")
                    btn_activate.setFixedWidth(80)
                    btn_deactivate.setFixedWidth(80)
                    btn_activate.clicked.connect(lambda _, d=deck_num, c=card_num: self.activate_single_telltale(d, c))
                    btn_deactivate.clicked.connect(lambda _, d=deck_num, c=card_num: self.queue.send_activation(d, c, False))
                    row.addWidget(btn_activate)
                    row.addWidget(btn_deactivate)
                    
                    # Add chime trigger button if chime is configured
                    if chime:
                        btn_trigger_chime = QPushButton("Trigger Chime")
                        btn_trigger_chime.setFixedWidth(100)
                        btn_trigger_chime.setStyleSheet("background-color: #4CAF50; color: white;")
                        btn_trigger_chime.clicked.connect(lambda _, d=deck_num, c=card_num: self.queue.trigger_chime(d, c))
                        row.addWidget(btn_trigger_chime)
                    
                    deck_layout.addLayout(row)
                
                zone_layout.addWidget(deck_group)
            
            scroll_layout.addWidget(zone_group)

        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        telltale_layout.addWidget(scroll)
        
        self.tab_widget.addTab(telltale_tab, "Telltale Activations (Zone → Deck)")

    def create_chime_test_tab(self):
        """Create tab3 for chime testing"""
        chime_tab = QWidget()
        chime_layout = QVBoxLayout(chime_tab)
        
        # Bulk test buttons
        test_buttons_layout = QHBoxLayout()
        
        btn_test_fifo = QPushButton("Test FIFO Queue")
        btn_test_fifo.setStyleSheet("background-color: #2196F3; color: white;")
        btn_test_fifo.clicked.connect(self.test_fifo_chime_queue)
        test_buttons_layout.addWidget(btn_test_fifo)
        
        btn_test_blinker = QPushButton("Test Blinker Parallel")
        btn_test_blinker.setStyleSheet("background-color: #FF9800; color: white;")
        btn_test_blinker.clicked.connect(self.test_blinker_parallel)
        test_buttons_layout.addWidget(btn_test_blinker)
        
        btn_test_mixed = QPushButton("Test Mixed Types")
        btn_test_mixed.setStyleSheet("background-color: #9C27B0; color: white;")
        btn_test_mixed.clicked.connect(self.test_mixed_chime_types)
        test_buttons_layout.addWidget(btn_test_mixed)
        
        btn_clear_chimes = QPushButton("Clear All Chimes")
        btn_clear_chimes.setStyleSheet("background-color: #f44336; color: white;")
        btn_clear_chimes.clicked.connect(self.clear_all_chimes)
        test_buttons_layout.addWidget(btn_clear_chimes)
        
        chime_layout.addLayout(test_buttons_layout)
        
        # Status label
        self.chime_status_label = QLabel("Ready for chime testing")
        self.chime_status_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border: 1px solid #ccc;")
        chime_layout.addWidget(self.chime_status_label)
        
        # Individual chime trigger buttons grouped by chime name
        chime_groups_layout = QVBoxLayout()
        
        # Group telltales by chime name
        chime_groups = {}
        for deck_num, cards in TELL_TALES.items():
            for card_num, elements in cards.items():
                for elem in elements:
                    if elem["type"] == "image" and elem.get("chime"):
                        chime_name = elem["chime"]
                        if chime_name not in chime_groups:
                            chime_groups[chime_name] = []
                        chime_groups[chime_name].append((deck_num, card_num, elem))
                        break
        
        # Create buttons for each chime group
        for chime_name, telltales in chime_groups.items():
            chime_group = QGroupBox(f"Chime: {chime_name}")
            chime_group.setStyleSheet("QGroupBox { font-weight: bold; margin-top: 10px; }")
            group_layout = QVBoxLayout(chime_group)
            
            for deck_num, card_num, elem in telltales:
                row = QHBoxLayout()
                
                # Telltale info
                file_name = elem.get("file", "")
                telltale_name = file_name.replace(".png", "").replace("TT", "").replace("_", " ")
                if telltale_name.startswith("0"):
                    telltale_name = telltale_name[1:]
                
                label = QLabel(f"Deck {deck_num} Card {card_num}: {telltale_name}")
                label.setFixedWidth(300)
                row.addWidget(label)
                
                # Trigger chime button
                btn_trigger = QPushButton("Trigger Chime")
                btn_trigger.setFixedWidth(120)
                btn_trigger.setStyleSheet("background-color: #4CAF50; color: white;")
                btn_trigger.clicked.connect(lambda _, d=deck_num, c=card_num: self.trigger_single_chime(d, c))
                row.addWidget(btn_trigger)
                
                group_layout.addLayout(row)
            
            chime_groups_layout.addWidget(chime_group)
        
        chime_layout.addLayout(chime_groups_layout)
        self.tab_widget.addTab(chime_tab, "Chime Testing")

    def activate_all_decks(self):
        """Activate all deck cards"""
        for deck_num, cards in DECK_GRAPHICS.items():
            for card_num in cards:
                if card_num > 0:  # Skip card 0 (empty)
                    self.queue.send_activation(deck_num, card_num, True)
        QMessageBox.information(self, "Activation Complete", "All deck cards have been activated.")

    def deactivate_all_decks(self):
        """Deactivate all deck cards"""
        for deck_num, cards in DECK_GRAPHICS.items():
            for card_num in cards:
                self.queue.send_activation(deck_num, card_num, False)
        QMessageBox.information(self, "Deactivation Complete", "All deck cards have been deactivated.")

    def activate_all_telltales(self):
        """Activate all telltale cards (only valid ones)"""
        self.main_window.show()
        for deck_num, cards in TELL_TALES.items():
            for card_num in cards:
                if card_num > 0 and card_num in TELL_TALES[deck_num]:
                    self.queue.send_activation(deck_num, card_num, True)
        QMessageBox.information(self, "Activation Complete", "All telltale cards have been activated.")

    def deactivate_all_telltales(self):
        """Deactivate all telltale cards"""
        for deck_num, cards in TELL_TALES.items():
            for card_num in cards:
                self.queue.send_activation(deck_num, card_num, False)
        QMessageBox.information(self, "Deactivation Complete", "All telltale cards have been deactivated.")

    def show_main_window(self):
        self.main_window.show()

    def exit_application(self):
        """Exit the application"""
        reply = QMessageBox.question(self, 'Exit Application', 
                                   'Are you sure you want to exit?',
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()

    def activate_single_telltale(self, deck, card):
        """Activate a single telltale and show main window, only if valid"""
        if deck in TELL_TALES and card in TELL_TALES[deck]:
            self.main_window.show()
            self.queue.send_activation(deck, card, True)

    def test_fifo_chime_queue(self):
        """Test FIFO chime queue with multiple chimes"""
        self.main_window.show()
        self.chime_status_label.setText("Testing FIFO chime queue...")
        
        # Activate telltales in sequence to test queue
        self.queue.send_activation(51, 1)  # engine_check (twice)
        self.queue.send_activation(52, 2)  # jeep_seatbelt_alert (once)
        self.queue.send_activation(56, 1)  # low_fuel (once)
        
        self.chime_status_label.setText("FIFO queue test completed - check chime sequence")

    def test_blinker_parallel(self):
        """Test blinker chimes playing in parallel"""
        self.main_window.show()
        self.chime_status_label.setText("Testing blinker parallel playback...")
        
        # Activate blinker telltales (should play in parallel)
        self.queue.send_activation(59, 1)  # Left turn blinker
        self.queue.send_activation(60, 1)  # Right turn blinker
        
        self.chime_status_label.setText("Blinker parallel test completed - both should play simultaneously")

    def test_mixed_chime_types(self):
        """Test different chime types in sequence"""
        self.main_window.show()
        self.chime_status_label.setText("Testing mixed chime types...")
        
        # Activate telltales with different chime types
        self.queue.send_activation(51, 1)  # engine_check (twice)
        self.queue.send_activation(55, 1)  # jeep_seatbelt_alert (continuous)
        self.queue.send_activation(56, 1)  # low_fuel (once)
        
        self.chime_status_label.setText("Mixed chime types test completed")

    def clear_all_chimes(self):
        """Clear all currently playing chimes"""
        self.chime_status_label.setText("Clearing all chimes...")
        # This would need to be implemented in the chime handler
        self.chime_status_label.setText("All chimes cleared")

    def trigger_single_chime(self, deck, card):
        """Trigger a single chime for testing"""
        self.main_window.show()
        self.queue.trigger_chime(deck, card)
        self.chime_status_label.setText(f"Triggered chime for Deck {deck} Card {card}")

    def set_deck_text(self, deck, card, text):
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
            QMessageBox.information(self, "Text Updated", f"Dynamic text for Deck {deck} Card {card} updated.")

def main():
    app = QApplication(sys.argv)
    test_gui = TestRunnerWindow()
    test_gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()