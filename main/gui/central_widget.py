from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QTabWidget, QSizePolicy, QScrollArea
from gui.gui_image import GuiImage
from gui.buttons.open_image_button import OpenImageButton
from gui.buttons.convert_to_bw_button import ConvertToBWButton
from gui.buttons.find_speech_bubbles_button import FindSpeechBubblesButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from functions.speech_bubble_extraction import setLang
from functions.speech_bubble_classifier import classify_images, set_model
from PyQt5.QtCore import QTimer
import os

class ImageWidget(QLabel):
    def set_image(self, image_path):
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio)
        self.setPixmap(pixmap)

class ImageContainer(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        self.setLayout(layout)

    def addImage(self, image_path):
        image_label = ImageWidget()
        image_label.set_image(image_path)
        self.layout().addWidget(image_label)

    def clearLayout(self):
        while self.layout().count():
            item = self.layout().takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a tab widget
        self.tab_widget = QTabWidget(self)

        # Create tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        layout = QVBoxLayout(self.tab1)
        
        # Add tabs to the tab widget
        self.tab_widget.addTab(self.tab1, "Main")
        self.tab_widget.addTab(self.tab2, "Extracted Bubbles")

        self.message_label = QLabel("Detection and Classification of Speech Bubbles in Comics Using Convolutional Neural Networks", self)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align text
        layout.addWidget(self.message_label, alignment=Qt.AlignmentFlag.AlignTop)

        # Dropdowns and Labels
        dropdown_layout = QHBoxLayout()

        # Language Label and dropdown
        language_layout = QHBoxLayout()
        language_label = QLabel("Select Language:")
        self.language_combo_box = QComboBox(self)
        self.language_combo_box.addItems(["English", "Japanese", "French"])
        self.language_combo_box.currentIndexChanged.connect(self.language_selected)
        language_layout.addWidget(language_label, alignment=Qt.AlignmentFlag.AlignCenter)
        language_layout.addWidget(self.language_combo_box, alignment=Qt.AlignmentFlag.AlignTop)

        # Model Label and dropdown
        model_layout = QHBoxLayout()
        model_label = QLabel("Select Model:")
        self.model_combo_box = QComboBox(self)
        self.load_models()
        self.model_combo_box.currentIndexChanged.connect(self.model_selected)
        model_layout.addWidget(model_label, alignment=Qt.AlignmentFlag.AlignCenter)
        model_layout.addWidget(self.model_combo_box, alignment=Qt.AlignmentFlag.AlignTop)

        # Set stretch factors
        language_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.language_combo_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        model_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.model_combo_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        dropdown_layout.addLayout(language_layout)
        dropdown_layout.addLayout(model_layout)

        layout.addLayout(dropdown_layout)

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

        #self.open_image_file_button = QPushButton("classify bubbles", self)
        #self.open_image_file_button.clicked.connect(self.classify_bubbles)
        #buttons_layout.addWidget(self.open_image_file_button)

        # Add the buttons layout to the main layout
        layout.addLayout(buttons_layout)

        # Set up a timer to check for changes every 5 seconds (5000 milliseconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_tab2)
        self.timer.start(5000)  # Set the timer interval in milliseconds (5000 ms = 5 seconds)

        # Create an instance of ImageContainer for Tab 2
        self.image_container = ImageContainer()
        layout = QVBoxLayout(self.tab2)

        # Create a horizontal scroll area
        scroll_area = QScrollArea(self.tab2)
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)

        layout.addWidget(scroll_area)
        content_layout.addWidget(self.image_container)

        # Initialize images in Tab 2
        self.update_tab2()

    def update_tab2(self):
        # Clear the current content of Tab 2
        self.image_container.clearLayout()
        # Load and display images from a folder
        folder_path = "output/extracted_bubbles"
        for filename in os.listdir(folder_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(folder_path, filename)
                self.image_container.addImage(image_path)

    def load_models(self): 
        models_folder = "models/trained_models"
        model_files = os.listdir(models_folder)
        model_files = [file for file in model_files]
        model_names = [os.path.splitext(file)[0] for file in model_files]
        self.model_combo_box.addItems(model_names)

    def language_selected(self, index):
        selected_language = self.language_combo_box.currentText()
        if (selected_language == "English"):
            setLang("en")
        if (selected_language == "Japanese"):
            setLang("ja")
        if (selected_language == "French"):
            setLang("fr")

    def model_selected(self, index):
        set_model(index)

    def classify_bubbles(self):
        classify_images()