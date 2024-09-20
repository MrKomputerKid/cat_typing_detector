import sys
import time
import os
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from pynput import keyboard
from sklearn.linear_model import LogisticRegression
from collections import deque
import logging
import threading
from pystray import Icon as TrayIcon, MenuItem as Item
from PIL import Image, ImageDraw

# Set up logging
logging.basicConfig(filename='cat_typing_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# Train a simple logistic regression model (placeholder data)
def train_model():
    X_train = np.array([[0.1, 10], [0.2, 2], [0.05, 12], [0.3, 3]])
    y_train = np.array([1, 0, 1, 0])  # 1 = cat-like, 0 = human-like
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

model = train_model()

# Track key press patterns
cat_typing_threshold = 0.1  # seconds between keys
key_times = deque(maxlen=10)

def detect_cat_typing():
    if len(key_times) >= 10:
        avg_time_between_keys = np.mean(np.diff(key_times))
        key_count = len(key_times)
        features = np.array([[avg_time_between_keys, key_count]])
        prediction = model.predict(features)[0]
        return prediction == 1
    return False

class CatTypingWindow(QWidget):
    def __init__(self, timeout=5000):
        super().__init__()
        self.timeout = timeout
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout_reached)

    def initUI(self):
        self.setWindowTitle('Cat Typing Detected')
        self.setGeometry(300, 300, 400, 200)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: #f0f0f0; font-size: 16px;")

        self.label = QLabel('Cat is typing! Enter "human" or click the button to dismiss.', self)
        self.input = QLineEdit(self)
        self.input.setFocus()
        self.input.returnPressed.connect(self.check_input)

        self.button = QPushButton('Let me use my computer!', self)
        self.button.clicked.connect(self.close_window)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.start_timer()

    def start_timer(self):
        self.timer.start(self.timeout)

    def check_input(self):
        if self.input.text().lower() == "human":
            self.close_window()

    def close_window(self):
        self.timer.stop()
        self.hide()  # Hide the window instead of closing

    def timeout_reached(self):
        self.close_window()

class TrayApplication:
    def __init__(self):
        self.icon = self.create_icon()
        self.tray_icon = TrayIcon("Cat Typing Detector", self.icon, menu=self.create_menu())
        self.listener_thread = None
        self.is_running = False

    def create_icon(self):
        # Create a simple tray icon image
        icon_image = Image.new('RGB', (64, 64), color = (255, 255, 255))
        draw = ImageDraw.Draw(icon_image)
        draw.text((10, 25), "🐾", fill=(0, 0, 0))  # Simple paw emoji as tray icon
        return icon_image

    def create_menu(self):
        # Create the menu for the tray icon
        return (
            Item('Start Detector', self.start_detector),
            Item('Stop Detector', self.stop_detector),
            Item('Exit', self.exit_app)
        )

    def start_detector(self, icon=None, item=None):
        if not self.is_running:
            self.listener_thread = threading.Thread(target=self.run_listener, daemon=True)
            self.listener_thread.start()
            self.is_running = True

    def stop_detector(self, icon=None, item=None):
        self.is_running = False
        print("Cat Typing Detection Stopped")

    def exit_app(self, icon=None, item=None):
        if self.is_running:
            self.stop_detector()
        self.tray_icon.stop()
        sys.exit()

    def run_listener(self):
        def on_press(key):
            global key_times
            key_times.append(time.time())

            if detect_cat_typing():
                print("Cat detected! Redirecting...")
                app = QApplication.instance()  # Use existing app if it exists
                if app is None:
                    app = QApplication(sys.argv)
                window = CatTypingWindow()
                window.show()
                app.exec_()

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def run(self):
        self.tray_icon.run()

def run_tray_app():
    tray_app = TrayApplication()
    tray_app.run()

if __name__ == "__main__":
    run_tray_app()
