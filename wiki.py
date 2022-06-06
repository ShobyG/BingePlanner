import requests


def find_titles(movieTitle):
    url = f"https://imdb-api.com/API/AdvancedSearch/k_7pwb2ci4?title={movieTitle}"

    response = requests.get(url)

    data = response.json()
    # print(data)
    results = data['results']

    # runtime = int(data["results"][0]["runtimeStr"])

    return results


def most_popular_movies():
    url = "https://imdb-api.com/en/API/MostPopularMovies/k_7pwb2ci4"
    response = requests.get(url)
    data = response.json()
    results = data['items']
    return results


def most_popular_series():
    url = "https://imdb-api.com/en/API/MostPopularTVs/k_7pwb2ci4"
    response = requests.get(url)
    data = response.json()
    results = data['items']
    return results


def top_250_movies():
    url = "https://imdb-api.com/en/API/Top250Movies/k_7pwb2ci4"
    response = requests.get(url)
    data = response.json()
    results = data['items']
    return results


def box_office():
    url = "https://imdb-api.com/en/API/BoxOffice/k_7pwb2ci4"
    response = requests.get(url)
    data = response.json()
    results = data['items']
    return results


def top_250_series():
    url = "https://imdb-api.com/en/API/Top250TVs/k_7pwb2ci4"
    response = requests.get(url)
    data = response.json()
    results = data['items']
    return results


def find_id(imdbID):
    url = f"https://imdb-api.com/en/API/Title/k_7pwb2ci4/{imdbID}"

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

def find_season_episodes(imdbID, season_no):
    url = f"https://imdb-api.com/en/API/SeasonEpisodes/k_7pwb2ci4/{imdbID}/{season_no}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()
    # results = data[]
    # return print(results)
    # # return data
    # print(data)
    return data

# myData = []
if __name__ == '__main__':
    # j = find_id('tt8740790')
    # print(j['tvSeriesInfo']['seasons'])
    # i = find_season_episodes('tt8740790', '2')
    # print(i)
    print(box_office())
    print(top_250_movies())
    print(most_popular_movies())
