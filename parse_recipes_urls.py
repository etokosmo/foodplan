import json
import time

import requests

URL = 'https://lenta.com/api/v1/magazinesearch/recipes/filter'
request_size = 100

if __name__ == "__main__":
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
        'Connection': 'keep-alive',
        'Content-Length': '182',
        'Content-Type': 'application/json',
        'Host': 'lenta.com',
        'Origin': 'https://lenta.com',
        'Referer': 'https://lenta.com/recepty/catalog-recepty/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': 'Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows'
    }

    recipe_urls = []
    offset = 0
    while True:
        payload = '''{{"searchValue": "", "filter": {{"tags": [], "ingredientIds": [], "ingredientsSearchValue": "",
                 "journalIds": [], "recipesSelectionId": "", "videoOnly": false}},
                 "sorting": null, "offset": {}, "limit": {} }}'''.format(offset, request_size)
        offset += request_size
        response = requests.post(URL, data=payload, headers=headers)
        response.raise_for_status()
        response_content = response.json()
        recipes_chunk = response_content.get('recipes')

        if not recipes_chunk:
            break

        for recipe in recipes_chunk:
            recipe_urls.append(recipe.get('url'))

        time.sleep(2)

    with open('recipes_urls.json', 'w', encoding='utf-8') as file:
        json.dump(recipe_urls, file)
