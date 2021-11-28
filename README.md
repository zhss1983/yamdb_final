# Документация к API YaMDb

Текущий статус:

![example workflow](https://github.com/zhss1983/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Как запустить проект:

### Загрузите API YaMDB с git

Скачать с https://github.com/zhss1983/yamdb_final файл docker-compose.yamdb

### Создайте 3 файла с переменными окружения:
   
 - .env_db

```Python
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=<ИМЯ_ПОЛЬЗОВАТЕЛЯ_POSTGRES>
POSTGRES_PASSWORD=<ПАРОЛЬ_ПОЛЬЗОВАТЕЛЯ_POSTGRES>
DB_HOST=db
DB_PORT=5432
```

 - .env_mail

```Python
EMAIL_HOST=smtp.mail.ru
EMAIL_PORT=2525
EMAIL_HOST_USER=<ВАША_ПОЧТА>
EMAIL_HOST_PASSWORD=<ПАРОЛЬ_ДЛЯ_ПОЧТЫ>
EMAIL_USE_TLS|EMAIL_USE_SSL=True
```

EMAIL_USE_TLS либо EMAIL_USE_SSL - выбирайте один из двух, текст может быть любой кроме пустой строки.
    
 - .env_web

```Python
SECRET_KEY=<КЛЮЧ_DJANGO>
SENTRY_DSN=<ВАША_ССЫЛКА_ДЛЯ_https://sentry.io/>
EMAIL_YAMDB=zhss.83@mail.ru
```

SENTRY_DSN - Это ссылка предоставляемая https://sentry.io/ для отслеживания ошибок. Если у вас её нет, вообще не добавляйте это поле.

### Конфигурация nginx

Убедитесь что файл конфигурации nginx присутствует в папке ./nginx/

В файле default.conf есть три включаемых конфигурации (в любой момент должна быть подключена лишь одна из трёх):

 - default_mini.conf - позволяет запустить минимальный функционал. Доступ к сайту будет обеспечиваться по протоколу http
 - default_first.conf - данная конфигурация необходима для получения SSL сертификата. Для его получения необходимо выполнить от имени администратора скрипт init-letsencrypt.sh. В самом скрипте необходимо предварительно задать следующие параметры:
   - domains=(zhss.tk www.zhss.tk) - Домен
   - email="zhss.83@mail.ru" - Почта
 - default_evryday.conf - после запуска init-letsencrypt.sh необходимо переключить конфигурацию на эту и перезапустить nginx контейнер.

### Работа с образами

Все операции выполнять от имени администратора или выполнить следующие команды:

 - sudo groupadd docker
 - sudo usermod -aG docker <ИМЯ_ПОЛЬЗОВАТЕЛЯ>
 - Перезапуск окружения (выход из сессии и вход заново).

#### Собрать все образы вместе.

docker-compose up -d

#### Пересобрать все образы вместе

docker-compose up -d --build

#### Перезапустить все образы

docker-compose restart

### Выполнить подготовку базы данных

docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py createsuperuser

docker-compose exec web python manage.py collectstatic

Восстановить данные по умолчанию:

docker-compose exec web python manage.py loaddata fixtures.json

Все эти команды уже прописаны в first_run.sh, достаточно его запустить.

## Описание проекта:

Проект YaMDb собирает отзывы пользователей на различные произведения
сохранённые в базе данных (БД) проекта. Произведения делятся на категории:
«Книги», «Фильмы», «Музыка» и т.д. Список категорий может быть расширен
администратором (например, можно добавить категорию «Изобразительное искусство»
или «Ювелирка»).

Система не хранит в своей БД YaMDb исходный контент, нельзя посмотреть фильм
или послушать музыку.

Новые произведения могут вносить только администраторы, для рядовых
пользователей данный функционал недоступен. Произведению может быть присвоен
жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
Новые жанры также может создавать только администратор.

## Работа с эндпоинтами:

Краткое описание основных возможностей, за более подробной информацией
обратитесь к [/redoc/](http://127.0.0.1:8000/redoc/) 

### Авторизация с применением JWT токена

#### Регистрация нового пользователя

Для получения JWT-токена необходимо отправить **JSON** запрос, содержащий
имя пользователя и имя почтового ящика.

**JSON** запрос:

```JSON
{
  "email": "string",
  "username": "string"
}
```

POST: [/api/v1/auth/signup/](http://127.0.0.1:8000/api/v1/auth/signup/)

В письме придёт код подтверждения. Дальше необходимо необходимо отправить
**JSON** запрос, содержащий код подтверждения:

```JSON
{
  "username": "string",
  "confirmation_code": "string"
}
```

POST: [/api/v1/auth/token/](http://127.0.0.1:8000/api/v1/auth/token/)

В ответ вы получите токен для доступа к сервису.

```JSON
{
  "token": "string"
}
```

Вам будут доступны:
- Категории:
  [/api/v1/categories/](http://127.0.0.1:8000/api/v1/categories/)
- Жанры:
  [/api/v1/genres/](http://127.0.0.1:8000/api/v1/genres/)
- Произведения:
  [/api/v1/titles/](http://127.0.0.1:8000/api/v1/titles/)
- Отзывы:
  [/api/v1/titles/{title_id}/reviews/](http://127.0.0.1:8000/api/v1/titles/1/reviews/)
- Комментарии:
  [/api/v1/titles/{title_id}/reviews/{review_id}/comments/](http://127.0.0.1:8000/api/v1/titles/1/reviews/1/comments/)
 
По всем вопросам обращайтесь к администраторам по [электронной почте](mailto:zhss.83@mail.ru)
