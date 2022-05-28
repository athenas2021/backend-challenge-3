from django.urls import path
from . import views

urlpatterns = [
     path('', views.users, name='users'),
     path('user/', views.user, name='user'),
     path('create_user', views.create_user, name='create_user'),
     path('edit_user', views.edit_user, name='edit_user')
]
