# Yandex
Второе задание школы бэкенд‑разработки Yandex

# Рабочее окружение
* **Docker** (v. 19.3) и **Docker-Compose** (v. 1.24):
    * Для работы веб-приложения в контейнерах
* **Nginx** (v. 1.14):
    * веб-сервер, используемый в качестве обратного прокси-сервера для веб-приложения
* **PostgreSQL** (v. 10.10):
    * СУБД, используемая в веб-приложения
* **Python** (v. 3.6):
    * Сам `python`
    * `Gunicorn` - запуск веб-приложения
    * `Eventlet` - для асинхронных воркеров *gunicorn*
    * `Django` - фреймворк для веб-приложения
    * `DjangoRestFramework` - библиотека поверх Django для создания REST API
    * `Psycopg2` - адаптер PostgreSQL (связь python - СУБД)
    * `Numpy` - библиотека для вычисления percentile

# Развёртывание проекта

## 1. Установка Docker и Docker-Compose
* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)
* [ubuntu 18.04](docker/installdocker.md)
## 2. Клонирование репозитория
```bash
git clone https://github.com/SLKClub/yandex.git
```
## 3. Запуск
```bash
cd yandex
docker-compose up -d
docker-compose exec webapi python manage.py makemigrations analitics
docker-compose exec webapi python manage.py migrate
docker-compose exec webapi python manage.py collectstatic
```

# Тесты
> Зависимости curl, apache2-utils
```bash
cd tests
# Тест: POST /imports
./imports_test.sh
# Тест: PATCH /imports/$import_id/citizens/$citizen_id
./patch_test.sh
# Тест: GET /imports/$import_id/citizens
./citizenlist_test.sh
# Тест: GET /imports/$import_id/citizens/birthdays
./birthdays_test.sh
# Тест: GET /imports/$import_id/towns/stat/percentile/age
./percentile_test.sh
# Тест: На большие данные
./bigdata_test.sh
```
