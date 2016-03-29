from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

class ApplicationWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.window = uic.loadUi("src/applicationwindow.ui")


    def show(self):
        self.window.show()
    

