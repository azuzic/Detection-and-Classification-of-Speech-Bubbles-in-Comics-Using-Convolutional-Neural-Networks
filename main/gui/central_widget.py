from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QFileDialog
from gui.gui_image import GuiImage
from gui.buttons.open_image_button import OpenImageButton
from gui.buttons.convert_to_bw_button import ConvertToBWButton
from gui.buttons.enchance_image_button import EnchanceImageButton
from gui.buttons.find_speech_bubbles_button import FindSpeechBubblesButton
from PyQt5.QtCore import Qt
from functions.speech_bubble_extraction import setLang
from functions.test import classify_image

class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)

        self.message_label = QLabel("Detection and Classification of Speech Bubbles in Comics Using Convolutional Neural Networks", self)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align text
        layout.addWidget(self.message_label, alignment=Qt.AlignmentFlag.AlignTop)

        # Language dropdown
        self.language_combo_box = QComboBox(self)
        self.language_combo_box.addItems(["English", "Japanese", "French"])
        self.language_combo_box.currentIndexChanged.connect(self.language_selected)
        layout.addWidget(self.language_combo_box, alignment=Qt.AlignmentFlag.AlignTop)

        # Set image/info layout 
        self.labels_layout = GuiImage(self)
        layout.addWidget(self.labels_layout)

        # Buttons
        buttons_layout = QHBoxLayout()

        self.open_image_button = OpenImageButton(self, self.labels_layout.image)
        #self.convert_to_bw_button = ConvertToBWButton(self, self.labels_layout.image)
        #self.enchance_image_button = EnchanceImageButton(self, self.labels_layout.image)
        self.find_speech_bubbles_button = FindSpeechBubblesButton(self, self.labels_layout.image)

        buttons_layout.addWidget(self.open_image_button)
        #buttons_layout.addWidget(self.convert_to_bw_button)
        #buttons_layout.addWidget(self.enchance_image_button)
        buttons_layout.addWidget(self.find_speech_bubbles_button)

        self.open_image_file_button = QPushButton("Open Image File", self)
        self.open_image_file_button.clicked.connect(self.open_image_dialog)
        buttons_layout.addWidget(self.open_image_file_button)

        # Add the buttons layout to the main layout
        layout.addLayout(buttons_layout)

    def language_selected(self, index):
        selected_language = self.language_combo_box.currentText()
        if (selected_language == "English"):
            setLang("en")
        if (selected_language == "Japanese"):
            setLang("ja")
        if (selected_language == "French"):
            setLang("fr")

    def open_image_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog(self)
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        file_dialog.setViewMode(QFileDialog.List)
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                image_path = selected_files[0]
                classify_image(image_path)  # Call your image classification function
