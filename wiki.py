import requests


def find_titles(movieTitle):
    url = f"https://imdb-api.com/API/AdvancedSearch/k_7pwb2ci4?title={movieTitle}"
    # url = f"https://imdb-api.com/API/AdvancedSearch/k_7pwb2ci4?title_type=feature,tv_movie,tv_series,tv_episode={movieTitle} "

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
    url = f"https://imdb-api.com/en/API/Title/k_7pwb2ci4/{imdbID}"

    response = requests.request("GET", url)

    data = response.json()
    # results = data[]
    # return print(results)
    # return data
    print(data)
    title = data['title']
    return title

    # results = data['results']
    # return results


# myData = []
if __name__ == '__main__':
    i = find_id("tt0162065")
    print(i)