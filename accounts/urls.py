# Created by elham at 11/28/20
from django.conf.urls import url
from django.urls import path

from . import views
from .views import login

urlpatterns = [
    url(r'^$', views.UserCreate.as_view(), name='account-create'),
    url(r'^token$', views.generate_refresh_token, name='generate-access-token'),
    path('login', login)
]
