import requests


def find_titles(movieTitle):
    # url = f"https://imdb-api.com/API/AdvancedSearch/k_w5d8b9r3?title={movieTitle}"
    # url = f"https://imdb-api.com/API/AdvancedSearch/k_z7g2vpw7?title={movieTitle}"
    # url = f"https://imdb-api.com/API/AdvancedSearch/k_7pwb2ci4?title_type=feature,tv_movie,tv_series,tv_episode={movieTitle} "
    url = f"https://imdb-api.com/API/AdvancedSearch/k_qwzf296o?title={movieTitle}"

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
    url = f"https://imdb-api.com/en/API/Title/k_qwzf296o/{imdbID}"
    
    

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


def find_episodes(imdbID, season):
    # url = f"https://imdb-api.com/en/API/SeasonEpisodes/k_w5d8b9r3/{imdbID}/{season}"
    # url = f"https://imdb-api.com/en/API/SeasonEpisodes/k_z7g2vpw7/{imdbID}/{season}"
    url = f"https://imdb-api.com/en/API/SeasonEpisodes/k_qwzf296o/{imdbID}/{season}"

    response = requests.request("GET", url)

    data = response.json()

    print(f"EPISODE DATA: SEASON {season}: {data}")

    return data


# myData = []
if __name__ == '__main__':
    i = find_id("tt0162065")
    print(i)