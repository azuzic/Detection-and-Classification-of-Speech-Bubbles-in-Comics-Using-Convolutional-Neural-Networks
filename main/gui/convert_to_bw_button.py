from PyQt5.QtWidgets import QPushButton
from image_manipulation import convertToBW, resizeImage

class ConvertToBW(QPushButton):
    def __init__(self, parent, image_label, image_info_label):
        super().__init__("Convert to BW", parent)
        self.image_label = image_label
        self.image_info_label = image_info_label
        self.clicked.connect(self.convertImage)

    def convertImage(self):
        # Get the current pixmap from the image_label
        pixmap = self.image_label.pixmap()

        if pixmap:           
            convertToBW()
            pixmap = resizeImage(self, pixmap)
