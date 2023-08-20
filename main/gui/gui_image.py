from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt

class GuiImage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Image label
        self.image_label = QLabel(parent)
        self.image_label.setMinimumSize(400, 400)
        self.image_label.setStyleSheet("background-color: lightgray; border: 1px solid gray;")
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Image info label
        self.image_info_label = QLabel("Image Information Here", parent)
        layout.addWidget(self.image_info_label, alignment=Qt.AlignmentFlag.AlignCenter)
