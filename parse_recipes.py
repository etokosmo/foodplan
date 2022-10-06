import json
import requests
import unidecode
import unicodedata

from bs4 import BeautifulSoup


def parse_ingredient_value(text):
    splitted_string = text.strip().split()
    if splitted_string[0].isnumeric():
        amount = int(splitted_string[0])
        weight_type = ' '.join(splitted_string[1:])
        return amount, weight_type
    return None, ' '.join(splitted_string)


if __name__ == "__main__":

    headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
      'Cache-Control': 'max-age=0',
      'Connection': 'keep-alive',

      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'none',
      'Sec-Fetch-User': '?1',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
      'sec-ch-ua': 'Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': 'Windows'
    }

    with open('recipes_urls.json', 'r', encoding='utf-8') as file:
        recipe_urls = json.load(file)

    recipes = []
    for recipe_url in recipe_urls:
        response = requests.get(recipe_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(
            response.text.replace('\r', '').replace('\n', '').replace('&#160;', ' '),
            'lxml'
        )

        recipe = {}
        recipe['title'] = soup.select_one('title').get_text()
        recipe['portions'] = int(soup.select_one('.recipe-portions__portion').get_text().strip())

        recipe['ingredients'] = []
        ingredient_rows = soup.select('.recipe-ingredients-list-row')
        for ingredient_row in ingredient_rows:
            ingredient = {}
            ingredient['title'] = ingredient_row.select_one('.recipe-checkbox__label').get_text()
            ingredient['amount'], ingredient['weight_type'] = parse_ingredient_value(
                ingredient_row.select_one('.recipe-ingredients-list-row__value').get_text()
            )
            recipe['ingredients'].append(ingredient)



        print(recipe)


        break