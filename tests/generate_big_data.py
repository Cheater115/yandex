import json
import random
import datetime


def generate_city():
    cities = [
        "Москва",
        "Санкт-Петербург",
        "Курс",
        "Пермь",
        "Одинцово",
        "Минск",
        "Саратов",
        "Можайск",
        "Архангельск",
    ]
    random.seed()
    city = random.choice(cities)
    return city


def generate_date():
    start_date = datetime.datetime(1970, 1, 1)
    end_date = datetime.datetime.utcnow()
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    res = start_date + datetime.timedelta(days=random_days)
    return res.strftime("%d.%m.%Y")


citizens = []
for ind in range(1, 2001):
    citizen = {}
    citizen["citizen_id"] = ind
    citizen["town"] = generate_city()
    citizen["street"] = "Test"
    citizen["building"] = "Test"
    citizen["apartment"] = 1
    citizen["name"] = "Test"
    citizen["birth_date"] = generate_date()
    citizen["gender"] = "female"
    if ind % 2 == 0:
        citizen["relatives"] = [ind-1]
    else:
        citizen["relatives"] = [ind+1]
    citizens.append(citizen)

for ind in range(2001, 15001):
    citizen = {}
    citizen["citizen_id"] = ind
    citizen["town"] = generate_city()
    citizen["street"] = "Test"
    citizen["building"] = "Test"
    citizen["apartment"] = 1
    citizen["name"] = "Test"
    citizen["birth_date"] = generate_date()
    citizen["gender"] = "female"
    citizen["relatives"] = []
    citizens.append(citizen)


ftest_name = "big_data.json"
with open(ftest_name, "w") as jf:
    data = {}
    data["citizens"] = citizens
    json.dump(data, jf, indent=4, ensure_ascii=False)
