"""
Katerina Kolarikova
Applied Data Science with Python, Ostbayerische technische hochschule regensburg
30.5.2022

Goal of this project is to develop the application processing data about share bikes in LA.
Live data are downloaded from official site 'http://bikeshare.metro.net and the main functions are :
 -  display K nearest stations with availble bikes around given location
 -  display K nearest stations with availble docks around given location
 -  find fastest way between two points using sharing bike and feet

 Used Libraries:
 - folium - map client
 - open route service - finding route between two points
 - pyQT - GUI
 - geopy - processing geo data

"""

from PyQt5 import QtWidgets
from ui_setup import Ui_MainWindow
import core_functions
import sys

if __name__ == "__main__":
    core_functions.clean_map()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


