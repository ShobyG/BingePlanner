import requests

def find_titles(movieTitle):
    url = f"https://imdb-api.com/en/API/SearchSeries/k_7pwb2ci4/{movieTitle}"
    response = requests.get(url)

    data = response.json()
    results = data['results']

    return results

# def srchIMDB(srch_str): 
#     url = "https://imdb-api.com/en/API/SearchMovie/k_z7g2vpw7/" + srch_str
    
#     payload = {}
#     headers= {}
    
#     response = requests.request("GET", url, headers=headers, data = payload)
#     data=response.json()

#     # print(data)
#     print(response.text.encode('utf8'))    

if __name__ == "__main__":

    tmp = find_titles("Stranger")    
    
