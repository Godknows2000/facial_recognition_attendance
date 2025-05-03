from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='locations_index'),
    path('details/<uuid:id>/', views.detail_view, name='location_detail'),
]
