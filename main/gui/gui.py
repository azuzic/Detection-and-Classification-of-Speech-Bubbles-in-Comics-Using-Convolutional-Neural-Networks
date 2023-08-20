import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from gui_colors import set_dark_palette, set_fusion_style

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Detection and Classification of Speech Bubbles in Comics Using Convolutional Neural Networks")
        set_dark_palette(self)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.message_label = QLabel("Welcome to the Dark GUI!", self)
        layout.addWidget(self.message_label, alignment=Qt.AlignmentFlag.AlignCenter)


        self.button = QPushButton("Click Me", self)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.button.clicked.connect(self.display_message)

    def display_message(self):
        self.message_label.setText("Hello, Dark World!")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    set_fusion_style(app)

    dark_window = MainWindow()
    dark_window.resize(500, 500)
    dark_window.show()

    sys.exit(app.exec_())