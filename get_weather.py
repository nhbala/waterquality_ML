import requests, json
import time
import datetime

"""
This class represents an instance of a water treament plant and contains information
about it, specifically its name, coordinates, and the coordinates of its watershed,
defaulted to 0,0 if not inputted.
"""
class Plant:
    """
    Constructs an object of class Plant with name, coordinates, and coordinates of watershed
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

    def get_watershed(self):
        return self.watershed

"""
Primary class for weather api
"""
class Weather:
    """
    Constructs an object of class Weather through which useful methods are called
    """
    def __init__(self):
        self.db = {"moroceli": Plant("Moroceli", (14.116667,-86.866667))}
        self.api_key = "56132dfa8c3dc4b5cb47372c76f9f618"

    """
    Returns the json containing weather information at specified plant's watershed and time
    """
    def general_call(self, plant_name, when):
        assert type(when) == datetime.datetime

        plant_name = plant_name.lower()
        plant_coords = self.db[plant_name].get_watershed()
        unixtime = time.mktime(when.timetuple())
        complete_url = "https://api.darksky.net/forecast/"+self.api_key+"/"+str(plant_coords[0])+","+str(plant_coords[1])+","+str(int(unixtime))+ "?exclude=currently,flags"
        response = requests.get(complete_url)
        print(type(response))
        return response.json()

    def spec_call(self, param, plant_name, when):
        big_dict = self.general_call(plant_name, when)


if __name__=="__main__":
    weather = Weather()
    print(weather.general_call("moroceli", datetime.datetime(1999,6,7)))
    #weather.spec_call("precipitation", "moroceli", datetime.datetime(1999,6,7))
