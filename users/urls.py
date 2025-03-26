from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_view),
    path('add', views.add_view),
    path('details/<id>', views.details_view),
]