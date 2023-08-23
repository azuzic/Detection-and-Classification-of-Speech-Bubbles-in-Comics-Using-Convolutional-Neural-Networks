from PyQt5.QtWidgets import QPushButton
from functions.image_manipulation import open_image_dialog, setImage

class OpenImageButton(QPushButton):
    def __init__(self, parent, image):
        super().__init__("Open Image", parent)
        self.image = image
        self.clicked.connect(self.open_image_and_display)

    def open_image_and_display(self):
        open_image_dialog()

        pixmap = self.image.pixmap()
        pixmap = setImage(self, pixmap)