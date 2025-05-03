from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='attendance_index'),
    path('', views.daily_attendance, name='attendance_daily'),
    path('week/', views.weekly_attendance, name='attendance_weekly'),
    path('2weeks/', views.biweekly_attendance, name='attendance_biweekly'),
    path('month/', views.monthly_attendance, name='attendance_monthly'),
]
