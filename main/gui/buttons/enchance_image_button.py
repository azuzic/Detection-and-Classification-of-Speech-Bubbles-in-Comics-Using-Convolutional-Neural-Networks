from PyQt5.QtWidgets import QPushButton, QInputDialog
from image_manipulation import imageContrast, resizeImage

class EnchanceImageButton(QPushButton):
    def __init__(self, parent, image_label, image_info_label):
        super().__init__("Enchance Image", parent)
        self.image_label = image_label
        self.image_info_label = image_info_label
        self.clicked.connect(self.enchanceImage)

    def enchanceImage(self):
        # Get the current pixmap from the image_label
        pixmap = self.image_label.pixmap()

        if pixmap:   
            value, ok = QInputDialog.getDouble(self, "Enhance Image", "Enter contrast enhancement factor:", 1.0, 0.1, 1000.0, 1)        
            if ok:
                imageContrast(value)
                pixmap = resizeImage(self, pixmap)
