# students/urls.py
from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.StudentListView.as_view(), name='index'),
    path('add/', views.StudentCreateView.as_view(), name='add'),
    path('<uuid:pk>/', views.StudentDetailView.as_view(), name='details'),
]
