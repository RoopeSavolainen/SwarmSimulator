import sys
import ui
from PyQt5.QtWidgets import QApplication
import os.path

from parameters import Parameters

def main():
    application = QApplication(sys.argv)

    params = Parameters()
    if os.path.isfile("default.cfg"):
        try:
            params.load_from_file("default.cfg")
        except:
            # Even if the operation fails the object should still be usable.
            pass

    window = ui.ApplicationWidget(params)
    window.show()

    sys.exit(application.exec_())


if __name__ == '__main__':
    main()

