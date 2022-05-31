import requests


def find_specific_titles(movieTitle, imdbID):
    # url = "https://imdb-api.com/en/API/SearchSeries/k_aaaaaaaa/angel"
    # url = "https://imdb-api.com/en/API/SearchSeries/k_7pwb2ci4/angel"
    # url = f"https://imdb-api.com/en/API/SearchSeries/k_7pwb2ci4/{movieTitle}"

    # k_7x1fyzmq
    # url = f"https://imdb-api.com/API/AdvancedSearch/k_7pwb2ci4?title={movieTitle}"
    url = f"https://imdb-api.com/API/AdvancedSearch/k_z7g2vpw7?title={movieTitle}"

    # url_season = "https://imdb-api.com/en/API/SearchEpisode/k_aaaaaaaa/Welcome to the Hellmouth"

    # response = requests.request("GET", url)
    response = requests.get(url)

    data = response.json()
    # print(data["results"][3]["id"])

    results = data['results']

    for x in range(len(results)):
        if data["results"][x]["id"] == imdbID:
            soughtData = data["results"][x]
            # return print(soughtData)
            return soughtData

        else:
            pass

    # return data

    # print(data)
    # print(data[0])

    # print(data["results"][0]["image"])
    # print(data["results"][0]["title"])
    # print(data["results"][0]["id"])
    # print(data["results"][0]["runtimeStr"])
    # print(data["results"][0]["imDbRating"])

    # runtime = int(data["results"][0]["runtimeStr"])

    # imdb_ID = data["results"][0]["id"]

    # print(data)


def find_season(imdb_ID, seasons):
    # seasons = 1
    episodes = 0
    url = f"https://imdb-api.com/en/API/SeasonEpisodes/k_7pwb2ci4/{imdb_ID}/{seasons}"

    response = requests.get(url)
    data = response.json()

    results = data["episodes"]

    for i in range(len(results)):
        if data["episodes"][i]["id"] == imdb_ID:
            # for i in range(len(data["seasonNumber"])):

            for seasons in range(len(data["episodes"]["seasonNumber"])):

                for episodes in range(len(data["episodes"]["episodeNumber"])):
                    episodes += 1
                    if data["episodeNumber"] is None:
                        seasons += 1

        return data["seasonNumber", "episodeNumber"]


if __name__ == '__main__':
    find_specific_titles("angel", "tt0162065")
    # find_season("tt0162065", "1")



# def runTime(movieTitle):
#     # find_titles(movieTitle=input())
#     url = f"https://imdb-api.com/API/AdvancedSearch/k_7pwb2ci4?title={movieTitle}"
#     response = requests.get(url)
#
#     data = response.json()
#     runtime = data["results"][0]["runtimeStr"]
#     runtime = runtime.replace(" min", "")
#     # print(runtime)
#     runtime = int(runtime)
#
#     transTime = runtime
#     userTime = int(input())
#
#     print("Hi")
#     while int(runtime) > 0:
#         if int(runtime) > 0:
#             print(f"please input how much time you wish to binge in minutes:, {int(userTime)}")
#             print(runtime)
#         # if userTime <= runtime:
#         #     print(f"please input how much time you wish to binge in minutes:, {userTime}")
#
#             runtime = int(transTime) - int(userTime)
#             transTime = int(runtime)
#
#             print(runtime)
#
#         # elif userTime is not int:
#         #     print(f"Error!!! Please input a number: {userTime}")
#         else:
#             print(f"Error!!! You've gone over the the allotted time for your binge (you have {runtime} minutes left!). "
#                   f"Please input a new amount:, {userTime}")
#
#
#     print(data)


# if __name__ == '__main__':
#     find_specific_titles("angel", "tt0162065")
# runTime("angel", "43")
# runTime("angel")


# def display_episodes(movieTitle, imdb_ID):
#     url = f"https://imdb-api.com/en/API/SearchSeries/k_7pwb2ci4/{movieTitle}"
#     find_titles(movieTitle)
#     response = requests.get(url)
#
#     data = response.json()
#     imdb_ID = data["results"][0]["id"]
#
#
# # myData = []


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
