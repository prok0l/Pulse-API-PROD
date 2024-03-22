from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import APIView

from countries.models import Countries
from friends.models import Friends
from .auth import TokenAuth, delete_token
from .serializers import *


class CreateUser(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        serializer = RegisterSerializers(data=request.data)
        cc = Countries.objects.filter(
            alpha2=request.data.get('countryCode')).first()
        if serializer.is_valid() and cc:
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            response = {k: v for k, v in
                        ProfileSerializer(user).data.items() if v is not None}

            return JsonResponse(data={'profile': response},
                                status=status.HTTP_201_CREATED)
        unique = False
        for error_lst in serializer.errors.values():
            for error in error_lst:
                if error.code == 'unique':
                    unique = True
        if unique:
            return JsonResponse(data={'reason': 'Not unique data'},
                                status=status.HTTP_409_CONFLICT)

        else:
            return JsonResponse(data={'reason': 'Not valid data'},
                                status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(login=serializer.validated_data['login'],
                                password=serializer.validated_data['password'])
            if user is not None:
                token = Token.objects.filter(user=user).first()
                if token:
                    token.delete()
                token = Token.objects.create(user=user)
                return JsonResponse(data={'token': token.key},
                                    status=status.HTTP_200_OK)
            return JsonResponse(data={'reason': (
                'Пользователь с указанным логином и паролем не найден')},
                                status=status.HTTP_401_UNAUTHORIZED)
        return JsonResponse(data={'reason': (
            'Пользователь с указанным логином и паролем не найден')},
                            status=status.HTTP_401_UNAUTHORIZED)


class Profile(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        res = TokenAuth.check(request)
        if res:
            return res
        response = {k: v for k, v in
                    ProfileSerializer(request.user).data.items()
                    if v is not None}
        return JsonResponse(response,
                            status=status.HTTP_200_OK)

    @staticmethod
    def patch(request, *args, **kwargs):
        res = TokenAuth.check(request)
        if res:
            return res

        instance = request.user
        serializer = ProfileUpdateSerializer(data=request.data,
                                             instance=instance)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(ProfileSerializer(request.user).data,
                                status=status.HTTP_200_OK)
        else:
            unique = False
            for error_lst in serializer.errors.values():
                for error in error_lst:
                    if error.code == 'unique':
                        unique = True
            if unique:
                return JsonResponse({"reason": "Not unique data"},
                                    status=status.HTTP_409_CONFLICT)
            else:
                return JsonResponse({"reason": "Not valid data"},
                                    status=status.HTTP_400_BAD_REQUEST)


class Profiles(APIView):
    @staticmethod
    def get(request, login, *args, **kwargs):
        res = TokenAuth.check(request)
        if res:
            return res

        user = UserModel.objects.filter(login=login).first()
        if not user:
            return JsonResponse({"reason": "No profile"},
                                status=status.HTTP_403_FORBIDDEN)

        if not user.isPublic and user != request.user:
            if not Friends.objects.filter(from_user=user,
                                          to_user=request.user).first():
                return JsonResponse({"reason": "No friend link"},
                                    status=status.HTTP_403_FORBIDDEN)
        return JsonResponse(ProfileSerializer(user).data,
                            status=status.HTTP_200_OK)


class UpdatePassword(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        res = TokenAuth.check(request)
        if res:
            return res

        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                login=request.user.login,
                password=serializer.validated_data["oldPassword"])
            if user:
                user.set_password(serializer.validated_data["newPassword"])
                user.save()
                delete_token(request)
                return JsonResponse({"status": "ok"},
                                    status=status.HTTP_200_OK)

            return JsonResponse({"reason": "Password incorrect"},
                                status=status.HTTP_403_FORBIDDEN)
        return JsonResponse({"reason": "Password is not valid"},
                            status=status.HTTP_400_BAD_REQUEST)
