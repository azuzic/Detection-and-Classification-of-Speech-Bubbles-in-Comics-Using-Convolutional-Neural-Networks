from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image, ImageEnhance
from functions.log import log, color, bold
import os

image_size = 800
empty_image = Image.new("RGBA", (image_size, image_size), (11, 12, 18, 255))
image_name = ""

def getImageName():
    global image_name
    return image_name

def getEmptyImage():
    global empty_image
    return empty_image

def setEmptyImage(image):
    global empty_image
    empty_image = image

def open_image_dialog():
    global empty_image, image_name
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly

    file_name, _ = QFileDialog.getOpenFileName(None, "Open Image File", "", "Image Files (*.jpg *.png *.bmp *.jpeg);;All Files (*)", options=options)
    
    if file_name:
        original_image = Image.open(file_name)
        file_name = os.path.basename(file_name)
        
        # Resize the image if its width or height is bigger than 800
        if original_image.width > 800 or original_image.height > 800:
            aspect_ratio = original_image.width / original_image.height
            if original_image.width > original_image.height:
                new_width = 800
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = 800
                new_width = int(new_height * aspect_ratio)
            empty_image = original_image.resize((new_width, new_height))
        else:
            empty_image = original_image
        
        log(f'🖼️ Image {bold(color("#7170c4", file_name))} opened ! ', True)
        image_name = os.path.splitext(file_name)[0]
        return True
    return False

def convertToBW():
    global empty_image
    empty_image = empty_image.convert("L")
    log(f'{bold("Converted")} image to {color("#70c4a0" , "Grayscale")} format !', True)

def imageContrast(factor):
    global empty_image
    
    enhancer = ImageEnhance.Contrast(empty_image)
    adjusted_image = enhancer.enhance(factor)
    
    empty_image = adjusted_image
    log(f'Increased image {bold("contrast")} by a factor of {color("#70c4a0" , factor)} !', True)

def setImage(self, pixmap, debug=True):
    global empty_image
    global image_size
    img = empty_image.convert("RGBA")
    qimage = QImage(img.tobytes(), img.width, img.height, QImage.Format_RGBA8888)
    pixmap = QPixmap.fromImage(qimage)
    
    aspect_ratio = pixmap.width() / pixmap.height()

    # Allow the label to expand horizontally
    self.image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    # Adjust label's width according to image's aspect ratio
    new_label_width = self.image.height() * aspect_ratio
    if new_label_width > image_size:
        self.image.setFixedWidth(image_size)
        self.image.setFixedHeight(image_size * aspect_ratio)
        pixmap = pixmap.scaledToWidth(image_size, Qt.TransformationMode.FastTransformation)
    else:
        self.image.setFixedWidth(image_size * aspect_ratio)
        self.image.setFixedHeight(image_size)
        pixmap = pixmap.scaledToWidth(image_size * aspect_ratio, Qt.TransformationMode.FastTransformation)

    self.image.setMinimumSize(pixmap.width(), pixmap.height())
    self.image.setPixmap(pixmap)
    self.image.setScaledContents(True)

    if debug:
        log(f'{color("#bf9858" ,"🖼️ Image set ! ")} ', True)
        log(f'{bold("Height")}: {color("#70c4a0" , f"{qimage.size().height()} px")}', False)
        log(f'{bold(color("#bf9858" , " | "))}', False)   
        log(f'{bold("Width")}: {color("#70c4a0" , f"{qimage.size().width()} px")}', False)
        log(f'{bold(color("#bf9858" , " | "))}', False)
        log(f'{bold("Aspect_Ratio")}: {color("#70c4a0" , aspect_ratio)}', False)

    QApplication.processEvents()

    return pixmap