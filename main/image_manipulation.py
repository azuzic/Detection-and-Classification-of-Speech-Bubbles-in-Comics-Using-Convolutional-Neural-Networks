from PyQt5.QtWidgets import QFileDialog
from PIL import Image

def open_image_dialog():
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly

    file_name, _ = QFileDialog.getOpenFileName(None, "Open Image File", "", "Image Files (*.jpg *.png *.bmp *.jpeg);;All Files (*)", options=options)
    
    if file_name:
        img = Image.open(file_name)
        return img