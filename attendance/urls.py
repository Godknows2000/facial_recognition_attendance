from django.urls import path
from . import views

urlpatterns = [
    path('attendance/', views.attendance_today_view, name='attendance_today'),
    path('attendance/week/', views.attendance_week_view, name='attendance_week'),
    path('attendance/2weeks/', views.attendance_two_weeks_view, name='attendance_two_weeks'),
    path('attendance/month/', views.attendance_month_view, name='attendance_month'),
]
