from django.db import models


class Import(models.Model):
    id = models.AutoField(primary_key=True)


class Citizen(models.Model):
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

    relatives = models.ManyToManyField('self', related_name='relatives', blank=True)
