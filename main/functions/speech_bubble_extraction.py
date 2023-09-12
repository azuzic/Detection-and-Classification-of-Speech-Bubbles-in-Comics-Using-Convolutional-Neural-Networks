from PyQt5.QtWidgets import QApplication
from PIL import Image
import numpy as np
import easyocr
import cv2

from PyQt5.QtWidgets import QLabel

from functions.image_manipulation import getEmptyImage, setEmptyImage, setImage, getImageName
from functions.log import log, color, bold, error, logClear

lang = "en"
self = None
self2 = None
pixmap2 = None
overlay = None
boxes = []
magenta_pixel_coordinates = set()
area_bw = None
centers = set()
from collections import Counter

def setLang(value):
    global lang
    lang = value

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
    box.setStyleSheet("background-color: rgba(255, 0, 0, 85); font-weight: bold; border: 1px solid red")
    box.setWordWrap(True)
    font = box.font()
    font.setPointSize(6) 
    box.setFont(font)
    box.show()
    box.raise_()

    boxes.append(box)

def findNeighboringBlackPixels(x, y, area_bw, cv_image, visited_pixels):
    try:
        if len(visited_pixels) >= 300:
            return False

        visited_pixels.add((x, y))  # Mark current pixel as visited

        # Define the neighborhood offsets (8 directions)
        neighborhood_offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        # Recursively search for neighboring black pixels
        for dx, dy in neighborhood_offsets:
            new_x = x + dx
            new_y = y + dy

            if new_x >= 0 and new_x < area_bw.shape[1] and new_y >= 0 and new_y < area_bw.shape[0]:
                if area_bw[new_y, new_x] == 0 and (new_x, new_y) not in visited_pixels:
                    findNeighboringBlackPixels(new_x, new_y, area_bw, cv_image, visited_pixels)

        return True
    except Exception as e:
        error("findNeighboringBlackPixels", e) 

def exploreAndColor(x, y, cv_image, area_bw):
    global self2, pixmap2
    stack = [(x, y)]
    pixelsGreen = set()
    pixelsGray = set()

    while stack:
        x, y = stack.pop()

        if x < 0 or x >= cv_image.shape[1] or y < 0 or y >= cv_image.shape[0]:
            continue
        
        neighborhood_offsets = [
            (0, 0),
        ]
    
        exit = False
        for dx, dy in neighborhood_offsets:
            new_x = x + dx
            new_y = y + dy
            if new_x >= 0 and new_x < area_bw.shape[1] and new_y >= 0 and new_y < area_bw.shape[0]:
                if area_bw[new_y, new_x] == 0:
                    for dx, dy in neighborhood_offsets:
                        new_x = x + dx
                        new_y = y + dy
                        if new_x >= 0 and new_x < area_bw.shape[1] and new_y >= 0 and new_y < area_bw.shape[0]:
                            #cv_image[new_y, new_x] = [0, 255, 0]  # Color it green
                            area_bw[new_y, new_x] = 128
                            pixelsGreen.add((new_y, new_x))
                    exit = True
                if exit:
                    continue

        if area_bw[y, x] == 128:
            continue

        #cv_image[y, x] = [200, 200, 200]
        area_bw[y, x] = 128
        pixelsGray.add((y, x))

        stack.append((x - 1, y))
        stack.append((x + 1, y))
        stack.append((x, y - 1))
        stack.append((x, y + 1))
    
    log(f'{bold(color("#d1cd4b","💬 Gray pixel count is: "))} {len(pixelsGray)}', True)
    log(f'{bold(color("#d1cd4b","💬 Green pixel count is: "))} {len(pixelsGreen)}', True)
    if len(pixelsGray) < 20000 and len(pixelsGreen) < 10000:
        for x, y in pixelsGray:
            cv_image[x, y] = [200, 200, 200]
        for x, y in pixelsGreen:
            cv_image[x, y] = [0, 255, 0]

