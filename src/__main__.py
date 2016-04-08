import sys
from ui import ApplicationWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QGraphicsScene
import os.path

from parameters import Parameters


def main():
    application = QApplication(sys.argv)
    application.quitOnLastWindowClosed = True

    params = Parameters()
    if os.path.isfile("default.cfg"):
        try:
            params.load_from_file("default.cfg")
        except:
            # Even if the operation fails the object should still be usable.
            pass

    window = ApplicationWidget(params)
    window.show()

    sys.exit(application.exec_())


if __name__ == '__main__':
    main()


