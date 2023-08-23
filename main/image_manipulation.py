from PyQt5.QtWidgets import QFileDialog, QSizePolicy, QApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image, ImageEnhance
import numpy as np
import pytesseract
import cv2
import math
import easyocr

image_size = 800
empty_image = Image.new("RGBA", (image_size, image_size), (0, 0, 0, 0))

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

def imageContrast(factor):
    global empty_image
    
    enhancer = ImageEnhance.Contrast(empty_image)
    adjusted_image = enhancer.enhance(factor)
    
    empty_image = adjusted_image

def resizeImage(self, pixmap):
    global empty_image
    global image_size
    img = empty_image.convert("RGBA")
    qimage = QImage(img.tobytes(), img.width, img.height, QImage.Format_RGBA8888)
    pixmap = QPixmap.fromImage(qimage)
    
    aspect_ratio = pixmap.width() / pixmap.height()

    # Allow the label to expand horizontally
    self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    # Adjust label's width according to image's aspect ratio
    new_label_width = self.image_label.height() * aspect_ratio
    if new_label_width > image_size:
        self.image_label.setFixedWidth(image_size)
        self.image_label.setFixedHeight(image_size * aspect_ratio)
        pixmap = pixmap.scaledToWidth(image_size, Qt.TransformationMode.SmoothTransformation)
        #empty_image = empty_image.resize((pixmap.width(),pixmap.height()), resample=Image.BILINEAR)
    else:
        self.image_label.setFixedWidth(image_size * aspect_ratio)
        self.image_label.setFixedHeight(image_size)
        pixmap = pixmap.scaledToWidth(image_size * aspect_ratio, Qt.TransformationMode.SmoothTransformation)
        #empty_image = empty_image.resize((pixmap.width(),pixmap.height()), resample=Image.BILINEAR)

    self.image_label.setMinimumSize(pixmap.width(), pixmap.height())

    self.image_label.setPixmap(pixmap)
    self.image_label.setScaledContents(True)

    return pixmap

def group_boxes(boxes):
    grouped_boxes = []
    
    while boxes:
        bbox, text, prob = boxes[0]
        print(bbox)
        x_points, y_points = zip(*bbox)

        x1, x2 = min(x_points), max(x_points)
        y1, y2 = min(y_points), max(y_points)
        combined_text = text
        
        del boxes[0]
        
        i = 0
        while i < len(boxes):
            (bbox_i, text_i, _), _, _ = boxes[i]
            x_points_i, y_points_i = zip(*bbox_i)

            x1_i, x2_i = min(x_points_i), max(x_points_i)
            y1_i, y2_i = min(y_points_i), max(y_points_i)
            
            overlap = (x1 < x2_i) and (x2 > x1_i) and (y1 < y2_i) and (y2 > y1_i)
            
            if overlap:
                combined_text += ' ' + text_i
                x1 = min(x1, x1_i)
                x2 = max(x2, x2_i)
                y1 = min(y1, y1_i)
                y2 = max(y2, y2_i)
                del boxes[i]
            else:
                i += 1
        
        grouped_boxes.append((((x1, y1), (x2, y2)), combined_text))
    
    return grouped_boxes


    image_height, image_width = image_shape.shape
    reconstructed_image = Image.new('RGB', (image_width, image_height))
    
    piece_idx = 0
    
    for y in range(0, image_height, piece_size):
        for x in range(0, image_width, piece_size):
            piece = piece_list[piece_idx]
            piece_img = Image.fromarray(piece)
            reconstructed_image.paste(piece_img, (x, y))
            piece_idx += 1
    
    return reconstructed_image

def detect_and_draw_speech_bubbles(self, pixmap):
    global empty_image
    
    try:
        cv_image = cv2.cvtColor(np.array(empty_image), cv2.COLOR_RGB2BGR)
        
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        reader = easyocr.Reader(lang_list=['en'])  # Specify the language(s) you want to detect

        results = reader.readtext(gray_image)

        grouped_boxes = group_boxes(results)

        for (bbox, text) in grouped_boxes:
            x_points, y_points = zip(*bbox)
            x1, x2 = min(x_points), max(x_points)
            y1, y2 = min(y_points), max(y_points)
            cv2.rectangle(cv_image, (x1, y1), (x2, y2), (0, 0, 255), 1)
            cv2.putText(cv_image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            empty_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
            resizeImage(self, pixmap)
            QApplication.processEvents()
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")














    