from PyQt5.QtWidgets import QPushButton
from functions.speech_bubble_extraction import detect_and_draw_speech_bubbles, setImage

class FindSpeechBubblesButton(QPushButton):
    def __init__(self, parent, image):
        super().__init__("Find Bubbles", parent)
        self.image = image
        self.clicked.connect(self.findSpeechBubbles)

    def findSpeechBubbles(self):
        pixmap = self.image.pixmap()

        if pixmap:   
            detect_and_draw_speech_bubbles(self, pixmap)
            pixmap = setImage(self, pixmap)
