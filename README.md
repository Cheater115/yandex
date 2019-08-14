# Yandex
второе задание школы бэкенд‑разработки Yandex

## Рабочее окружение
* Python3 (v. 3.6.8)
* Nginx (v. 1.14.0)
* PostgreSQL (v. 10.10)
* Gunicorn (v. 19.9.0)
* Django (v. 2.2.4)
* Djangorestframework (v. 3.10.2)

## Настройка рабочего окружения

### 1. Установка зависимостей
* Менеджер пакетов pip (и обновим его), инструменты разработки Python и модуль для создания виртуальной среды (в ней будет храниться приложение):
    > sudo apt-get install python3-pip python3-dev python3-venv  
    > sudo -H pip3 install --upgrade pip
* Веб сервер nginx (в качестве обратного прокси-сервер для Gunicorn: помогает работать с медленными клиентами за счет управления запросами => backend занят min возможное время):
    > sudo apt-get install nginx
* СУБД PostgreSQL:
    > sudo apt-get install libpq-dev postgresql postgresql-contrib

### 2. Развертывание проекта
* Клонирование репозитория:
    > git clone https://github.com/SLKClub/yandex.git
* Создание виртуальной среды:
    > cd yandex  
    > python3 -m venv yaenv
* Установка оставшихся компонентов Python
    * Gunicorn - запуск веб-приложения
    * Django - фреймворк для веб-приложения
    * Djangorestframework - библиотека поверх Django для создания REST API
    * Psycopg2 - адаптер PostgreSQL (связь python - СУБД)
    > source yaenv/bin/activate  
    > pip install -r requirements.txt
* Создание БД и пользователя и настройки:
    > sudo -u postgres psql  
    > CREATE DATABASE analitics_db;  
    > CREATE USER cheater WITH PASSWORD 'gif54TRU';  
    > ALTER ROLE cheater SET client_encoding TO 'utf8';  
    > ALTER ROLE cheater SET default_transaction_isolation TO 'read committed';  
    > ALTER ROLE cheater SET timezone TO 'UTC';  
    > GRANT ALL PRIVILEGES ON DATABASE analitics_db TO cheater;  
    > \q
* Применение настроек nginx:
    > sudo rm -rf /etc/nginx/sites-enabled/default  
    > sudo cp -f etc/nginx.conf /etc/nginx/sites-enabled/nginx.conf  
    > sudo /etc/init.d/nginx restart
* Миграции:
    > ./manage.py makemigrations analitics  
    > ./manage.py migrate
