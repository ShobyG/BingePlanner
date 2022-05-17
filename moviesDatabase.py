import requests


def find_titles(movieTitle, size=10):
    size = int(size)
    url = "https://moviesdatabase.p.rapidapi.com/titles/search/title/"

    querystring = {"info": "mini_info", "limit": "10", "page": "1", "titleType": "movie"}

    headers = {
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com",
        "X-RapidAPI-Key": "2c5309d41amshd48304e086ef266p111a0bjsnf5f5f94a87b7"
    }

    response = requests.get(url + f"{movieTitle}")
    # response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    return print(response.text)
	# return (print(response.text))



    # year = int(year)
    # path = "https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday"
    # response = requests.get(path + "/births/" + monthDay)
    # data = response.json()
    # sortedbyClosestYear = sorted(data["births"], key=lambda i: abs(int(i['year']) - year))
	#
    # if len(sortedbyClosestYear) > size:
    #     sortedbyClosestYear = sortedbyClosestYear[0:size]
	#
    # for item in sortedbyClosestYear:
    #     item['thumbnail'] = "localhost"
	#
    #     if "thumbnail" in item['pages'][0]:
    #         item['thumbnail'] = item['pages'][0]["thumbnail"]["source"]
	#
    # return sortedbyClosestYear
