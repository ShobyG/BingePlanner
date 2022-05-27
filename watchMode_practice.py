import urllib.request
import json


def findTitles(titles):
    with urllib.request.urlopen(f"https://api.watchmode.com/v1/list-titles/?apiKey=BXNA5ljscb6j63EwJBgc8C6dfr97DiVplN1j1SAi&source_ids=203,57") as url:
        data = json.loads(url.read().decode())
    print(data)

if __name__ == '__main__':
    findTitles("buffy")