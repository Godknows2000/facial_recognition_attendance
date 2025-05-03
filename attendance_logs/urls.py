from django.urls import path
from . import views

urlpatterns = [
    path('', views.logs_index, name='attendance_logs'),
    path('details/<id>', views.log_detail, name='attendance_log_detail')
]