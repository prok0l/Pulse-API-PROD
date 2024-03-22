from datetime import datetime, timezone

from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import UserModel


class TokenAuth:
    @staticmethod
    def check(request):
        token = request.META.get('HTTP_AUTHORIZATION', b'').strip().split()
        if not token:
            return JsonResponse({'reason': 'No token'},
                                status=status.HTTP_401_UNAUTHORIZED)
        token_obj = Token.objects.filter(key=token[-1]).first()
        if not token_obj or token[0] != 'Bearer':
            return JsonResponse({'reason': 'Invalid Token'},
                                status=status.HTTP_401_UNAUTHORIZED)
        if (datetime.now(timezone.utc) - (token_obj.created)).seconds > 3600:
            token_obj.delete()
            return JsonResponse({'reason': 'Old Token'},
                                status=status.HTTP_401_UNAUTHORIZED)
        request.user = UserModel.objects.get(id=token_obj.user_id)


def delete_token(request):
    token = request.META.get('HTTP_AUTHORIZATION', b'').split()
    if token:
        token_obj = Token.objects.filter(key=token[1]).first()
        if token_obj:
            token_obj.delete()