import requests


def find_titles(movieTitle):
    url = f"https://imdb-api.com/API/AdvancedSearch/k_7x1fyzmq?title={movieTitle}"
    # url = f"https://imdb-api.com/API/AdvancedSearch/k_7pwb2ci4?title_type=feature,tv_movie,tv_series,tv_episode={movieTitle} "

    response = requests.get(url)

    data = response.json()
    print(data)
    results = data['results']

    # runtime = int(data["results"][0]["runtimeStr"])

    return results

    # return data

    # print(data)
    # print(data[0])

    # print(data["results"][0]["image"])
    # print(data["results"][0]["title"])

    # print(response.text)


def find_id(imdbID):
    url = f"https://imdb-api.com/en/API/Title/k_7x1fyzmq/{imdbID}"

    response = requests.request("GET", url)

    data = response.json()
    # results = data[]
    # return print(results)
    # return data
    print(data)
    title = data['title']

    return data

    # results = data['results']
    # return results

def find_season_episodes(imdbID, season_no):
    url = f"https://imdb-api.com/en/API/SeasonEpisodes/k_7x1fyzmq/{imdbID}/{season_no}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()
    # results = data[]
    # return print(results)
    # return data
    print(data)
    return data

# myData = []
if __name__ == '__main__':
    j = find_id('tt8740790')
    print(j['tvSeriesInfo']['seasons'])
    i = find_season_episodes('tt8740790', '2')
    print(i)

