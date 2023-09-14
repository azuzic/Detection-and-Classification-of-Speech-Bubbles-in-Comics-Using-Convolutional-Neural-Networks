from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QScrollArea, QVBoxLayout, QHBoxLayout, QFrame, QTextBrowser 

from functions.log import initialiseLog
from functions.speech_bubble_extraction import initialiseImageLayout

class GuiImage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create the container frame
        container_frame = QFrame()
        container_frame.setFixedSize(800, 800)
        container_frame.setStyleSheet("background-color: #0b0c12;")
        main_layout.addWidget(container_frame)

        # Create a stacked layout for the container frame
        self.container_layout = QHBoxLayout(container_frame)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.container_layout.setContentsMargins(0, 0, 0, 0)

        # Main Image
        self.image = QLabel()
        self.image.setMinimumSize(800, 800)
        self.image.setStyleSheet("background-color: #0b0c12;")
        self.container_layout.addWidget(self.image)

        # Layout for log
        log_layout = QVBoxLayout()
        log_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        log_widget = QWidget()
        log_widget.setFixedSize(800, 800)
        log_widget.setLayout(log_layout)
        log_widget.setStyleSheet("background-color: #0b0c12;")
        main_layout.addWidget(log_widget)

        # Log Scroll Area
        self.log_scroll_area = QScrollArea()
        self.log_scroll_area.setStyleSheet("background-color: #0b0c12;")
        self.log_scroll_area.setWidgetResizable(True)
        log_layout.addWidget(self.log_scroll_area)
        
        # Log
        self.log = QTextBrowser(parent)
        self.log.setStyleSheet("color: #c8d8de;")
        initialiseLog(self)
        self.log.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.log.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.log_scroll_area.setWidget(self.log)

        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 800, 800)

        initialiseImageLayout(self)