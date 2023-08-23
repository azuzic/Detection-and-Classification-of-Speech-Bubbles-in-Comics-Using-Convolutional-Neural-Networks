from PyQt5.QtWidgets import QApplication
from PIL import Image
import numpy as np
import easyocr
import cv2

from functions.image_manipulation import empty_image, setImage
from functions.log import log, color, bold

def group_boxes(boxes):
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

def detect_and_draw_speech_bubbles2(self, pixmap):
    global empty_image
    print(empty_image)
    log(f'{bold(color("#00c8ff","Initiating speech bubble detection process ..."))}', True)
    
    try:
        cv_image = cv2.cvtColor(np.array(empty_image), cv2.COLOR_RGB2BGR)
        print(cv_image)
        
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        print(gray_image)

        log(f'{bold(color("#45d163","Commencing EasyOCR text extraction..."))}', True)
        reader = easyocr.Reader(lang_list=['en']) 

        results = reader.readtext(gray_image)
        print(results)
        log(f'{bold(color("#db3030","EasyOCR reader concluded."))}', True)

        grouped_boxes = group_boxes(results)
        print(grouped_boxes)
        log(f'{grouped_boxes}', True)

        for (bbox, text) in grouped_boxes:
            x_points, y_points = zip(*bbox)
            x1, x2 = min(x_points), max(x_points)
            y1, y2 = min(y_points), max(y_points)
            cv2.rectangle(cv_image, (x1, y1), (x2, y2), (0, 0, 255), 1)
            cv2.putText(cv_image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            empty_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
            setImage(self, pixmap)
            QApplication.processEvents()
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def detect_and_draw_speech_bubbles(self, pixmap):
    global empty_image
    
    cv_image = cv2.cvtColor(np.array(empty_image), cv2.COLOR_RGB2BGR)
    
    gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    reader = easyocr.Reader(lang_list=['en'])  # Specify the language(s) you want to detect

    results = reader.readtext(gray_image)
    print(results)

    for (bbox, text, prob) in results:
        x1, y1, x2, y2 = bbox
        cv2.rectangle(cv_image, (x1, y1), (x2, y2), (0, 0, 255), 1)
        cv2.putText(cv_image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    empty_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
    setImage(self, pixmap)
    QApplication.processEvents()