from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status, serializers

from analitics.models import Import, Citizen
from analitics.serializers import ImportSerializer, CitizenSerializer
from analitics.serializers import CitizenSerializerRel
from analitics.functions import *


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


class ImportPercentile(APIView):
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
