import json
import time

import requests
from bs4 import BeautifulSoup
from environs import Env


def parse_ingredient(text):
    splitted_string = text.strip().split()
    first_word = splitted_string[0].replace(',', '.')
    if is_float(first_word):
        amount = float(first_word)
        weight_type = ' '.join(splitted_string[1:])
        return amount, weight_type
    return None, ' '.join(splitted_string)


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def parse_calories(text):
    splitted_string = text.strip().split()
    if splitted_string[0].isnumeric():
        return int(splitted_string[0])


def parse_tags(soup):
    tags = [tag.attrs.get('value') for tag in soup.select('.recipe-tags__item')]
    return tags


def get_recipe_periods(tags):
    tags_str = ' '.join(tags)
    periods = []
    if 'obed' in tags_str:
        periods.append({"period": "Обед"})
    if 'uzhin' in tags_str:
        periods.append({"period": "Ужин"})
    if 'zavtrak' in tags_str:
        periods.append({"period": "Завтрак"})
    return periods


def get_food_category(tags):
    tags_str = ' '.join(tags)
    if 'vegatarianskoe' in tags_str:
        return 'Вегетарианское'
    elif 'keto' in tags_str:
        return 'Кето'
    elif 'nizkokalorijjnoe' in tags_str:
        return 'Низкокалорийное'
    else:
        return 'Классическое'


def is_new_year_tag_contained(tags):
    tags_str = ' '.join(tags)
    return 'novyjj-god' in tags_str


def parse_recipe(url):
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    soup = BeautifulSoup(
        response.text.replace('\r', '').replace('\n', '').replace('&#160;', ' ').replace('&#173;', ''),
        'lxml'
    )

    recipe = {}
    recipe_tags = parse_tags(soup)
    recipe['title'] = soup.select_one('title').get_text()
    recipe['period'] = get_recipe_periods(recipe_tags)
    recipe['portions'] = int(soup.select_one('.recipe-portions__portion').get_text().strip())
    calories_tag = soup.select_one('.recipe-nutritional-cell__sub-value')
    recipe['calories'] = parse_calories(calories_tag.get_text()) if calories_tag else 0
    recipe['image'] = soup.select_one('.recipe-main-header__image-source').get('src').split('?')[0]
    recipe['food_category'] = get_food_category(recipe_tags)
    recipe['new_year_tag'] = is_new_year_tag_contained(recipe_tags)

    steps = []
    recipe_steps_soup = soup.select('.recipe-step__content-wrapper')
    for step in recipe_steps_soup:
        step_title = step.select_one('.recipe-step__title').get_text().strip()
        step_description = step.select_one('.recipe-step__description').get_text().strip()
        steps.append('<br>'.join(['<b>{}</b>'.format(step_title), step_description]))

    recipe['recipe'] = '<br>'.join(steps)

    recipe['recipe_ingredient'] = []
    ingredient_rows = soup.select('.recipe-ingredients-list-row')
    for ingredient_row in ingredient_rows:
        ingredient = {}
        ingredient['ingredient'] = ingredient_row.select_one('.recipe-checkbox__label').get_text()
        ingredient['amount'], ingredient['weight_type'] = parse_ingredient(
            ingredient_row.select_one('.recipe-ingredients-list-row__value').get_text()
        )
        recipe['recipe_ingredient'].append(ingredient)
    return recipe


def get_headers():
    return {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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


def send_recipe(url, recipe):
    response = requests.post(
        url,
        headers={'Content-Type': 'application/json'},
        json=recipe,
    )
    response.raise_for_status()


if __name__ == "__main__":
    env = Env()
    env.read_env()
    django_api = env.str('DRF_CREATE_URL')


    with open('recipes_urls.json', 'r', encoding='utf-8') as file:
        recipe_urls = json.load(file)

    for recipe_url in recipe_urls:
        try:
            recipe = parse_recipe(recipe_url)
            send_recipe(django_api, recipe)
            print(recipe['title'])
            # with open('./parse/{}.json'.format(recipe['title']), 'w', encoding='utf-8') as file:
            #     json.dump(recipe, file, ensure_ascii=False)
            # print(recipe['title'])
        except Exception as err:
            time.sleep(1)

