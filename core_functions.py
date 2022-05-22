import geopandas as gpd
import io
from geopy.distance import geodesic as gd
import requests
import folium
import openrouteservice as ors
import API_KEYS
class Core_Functions():

    def download_live_data(self):
        URL = 'http://bikeshare.metro.net/stations/json/'
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        headers = {"user-agent": USER_AGENT}  # adding the user agent
        resp = requests.get(URL, headers=headers)
        f = open("map_data.json", "w")
        f.write(resp.text)
        f.close()

    def parse_geo_data_stations(self):
        file = open('map_data.json')
        read = gpd.read_file(file)
        read = read.reset_index()
        # dictionary with neccesary informations  - street, location, num of available bikes, num of available bikes, distance from user (-1 for not count)
        station_info = {}
        for index, row in read.iterrows():
            coordinates = (row['latitude'], row['longitude'])
            station_info[row['addressStreet']] = {'coordinates': coordinates, 'bikes': row['bikesAvailable'],
                                                  'docks': row['docksAvailable'], 'distance': -1}

        return station_info

    # reset the distance info - the same structure might be used multiple times
    def reset_station_distance(station_info):
        for item in station_info.items():
            item[1]['distance'] = -1

    def find_nearest_stations_with_bikes(self, position, num_k):
            points = []
            self.download_live_data()
            k_stations = int(num_k)
            station_info = {}
            station_info = self.parse_geo_data_stations()
            splited = position.split(',')
            pos = (float(splited[0][1:]), float(splited[1][:-1]))
            map = folium.Map(location=pos, zoom_start=15)
            icon = folium.Icon(color="red")
            folium.Marker(location=[34.04862, -118.25874], icon=icon).add_to(map)
           # self.reset_station_distance(station_info)  # be sure that structure is empty and ready to use
            user_position = (position[0], position[1])
            for item in station_info.items():
                if item[1]['bikes'] > 0:  # count distance for stations with available bikes
                    item[1]['distance'] = gd(pos, item[1]['coordinates']).kilometers
            station_info = sorted(station_info.items(), key=lambda item: item[1]['distance'], reverse=False)
            # print the nearest stations -  skip the stations without distance
            station_counter = 0
            for item in station_info:
                if item[1]['distance'] != -1:
                    points.append(item[1]['coordinates'])
                    print(item)
                    station_counter += 1
                if station_counter == k_stations:  # check how many stations was already printed
                    break

            for point in range(0, len(points)):
                folium.Marker(points[point]).add_to(map)

            # folium.Marker([item[1]['coordinates'][0], item[1]['coordinates'][1]], icon=icon).add_to(map)
            map.save('index.html')
            data = io.BytesIO()
            map.save(data, close_file=False)

            return station_info