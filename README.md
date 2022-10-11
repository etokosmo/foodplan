# FoodPlan Service

## About

Service for providing recipes for the day, taking into account preferences.

## Website example

You can see this project [here]().

Order

![image](https://user-images.githubusercontent.com/93794917/195024418-fcc0cf36-87c5-4747-95d2-f6c5380c63e1.png)

Menu

![image](https://user-images.githubusercontent.com/93794917/195024504-6b7ed81e-9612-4d3a-b78d-6f0e47f4b15d.png)

Recipe

![image](https://user-images.githubusercontent.com/93794917/195024661-854d4361-1a83-4dbc-826b-a5941a305f54.png)


## API

You can send POST request to `http://<YOUR_DOMEN>/recipes/api/create`.

You can add recipe.

<details>
  <summary>Example</summary>

#### Request
`http://127.0.0.1:8000/recipes/api/create`

```json
{
    "title": "Соленая вода",
    "period": [{"period": "Обед"}, {"period": "Ужин"}],
    "image": "https://get.wallhere.com/photo/1920x1200-px-building-city-cityscape-Gold-Coast-1270905.jpg",
    "recipe": "1 шаг.<br>Высыпать соль в воду.<br>2 шаг.<br>Размешать соль в воде",
    "new_year_tag": "False",
    "calories": 1,
    "portions": 2,
    "food_category": "Classic",
    "recipe_ingredient": [
        {"ingredient": "Water",
         "amount": 10, "weight_type": "л"},
        {"ingredient": "Соль",
         "amount": 5, "weight_type": "ст.ложек"}
    ]
}
```
</details>

## Parser

* `parse_recipes_urls.py` - Parsing recipes from a foreign resource into a file.
* `parse_recipes.py` - Parsing recipes to your website.

## Configurations

* Python version: 3.10
* Libraries: [requirements.txt]()

## Launch

### Local server

- Download code
- Through the console in the directory with the code, install the virtual environment with the command:
```bash
python3 -m venv env
```

- Activate the virtual environment with the command:
```bash
source env/bin/activate
```

- Install the libraries with the command:
```bash
pip install -r requirements.txt
```

- Write the environment variables in the `.env` file in the format KEY=VALUE

`SECRET_KEY` - A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.

`ALLOWED_HOSTS` - A list of strings representing the host/domain names that this Django site can serve. This is a security measure to prevent HTTP Host header attacks, which are possible even under many seemingly-safe web server configurations.

`DEBUG` - A boolean that turns on/off debug mode. If your app raises an exception when DEBUG is True, Django will display a detailed traceback, including a lot of metadata about your environment, such as all the currently defined Django settings (from settings.py).

`DATABASE_URL` - URL to db. For more information check [this](https://github.com/jazzband/dj-database-url).

`MEDIA_URL` - URL that handles the media served from MEDIA_ROOT, used for managing stored files. It must end in a slash if set to a non-empty value.

`SBOL_SECRET_TOKEN` - Sberbank PAY TOKEN. For more information check [this](https://securepayments.sberbank.ru/wiki/doku.php/integration:paybutton:start).

`DRF_CREATE_URL` - API url to create orders with parser, e.g. `http://127.0.0.1:8000/recipes/api/create`.

- Create your database with the command:
```bash
python manage.py makemigrations
python manage.py migrate
```

- Run local server with the command (it will be available at http://127.0.0.1:8000/):
```bash
python manage.py runserver
```
