from PyQt5.QtWidgets import QApplication
from PIL import Image
import numpy as np
import easyocr
import cv2

from PyQt5.QtWidgets import QLabel

from functions.image_manipulation import getEmptyImage, setEmptyImage, setImage
from functions.log import log, color, bold

self = None
overlay = None
boxes = []
from collections import Counter

def initialiseImageLayout(gui):
    global self
    self = gui

def deleteBoxes():
    global boxes
    for box in boxes:
        if isinstance(box, QLabel):
            box.deleteLater()
    boxes.clear()

def drawBox(w,h,x,y,cv_image,text):
    global self
    global boxes

    width = cv_image.shape[1]
    height = cv_image.shape[0]

    wp = 800/width
    wh = 800/height

    if width > height:
        aspect_ratio = height/width
        w = int(wp*w)
        h = int(wh*h*aspect_ratio)
        x = int(wp*x)
        y = int(wh*y*aspect_ratio)
    else:
        aspect_ratio = width/height
        w = int(wp*w*aspect_ratio)
        h = int(wh*h)
        x = int(wp*x*aspect_ratio)
        y = int(wh*y)

    box = QLabel(self.container)
    box.setGeometry(x,y,w,h)
    box.setText(text)
    box.setStyleSheet("background-color: rgba(255, 0, 0, 127); font-weight: bold; border: 1px solid red")
    box.setWordWrap(True)
    font = box.font()
    font.setPointSize(6) 
    box.setFont(font)
    box.show()
    box.raise_()

    boxes.append(box)

def fillArea(x1, x2, y1, y2, cv_image):
    # Ensure the coordinates are within bounds
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(x2, cv_image.shape[1])
    y2 = min(y2, cv_image.shape[0])

    # Extract the specified area from the image
    area = cv_image[y1:y2, x1:x2]

    # Convert the area to grayscale
    area_gray = cv2.cvtColor(area, cv2.COLOR_BGR2GRAY)

    # Convert grayscale to binary (black and white) using a threshold
    _, area_bw = cv2.threshold(area_gray, 128, 255, cv2.THRESH_BINARY)

    # Calculate the unique pixel values and their counts in the area
    pixel_counter = Counter(area_bw.flatten())

    # Print or log the counts of black and white pixels
    log(f"Pixels", True)
    for pixel_value, count in pixel_counter.items():
        log(f'Pixel value {pixel_value}: Count {bold(color("#4eaf4a",f"[{count}]"))}', False)

    # Find the first white pixel from the center
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    for y in range(center_y, y2):
        for x in range(center_x, x2):
            if area_bw[y - y1, x - x1] == 255:  # Adjusted indices
                # Color the pixel blue
                cv_image[y, x] = [255, 0, 0]  # BGR color
                cv_image[y+1, x] = [255, 0, 0]  # BGR color
                cv_image[y-1, x] = [255, 0, 0]  # BGR color
                cv_image[y, x+1] = [255, 0, 0]  # BGR color
                cv_image[y, x-1] = [255, 0, 0]  # BGR color
                break
        else:
            continue
        break

def group_boxes(boxes):
    log(f'{bold(color("#a477b8","📁 Beginning the process of clustering nearby boxes."))}', True)
    grouped_boxes = []
    
    while boxes:
        bbox, text, prob = boxes[0]
        x_points, y_points = zip(*bbox)

        x1, x2 = min(x_points), max(x_points)
        y1, y2 = min(y_points), max(y_points)
        combined_text = text
        
        del boxes[0]
        
        i = 0
        while i < len(boxes):
            bbox_i, text_i, prob_i = boxes[i]
            x_points_i, y_points_i = zip(*bbox_i)

            x1_i, x2_i = min(x_points_i), max(x_points_i)
            y1_i, y2_i = min(y_points_i), max(y_points_i)
            
            overlap = (x1 < x2_i) and (x2 > x1_i) and (y1 < y2_i) and (y2 > y1_i)
            
            if overlap:
                combined_text += ' ' + text_i + ' <br/> '
                x1 = min(x1, x1_i)
                x2 = max(x2, x2_i)
                y1 = min(y1, y1_i)
                y2 = max(y2, y2_i)
                del boxes[i]
            else:
                i += 1
        
        grouped_boxes.append((((x1, y1), (x2, y2)), combined_text))
    
    log(f'{bold(color("#a477b8","✅ Clustering of nearby boxes completed."))}', True)
    return grouped_boxes

