from django.urls import path

from analitics.views import *

urlpatterns = [
    path('imports/<int:import_id>/towns/stat/percentile/age', ImportParcentile.as_view()),
    path('imports/<int:import_id>/citizens/birthdays', CitizenBirthdays.as_view()),
    path('imports/<int:import_id>/citizens/<int:citizen_id>', CitizenDetail.as_view()),
    path('imports/<int:import_id>/citizens', CitizenList.as_view()),
    path('imports', ImportCreate.as_view()),
]
