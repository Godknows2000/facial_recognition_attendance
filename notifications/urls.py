from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='notifications_index'),
    path('details/<uuid:pk>/', views.detail_view, name='notifications_detail'),
]
