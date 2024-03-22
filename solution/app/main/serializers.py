from django.core.validators import MinValueValidator
from rest_framework import serializers


class PaginationSerializer(serializers.Serializer):
    offset = serializers.IntegerField(default=0,
                                      validators=[
                                          MinValueValidator(limit_value=0)])
    limit = serializers.IntegerField(default=5,
                                     validators=[
                                         MinValueValidator(limit_value=0)]
                                     )
