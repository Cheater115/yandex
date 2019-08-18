from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status, serializers


from analitics.models import Import, Citizen
from analitics.serializers import ImportSerializer, CitizenSerializer
from analitics.serializers import CitizenSerializerRel


class ImportCreate(APIView):
    '''
    Принимает на вход набор с данными о жителях в формате json
    и сохраняет его с уникальным идентификатором: import_id
    '''
    parser_classes = (JSONParser,)  # принимать только json, иначе 415

    def post(self, request):
        serializer = ImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # не корректно - 400
        tmp = serializer.save()

        return_data = {"data":{"improt_id":tmp.id}}
        return Response(
            data=return_data,
            status=status.HTTP_201_CREATED
        )


class CitizenDetail(APIView):

    def patch(self, request, import_id, citizen_id):
        try:
            imp = Import.objects.get(id=import_id)
        except Import.DoesNotExist:
            raise serializers.ValidationError('hasnt such import')
        try:
            citizen = imp.citizen_set.get(citizen_id=citizen_id)
        except Citizen.DoesNotExist:
            raise serializers.ValidationError('hasnt such citizen')
        # update
        # Update `comment` with partial data
        # serializer = CommentSerializer(comment, data={'content': u'foo bar'}, partial=True)


class CitizenList(APIView):
    '''
    Возвращает список всех жителей для указанного набора данных
    '''
    def get(self, request, import_id):
        try:
            imp = Import.objects.get(id=import_id)
        except Import.DoesNotExist:
            raise serializers.ValidationError('hasnt such import')
        citizens = imp.citizen_set.all()
        serializer = CitizenSerializerRel(citizens, many=True)
        return_data = {"data":serializer.data}
        return Response(return_data) 
        return Response(serializer.data)


class CitizenBirthdays(APIView):

    def get(self, request, import_id):
        pass


class ImportParcentile(APIView):

    def get(self, request, import_id):
        pass
