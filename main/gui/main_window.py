from PyQt5.QtWidgets import QMainWindow
from gui.central_widget import CentralWidget
from gui.gui_colors import set_dark_palette

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Title and theme
        self.setWindowTitle("Detection and Classification of Speech Bubbles in Comics Using Convolutional Neural Networks")
        set_dark_palette(self)

        central_widget = CentralWidget()
        self.setCentralWidget(central_widget)