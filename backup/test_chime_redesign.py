#!/usr/bin/env python3
"""
Test script for the redesigned chime system
Demonstrates the new queue-based architecture and special blinker handling
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QLabel
from PyQt5.QtCore import QTimer
from workshop4 import MainWindow, logger

class ChimeTestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chime System Test")
        self.setFixedSize(400, 500)
        
        # Create main dashboard window
        self.dashboard = MainWindow()
        
        # Create test UI
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Chime System Redesign Test")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Test buttons
        btn1 = QPushButton("Test 1: FIFO Queue (3 chimes)")
        btn1.clicked.connect(self.test_fifo_queue)
        layout.addWidget(btn1)
        
        btn2 = QPushButton("Test 2: Blinker Parallel Playback")
        btn2.clicked.connect(self.test_blinker_parallel)
        layout.addWidget(btn2)
        
        btn3 = QPushButton("Test 3: Mixed Chime Types")
        btn3.clicked.connect(self.test_mixed_types)
        layout.addWidget(btn3)
        
        btn4 = QPushButton("Test 4: Blinker + Queue Chimes")
        btn4.clicked.connect(self.test_blinker_with_queue)
        layout.addWidget(btn4)
        
        btn5 = QPushButton("Clear All Telltales")
        btn5.clicked.connect(self.clear_all)
        layout.addWidget(btn5)
        
        # Status label
        self.status_label = QLabel("Ready to test chime system")
        self.status_label.setStyleSheet("margin: 10px; padding: 10px; background-color: #f0f0f0;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def test_fifo_queue(self):
        """Test FIFO queue with 3 chimes"""
        self.status_label.setText("Testing FIFO queue with 3 chimes...")
        
        # Clear any existing telltales
        self.clear_all()
        
        # Activate telltales in sequence
        QTimer.singleShot(500, lambda: self.dashboard.activate_telltale(51, 1))  # engine_check (twice)
        QTimer.singleShot(1000, lambda: self.dashboard.activate_telltale(56, 1))  # low_fuel (once)
        QTimer.singleShot(1500, lambda: self.dashboard.activate_telltale(52, 2))  # jeep_seatbelt_alert (once)
        
        logger.info("Test 1: FIFO queue test initiated")
    
    def test_blinker_parallel(self):
        """Test blinker chimes playing in parallel"""
        self.status_label.setText("Testing blinker parallel playback...")
        
        # Clear any existing telltales
        self.clear_all()
        
        # Activate both blinker telltales
        QTimer.singleShot(500, lambda: self.dashboard.activate_telltale(59, 1))  # Left turn
        QTimer.singleShot(1000, lambda: self.dashboard.activate_telltale(60, 1))  # Right turn
        
        logger.info("Test 2: Blinker parallel test initiated")
    
    def test_mixed_types(self):
        """Test different chime types"""
        self.status_label.setText("Testing mixed chime types...")
        
        # Clear any existing telltales
        self.clear_all()
        
        # Activate telltales with different chime types
        QTimer.singleShot(500, lambda: self.dashboard.activate_telltale(51, 1))  # twice
        QTimer.singleShot(1000, lambda: self.dashboard.activate_telltale(55, 1))  # continuous
        QTimer.singleShot(1500, lambda: self.dashboard.activate_telltale(56, 1))  # once
        
        logger.info("Test 3: Mixed chime types test initiated")
    
    def test_blinker_with_queue(self):
        """Test blinker playing alongside queue chimes"""
        self.status_label.setText("Testing blinker with queue chimes...")
        
        # Clear any existing telltales
        self.clear_all()
        
        # Activate queue chimes first
        QTimer.singleShot(500, lambda: self.dashboard.activate_telltale(51, 1))  # engine_check
        QTimer.singleShot(1000, lambda: self.dashboard.activate_telltale(56, 1))  # low_fuel
        
        # Activate blinker in the middle (should play immediately)
        QTimer.singleShot(2000, lambda: self.dashboard.activate_telltale(59, 1))  # blinker
        
        # Add another queue chime
        QTimer.singleShot(2500, lambda: self.dashboard.activate_telltale(52, 2))  # jeep_seatbelt_alert
        
        logger.info("Test 4: Blinker with queue test initiated")
    
    def clear_all(self):
        """Clear all active telltales"""
        self.status_label.setText("Clearing all telltales...")
        
        # Deactivate all telltales
        for deck_num in range(50, 62):
            for card_num in range(1, 5):  # Assuming max 4 cards per deck
                self.dashboard.deactivate_telltale(deck_num, card_num)
        
        logger.info("All telltales cleared")

def main():
    app = QApplication(sys.argv)
    
    # Create test window
    test_window = ChimeTestWindow()
    test_window.show()
    
    # Create dashboard window (hidden initially)
    dashboard = test_window.dashboard
    dashboard.show()
    
    print("Chime System Redesign Test")
    print("==========================")
    print("1. Use the test buttons to trigger different chime scenarios")
    print("2. Watch the console for detailed logging")
    print("3. Listen for the chime playback behavior")
    print("4. Check the logs/ directory for detailed chime event logs")
    print()
    print("Key Features to Test:")
    print("- FIFO queue processing for regular chimes")
    print("- Parallel playback for blinker chimes")
    print("- Different chime types (once, twice, continuous)")
    print("- Queue management and timing")
    
    return app.exec_()

if __name__ == "__main__":
    main() 