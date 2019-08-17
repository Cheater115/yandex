from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status


class ImportCreate(APIView):
    parser_classes = (JSONParser,)  # принимать только json
    def post(self, request):
        return Response(status=status.HTTP_200_OK)


class CititzenDetail(APIView):
    def patch(self, request, import_id, citizen_id):
        pass


class CititzenList(APIView):
    def get(self, request, import_id):
        pass 


class CititzenBirthdays(APIView):
    def get(self, request, import_id):
        pass


class ImportParcentile(APIView):
    def get(self, request, import_id):
        pass
