from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from friends.models import Friends
from main.serializers import PaginationSerializer
from user.auth import TokenAuth
from user.models import UserModel
from .models import Post, Reactions
from .serializers import NewPostSerializer, ViewPostSerializer


class NewPost(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        res = TokenAuth.check(request)
        if res:
            return res

        data = request.data
        data['author'] = request.user.id
        serializer = NewPostSerializer(data=data)
        if serializer.is_valid():
            post: Post = serializer.save()
            return JsonResponse(ViewPostSerializer(post).data,
                                status=status.HTTP_200_OK)
        else:
            return JsonResponse({"reason": "Invalid data"},
                                status=status.HTTP_400_BAD_REQUEST)


class PostView(APIView):
    @staticmethod
    def get(request, post_id, *args, **kwargs):
        res = TokenAuth.check(request)
        if res:
            return res

        post = Post.objects.filter(id=post_id).first()
        if not post:
            return JsonResponse({"reason": "Post not found"},
                                status=status.HTTP_404_NOT_FOUND)

        if not post.author.isPublic and post.author != request.user:
            if not Friends.objects.filter(from_user=post.author,
                                          to_user=request.user).first():
                return JsonResponse({"reason": "Post not found"},
                                    status=status.HTTP_404_NOT_FOUND)

        return JsonResponse(ViewPostSerializer(post).data,
                            status=status.HTTP_200_OK)


class MyFeed(APIView):
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
        posts = Post.objects.filter(
            author=request.user).order_by('-createdAt')[offset:offset+limit]
        return JsonResponse([] + ViewPostSerializer(posts, many=True).data,
                            status=status.HTTP_200_OK, safe=False)


class LoginFeed(APIView):
    @staticmethod
    def get(request, login, *args, **kwargs):
        res = TokenAuth.check(request)
        if res:
            return res

        user = UserModel.objects.filter(login=login).first()
        if not user:
            return JsonResponse({"reason": "User not found"},
                                status=status.HTTP_404_NOT_FOUND)

        if not user.isPublic and user != request.user:
            if not Friends.objects.filter(from_user=user,
                                          to_user=request.user).first():
                return JsonResponse({"reason": "User not found"},
                                    status=status.HTTP_404_NOT_FOUND)

        serializer = PaginationSerializer(data=request.GET)
        if not serializer.is_valid():
            return JsonResponse({"reason": "Invalid data"},
                                status=status.HTTP_400_BAD_REQUEST)

        offset = serializer.validated_data.get('offset', 0)
        limit = serializer.validated_data.get('limit', 5)
        posts = Post.objects.filter(
            author=user).order_by('-createdAt')[offset:offset + limit]
        return JsonResponse([] + ViewPostSerializer(posts, many=True).data,
                            status=status.HTTP_200_OK, safe=False)


class Like(APIView):
    @staticmethod
    def post(request, postId, *args, **kwargs):
        res = TokenAuth.check(request)
        if res:
            return res

        post = Post.objects.filter(id=postId).first()
        if not post:
            return JsonResponse({"reason": "Post not found"},
                                status=status.HTTP_404_NOT_FOUND)

        if not post.author.isPublic and post.author != request.user:
            if not Friends.objects.filter(from_user=post.author,
                                          to_user=request.user).first():
                return JsonResponse({"reason": "Post not found"},
                                    status=status.HTTP_404_NOT_FOUND)

        reaction = Reactions.objects.filter(post=post,
                                            from_user=request.user).first()
        if not reaction:
            reaction = Reactions(post=post, from_user=request.user,
                                 positive=True)
        reaction.positive = True
        reaction.save()

        return JsonResponse(ViewPostSerializer(post).data,
                            status=status.HTTP_200_OK)


class Dislike(APIView):
    @staticmethod
    def post(request, postId, *args, **kwargs):
        res = TokenAuth.check(request)
        if res:
            return res

        post = Post.objects.filter(id=postId).first()
        if not post:
            return JsonResponse({"reason": "Post not found"},
                                status=status.HTTP_404_NOT_FOUND)

        if not post.author.isPublic and post.author != request.user:
            if not Friends.objects.filter(from_user=post.author,
                                          to_user=request.user).first():
                return JsonResponse({"reason": "Post not found"},
                                    status=status.HTTP_404_NOT_FOUND)

        reaction = Reactions.objects.filter(post=post,
                                            from_user=request.user).first()
        if not reaction:
            reaction = Reactions(post=post, from_user=request.user,
                                 positive=False)
        reaction.positive = False
        reaction.save()

        return JsonResponse(ViewPostSerializer(post).data,
                            status=status.HTTP_200_OK)
