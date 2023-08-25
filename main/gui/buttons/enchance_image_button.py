from PyQt5.QtWidgets import QPushButton, QInputDialog
from functions.image_manipulation import imageContrast, setImage

class EnchanceImageButton(QPushButton):
    def __init__(self, parent, image):
        super().__init__("Enchance Image", parent)
        self.image = image
        self.clicked.connect(self.enchanceImage)

    def enchanceImage(self):
        # Get the current pixmap from the image
        pixmap = self.image.pixmap()

        if pixmap:   
            value, ok = QInputDialog.getDouble(self, "Enhance Image", "Enter contrast enhancement factor:", 1.0, 0.1, 1000.0, 1)        
            if ok:
                imageContrast(value)
                pixmap = setImage(self, pixmap, False)
