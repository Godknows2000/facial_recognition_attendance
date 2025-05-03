from django.shortcuts import render, redirect
from datetime import timedelta, date
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import Attendance

def get_attendance(user, start_date, end_date):
    return Attendance.objects.filter(user=user, date__range=(start_date, end_date)).order_by('-date')

@login_required
def daily_attendance(request):
    today = date.today()
    records = get_attendance(request.user, today, today)
    return render(request, 'attendance/daily.html', {'records': records, 'period': 'Today'})

@login_required
def weekly_attendance(request):
    today = date.today()
    start = today - timedelta(days=today.weekday())  # Monday
    end = start + timedelta(days=6)  # Sunday
    records = get_attendance(request.user, start, end)
    return render(request, 'attendance/weekly.html', {'records': records, 'period': 'This Week'})

@login_required
def biweekly_attendance(request):
    today = date.today()
    start = today - timedelta(days=13)
    records = get_attendance(request.user, start, today)
    return render(request, 'attendance/biweekly.html', {'records': records, 'period': 'Last 2 Weeks'})

@login_required
def monthly_attendance(request):
    today = date.today()
    start = today.replace(day=1)
    records = get_attendance(request.user, start, today)
    return render(request, 'attendance/monthly.html', {'records': records, 'period': 'This Month'})
