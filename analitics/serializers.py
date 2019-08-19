from rest_framework import serializers


from analitics.models import Citizen, Import


class MyPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    '''
    В качестве primary key использует citizen_id,
    в пределах конкретного набора данных(import_id)
    '''
    def to_representation(self, value):
        return value.citizen_id

    def get_queryset(self):
        if self.context.get('import_id') is not None:
            return self.context['import_id'].citizen_set.all()
        return self.objects.all()

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(citizen_id=data)
        except:
            raise serializers.ValidationError("not such relation")


class CitizenSerializerRel(serializers.ModelSerializer):
    '''
    Сериализация данных жителя и валидация при PATCH
    '''
    birth_date = serializers.DateField(
        format='%d.%m.%Y',
        input_formats=['%d.%m.%Y']
    )
    relatives = MyPrimaryKeyRelatedField(
        many=True,
        required=False
    )
    class Meta:
        model = Citizen
        exclude = ('import_id', 'id')

    def validate_citizen_id(self, value):
        raise serializers.ValidationError('can\'t change citizen_id')

    def validate(self, check_data):
        if len(check_data) == 0:
            raise serializers.ValidationError('bad query')
        return check_data


class CitizenSerializer(serializers.ModelSerializer):
    '''
    Валидация конкретного жителя при импорте
    '''
    birth_date = serializers.DateField(
        format='%d.%m.%Y', input_formats=['%d.%m.%Y'])
    relatives = serializers.ListField(
        child=serializers.IntegerField(min_value=0))
    class Meta:
        model = Citizen
        exclude = ('import_id', 'id')


class ImportSerializer(serializers.ModelSerializer):
    '''
    Осуществляет проверку импорта и создание
    '''
    citizens = CitizenSerializer(many=True)  # проверка полей жителей
    class Meta:
        model = Import
        fields = ('citizens',)

    def validate(self, check_data):
        data = check_data['citizens']
        citizens = {}
        for item in data:
            if len(item) != 9:  # только описанные поля
                raise serializers.ValidationError('fields')
            if item['citizen_id'] in citizens:  # уникальные citizen_id
                raise serializers.ValidationError('not unique citizens')
            citizens[item['citizen_id']] = item['relatives']
        for citizen in citizens:
            for rel in citizens[citizen]:
                if rel not in citizens:
                    raise serializers.ValidationError('no such relation')
                if citizen not in citizens[rel]:
                    raise serializers.ValidationError('not symm relations')
        return check_data

    def create(self, validated_data):
        citizen_data = validated_data.pop('citizens')
        import_id = Import.objects.create()

        relatives = {}
        for citizen in citizen_data:
            rel = citizen.pop('relatives')  # создаем без родственников
            cit = Citizen.objects.create(import_id=import_id, **citizen)
            relatives[cit.citizen_id] = (cit, rel)
        for item in relatives:  # добавляем родственников
            for i in relatives[item][1]:
                relatives[item][0].relatives.add(relatives[i][0])
        return import_id
