import urllib.request
import json
import requests



def find_length_of_series():

    #find episdoes
    # with urllib.request.urlopen("https://api.watchmode.com/v1/title/345534/episodes/?apiKey"
    #                             "=BXNA5ljscb6j63EwJBgc8C6dfr97DiVplN1j1SAi") as url:

    # data = json.loads(url.read().decode())
    # print(data)

    url = "https://api.watchmode.com/v1/title/345534/episodes/?apiKey=BXNA5ljscb6j63EwJBgc8C6dfr97DiVplN1j1SAi"
    response = requests.get(url)
    # print(response.text)
    data = response.json()

    print(data[0]["id"])
    # print(data[0]["runtime_minutes"])

    season_num = print(data[0]["season_number"])
    imdb_ID = data[0]["imdb_id"]
    running_time = print(data[0]["runtime_minutes"])


    season = 0
    episode = 0
    for season in range(100):
        if imdb_ID is None:
            pass
        elif season_num is None:
            pass
        else:
            season += 1
            imdb_ID = data[season]["imdb_id"]
            for episode in range(100):
                if imdb_ID is None:
                    pass
                elif season_num is None:
                    pass
                else:
                    episode += 1
                    imdb_ID = data[episode]["imdb_id"]
                    running_time = print(episode["runtime_minutes"])
                    return (print(running_time))

    # print(f"{season}, {episode}")
    # print(data)
    #
    # print(data[0]["id"])
    # print(data[0]["runtime_minutes"])



if __name__ == '__main__':
    find_length_of_series()