def findSpeechBubbleContour(cv_image, rect_coordinates):
    x1, y1 = rect_coordinates[0]
    x2, y2 = rect_coordinates[1]

    # Dilate the rectangle slightly
    dilation_factor = 1.2
    dilated_x1 = int(x1 - (x2 - x1) * (dilation_factor - 1) / 2)
    dilated_x2 = int(x2 + (x2 - x1) * (dilation_factor - 1) / 2)
    dilated_y1 = int(y1 - (y2 - y1) * (dilation_factor - 1) / 2)
    dilated_y2 = int(y2 + (y2 - y1) * (dilation_factor - 1) / 2)

    # Crop the dilated region
    dilated_region = cv_image[dilated_y1:dilated_y2, dilated_x1:dilated_x2]

    # Convert to grayscale
    gray_dilated = cv2.cvtColor(dilated_region, cv2.COLOR_BGR2GRAY)

    # Threshold the grayscale image to create a binary mask
    _, thresholded = cv2.threshold(gray_dilated, 1, 255, cv2.THRESH_BINARY)

    # Find contours in the mask
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on size and shape
    for contour in contours:
        if cv2.contourArea(contour) > 1000:  # Adjust the threshold based on your use case
            return contour

    return None

def drawBoxes(grouped_boxes, cv_image, self, pixmap):
    for index, (bbox, text) in enumerate(grouped_boxes):
            x_points, y_points = zip(*bbox)
            x1, x2 = int(min(x_points)), int(max(x_points))
            y1, y2 = int(min(y_points)), int(max(y_points))
            
            drawBox(x2-x1,y2-y1,x1,y1,cv_image, text)
            fillArea(x1, x2, y1, y2, cv_image)

            empty_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
            setEmptyImage(empty_image)
            setImage(self, pixmap, False)
            log(f'Completed processing box {bold(color("#4eaf4a",f"[{index+1}]"))}', True)
            QApplication.processEvents()

def detect_and_draw_speech_bubbles(self, pixmap):
    deleteBoxes()
    QApplication.processEvents()
    empty_image = getEmptyImage()
    log(f'', True)
    log(f'🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 ', True)
    log(f'{bold(color("#00c8ff","🔍 Initiating speech bubble detection process ..."))}', True)
    
    try:
        cv_image = cv2.cvtColor(np.array(empty_image), cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        log(f'{bold(color("#db3030","📖 Commencing EasyOCR text extraction..."))}', True)
        reader = easyocr.Reader(lang_list=['en']) 
        results = reader.readtext(gray_image)
        log(f'{bold(color("#db3030","✅ EasyOCR reader concluded."))}', True)

        grouped_boxes = group_boxes(results)

        log(f'{bold(color("#c9b34f","🖋️ Commencing drawing of boxes and text."))}', True)
        drawBoxes(grouped_boxes, cv_image, self, pixmap)
        log(f'{bold(color("#c9b34f","✅ Box and text drawing completed successfully."))}', True)

        log(f'{bold(color("#00c8ff","✅ Speech bubble detection process successfully accomplished."))}', True)
        log(f'🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 ', True)
        log(f'', True)
    
    except Exception as e:
        log(f'', True)
        log(f'❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ', True)
        log(f'{bold(color("#ff0000","💥 An error occurred:"))} {str(e)}', True)
        log(f'❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ', True)
        log(f'', True)
        print(f"An error occurred: {str(e)}")