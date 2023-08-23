
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from functions.log import initialise_log

class GuiImage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Layout for image
        image_layout = QVBoxLayout()
        image_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_widget = QWidget()
        image_widget.setLayout(image_layout)
        image_widget.setStyleSheet("background-color: #0b0c12;")
        image_layout.setContentsMargins(0, 0, 0, 0)  
        image_layout.setSpacing(0) 
        image_widget.setFixedSize(800, 800) 
        main_layout.addWidget(image_widget)

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
        
        # Image 
        self.image = QLabel(parent)
        self.image.setMinimumSize(800, 800)
        self.image.setStyleSheet("background-color: #0b0c12;")
        image_layout.addWidget(self.image)
        
        # Log
        self.log = QLabel("", parent)
        self.log.setStyleSheet("color: #c8d8de;")
        initialise_log(self.log)
        self.log.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.log.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.log_scroll_area.setWidget(self.log)
