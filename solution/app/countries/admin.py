from django.contrib import admin
from .models import Countries


@admin.register(Countries)
class CountriesView(admin.ModelAdmin):
    list_display = ("name", "alpha2", "alpha3", "region")
    list_filter = ("region",)