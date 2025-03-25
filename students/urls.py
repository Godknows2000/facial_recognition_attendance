# students/urls.py
from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('add/', views.add_view, name='add'),
    path('details/<uuid:id>/', views.details_view, name='details'),
]
