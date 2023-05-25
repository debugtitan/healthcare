
from .views import UsersList
from django.urls import path


urlpatterns = [
    path('users/',UsersList.as_view(),name='usersList'),
]
