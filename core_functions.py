import geopandas as gpd
import io

from PyQt5.QtWidgets import QMessageBox
from geopy.distance import geodesic as gd
import requests
import folium
import time
import openrouteservice as ors
import API_KEYS

"""
Background of the application
"""

class CoreFunctions():

    # scraping the live feed data about bike stations
    def download_live_data(self):
        URL = 'http://bikeshare.metro.net/stations/json/'
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        headers = {"user-agent": USER_AGENT}  # adding the user agent
        resp = requests.get(URL, headers=headers)
        f = open("map_data.json", "w")
        f.write(resp.text)
        f.close()

    # Taking neccesary data about bike stations and store them into dictionary
    # street, location, num of available bikes, num of available bikes, distance from user (-1 for not count)
    def parse_geo_data_stations(self):
        file = open('map_data.json')
        read = gpd.read_file(file)
        read = read.reset_index()

        station_info = {}
        for index, row in read.iterrows():
            coordinates = (row['latitude'], row['longitude'])
            station_info[row['addressStreet']] = {'coordinates': coordinates, 'bikes': row['bikesAvailable'],
                                                  'docks': row['docksAvailable'], 'distance': -1}

        return station_info

    # displaying the error message box
    # error_message : text we would like to display
    def print_error(self, error_message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Opps")
        msg.setInformativeText(error_message)
        msg.setWindowTitle("Error")
        msg.exec_()

    # accept list of locations, add them to the map and save the map
    # user_location: position of the user
    # points: list of location - available stations
    def draw_map_points(self, user_position, points):
        map = folium.Map(location=user_position, zoom_start=15)
        icon = folium.Icon(color="red")
        folium.Marker(location=user_position, icon=icon).add_to(map)
        for point in range(0, len(points)):
            folium.Marker(points[point]).add_to(map)

        map.save('index.html')
        data = io.BytesIO()
        map.save(data, close_file=False)

    # save map without points or routes
    def clean_map(self):
        map = folium.Map(location=(34.04850, -118.25894), zoom_start=15)
        map.save('index.html')
        data = io.BytesIO()
        map.save(data, close_file=False)

    # function returns k stations with available bikes or docks
    # location of these station is added into the map
    # user_position: position of the user
    # num_k : how many stations should be returned
    # dock_bikes : info if we look for stations with available bikes or docks
    def find_nearest_stations(self, user_position, num_k, dock_bikes):
        points = []
        nearest_stations = []
        type = 'bikes'

        self.download_live_data()
        try:
            if dock_bikes == 'docks':
                type = 'docks'
            k_stations = int(num_k)
            station_info = self.parse_geo_data_stations()
            position_data_split = user_position.split(',')
            user_position = (float(position_data_split[0]), float(position_data_split[1]))
        except ValueError:
            self.print_error('Something went wrong... Please check the input validity')
            return -1

        for item in station_info.items():
            if item[1][type] > 0:  # count distance for stations with available bikes
                item[1]['distance'] = gd(user_position, item[1]['coordinates']).kilometers
        station_info = sorted(station_info.items(), key=lambda item: item[1]['distance'], reverse=False)
        # print the nearest stations -  skip the stations without distance
        station_counter = 0
        for item in station_info:
            if item[1]['distance'] != -1:
                points.append(item[1]['coordinates'])
                print(item)
                nearest_stations.append(item)
                station_counter += 1
            if station_counter == k_stations:  # check how many stations was already printed
                break

        if len(points) < k_stations:
            self.print_error('Not enough stations available')

        self.draw_map_points(user_position, points)

        return nearest_stations

    # find shortest route between two points using walk and share bikes
    # start_location: first point
    # end_location: second point
    def find_shortest_route(self, start_location, end_location):
        # direct route by walks
        ors_key = API_KEYS.OPEN_ROUTE
        client = ors.Client(key=ors_key)
        available_routes = []
        closest_stations = self.find_nearest_stations(str(start_location), 6, 'bikes')

        direct_route_coordinates = ((start_location[1], start_location[0]), (end_location[1], end_location[0]))
        route_walking = client.directions(coordinates=direct_route_coordinates, profile='foot-walking',
                                          format='geojson', units='km')
        distance_walking = route_walking['features'][0]['properties']['summary']['duration']
        available_routes.append({'station': 'walk', 'duration': distance_walking, 'route': route_walking})

        for item in closest_stations:
            # route from start point to the station
            start_to_station_coordinates = (
                (start_location[1], start_location[0]), (item[1]['coordinates'][1], item[1]['coordinates'][0]))
            start_to_station_route = client.directions(coordinates=start_to_station_coordinates, profile='foot-walking',
                                                       format='geojson',
                                                       units='km')

            # route from station to the end point
            from_station_to_end_coordinates = (
                (item[1]['coordinates'][1], item[1]['coordinates'][0]), (end_location[1], end_location[0]))
            from_station_to_end_route = client.directions(coordinates=from_station_to_end_coordinates,
                                                          profile='cycling-regular',

                                                          format='geojson', units='km')
            time.sleep(0.5)
            # totral duration between start and station + station to end
            total_duration = start_to_station_route['features'][0]['properties']['summary']['duration'] + \
                             from_station_to_end_route['features'][0]['properties']['summary']['duration']

            # add whole route to the possible routes
            available_routes.append(
                {'station': item, 'duration': total_duration, 'route_to_statio': start_to_station_route,
                 'route_to_end': from_station_to_end_route})

            time.sleep(0.5)

        # sorted route from fastest
        available_routes = sorted(available_routes, key=lambda item: item['duration'], reverse=False)
        return available_routes[0]

    # add given route to the folium map
    def draw_route_map(self, start_location, end_location, route):
        map = folium.Map(location=start_location, zoom_start=13)
        style = {'fillColor': '#228B22', 'lineColor': '#228B22'}
        folium.Marker(start_location, icon=folium.Icon(color='red')).add_to(map)
        folium.Marker(end_location, icon=folium.Icon(color='red')).add_to(map)
        if route['station'] != 'walk':
            folium.GeoJson(route['route_to_statio'], name='route', style_function=lambda x: style).add_to(
                map)
            folium.Marker(route['station'][1]['coordinates'],
                          icon=folium.Icon(icon='bicycle', prefix='fa')).add_to(map)
            folium.GeoJson(route['route_to_end'], name='route2').add_to(map)
        else:
            folium.GeoJson(route['route'], name='route').add_to(map)

        map.save('index.html')
        data = io.BytesIO()
        map.save(data, close_file=False)

    #finding route between two points
    # start_location: first point
    # end_location: second point
    def find_route_between_points(self, start_location, end_location):
        # (34.04850, -118.25894)
        # (34.02851,-118.25667)

        # parse data from user
        try:
            start_location_split = start_location.split(',')
            start_location = (float(start_location_split[0][1:]), float(start_location_split[1][:-1]))

            end_location_split = end_location.split(',')
            end_location = (float(end_location_split[0][1:]), float(end_location_split[1][:-1]))
        except ValueError:
            self.print_error('Something went wrong... Please check the input validity')
            return -1

        shortest_route = self.find_shortest_route(start_location, end_location)
        self.draw_route_map(start_location, end_location, shortest_route)
