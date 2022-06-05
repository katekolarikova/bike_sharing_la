import io
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import core_functions

"""
Set up the GUI
"""
class Ui_MainWindow(object):

    def draw_map(self):
        with open('index.html', 'rb') as f:
            data = io.BytesIO(f.read())
        self.view.setHtml(data.getvalue().decode())

    #creating main window elements
    def setupUi(self, MainWindow):

        #set window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(708, 800)

        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.setContentsMargins(10, 500, 10, 10)


        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.heading_label = QtWidgets.QLabel(self.centralwidget)
        self.heading_label.setGeometry(QtCore.QRect(150, 0, 411, 81))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)

        lay = QtWidgets.QHBoxLayout(self.centralwidget)
        lay.addWidget(self.view, stretch=1)
        self.draw_map()


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 708, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        # set main heading and description
        self.heading_label.setFont(font)
        self.heading_label.setObjectName("heading_label")
        self.description_label = QtWidgets.QLabel(self.centralwidget)
        self.description_label.setGeometry(QtCore.QRect(60, 70, 631, 36))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setItalic(True)
        self.description_label.setFont(font)
        self.description_label.setObjectName("description_label")

        # user location input
        self.location_label = QtWidgets.QLabel(self.centralwidget)
        self.location_label.setGeometry(QtCore.QRect(10, 130, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.user_location_input = QtWidgets.QLineEdit(self.centralwidget)
        self.user_location_input.setGeometry(QtCore.QRect(130, 130, 191, 28))
        self.user_location_input.setObjectName("user_location_input")
        self.location_label.setFont(font)
        self.location_label.setObjectName("location_label")

        #find nearest k stations with available bikes
        self.nearest_bike_label = QtWidgets.QLabel(self.centralwidget)
        self.nearest_bike_label.setGeometry(QtCore.QRect(10, 190, 361, 16))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setItalic(True)
        self.nearest_bike_label.setFont(font)
        self.nearest_bike_label.setObjectName("nearest_bike_label")

        self.k_bikes1_label = QtWidgets.QLabel(self.centralwidget)
        self.k_bikes1_label.setGeometry(QtCore.QRect(10, 240, 301, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)

        self.k_bikes1_label.setFont(font)
        self.k_bikes1_label.setObjectName("k_bikes1_label")

        self.k_bikes_input = QtWidgets.QLineEdit(self.centralwidget)
        self.k_bikes_input.setGeometry(QtCore.QRect(290, 240, 113, 28))
        self.k_bikes_input.setObjectName("k_bikes_input")

        self.search_bikes_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_bikes_button.setGeometry(QtCore.QRect(430, 240, 90, 28))
        self.search_bikes_button.setObjectName("search_bikes_button")
        self.search_bikes_button.clicked.connect(lambda:core_functions.find_nearest_stations(self.user_location_input.text(),
                                                                                                 self.k_bikes_input.text(),'bikes'))

        self.search_bikes_button.clicked.connect(lambda :self.draw_map())

        #find k stations with available docks
        self.Stations_docks_lable = QtWidgets.QLabel(self.centralwidget)
        self.Stations_docks_lable.setGeometry(QtCore.QRect(10, 290, 381, 16))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setItalic(True)
        self.Stations_docks_lable.setFont(font)
        self.Stations_docks_lable.setObjectName("Stations_docks_lable")

        self.k_docks_lable = QtWidgets.QLabel(self.centralwidget)
        self.k_docks_lable.setGeometry(QtCore.QRect(10, 350, 301, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.k_docks_lable.setFont(font)
        self.k_docks_lable.setObjectName("k_docks_lable")

        self.k_docks_input = QtWidgets.QLineEdit(self.centralwidget)
        self.k_docks_input.setGeometry(QtCore.QRect(290, 350, 113, 28))
        self.k_docks_input.setObjectName("k_docks_input")

        self.search_docks_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_docks_button.setGeometry(QtCore.QRect(430, 350, 90, 28))
        self.search_docks_button.setObjectName("search_docks_button")

        self.search_docks_button.clicked.connect(lambda:
                                                 core_functions.find_nearest_stations(self.user_location_input.text(),
                                                                                     self.k_docks_input.text(),'docks'))


        self.search_docks_button.clicked.connect(lambda: self.draw_map())

        # find route between two points
        self.route_label = QtWidgets.QLabel(self.centralwidget)
        self.route_label.setGeometry(QtCore.QRect(10, 400, 431, 16))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setItalic(True)
        self.route_label.setFont(font)
        self.route_label.setObjectName("route_label")

        self.point1_label = QtWidgets.QLabel(self.centralwidget)
        self.point1_label.setGeometry(QtCore.QRect(10, 460, 58, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.point1_label.setFont(font)
        self.point1_label.setObjectName("point1_label")
        self.point1_input = QtWidgets.QLineEdit(self.centralwidget)
        self.point1_input.setGeometry(QtCore.QRect(80, 460, 113, 28))
        self.point1_input.setObjectName("point1_input")

        self.point2_label = QtWidgets.QLabel(self.centralwidget)
        self.point2_label.setGeometry(QtCore.QRect(210, 460, 58, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.point2_label.setFont(font)
        self.point2_label.setObjectName("label")

        self.point2_input = QtWidgets.QLineEdit(self.centralwidget)
        self.point2_input.setGeometry(QtCore.QRect(290, 460, 113, 28))
        self.point2_input.setObjectName("lineEdit_2")

        self.shortest_route_button = QtWidgets.QPushButton(self.centralwidget)
        self.shortest_route_button.setGeometry(QtCore.QRect(430, 460, 90, 28))
        self.shortest_route_button.setObjectName("shortest_route_button")

        self.shortest_route_button.clicked.connect(lambda:
                                                       core_functions.find_route_between_points(self.point1_input.text(),
                                                                                self.point2_input.text()))

        self.shortest_route_button.clicked.connect(lambda: self.draw_map())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    # set text
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Bikes in LA"))
        self.heading_label.setText(_translate("MainWindow", "Bike Sharing System in LA"))
        self.location_label.setText(_translate("MainWindow", "Your Location:"))
        self.search_bikes_button.setText(_translate("MainWindow", "Search"))
        self.description_label.setText(
            _translate("MainWindow", "Use this app for finding nearest bike stations or counting the route"))
        self.nearest_bike_label.setText(_translate("MainWindow", "Find nearest stations with available bikes"))
        self.k_bikes1_label.setText(_translate("MainWindow", "How many stations you would like to see: "))
        self.Stations_docks_lable.setText(_translate("MainWindow", "Find nearest stations with available docks"))
        self.k_docks_lable.setText(_translate("MainWindow", "How many stations you would like to see:"))
        self.search_docks_button.setText(_translate("MainWindow", "Search"))
        self.route_label.setText(_translate("MainWindow", "Find the shortest route between these two points"))
        self.point1_label.setText(_translate("MainWindow", "Point 1: "))
        self.point2_label.setText(_translate("MainWindow", "Point 2:"))
        self.shortest_route_button.setText(_translate("MainWindow", "Search"))
