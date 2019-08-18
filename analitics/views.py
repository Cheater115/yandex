from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status, serializers


from analitics.models import Import, Citizen
from analitics.serializers import ImportSerializer, CitizenSerializer


class ImportCreate(APIView):
    parser_classes = (JSONParser,)  # принимать только json
    def post(self, request):
        serializer = ImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.validated_data, status=status.HTTP_200_OK)


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
    def get(self, request, import_id):
        try:
            imp = Import.objects.get(id=import_id)
        except Import.DoesNotExist:
            raise serializers.ValidationError('hasnt such import')
        citizens = imp.citizen_set.all()
        # citizens = Citizen.objects.filter(import_id=import_id) 
        serializer = CitizenSerializer(citizens, many=True)
        return Response(serializer.data)


class CitizenBirthdays(APIView):
    def get(self, request, import_id):
        pass


class ImportParcentile(APIView):
    def get(self, request, import_id):
        pass
