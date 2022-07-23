# Dating-Site-API

API-сервис для сайта знакомств.
</br>Хост развернутого проекта: https://manydates.ml
<hr><br>

# Концепция
1. Пользователи регистрируются и проходят авторизацию по логину и паролю.
2. Модели пользователей имеют обязательные поля:
<br>аватар | пол | имя и фамилия | электронная почта | долгота и широта
<br>**на картинку аватара при регистрации накладывается водяной знак.*
3. Авторизованные пользователь должны иметь возможность:
<br>1) отмечать понравившихся пользователей. Если возникает взаимная <br>симпатия, то на емеил обоих отправляется уведомление об этом.
<br>2) выводить и фильтровать список всех пользователей по полу, имени, <br>фамилии, а также выводить пользователей в пределах заданной дистанции. 
4. Запросы к БД должны быть оптимизированы.
<br><br>

# Краткое описание проекта
## Особенности
<li>Полная интеграция с Docker Compose для продакшн и локальной разработки.
<li>HTTP-сервер Docker на базе Nginx.
<li>WSGI-сервер ***Gunicorn***.
<li>Django REST API backend.
<li>Кэширование в контейнере Docker с Redis.
<li>Автоматическая интерактивная документация Swagger, совместимая открытыми стандартами для API: Open API и JSON Schema.
<li>Автоматическая генерация DJANGO SECRET KEY при развертывании проекта.
<li>Безопасное хэширование паролей по умолчанию.
<li>Расширения PostGIS для базы данных сразу встроены в docker-образ.
<li>Включен CORS.
<li>Интеграция с Sentry.
<li>GitHub CI (непрерывная интеграция).
<li>Сервис использует SMPT-сервер **mail.ru**
<li>Заполнение базы данных фиктивными данными одной командой.
<br><br>

## Перспективные доработки проекта
<li>Настроить оптимальное логгирование.
<li>Поставить проект при развертывании на "колёса" - python wheels.
<li>Перенести и спрятать админку.
<li>Улучшить web-безопасность сервиса.
<li>Добавить интеграцию frontend.
<li>Добавить балансировку нагрузки между интерфейсом и бэкендом с помощью Traefik.
<li>Создать demo-фронтенд в отдельном контейнере.
<br><br>

# Технологии
    Django 4.0.2
    Django REST framework 3.13.1
    Python 3.10.5
    Redis 4.2.2
<br>

# Запуск и работа с проектом
## Разворачиваем проект
1) На GitHub делаем себе ***fork*** и клонируем репозиторий через протокол HTTPS или SSH (не забываем создать виртуальное окружение), например:
```python
git clone https://github.com/<your-github-profile>/dating-site
```
2) Создаём файл с секретами ```.env.local``` и ```.env.prod``` из копии ```.env.example``` в папке проекта ```./.envs/```
3) Собраем контейнеры локально:
```python
docker-compose -f docker-compose.local.yaml up -d --build
```
Или на хосте:
```python
docker-compose -f docker-compose.prod.yaml up -d --build
```

При успешном создании контейнеров в терминале должен быть статус в терминале:
```
    Successfully tagged dating-site_nginx:latest
    Creating dating-site_db_1    ... done
    Creating dating-site_redis_1 ... done
    Creating dating-site_web_1   ... done
    Creating dating-site_nginx_1 ... done
    Attaching to dating-site_db_1, dating-site_redis_1, dating-site_web_1, dating-site_nginx_1
```
<br>

## Тестирование API
Можно использовать встроенный Swagger или направить HTTP-запросы в соответствии с правами доступа и эндпоинтам через любой инструмент тестирования.
<br>Для созданя фиктивных данных исользуйте команду управления ***manage.py***:
```python
python manage.py dummy_data_maker
```
<br>

# Ресурсы сервиса

## На сервисе доступны эндпоинты:
1) Регистрация нового клиента:
</br><code>
    /api/clients/create/
</code>

2) Оценивание участником другого участника: 
</br><code>
    /api/clients/{client_id}/match/
</code>

3) Просмотр списка участников:
</br><code>
    /api/list/
</code>

## Фильтрация списка 
Фильтрацию списка можно произвести по полу, имени, фамилии,
<br>а также фильтровать участников в пределах заданной дистанции <br>относительно авторизованного пользователя.
<br><br>
Для фильтрации списка участников используйте ключи в соотвествии с таблицей:
Фильтр             | Ключ
-------------------|-----------------------|
 по полу:          | /?gender=
 по имени:         | /?first_name=
 по фамилии:       | /?last_name=
 по дистанции, км: | /?get_in_distance_km=

## Права доступа к ресурсам сервиса

В проекте использована базовая авторизация: по логину и паролю.

### Неавторизованные участники могут:

    - создать аккаунт

### Авторизованные участники могут:

    - входить в систему под своим логином и паролем;
    - оценивать других участников;
    - просматривать и фильтровть список участников.
<br>

# Примеры запросов к API
Запросы к API начинаются с «/api/»
1. Регистрация участника:
<br>**POST**-запрос:
<br><code>
    /clients/create/
</code>
<br /> *Request sample:*
```python
{
    "email": "man0@fake.ru",
    "username": "man0",
    "password": "pass_man",
    "first_name": "name0",
    "last_name": "surname0",
    "avatar": "avatar.jpg",
    "gender": "М",
    "longitude": 36.57912284676751,
    "latitude": 50.61301720349709
}
```
*Response sample (201):*
```python
{
    "id": 2,
    "username": "man0",
    "email": "man0@fake.ru",
    "first_name": "man0",
    "last_name": "man0",
    "avatar": "https://manydates.ml/media/clients/avatar.jpg",
    "gender": "М",
    "is_match": false,
    "longitude": 36.57912284676751,
    "latitude": 50.61301720349709
}
```
*Response sample (400):*
```python
{
    "email": [
        "пользователь с таким e-mail уже существует."
    ],
    "username": [
        "Обязательное поле."
    ]
}
```

2. Создание отметки у участника:
<br>**GET**-запрос:
<br><code>
/clients/2/match/
</code>
<br /> *Response sample: (200)*
```python
{
    "follower": 1,
    "person": 2
}
```

3. Удаление отметки у участника:
<br>**DELETE**-запрос:
<br><code>
    /clients/2/match/
</code>
<br /> *Response sample: (204)*
```python
<no content>
```

4. Фильтр по списку участников:
<br>**GET**-запрос:
<br><code>
    /list/?gender=М&first_name=man0&last_name=man0
</code>
<br /> *Response sample: (200)*
```python
[
    {
        "id": 2,
        "username": "man0",
        "email": "man0@fake.ru",
        "first_name": "man0",
        "last_name": "man0",
        "avatar": "https://manydates.ml/media/clients/man_symbol.jpg",
        "gender": "М",
        "is_match": false,
        "longitude": 36.57912284676751,
        "latitude": 50.61301720349709
    }
]
```

### <br /> Автор проекта
***
***Немыкин Евгений<br />***
***nonwander@gmail.com<br />***
***Telegram: @nonwander***
***
