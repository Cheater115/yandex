from django.urls import path

from analitics.views import *

urlpatterns = [
    path('<int:import_id>/towns/stat/percentile/age', ImportParcentile.as_view()),
    path('<int:import_id>/citizens/birthdays', CitizenBirthdays.as_view()),
    path('<int:import_id>/citizens/<int:citizen_id>', CitizenDetail.as_view()),
    path('<int:import_id>/citizens', CitizenList.as_view()),
    path('', ImportCreate.as_view()),
]
