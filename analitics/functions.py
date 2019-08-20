from collections import Counter
from datetime import datetime
from numpy import percentile
from rest_framework import serializers
from analitics.models import Import, Citizen

def _check_fields(data):
    correct = (
        'citizen_id',
        'town',
        'street',
        'building',
        'apartment',
        'name',
        'birth_date',
        'gender',
        'relatives'
    )
    for item in data:
        if item not in correct:
            raise serializers.ValidationError('unknown field ' + str(item))


def check_unknown_fields(data):
    if data.get('citizens'):
        citizens = data['citizens']
        for citizen in citizens:
            _check_fields(citizen)
    else:
        _check_fields(data)


def get_import_or_400(import_id):
    try:
        return Import.objects.get(id=import_id)
    except Import.DoesNotExist:
        raise serializers.ValidationError('hasnt import: ' + str(import_id))


def get_citizen_or_400(import_id, citizen_id):
    # import_id - объект
    try:
        return import_id.citizen_set.get(citizen_id=citizen_id)
    except Citizen.DoesNotExist:
        raise serializers.ValidationError('hasnt citizen: ' + str(citizen_id))


def get_birthdays_info(citizens):
    data = {str(item):[] for item in range(1, 13)}
    for citizen in citizens:
        month = str(int(citizen['birth_date'].split('.')[1]))
        for rel in citizen['relatives']:
            data[month].append(rel)
    for item in data:
        res = []
        counter = Counter(data[item])
        for c in counter:
            res.append({'citizen_id': int(c), 'presents': counter[c]})
        data[item] = res
    return data


def get_age(day, month, year):
    ''''''
    birth_date = datetime(int(year), int(month), int(day))
    cur_date = datetime.utcnow()
    age = cur_date.year - birth_date.year \
        - ((cur_date.month, cur_date.day) < (birth_date.month, birth_date.day))
    return age


def get_percentile(citizens):
    data = []
    dates = {}
    for citizen in citizens:
        town = citizen['town']
        age = get_age(*citizen['birth_date'].split('.'))
        if dates.get(town) is None:
            dates[town] = [age]
        else:
            dates[town].append(age)
    for town in dates:
        # p50 = percentile(dates[town], 50, interpolation='linear')
        # p75 = percentile(dates[town], 75, interpolation='linear')
        # p99 = percentile(dates[town], 99, interpolation='linear')
        p50, p75, p99 = percentile(dates[town], (50,75,99), interpolation='linear')
        data.append({
            'town': town,
            'p50': round(p50, 2),
            'p75': round(p75, 2),
            'p99': round(p99, 2)
        })
    return data
