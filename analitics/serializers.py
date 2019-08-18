from rest_framework import serializers


from analitics.models import Citizen, Import


class CitizenSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(format='%d.%m.%Y', input_formats=['%d.%m.%Y'])
    class Meta:
        model = Citizen
        exclude = ('import_id', 'id')


class ImportSerializer(serializers.ModelSerializer):
    citizens = CitizenSerializer(many=True)
    class Meta:
        model = Import
        fields = ('citizens',)

    # custom validators
    # score = IntegerField(validators=[multiple_of_ten])

    def validate(self, check_data):
        data = check_data['citizens']
        citizens = {} 
        for item in data:
            if len(item) != 9:  # item.get('relatives') is None ???
                raise serializers.ValidationError('fields')
            if item['citizen_id'] in citizens:
                raise serializers.ValidationError('not unique citizens')
            citizens[item['citizen_id']] = 1
        return check_data


    def create(self, validated_data):
        citizen_data = validated_data.pop('citizens')
        import_id = Import.objects.create()
        for citizen in citizen_data:
            citizen.pop('relatives')
            Citizen.objects.create(import_id=import_id, **citizen)
        return import_id
