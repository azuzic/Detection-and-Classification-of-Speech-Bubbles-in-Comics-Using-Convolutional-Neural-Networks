from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout
from gui.gui_image import GuiImage
from gui.buttons.open_image_button import OpenImageButton
from gui.buttons.convert_to_bw_button import ConvertToBWButton
from gui.buttons.enchance_image_button import EnchanceImageButton
from gui.buttons.find_speech_bubbles_button import FindSpeechBubblesButton
from PyQt5.QtCore import Qt

class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)

        self.message_label = QLabel("Detection and Classification of Speech Bubbles in Comics Using Convolutional Neural Networks", self)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align text
        layout.addWidget(self.message_label, alignment=Qt.AlignmentFlag.AlignTop)

        # Set image/info layout 
        self.labels_layout = GuiImage(self)
        layout.addWidget(self.labels_layout)

        # Buttons
        buttons_layout = QHBoxLayout()

        self.open_image_button = OpenImageButton(self, self.labels_layout.image_label, self.labels_layout.image_info_label)
        self.convert_to_bw_button = ConvertToBWButton(self, self.labels_layout.image_label, self.labels_layout.image_info_label)
        self.enchance_image_button = EnchanceImageButton(self, self.labels_layout.image_label, self.labels_layout.image_info_label)
        self.find_speech_bubbles_button = FindSpeechBubblesButton(self, self.labels_layout.image_label, self.labels_layout.image_info_label)

        buttons_layout.addWidget(self.open_image_button)
        buttons_layout.addWidget(self.convert_to_bw_button)
        buttons_layout.addWidget(self.enchance_image_button)
        buttons_layout.addWidget(self.find_speech_bubbles_button)

        # Add the buttons layout to the main layout
        layout.addLayout(buttons_layout)
