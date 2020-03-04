import requests, json
import time
import firebase_testing
from datetime import datetime, timedelta

class Plant:
    """
    """
    def __init__(self, name, coords, watershed = (0.0,0.0)):
        assert type(name) == str

        assert type(coords) == tuple
        assert type(coords[0]) == float
        assert type (coords[1]) == float

        assert type(watershed) == tuple
        assert type (watershed[0]) == float
        assert type(watershed[1]) == float

        self.name = name
        self.coords = coords
        self.watershed = watershed

    def get_coords(self):
        return self.coords

"""
Primary class for weather api
"""
class Weather:
    """
    """


    def __init__(self):
        self.db = {"moroceli": Plant("Moroceli", (14.148560659841669,-86.73088073730469))}
        self.api_key = "56132dfa8c3dc4b5cb47372c76f9f618"

    def general_call(self, plant_name, when):
        assert type(when) == datetime

        plant_name = plant_name.lower()
        plant_coords = self.db[plant_name].get_coords()
        unixtime = time.mktime(when.timetuple())
        print(int(unixtime))
        complete_url = "https://api.darksky.net/forecast/"+self.api_key+"/"+str(plant_coords[0])+","+str(plant_coords[1])+","+str(int(unixtime))+ "?exclude=currently,flags"
        print(complete_url)
        response = requests.get(complete_url)
        return response.json()


if __name__=="__main__":
    weather = Weather()
    data = firebase_testing.get_graph_data()
    moroceli_data = data['Moroceli']
    for data_point in moroceli_data:
        date = data_point['timeFinished']
        t_index = date.index("T")
        final_date = date[:t_index]
        final_time = date[t_index + 1: -1]
        final_total_date = final_date + " " + final_time
        datetime_object = datetime.strptime(final_total_date, '%Y-%m-%d %H:%M:%S.%f')
        curr_weather = weather.general_call("moroceli", datetime_object - timedelta(hours=2))
        print(curr_weather)
        first_point = curr_weather['hourly']['data'][0]
        #how to get data?
        curr_percep_intensity = first_point.get('precipIntensity', -1)
        curr_pressure = first_point.get('pressure', 1)
        print(curr_percep_intensity)
        print(curr_pressure)
        break
