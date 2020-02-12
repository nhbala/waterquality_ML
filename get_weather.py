import requests, json


def test_api():
    api_key = "56132dfa8c3dc4b5cb47372c76f9f618"
    complete_url = "https://api.darksky.net/forecast/" + api_key + "/" + "14.116667" + "," + "-86.866667" + "," + "1581545399?exclude=currently,flags"
    response = requests.get(complete_url)
    data_return = response.json()
    print(data_return)
if __name__=="__main__":
    test_api()
