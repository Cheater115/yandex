from collections import Counter
from datetime import datetime
from numpy import percentile
from rest_framework.serializers import ValidationError
from analitics.models import Import, Citizen


def _check_fields(data):
    '''
    Проверяет, что нет неописанных полей у жителя
    '''
    correct = (
        'citizen_id', 'town', 'street',
        'building', 'apartment', 'name',
        'birth_date', 'gender', 'relatives'
    )
    for item in data:
        if item not in correct:
            raise ValidationError('unknown field ' + str(item))


def check_unknown_fields(data):
    '''
    Проверяет, что нет неописанных полей у жителя/списка жителей.
    '''
    if data.get('citizens'):
        citizens = data['citizens']
        for citizen in citizens:
            _check_fields(citizen)
    else:
        _check_fields(data)


def get_import_or_400(import_id):
    '''
    Возвращает Import либо 400 Bad Request.
    '''
    try:
        return Import.objects.get(id=import_id)
    except Import.DoesNotExist:
        raise ValidationError('hasnt import: ' + str(import_id))


def get_citizen_or_400(import_id, citizen_id):
    '''
    Возвращает жителя из определенного импорта(import_id - объект).
    '''
    try:
        return import_id.citizen_set.get(citizen_id=citizen_id)
    except Citizen.DoesNotExist:
        raise ValidationError('hasnt citizen: ' + str(citizen_id))


def get_birthdays_info(citizens):
    '''
    Возвращает жителей и количество подарков,
    которые они будут покупать своим ближайшим родственникам.
    '''
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
    '''
    Вычисляет возраст, используя текущую дату (UTC).
    '''
    birth_date = datetime(int(year), int(month), int(day))
    cur_date = datetime.utcnow()
    age = cur_date.year - birth_date.year \
        - ((cur_date.month, cur_date.day) < (birth_date.month, birth_date.day))
    return age


def get_percentile(citizens):
    '''
    Вычисление персентиля по городам
    '''
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
        p50, p75, p99 = percentile(dates[town], (50,75,99),
            interpolation='linear')
        data.append({
            'town': town,
            'p50': round(p50, 2),
            'p75': round(p75, 2),
            'p99': round(p99, 2)
        })
    return data
