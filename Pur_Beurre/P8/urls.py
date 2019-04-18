from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.urls import include

from . import views

urlpatterns = [
    path('Legal_notice',views.Legal_notice),
    path('results', views.results),
]