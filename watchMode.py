import urllib.request
import json
import requests




#find episdoes
# with urllib.request.urlopen("https://api.watchmode.com/v1/title/345534/episodes/?apiKey"
#                             "=BXNA5ljscb6j63EwJBgc8C6dfr97DiVplN1j1SAi") as url:

# data = json.loads(url.read().decode())
# print(data)

url = "https://api.watchmode.com/v1/title/345534/episodes/?apiKey=BXNA5ljscb6j63EwJBgc8C6dfr97DiVplN1j1SAi"
response = requests.request("GET", url)

print(response.text)

