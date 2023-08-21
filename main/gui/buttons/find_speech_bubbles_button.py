from PyQt5.QtWidgets import QPushButton
from image_manipulation import detect_and_draw_speech_bubbles, resizeImage

class FindSpeechBubblesButton(QPushButton):
    def __init__(self, parent, image_label, image_info_label):
        super().__init__("Find Bubbles", parent)
        self.image_label = image_label
        self.image_info_label = image_info_label
        self.clicked.connect(self.findSpeechBubbles)

    def findSpeechBubbles(self):
        pixmap = self.image_label.pixmap()

        if pixmap:   
            detect_and_draw_speech_bubbles(self, pixmap)
            pixmap = resizeImage(self, pixmap)
