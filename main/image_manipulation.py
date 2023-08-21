from PyQt5.QtWidgets import QFileDialog, QSizePolicy, QApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image, ImageEnhance
import numpy as np
import pytesseract
import cv2
import math

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
        box = boxes[0]
        x1, y1, x2, y2 = map(int, box.split()[1:5])
        combined_text = box.split()[0]
        
        del boxes[0]
        
        i = 0
        while i < len(boxes):
            x1_i, y1_i, x2_i, y2_i = map(int, boxes[i].split()[1:5])
            overlap = (x1 < x2_i) and (x2 > x1_i) and (y1 < y2_i) and (y2 > y1_i)
            
            if overlap:
                combined_text += ' ' + boxes[i].split()[0]
                x1 = min(x1, x1_i)
                x2 = max(x2, x2_i)
                y1 = min(y1, y1_i)
                y2 = max(y2, y2_i)
                del boxes[i]
            else:
                i += 1
        
        grouped_boxes.append((x1, y1, x2, y2, combined_text))
    
    return combine_close_boxes(grouped_boxes)

def combine_close_boxes(grouped_boxes, distance_threshold = 10):
    combined_boxes = []
    
    while grouped_boxes:
        box = grouped_boxes[0]
        x1, y1, x2, y2, text = box
        
        del grouped_boxes[0]
        
        i = 0
        while i < len(grouped_boxes):
            x1_i, y1_i, x2_i, y2_i, text_i = grouped_boxes[i]
            distance = abs((y2 + y1) - (y2_i + y1_i))
            
            if distance < distance_threshold:
                combined_text = text + ' ' + text_i
                x1 = min(x1, x1_i)
                x2 = max(x2, x2_i)
                y1 = min(y1, y1_i)
                y2 = max(y2, y2_i)
                text = combined_text
                del grouped_boxes[i]
            else:
                i += 1
        
        combined_boxes.append((x1, y1, x2, y2, text))
    
    return combined_boxes

def divide_image_into_grid(image, piece_size):
    height, width = image.shape
    pieces = []
    
    for y in range(0, height, piece_size):
        for x in range(0, width, piece_size):
            piece = image[y:y+piece_size, x:x+piece_size]
            pieces.append(piece)
    
    return pieces

def divide_image_into_grid_color(image, piece_size):
    height, width, _ = image.shape
    pieces = []
    
    for y in range(0, height, piece_size):
        for x in range(0, width, piece_size):
            piece = image[y:y+piece_size, x:x+piece_size]
            pieces.append(piece)
    
    return pieces

def reconstruct_image_from_grid_color(piece_list, piece_size, image_shape):
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
    
    # Convert PIL image to cv2 image
    cv_image = cv2.cvtColor(np.array(empty_image), cv2.COLOR_RGB2BGR)
    
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    
    piecesColor = divide_image_into_grid_color(cv_image, 100)
    pieces = divide_image_into_grid(gray_image, 100)
    
    for piece, pieceColor in zip(pieces, piecesColor):
        # Apply OCR to get bounding box information and text for each word
        boxes = pytesseract.image_to_boxes(piece, config='--psm 6')

        grouped_boxes = group_boxes(boxes.splitlines())
        
        for box in grouped_boxes:
            x1, y1, x2, y2, text = box
            cv2.rectangle(pieceColor, (x1, piece.shape[0] - y1), (x2, piece.shape[0] - y2), (0, 0, 255), 1)
            cv2.putText(pieceColor, text, (x1, piece.shape[0] - y1 + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        empty_image = Image.fromarray(cv2.cvtColor(pieceColor, cv2.COLOR_BGR2RGB))
        resizeImage(self, pixmap)
        QApplication.processEvents()

    empty_image = reconstruct_image_from_grid_color(piecesColor, 100, gray_image)












    