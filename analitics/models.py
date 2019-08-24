from django.db import models
from django.contrib.postgres.fields import ArrayField


class Import(models.Model):
    '''
    Модель импорта
    '''
    id = models.AutoField(primary_key=True)


class Citizen(models.Model):
    '''
    Модель жителя
    '''
    import_id = models.ForeignKey(Import, on_delete=models.CASCADE)
    citizen_id = models.PositiveIntegerField()

    class Meta:
        unique_together = ('import_id', 'citizen_id')

    town = models.CharField(max_length=63)
    street = models.CharField(max_length=63)
    building = models.CharField(max_length=63)
    apartment = models.PositiveIntegerField()

    name = models.CharField(max_length=63)
    birth_date = models.DateField()
    GENDER = (('male', 'male'), ('female', 'female'))
    gender = models.CharField(choices=GENDER, max_length=15)
    # родственников в массиве, используя поле postgres: ArrayField
    relatives = ArrayField(models.PositiveIntegerField(), blank=True)
