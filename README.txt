Name: Katerina Kolarikova
Date: 5.6.2022
GitHub: https://github.com/katekolarikova/bike_sharing_la
Course: Applied Data Science with Python
School: Ostbayerische Technische Hochschule

This application is used for processing data about bikes in LA. The main functions are searching for stations with
available bikes/docks and calculating the route.

Part of this application is also a documentation - check kolarikova_project_description.pdf

For successful running the application please:
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
    - PyQT:pip install PyQt5, https://pypi.org/project/PyQt5/
    - geopandas: pip install geopandas, https://geopandas.org/en/stable/getting_started/install.html
    - geopy: pip install geopy, https://pypi.org/project/geopy/
    - folium: pip install folium, https://pypi.org/project/folium/
    - pip install -r requirements-dev.txt
    - openrouteservice: pip install openrouteservice, https://pypi.org/project/openrouteservice/
- for running the application use script main.py

I also recommended running application in its own virtual environment
    -python3 -m venv path_to_the_project