import sys

from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPixmap
from PySide6.QtCore import Signal



class QLabelXButton(QLabel):
    signal = Signal()
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("QLabelXButton")
        self.parent1 = parent
        pixmap = QPixmap("../../imgs/x_ button.png")
        pixmap = pixmap.scaled(100,100, Qt.KeepAspectRatio)
        self.setPixmap(pixmap)


    def mousePressEvent(self, event):
        print('teast')
        self.signal.emit()