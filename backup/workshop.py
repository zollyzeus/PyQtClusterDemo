import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt

class BgImageWidget(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.bg_pixmap = QPixmap(image_path)
        self.setWindowTitle("Qt Demo")
        self.resize(1920, 720)

    def paintEvent(self, event):
        painter = QPainter(self)
        # Draw the background image scaled to widget size
        painter.drawPixmap(self.rect(), self.bg_pixmap)

def show_overlays_as_single_window_on_second_screen(image_paths):
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    screens = app.screens()
    if len(screens) > 1:
        screen = screens[1]
        geometry = screen.geometry()
        class MultiOverlayWidget(QWidget):
            def __init__(self, image_paths):
                super().__init__()
                self.pixmaps = [QPixmap(path) for path in image_paths]
                self.setWindowTitle("Multi Overlay Window")
                self.setGeometry(geometry.x(), geometry.y(), geometry.width(), geometry.height())
                self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
                self.setAttribute(Qt.WA_TranslucentBackground)

            def paintEvent(self, event):
                painter = QPainter(self)
                for pixmap in self.pixmaps:
                    # Draw each overlay image centered and scaled to window size
                    painter.drawPixmap(self.rect(), pixmap)
        overlay_window = MultiOverlayWidget(image_paths)
        overlay_window.show()
        return overlay_window
    else:
        print("Second screen not detected.")
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    image_dir = os.path.join(os.path.dirname(__file__), "Images")
    bg_image_path = os.path.join(image_dir, "background.png")
    overlay_image_paths = [
        os.path.join(image_dir, "road surface.png"),
        os.path.join(image_dir, "Vector 2.png"),
        os.path.join(image_dir, "Vector 3.png"),
        os.path.join(image_dir, "Vector 4.png"),
        os.path.join(image_dir, "Vector 5.png")
    ]

    window = BgImageWidget(bg_image_path)
    window.show()

    # Show all overlay images together as a single window on second screen
    show_overlays_as_single_window_on_second_screen(overlay_image_paths)

    sys.exit(app.exec_())