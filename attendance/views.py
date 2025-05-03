from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from base.models import Attendance
from django.db.models import Q

@login_required
def attendance_today_view(request):
    today = now().date()
    attendance = Attendance.objects.filter(user=request.user, date=today)
    return render(request, 'attendance/today.html', {'attendance_list': attendance})

@login_required
def attendance_week_view(request):
    today = now().date()
    start_date = today - timedelta(days=7)
    attendance = Attendance.objects.filter(user=request.user, date__range=(start_date, today))
    return render(request, 'attendance/week.html', {'attendance_list': attendance, 'range': '1 Week'})

@login_required
def attendance_two_weeks_view(request):
    today = now().date()
    start_date = today - timedelta(days=14)
    attendance = Attendance.objects.filter(user=request.user, date__range=(start_date, today))
    return render(request, 'attendance/week.html', {'attendance_list': attendance, 'range': '2 Weeks'})

@login_required
def attendance_month_view(request):
    today = now().date()
    start_date = today - timedelta(days=30)
    attendance = Attendance.objects.filter(user=request.user, date__range=(start_date, today))
    return render(request, 'attendance/week.html', {'attendance_list': attendance, 'range': '1 Month'})

