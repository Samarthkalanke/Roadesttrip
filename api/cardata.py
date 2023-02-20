import requests

url = "https://car-data.p.rapidapi.com/cars"

querystring = {"limit":"10","page":"0"}

headers = {
	"X-RapidAPI-Key": "8e39206459msh63119b14325b472p1a320bjsnac696cb1d4af",
	"X-RapidAPI-Host": "car-data.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)