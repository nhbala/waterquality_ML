import requests, json
import time
import datetime


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
        self.db = {"moroceli": Plant("Moroceli", (14.116667,-86.866667))}
        self.api_key = "56132dfa8c3dc4b5cb47372c76f9f618"

    def general_call(self, plant_name, when):
        assert type(when) == datetime.datetime

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
    print(weather.general_call("moroceli", datetime.datetime(1999,6,7)))
