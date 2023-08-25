from PyQt5.QtWidgets import QPushButton
from functions.image_manipulation import convertToBW, setImage

class ConvertToBWButton(QPushButton):
    def __init__(self, parent, image):
        super().__init__("Convert to BW", parent)
        self.image = image
        self.clicked.connect(self.convertImage)

    def convertImage(self):
        # Get the current pixmap from the image
        pixmap = self.image.pixmap()

        if pixmap:           
            convertToBW()
            pixmap = setImage(self, pixmap, False)
