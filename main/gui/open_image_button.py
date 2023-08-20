from PyQt5.QtWidgets import QPushButton
from image_manipulation import open_image_dialog, resizeImage

class OpenImageButton(QPushButton):
    def __init__(self, parent, image_label, image_info_label):
        super().__init__("Open Image", parent)
        self.image_label = image_label
        self.image_info_label = image_info_label
        self.clicked.connect(self.open_image_and_display)

    def open_image_and_display(self):
        open_image_dialog()

        pixmap = self.image_label.pixmap()
        pixmap = resizeImage(self, pixmap)

        # Update image info label
        info = f"Image Size: {pixmap.width()} x {pixmap.height()}\n"
        self.image_info_label.setText(info)