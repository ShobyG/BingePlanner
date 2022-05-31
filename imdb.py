import requests


def find_titles(movieTitle):
    # k_7x1fyzmq
    url = f"https://imdb-api.com/API/AdvancedSearch/k_7pwb2ci4?title={movieTitle}"
    # url = f"https://imdb-api.com/API/AdvancedSearch/k_z7g2vpw7?title={movieTitle}"

    # url = f"https://imdb-api.com/API/AdvancedSearch/k_7pwb2ci4?title_type=feature,tv_movie,tv_series,tv_episode={movieTitle} "

    response = requests.get(url)

    data = response.json()
    # print(data)
    results = data['results']

    # print(data)


    # runtime = int(data["results"][0]["runtimeStr"])

    return results

    # return data

    # print(data[0])

    # print(data["results"][0]["image"])
    # print(data["results"][0]["title"])

    # print(response.text)


def find_id(imdbID):
    url = f"https://imdb-api.com/en/API/Title/k_7pwb2ci4/{imdbID}"

    response = requests.get(url)

    data = response.json()
    # results = data[]
    # return print(results)
    # return data

    return print(data)

    # results = data['results']
    # return results


# myData = []

# if __name__ == '__main__':
#     find_titles("angel")
#     find_id("tt0162065")
