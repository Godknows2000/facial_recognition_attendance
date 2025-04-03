from django.urls import path
from .views import staff_index, add_staff, staff_details

urlpatterns = [
    path('staff/', staff_index, name='staff_index'),
    path('staff/add/', add_staff, name='add_staff'),
    path('staff/details/<str:staff_id>/', staff_details, name='staff_details'),
]
