from PyQt5 import QtWidgets
from ui_setup import Ui_MainWindow
from core_functions import Core_Functions
import sys,time

if __name__ == "__main__":
    cf = Core_Functions()
    cf.clean_map()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())


