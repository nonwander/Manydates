# dating-site-API

API-сервис для сайта знакомств.
Хост развернутого проекта http://2.57.187.13/
<hr><br>

# Краткое описание
Проект развернут с использованием HTTP-сервера nginx и WSGI-сервера Gunicorn.

## Особенности
Сервис использует SMPT сервер mail.ru.
<br>При регистрации реального адреса электронной почты вы получите уведомление
<br>на свой ящик, если создать у пользователей взаимную отметку.

## Перспективные доработки проекта
<li>Оптимизировать запросы к БД.
<li>Перенести БД с SQLite на PostgreSQL.
<li>Контейнеризировать БД и веб-сервер в Docker-compose.
<br><br>

# Технологии:
    Django==2.2.19
    Django-rest-framework==3.13.1
    Python==3.10.0

# Запуск и работа с проектом
## Тестирование API
Можно направить запросы в соответствии с правами доступа и эндпоинтам.
<br><br>

# Ресурсы сервиса

## На сервисе доступны эндпоинты:
1) Регистрация нового клиента:
http://2.57.187.13/api/clients/create/

2) Оценивание участником другого участника: 
http://2.57.187.13/api/clients/{client_id}/match/

3) Просмотр списка участников:
http://2.57.187.13/api/list/

## Фильтрация списка по по полу, имени, фамилии.
Для фильтрации используйте ключи соотвествено:
- по полу: /?gender=
- по имени: /?first_name=
- по фамилии: /?last_name=
- по дистанции к другим участникам, км: /?get_in_distance_km=

## Права доступа к ресурсам сервиса

В проекте использована базовая авторизация: по логину и паролю.

### Неавторизованные участники могут:

    - создать аккаунт;

### Авторизованные участники могут:

    - входить в систему под своим логином и паролем;
    - оценивать других участников;
    - просматривать список участников.


# Примеры запросов к API

Запросы к API начинаются с «/api/»

1) Регистрация участника:

POST-запрос: http://2.57.187.13/api/clients/
<br /> *Request sample:*
```python
{
    "email": "man@fake.ru",
    "username": "man0",
    "password": "pass_man",
    "first_name": "name0",
    "last_name": "surname0",
    "avatar": "avatar.jpg",
    "gender": "М"
}
```
*Response sample (201):*
```python
{
    "email": "man0@fake.ru",
    "id": 2,
    "username": "man0",
    "first_name": "man0",
    "last_name": "man0",
    "avatar": "http://2.57.187.13/media/clients/avatar.jpg",
    "gender": "М",
    "is_match": false
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
2) Создание отметки у участника:

GET-запрос: http://2.57.187.13/api/clients/2/match/
<br /> *Response sample: (200)*
```python
{
    "follower": 1,
    "person": 2
}
```

3) Удаление отметки у участника:

DELETE-запрос: http://2.57.187.13/api/clients/2/match/
<br /> *Response sample: (204)*
```python

```

4) Фильтр по списку участников:

GET-запрос: http://2.57.187.13/api/list/?gender=М&first_name=man0&last_name=man0
<br /> *Response sample:*
```python
[
    {
        "email": "man0@fake.ru",
        "id": 2,
        "username": "man0",
        "first_name": "man0",
        "last_name": "man0",
        "avatar": "http://2.57.187.13/media/clients/man_symbol.jpg",
        "gender": "М",
        "is_match": false
    }
]
```

### <br /> Автор проекта:
Немыкин Евгений<br />
nonwander@gmail.com<br />
Telegram: @nonwander
