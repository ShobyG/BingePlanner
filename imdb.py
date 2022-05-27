import requests


def find_titles_k(movieTitle):
    # url = "https://imdb-api.com/en/API/SearchSeries/k_aaaaaaaa/angel"
    # url = "https://imdb-api.com/en/API/SearchSeries/k_7pwb2ci4/angel"
    # url = f"https://imdb-api.com/en/API/SearchSeries/k_7pwb2ci4/{movieTitle}"
    # url_season = "https://imdb-api.com/en/API/SearchEpisode/k_aaaaaaaa/Welcome to the Hellmouth"

    url = f"https://imdb-api.com/API/AdvancedSearch/k_7pwb2ci4?title={movieTitle}"

    response = requests.get(url)

    data = response.json()
    # return data

    results = data['results']
    return results


    # print(data)
    # print(data[0])

    # print(data["results"][0]["image"])
    # print(data["results"][0]["title"])

    # print(response.text)

# myData = []
if __name__ == '__main__':
    find_titles_k("angel")



    # print(response.text)

# import requests
#
# url = "https://moviesdatabase.p.rapidapi.com/titles/search/title/%7Btitle%7D"
#
# querystring = {"info":"mini_info","limit":"10","page":"1","titleType":"movie"}
#
# headers = {
# 	"X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com",
# 	"X-RapidAPI-Key": "76204ae464msh253ccc81519645cp1cfe49jsnf0ceabcd4b11"
# }
#
# response = requests.request("GET", url, headers=headers, params=querystring)
#
# print(response.text)
