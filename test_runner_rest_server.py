import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import queue
from workshop3_1 import MainWindow, MessageQueue, DECK_GRAPHICS, TELL_TALES

# Thread-safe queue for REST commands
task_queue = queue.Queue()

# FastAPI app
def create_api(main_window):
    app = FastAPI()
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    @app.post("/api/control")
    async def control(request: Request):
        data = await request.json()
        task_queue.put(data)
        return {"status": "received"}

    return app

class ServerThread(threading.Thread):
    def __init__(self, app, host, port):
        super().__init__()
        self.app = app
        self.host = host
        self.port = port
        self.daemon = True

    def run(self):
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="info")

class TestRunnerServer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Runner REST Server")
        self.setGeometry(100, 100, 500, 300)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.ip_input = QLineEdit("127.0.0.1")
        self.port_input = QLineEdit("8000")
        self.start_btn = QPushButton("Start Server")
        self.stop_btn = QPushButton("Stop Server")
        self.stop_btn.setEnabled(False)
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.activate_main_btn = QPushButton("Activate Main Window")
        self.layout.addWidget(self.activate_main_btn)
        self.activate_main_btn.clicked.connect(self.activate_main_window)

        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("IP:"))
        ip_layout.addWidget(self.ip_input)
        ip_layout.addWidget(QLabel("Port:"))
        ip_layout.addWidget(self.port_input)
        self.layout.addLayout(ip_layout)
        self.layout.addWidget(self.start_btn)
        self.layout.addWidget(self.stop_btn)
        self.layout.addWidget(QLabel("Log:"))
        self.layout.addWidget(self.log_box)

        self.start_btn.clicked.connect(self.start_server)
        self.stop_btn.clicked.connect(self.stop_server)

        self.server_thread = None
        self.api = None
        self.main_window = MainWindow()
        self.queue = MessageQueue(self.main_window)
        self.running = False
        self.timer = self.startTimer(100)  # 100 ms polling

    def start_server(self):
        host = self.ip_input.text()
        port = int(self.port_input.text())
        self.api = create_api(self.main_window)
        self.server_thread = ServerThread(self.api, host, port)
        self.server_thread.start()
        self.log_box.append(f"Server started at http://{host}:{port}")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.running = True

    def stop_server(self):
        # Uvicorn does not support programmatic shutdown easily; recommend closing app to stop server
        self.log_box.append("Stopping server: Please close the application to fully stop the server.")
        self.running = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def activate_main_window(self):
        self.main_window.show()
        self.main_window.raise_()

    def timerEvent(self, event):
        # Poll the queue for REST commands
        while not task_queue.empty():
            data = task_queue.get()
            self.handle_command(data)

    def handle_command(self, data):
        try:
            typ = data.get("type")
            deck = data.get("deck_num")
            card = data.get("card_num")
            action = data.get("action")
            value = data.get("value")
            if typ == "bulk":
                if action == "activate_all_decks":
                    self.activate_all_decks()
                    self.log_box.append("Bulk: Activated all decks via REST.")
                elif action == "deactivate_all_decks":
                    self.deactivate_all_decks()
                    self.log_box.append("Bulk: Deactivated all decks via REST.")
                elif action == "activate_all_telltales":
                    self.activate_all_telltales()
                    self.log_box.append("Bulk: Activated all telltales via REST.")
                elif action == "deactivate_all_telltales":
                    self.deactivate_all_telltales()
                    self.log_box.append("Bulk: Deactivated all telltales via REST.")
                elif action == "activate_main_window":
                    self.activate_main_window()
                    self.log_box.append("Bulk: Activated main window via REST.")
                else:
                    self.log_box.append(f"Unknown bulk action: {action}")
            elif typ in ("deck", "card", "telltale"):
                activation_status = action == "activate"
                self.queue.send_activation(deck, card, activation_status)
                self.log_box.append(f"send_activation({deck}, {card}, {activation_status})")
            elif typ == "dynamic_text":
                self.queue.send_dynamic_text(deck, card, value)
                self.log_box.append(f"send_dynamic_text({deck}, {card}, {value})")
            elif typ == "progress_bar":
                self.queue.send_progress_bar(deck, card, value)
                self.log_box.append(f"send_progress_bar({deck}, {card}, {value})")
            self.log_box.append(f"Handled: {data}")
        except Exception as e:
            self.log_box.append(f"Error handling command: {e}")

    def activate_all_decks(self):
        for deck_num, cards in DECK_GRAPHICS.items():
            for card_num in cards:
                if card_num > 0:
                    self.queue.send_activation(deck_num, card_num, True)
        self.log_box.append("All deck cards activated.")

    def deactivate_all_decks(self):
        for deck_num, cards in DECK_GRAPHICS.items():
            for card_num in cards:
                self.queue.send_activation(deck_num, card_num, False)
        self.log_box.append("All deck cards deactivated.")

    def activate_all_telltales(self):
        self.main_window.show()
        for deck_num, cards in TELL_TALES.items():
            for card_num in cards:
                if card_num > 0 and card_num in TELL_TALES[deck_num]:
                    self.queue.send_activation(deck_num, card_num, True)
        self.log_box.append("All telltale cards activated.")

    def deactivate_all_telltales(self):
        for deck_num, cards in TELL_TALES.items():
            for card_num in cards:
                self.queue.send_activation(deck_num, card_num, False)
        self.log_box.append("All telltale cards deactivated.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    server = TestRunnerServer()
    server.show()
    sys.exit(app.exec_())