def fillArea(x1, x2, y1, y2, cv_image):
    global magenta_pixel_coordinates, area_bw, centers
    log(f'{bold(color("#d1cd4b","💬🔍 Bubble anaylsis in progress..."))}', True)
    # Ensure the coordinates are within bounds
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(x2, cv_image.shape[1])
    y2 = min(y2, cv_image.shape[0])

    black_pixel_coordinates = set()

    # Iterate through the area_bw image to find letters
    for y in range(y1, y2):
        for x in range(x1, x2):
            if area_bw[y, x] == 0:  # Check for black pixel
                findNeighboringBlackPixels(x, y, area_bw, cv_image, black_pixel_coordinates)
                if len(black_pixel_coordinates) < 300:
                    for px, py in black_pixel_coordinates:
                        cv_image[py, px] = [255, 255, 255]
                        area_bw[py, px] = 255
                        magenta_pixel_coordinates.add((py, px))
            #cv_image[y, x] = [255, 255, 255]

            black_pixel_coordinates.clear()

    # Find the first white pixel from the center
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    centers.add((center_x, center_y))
    log(f'{bold(color("#d1cd4b","💬✅ Bubble anaylsis in finished."))}', True)

def colorText(cv_image):
    global self2, pixmap2, magenta_pixel_coordinates
    log(f'{bold(color("#d14bc1","📝 Coloring text."))}', True)
    for px, py in magenta_pixel_coordinates:
        cv_image[px, py] = [255, 0, 255]
    magenta_pixel_coordinates.clear()
    empty_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
    setEmptyImage(empty_image)
    setImage(self2, pixmap2, False)
    log(f'{bold(color("#d14bc1","✍️✅ Coloring finished."))}', True)

def colorBubble(cv_image):
    global centers
    log(f'{bold(color("#73c5d1","🖋️ Coloring bubbles."))}', True)
    for center_x, center_y in centers:
        exploreAndColor(center_x, center_y, cv_image, area_bw)
    centers.clear()
    empty_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
    setEmptyImage(empty_image)
    setImage(self2, pixmap2, False)
    log(f'{bold(color("#73c5d1","🖋️✅ Coloring bubbles finished."))}', True)

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
    log(f'{bold(color("#c9b34f","🖋️ Commencing drawing of boxes and text."))}', True)
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
    log(f'{bold(color("#c9b34f","✅ Box and text drawing completed successfully."))}', True)

def THRESH_BINARY(cv_image, gray_image, maxval, thresh):
    _, cv_image = cv2.threshold(gray_image, thresh, maxval, cv2.THRESH_BINARY)
    cv2.imwrite(f'output/{getImageName()}_THRESH_BINARY_{thresh}_{maxval}.png', cv_image)

def detect_and_draw_speech_bubbles(self, pixmap):
    global self2, pixmap2, area_bw, lang
    self2 = self
    pixmap2 = pixmap
    logClear()
    deleteBoxes()
    QApplication.processEvents()
    empty_image = getEmptyImage()
    log(f'', True)
    log(f'🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 🚀 ', True)
    log(f'{bold(color("#00c8ff","🔍 Initiating speech bubble detection process ..."))}', True)
    
    cv_image = cv2.cvtColor(np.array(empty_image), cv2.COLOR_RGB2BGR)
    gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    log(f'{bold(color("#db3030","📖 Commencing EasyOCR text extraction..."))}', True)
    reader = easyocr.Reader(lang_list=[lang])
    results = reader.readtext(gray_image)
    log(f'{bold(color("#db3030","✅ EasyOCR reader concluded."))}', True)

    grouped_boxes = group_boxes(results)

    _, area_bw = cv2.threshold(gray_image, 160, 255, cv2.THRESH_BINARY)
    _, cv_image = cv2.threshold(gray_image, 160, 255, cv2.THRESH_BINARY)

    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
    
    empty_image = Image.fromarray(cv2.cvtColor(area_bw, cv2.COLOR_BGR2RGB))
    setEmptyImage(empty_image)
    setImage(self2, pixmap2, False)

    drawBoxes(grouped_boxes, cv_image, self, pixmap)
    colorText(cv_image)
    colorBubble(cv_image)

    cv2.imwrite(f'output/{getImageName()}.png', cv_image)

    log(f'{bold(color("#00c8ff","✅ Speech bubble detection process successfully accomplished."))}', True)
    log(f'🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 🏁 ', True)
    log(f'', True)