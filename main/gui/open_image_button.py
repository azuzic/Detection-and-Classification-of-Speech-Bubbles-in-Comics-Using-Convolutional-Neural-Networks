from PyQt5.QtWidgets import QPushButton, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from image_manipulation import open_image_dialog

class OpenImageButton(QPushButton):
    def __init__(self, parent, image_label, image_info_label):
        super().__init__("Open Image", parent)
        self.image_label = image_label
        self.image_info_label = image_info_label
        self.clicked.connect(self.open_image_and_display)

    def open_image_and_display(self):
        img = open_image_dialog()
        if img:
            img = img.convert("RGBA")
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
            else:
                self.image_label.setFixedWidth(400 * aspect_ratio)
                self.image_label.setFixedHeight(400)
                pixmap = pixmap.scaledToWidth(400 * aspect_ratio, Qt.TransformationMode.SmoothTransformation)

            # Set minimum size to match the initial label size
            self.image_label.setMinimumSize(pixmap.width(), pixmap.height())

            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)

            # Update image info label
            info = f"Image Size: {pixmap.width()} x {pixmap.height()}\n"
            self.image_info_label.setText(info)