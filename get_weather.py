import requests, json


def five_day_weather(city):
    api_key = "7dee77df9de9d65a1de03be656176254"
    country = "HN"
    complete_url = "https://api.openweathermap.org/data/2.5/forecast?q=" + city + "," + country + "uk&appid=" + api_key
    response = requests.get(complete_url)
    data_return = response.json()
    weather_data = data_return['list']
    index = 2
    rain_index = []
    while index < len(weather_data):
        weather_dic = (weather_data[index])['weather']
        print(weather_dic[0]['main'] )
        if weather_dic[0]['main'] == 'Rain':
            rain_index.append(True)
        else:
            rain_index.append(False)
        index += 8
    return rain_index
