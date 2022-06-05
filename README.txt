Name: Katerina Kolarikova
Date: 5.6.2022
GitHub: https://github.com/katekolarikova/bike_sharing_la
Course: Applied data Science with Python
School: Ostbayerische Technische Hochschule

This application is used for processing data about bikes in LA. The main function are searching for stations with
available bikes/docks and calculating the route.

Part of this application is also a documentation - check kolarikova_project_description.pdf

For succesfull running the application please:
- be connected to the internet
- insert the coordination input in form latitude,longitude
    - examples:
        34.101614, -118.330265
        34.062774, -118.239546
        34.055062, -118.249323
        34.119237, -118.300283
        34.010800, -118.494234
- insert the number k as a whole number
- install following libraries :
    - PyQT pip3 install pyqt5
    - geopandas pip3 install geopandas
    - geopy: pip3 install geopy
    - folium: pip3 install folium
    - openrouteservice: pip3 install openrouteservice
- for running the application use scipt main.py

I also recommended running application in its own virtual enviroment
    -python3 -m venv path_to_the_project