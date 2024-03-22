from django.core.validators import RegexValidator
from django.db import models


class Countries(models.Model):
    name = models.CharField(max_length=100)
    alpha2 = models.CharField(max_length=2, unique=True,
                              validators=[RegexValidator("^[a-zA-Z]{2}S")])
    alpha3 = models.CharField(max_length=3, unique=True,
                              validators=[RegexValidator("^[a-zA-Z]{3}S")])
    region = models.CharField(max_length=100)

    class Meta:
        db_table = "countries"
