from PyQt5.QtWidgets import QFileDialog, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

empty_image = Image.new("RGBA", (400, 400), (0, 0, 0, 0))

def open_image_dialog():
    global empty_image
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly

    file_name, _ = QFileDialog.getOpenFileName(None, "Open Image File", "", "Image Files (*.jpg *.png *.bmp *.jpeg);;All Files (*)", options=options)
    
    if file_name:
        empty_image = Image.open(file_name)
    
def convertToBW():
    global empty_image
    empty_image = empty_image.convert("L")

def resizeImage(self, pixmap):
    global empty_image
    img = empty_image.convert("RGBA")
    qimage = QImage(img.tobytes(), img.width, img.height, QImage.Format_RGBA8888)
    pixmap = QPixmap.fromImage(qimage)
    
    aspect_ratio = pixmap.width() / pixmap.height()

    # Allow the label to expand horizontally
    self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    # Adjust label's width according to image's aspect ratio
    new_label_width = self.image_label.height() * aspect_ratio
    if new_label_width > 400:
        self.image_label.setFixedWidth(400)
        self.image_label.setFixedHeight(400 * aspect_ratio)
        pixmap = pixmap.scaledToWidth(400, Qt.TransformationMode.SmoothTransformation)
        empty_image = empty_image.resize((pixmap.width(),pixmap.height()), resample=Image.BILINEAR)
    else:
        self.image_label.setFixedWidth(400 * aspect_ratio)
        self.image_label.setFixedHeight(400)
        pixmap = pixmap.scaledToWidth(400 * aspect_ratio, Qt.TransformationMode.SmoothTransformation)
        empty_image = empty_image.resize((pixmap.width(),pixmap.height()), resample=Image.BILINEAR)

    self.image_label.setMinimumSize(pixmap.width(), pixmap.height())

    self.image_label.setPixmap(pixmap)
    self.image_label.setScaledContents(True)

    return pixmap