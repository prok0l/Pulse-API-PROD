from django.urls import path

from .views import *

app_name = 'friends'

urlpatterns = [
    path('add', AddFriend.as_view(), name='add friend'),
    path('remove', RemoveFriend.as_view(), name='remove friend'),
    path('', FriendsList.as_view(), name='friends list'),
]

