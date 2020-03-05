import requests, json
import time
import firebase_testing
from datetime import datetime, timedelta
from sklearn import cluster


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
        assert type(when) == datetime

        plant_name = plant_name.lower()
        plant_coords = self.db[plant_name].get_coords()
        unixtime = time.mktime(when.timetuple())
        complete_url = "https://api.darksky.net/forecast/"+self.api_key+"/"+str(plant_coords[0])+","+str(plant_coords[1])+","+str(int(unixtime))+ "?exclude=currently,flags"
        response = requests.get(complete_url)
        print(type(response))
        return response.json()

    def spec_call(self, param, plant_name, when):
        big_dict = self.general_call(plant_name, when)

def clusters(param_list):
    weather = Weather()
    data = firebase_testing.get_graph_data()
    moroceli_data = data['Moroceli']
    data_matrix = []
    total = 0
    curr_point = 0
    for i in range(len(moroceli_data)):
        # Only take every 100 data points
        if i % 100 != 0:
            i += 1
            continue
        data_point = moroceli_data[i]
        date_1 = data_point['timeFinished']
        t_index = date_1.index("T")
        final_date = date_1[:t_index]
        final_time = date_1[t_index + 1: -1]
        final_total_date = final_date + " " + final_time
        datetime_object = datetime.strptime(final_total_date, '%Y-%m-%d %H:%M:%S.%f')
        curr_weather = weather.general_call("moroceli", datetime_object - timedelta(hours=1))
        first_point = curr_weather['hourly']['data'][0]

        curr_point = []
        for str in param_list:
            curr_point.append(first_point.get(str, -1))
        data_matrix.append(curr_point)
        total += 1
        if total >= 50:
            break
    kmeans = cluster.KMeans(random_state=0).fit(data_matrix)

    cluster_dict = {}
    for i in range(len(data_matrix)):
        current_cluster = kmeans.labels_[i]
        curr_val = data_matrix[i]
        if current_cluster not in cluster_dict:
            cluster_dict[current_cluster] = [data_matrix[i]]
        new_lst = cluster_dict[current_cluster]
        new_lst.append(data_matrix[i])
        cluster_dict[current_cluster] = new_lst

    print(cluster_dict)


if __name__=="__main__":
    params = ["precep_intensity", "pressure", "windSpeed", "temperature", "rawWaterTurbidity", "settledWaterTurbidity"]
    clusters(params)
