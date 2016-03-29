import sys
import ui
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    application = QApplication(sys.argv)

    window = ui.ApplicationWidget()
    window.show()

    sys.exit(application.exec_())
