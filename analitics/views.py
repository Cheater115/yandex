from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status, serializers

from collections import Counter
from datetime import datetime
from numpy import percentile

from analitics.models import Import, Citizen
from analitics.serializers import ImportSerializer, CitizenSerializer
from analitics.serializers import CitizenSerializerRel
# import analitics.functions


def check_unknown_fields(data):
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


class ImportCreate(APIView):
    '''
    Принимает на вход набор с данными о жителях в формате json.
    Сохраняет его с уникальным идентификатором: import_id.
    В наборе данных для каждого жителя должны присутствовать все поля.
    Значения не могут быть null.
    Возвращается идентификатор: import_id.
    '''
    def post(self, request):
        check_unknown_fields(request.data)
        serializer = ImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # не корректно - 400
        import_id = serializer.save()
        return Response(
            data={'data': {'improt_id': import_id.id}},
            status=status.HTTP_201_CREATED
        )


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


class CitizenDetail(APIView):
    '''
    Изменяет информацию о жителе в указанном наборе данных.
    Любые поля, кроме citizen_id.
    Возвращается актуальная информация об указанном жителе.
    '''
    # only for debug
    def get(self, request, import_id, citizen_id):
        import_id = get_import_or_400(import_id)
        citizen = get_citizen_or_400(import_id, citizen_id)
        serializer = CitizenSerializerRel(citizen)
        return Response(data=serializer.data)

    def patch(self, request, import_id, citizen_id):
        check_unknown_fields(request.data)
        import_id = get_import_or_400(import_id)
        citizen = get_citizen_or_400(import_id, citizen_id)
        serializer = CitizenSerializerRel(
            citizen,
            data=request.data,
            partial=True,
            context={'import_id': import_id},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


class CitizenList(APIView):
    '''
    Возвращает список всех жителей для указанного набора данных.
    '''
    def get(self, request, import_id):
        import_id = get_import_or_400(import_id)
        citizens = import_id.citizen_set.all()
        serializer = CitizenSerializerRel(
            citizens,
            many=True,
            context={'import_id': import_id},
        )
        return Response({'data':serializer.data}) 


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

class CitizenBirthdays(APIView):
    '''
    Возвращает жителей и количество подарков,
    которые они будут покупать своим ближайшим родственникам,
    сгруппированных по месяцам из указанного набора данных.
    '''
    def get(self, request, import_id):
        import_id = get_import_or_400(import_id)
        citizens = import_id.citizen_set.all()
        serializer = CitizenSerializerRel(
            citizens,
            many=True,
            context={'import_id': import_id},
        )

        return_data = {'data': get_birthdays_info(serializer.data)}
        return Response(return_data)

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
        p50 = percentile(dates[town], 50, interpolation='linear')
        p75 = percentile(dates[town], 75, interpolation='linear')
        p99 = percentile(dates[town], 99, interpolation='linear')
        data.append({'town': town, 'p50': p50, 'p75': p75, 'p99': p99})
    return data


class ImportParcentile(APIView):
    '''
    Возвращает статистику по городам для указанного набора данных
    в разрезе возраста (полных лет) жителей: p50, p75, p99,
    где число - это значение перцентиля.
    '''
    def get(self, request, import_id):
        import_id = get_import_or_400(import_id)
        citizens = import_id.citizen_set.all()
        serializer = CitizenSerializerRel(
            citizens,
            many=True,
            context={'import_id': import_id},
        )
        
        return_data = {'data': get_percentile(serializer.data)}
        return Response(return_data)
