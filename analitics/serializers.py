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
        except ObjectDoesNotExist:
            self.fail('does_not_exist')
        except (TypeError, ValueError):
            self.fail('incorrect_type')
        


class CitizenSerializerRel(serializers.ModelSerializer):
    '''
    Сериализация данных жителя
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


class CitizenSerializer(serializers.ModelSerializer):
    '''
    Осуществляет проверку при импорте, конкретного жителя
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
    Осуществляет проверку импорта
    '''
    citizens = CitizenSerializer(many=True)  # проверка полей жителей
    class Meta:
        model = Import
        fields = ('citizens',)

    def validate(self, check_data):
        data = check_data['citizens']
        citizens = {}
        for item in data:
            # только описанные поля
            if len(item) != 9:
                raise serializers.ValidationError('fields')
            # уникальные citizen_id
            if item['citizen_id'] in citizens:
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

        # добавляем родственников
        for item in relatives:
            for i in relatives[item][1]:
                relatives[item][0].relatives.add(relatives[i][0])

        return import_id
