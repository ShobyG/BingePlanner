import requests

# api_key = "k_w5d8b9r3"
# api_key = "k_z7g2vpw7"
api_key = "k_7pwb2ci4"
# api_key = "k_qwzf296o"
# api_key = "k_yc1e8szx"
# api_key = "k_7x1fyzmq"

def find_titles(movieTitle):
    # url = f"https://imdb-api.com/API/AdvancedSearch/k_w5d8b9r3?title={movieTitle}"
    # url = f"https://imdb-api.com/API/AdvancedSearch/k_z7g2vpw7?title={movieTitle}"
    # url = f"https://imdb-api.com/API/AdvancedSearch/k_7pwb2ci4?title_type=feature,tv_movie,tv_series,tv_episode={movieTitle} "
    # url = f"https://imdb-api.com/API/AdvancedSearch/k_qwzf296o?title={movieTitle}"
    url = f"https://imdb-api.com/API/AdvancedSearch/{api_key}?title={movieTitle}"

    response = requests.get(url)

    data = response.json()
    # print(data)
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
    # url = f"https://imdb-api.com/en/API/Title/k_7pwb2ci4/{imdbID}"
    # url = f"https://imdb-api.com/en/API/Title/k_w5d8b9r3/{imdbID}"
    # url = f"https://imdb-api.com/en/API/Title/k_z7g2vpw7/{imdbID}"
    # url = f"https://imdb-api.com/en/API/Title/k_qwzf296o/{imdbID}"
    url = f"https://imdb-api.com/en/API/Title/{api_key}/{imdbID}"
    

    response = requests.request("GET", url)

    data = response.json()
    # results = data[]
    # return print(results)
    # return data
    # print(data)
    title = data['title']
    return data

    # results = data['results']
    # return results


def find_episodes(imdbID, season):
    # url = f"https://imdb-api.com/en/API/SeasonEpisodes/k_w5d8b9r3/{imdbID}/{season}"
    # url = f"https://imdb-api.com/en/API/SeasonEpisodes/k_z7g2vpw7/{imdbID}/{season}"
    # url = f"https://imdb-api.com/en/API/SeasonEpisodes/k_qwzf296o/{imdbID}/{season}"
    # url = f"https://imdb-api.com/en/API/SeasonEpisodes/k_yc1e8szx/{imdbID}/{season}"
    url = f"https://imdb-api.com/en/API/SeasonEpisodes/{api_key}/{imdbID}/{season}"



    response = requests.request("GET", url)

    data = response.json()

    # print(f"EPISODE DATA: SEASON {season}: {data}")

    return data

def find_season_episodes(imdbID, season_no):
    # url = f"https://imdb-api.com/en/API/SeasonEpisodes/k_7x1fyzmq/{imdbID}/{season_no}"
    url = f"https://imdb-api.com/en/API/SeasonEpisodes/{api_key}/{imdbID}/{season_no}"



    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()
    # results = data[]
    # return print(results)
    # return data
    # print(data)
    return data

if __name__ == '__main__':
    # j = find_id('tt8740790')
    j = find_id('tt18928124')
    print(j)
    print(j['tvSeriesInfo']['seasons'])
    i = find_season_episodes('tt8740790', '2')
    print(i)
