from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QDialogButtonBox, QProgressBar, QSlider, \
    QDial, QPushButton
from PySide6.QtGui import QPainter, QPixmap, QBitmap
from PySide6.QtCore import Qt


class CustomDial(QDial):
    def __init__(self, parent=None, image_path=""):
        super().__init__(parent)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)
        self.loadAndPrepareImage(image_path)

    def loadAndPrepareImage(self, image_path):
        pixmap_size = 170
        original_pixmap = QPixmap(image_path)
        if original_pixmap.width() != original_pixmap.height():
            scaled_pixmap = original_pixmap.scaled(pixmap_size, pixmap_size, Qt.KeepAspectRatioByExpanding,
                                                   Qt.SmoothTransformation)
            x0 = (scaled_pixmap.width() - pixmap_size) // 2
            y0 = (scaled_pixmap.height() - pixmap_size) // 2
            original_pixmap = scaled_pixmap.copy(x0, y0, pixmap_size, pixmap_size)
        else:
            original_pixmap = original_pixmap.scaled(pixmap_size, pixmap_size, Qt.IgnoreAspectRatio,
                                                     Qt.SmoothTransformation)

        mask = QBitmap(pixmap_size, pixmap_size)
        mask.fill(Qt.color0)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.color1)
        painter.drawEllipse(0, 0, pixmap_size, pixmap_size)
        painter.end()

        original_pixmap.setMask(mask)
        self.pixmap = original_pixmap
        self.setFixedSize(200, 200)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        angle = 360 * self.value() / (self.maximum() - self.minimum())
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(angle)
        painter.translate(-self.width() / 2, -self.height() / 2)
        painter.drawPixmap((self.width() - self.pixmap.width()) / 2, (self.height() - self.pixmap.height()) / 2,
                           self.pixmap)


class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # Add this line to make window decorations invisible
        self.leftEyeImage = "C:/Users/Frogs/Downloads/Example.jpg"
        self.rightEyeImage = "C:/Users/Frogs/Downloads/Example2.jpg"
        self.currentImage = self.leftEyeImage

        self.dial = CustomDial(self, self.currentImage)
        self.initUI()

    def initUI(self):
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.setFixedWidth(240)

        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.progressBar.setFixedWidth(275)

        self.slider.valueChanged.connect(self.dial.setValue)
        self.dial.valueChanged.connect(self.progressBar.setValue)
        self.dial.valueChanged.connect(self.slider.setValue)

        self.buttonBox = QVBoxLayout()
        self.leftEyeButton = QPushButton("Left Eye")
        self.rightEyeButton = QPushButton("Right Eye")
        self.exitButton = QPushButton("Exit")
        self.buttonBox.addWidget(self.leftEyeButton)
        self.buttonBox.addWidget(self.rightEyeButton)
        self.buttonBox.addWidget(self.exitButton)
        self.buttonBox.addStretch()

        self.leftEyeButton.clicked.connect(self.showLeftEye)
        self.rightEyeButton.clicked.connect(self.showRightEye)
        self.exitButton.clicked.connect(self.close)

        self.showLeftEye()

        mainLayout = QHBoxLayout()
        controlsLayout = QVBoxLayout()
        controlsLayout.addWidget(self.dial)
        controlsLayout.addWidget(self.slider)
        controlsLayout.addWidget(self.progressBar)
        mainLayout.addLayout(controlsLayout)
        mainLayout.addLayout(self.buttonBox)

        self.setLayout(mainLayout)
        self.setFixedSize(480, 288)

    def showLeftEye(self):
        self.currentImage = self.leftEyeImage
        self.dial.loadAndPrepareImage(self.currentImage)
        self.dial.update()  # Force the dial to repaint with the new image
        self.leftEyeButton.setStyleSheet("background-color: #555555;")  # Indicate active selection
        self.rightEyeButton.setStyleSheet("")  # Reset to default style
        self.leftEyeButton.setDisabled(True)
        self.rightEyeButton.setEnabled(True)

    def showRightEye(self):
        self.currentImage = self.rightEyeImage
        self.dial.loadAndPrepareImage(self.currentImage)
        self.dial.update()  # Force the dial to repaint with the new image
        self.rightEyeButton.setStyleSheet("background-color: #555555;")  # Indicate active selection
        self.leftEyeButton.setStyleSheet("")  # Reset to default style
        self.rightEyeButton.setDisabled(True)
        self.leftEyeButton.setEnabled(True)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    # Apply dark theme style sheet
    app.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                color: #cccccc; /* General text color */
            }
            QDialog {
                background-color: #2d2d2d;
            }
            QPushButton {
                background-color: #30BD82;
                border: 1px solid #555;
                border-radius: 2px;
                padding: 5px;
                min-height: 18px;
                color: #ffffff; /* White text */
            }
            QPushButton:pressed {
                background-color: #555555;
            }
            QPushButton:disabled {
                background-color: #333333;
                border-color: #444444;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #3a3a3a;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: #bcbcbc;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }

        """)

    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec())
