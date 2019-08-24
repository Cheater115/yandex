from rest_framework import serializers

from analitics.models import Citizen, Import


class CitizenSerializerPatch(serializers.ModelSerializer):
    '''
    Обновление данных о жителе
    '''
    birth_date = serializers.DateField(
        format='%d.%m.%Y', input_formats=['%d.%m.%Y'])
    class Meta:
        model = Citizen
        exclude = ('import_id', 'id')

    def validate_citizen_id(self, value):
        raise serializers.ValidationError('can\'t change citizen_id')

    def validate_relatives(self, relatives):
        for rel in relatives:
            if rel not in self.context['citizens_id']:
                raise serializers.ValidationError('Bad citizen')
        return relatives

    def validate(self, check_data):
        if len(check_data) == 0:
            raise serializers.ValidationError('empty query')
        return check_data

    def update(self, citizen, validated_data):
        citizen.town = validated_data.get('town', citizen.town)
        citizen.street = validated_data.get('street', citizen.street)
        citizen.building = validated_data.get('building', citizen.building)
        citizen.apartment = validated_data.get('apartment', citizen.apartment)
        citizen.name = validated_data.get('name', citizen.name)
        citizen.birth_date = validated_data.get('birth_date', citizen.birth_date)
        citizen.gender = validated_data.get('gender', citizen.gender)

        if validated_data.get('relatives') is not None:
            del_rel = [rel for rel in citizen.relatives if rel not in validated_data['relatives']]
            up_rel = [rel for rel in validated_data['relatives'] if rel not in citizen.relatives]

            for rel in del_rel:
                rm = self.context['import_id'].citizen_set.get(citizen_id=rel)
                rm.relatives.remove(citizen.citizen_id)
                rm.save()
            for rel in up_rel:
                rm = self.context['import_id'].citizen_set.get(citizen_id=rel)
                rm.relatives.append(citizen.citizen_id)
                rm.save()
        citizen.relatives = validated_data.get('relatives', citizen.relatives)

        citizen.save()
        return citizen


class CitizenROSerializer(serializers.ModelSerializer):
    '''
    Сериализация жителя/жителей, для анализа данных (менять нельзя)
    '''
    birth_date = serializers.DateField(
        format='%d.%m.%Y', input_formats=['%d.%m.%Y'])
    class Meta:
        model = Citizen
        fields = [
            'citizen_id', 'town', 'street',
            'building', 'apartment', 'name',
            'birth_date', 'gender', 'relatives'
        ]
        read_only_fields = fields


class CitizenImportSerializer(serializers.ModelSerializer):
    '''
    Сериализация и валидация конкретного жителя при импорте
    '''
    birth_date = serializers.DateField(
        format='%d.%m.%Y', input_formats=['%d.%m.%Y'])
    class Meta:
        model = Citizen
        exclude = ('import_id', 'id')


class ImportSerializer(serializers.ModelSerializer):
    '''
    Осуществляет проверку импорта и создание
    '''
    citizens = CitizenImportSerializer(many=True)  # проверка полей жителей
    class Meta:
        model = Import
        fields = ('citizens',)

    def validate(self, check_data):
        '''
        Проверяет поступившую выборку:
            - у каждого жителя 9 полей
            - уникальные citizen_id
            - не дублируются родственники
            - родственники симметричные
            - и существующие
        '''
        data = check_data['citizens']
        citizens = {}
        for item in data:
            if len(item) != 9:  # все поля
                raise serializers.ValidationError('fields')
            if item['citizen_id'] in citizens:  # уникальные citizen_id
                raise serializers.ValidationError('not unique citizens')
            citizens[item['citizen_id']] = item['relatives']
            rel = set(item['relatives'])
            if len(rel) != len(item['relatives']):
                raise serializers.ValidationError('not unique relations')
        for citizen in citizens:
            for rel in citizens[citizen]:
                if rel not in citizens:
                    raise serializers.ValidationError('no such relation')
                if citizen not in citizens[rel]:
                    raise serializers.ValidationError('not symm relations')
        return check_data

    def create(self, validated_data):
        '''
        Создание жителей в БД
        '''
        citizen_data = validated_data.pop('citizens')
        import_id = Import.objects.create()

        citizens = []
        for citizen in citizen_data:
            citizen['import_id'] = import_id
            cit = Citizen(**citizen)
            citizens.append(cit)
 
        Citizen.objects.bulk_create(citizens)

        return import_id
