import requests
def replaceEmptyImages(dictList, url):
    for d in dictList:
        if ("image-url" not in d or not d["image-url"]):
            d["image-url"]=url


def find_coffee():
    # client_id = "KqEICZ5PUU3UERU-I2ShWg"
    api_key = 'jiiT7hYQYWL3KbCv1oriJMjU8L09vx17EgPDnWDDZi24TkHSFxFKur-XfS6qxGQl0ISx9Fa6LtHpg0ICKwAob9gZj4ME8-iWL63GUZCK' \
              'RQrMzSAxx5rIhFLXoed6YnYx'
    headers = {'Authorization': 'Bearer {}'.format(api_key)}
    search_api_url = 'https://api.yelp.com/v3/businesses/search'
    params = {'term': 'coffee shop', 'location': 'Tacoma, Washington', 'limit': 50}
    response = requests.get(search_api_url, headers=headers, params=params, timeout=5)
    data = response.json()
    sortedRating = sorted(data['businesses'], key=lambda i: i['rating'], reverse=True)
    replaceEmptyImages(sortedRating, "localhost")
    return sortedRating
