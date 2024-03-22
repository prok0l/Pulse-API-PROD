from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from main.serializers import PaginationSerializer
from user.auth import TokenAuth
from user.models import UserModel
from .models import Friends
from .serializers import FriendsSerializer


class AddFriend(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        res = TokenAuth.check(request)
        if res:
            return res
        user = UserModel.objects.filter(
            login=request.data.get("login")).first()
        if not user:
            return JsonResponse({"reason": "no user"},
                                status=status.HTTP_404_NOT_FOUND)

        if (not Friends.objects.filter(from_user=request.user,
                                       to_user=user).first() and
                user != request.user):
            Friends(from_user=request.user, to_user=user).save()
        return JsonResponse({"status": "ok"},
                            status=status.HTTP_200_OK)


class RemoveFriend(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        res = TokenAuth.check(request)
        if res:
            return res

        user = UserModel.objects.filter(
            login=request.data.get("login")).first()
        if not user:
            return JsonResponse({"reason": "no user"},
                                status=status.HTTP_404_NOT_FOUND)

        friend = Friends.objects.filter(from_user=request.user,
                                        to_user=user).first()
        if friend:
            friend.delete()
        return JsonResponse({"status": "ok"},
                            status=status.HTTP_200_OK)


class FriendsList(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        res = TokenAuth.check(request)
        if res:
            return res

        serializer = PaginationSerializer(data=request.GET)
        if not serializer.is_valid():
            return JsonResponse({"reason": "Invalid data"},
                                status=status.HTTP_400_BAD_REQUEST)

        offset = serializer.validated_data.get('offset', 0)
        limit = serializer.validated_data.get('limit', 5)
        lst = Friends.objects.all().order_by('-addedAt')[offset:offset+limit]
        return JsonResponse([] + FriendsSerializer(lst, many=True).data,
                            status=status.HTTP_200_OK, safe=False)
