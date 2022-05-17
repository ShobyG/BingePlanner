import requests

url = "https://moviesdatabase.p.rapidapi.com/titles/search/title/%7Btitle%7D"

querystring = {"info":"mini_info","limit":"10","page":"1","titleType":"movie"}

headers = {
	"X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com",
	"X-RapidAPI-Key": "76204ae464msh253ccc81519645cp1cfe49jsnf0ceabcd4b11"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)