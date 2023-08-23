import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.gui_colors import set_fusion_style

if __name__ == "__main__":
    app = QApplication(sys.argv)
    set_fusion_style(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())