from django.urls import path

from .views import *

app_name = 'user'

urlpatterns = [
    path('register', CreateUser.as_view(), name='User Create'),
    path('sign-in', LoginUser.as_view(), name='User Login'),

]

