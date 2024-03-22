from django.urls import path

from .views import *

app_name = 'posts'

urlpatterns = [
    path('new', NewPost.as_view(), name='create post'),
    path('<str:post_id>', PostView.as_view(), name='view post by id'),
    path('feed/my', MyFeed.as_view(), name='Feed My'),
    path('feed/<str:login>', LoginFeed.as_view(), name='Feed by login'),
    path('<str:postId>/like', Like.as_view(), name='Like'),
    path('<str:postId>/dislike', Dislike.as_view(), name='Dislike'),
]

