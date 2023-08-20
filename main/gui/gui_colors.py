from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QStyleFactory

def set_dark_palette(widget):
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    widget.setPalette(dark_palette)

def set_fusion_style(app):
    app.setStyle(QStyleFactory.create("Fusion"))