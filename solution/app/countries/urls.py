from django.urls import path, re_path

from .views import *

app_name = 'countries'

urlpatterns = [
    path('', CountriesView.as_view(), name='countries view'),
    re_path(r"^(?P<alpha2>[A-Za-z]{2})$", GetCountryView.as_view(),
            name='get country by alpha2'),
]

