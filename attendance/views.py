from collections import defaultdict
from django.shortcuts import render
from datetime import timedelta, date
from django.contrib.auth.decorators import login_required
from base.models import Attendance
from base.section import Section
import random

# Section object to manage layout and navigation
section = Section()
section.actionbar = True
section.breadcrumb = True

def get_attendance(user, start_date, end_date):
    return Attendance.objects.filter(user=user, date__range=(start_date, end_date)).order_by('-date')

# Dummy departments
DEPARTMENTS = ['Computer Science', 'Mathematics', 'Biology', 'Physics']

def get_dummy_data():
    today = date.today()
    dates = [today - timedelta(days=i) for i in range(30)][::-1]  # Last 30 days

    dept_line_data = {dept: [random.randint(10, 50) for _ in dates] for dept in DEPARTMENTS}
    pie_data = {dept: random.randint(100, 300) for dept in DEPARTMENTS}
    calendar_data = {d.strftime('%Y-%m-%d'): random.randint(20, 80) for d in dates}

    return {
        'line_dates': [d.strftime('%Y-%m-%d') for d in dates],
        'dept_line_data': dept_line_data,
        'pie_data': pie_data,
        'calendar_data': calendar_data,
        'pie_labels': list(pie_data.keys()),
        'pie_values': list(pie_data.values()),
    }

@login_required
def index_view(request):
    section.page_title = "Attendance Overview"

    dummy_data = get_dummy_data()

    context = {
        'section': section,
        'user': request.user,
        **dummy_data,
    }

    return render(request, 'attendance/index.html', context)

@login_required
def daily_attendance(request):
    section.page_title = "Daily Attendance"
    section.sidebar = True

    today = date.today()
    records = get_attendance(request.user, today, today)

    context = {
        'section': section,
        'records': records,
        'period': 'Today',
        'user': request.user,
    }

    return render(request, 'attendance/daily.html', context)

@login_required
def weekly_attendance(request):
    section.page_title = "Weekly Attendance"
    section.sidebar = True

    today = date.today()
    start = today - timedelta(days=today.weekday())  # Monday
    end = start + timedelta(days=6)  # Sunday
    records = get_attendance(request.user, start, end)

    context = {
        'section': section,
        'records': records,
        'period': 'This Week',
        'user': request.user,
    }

    return render(request, 'attendance/weekly.html', context)

@login_required
def biweekly_attendance(request):
    section.page_title = "Biweekly Attendance"
    section.sidebar = True

    today = date.today()
    start = today - timedelta(days=13)  # Last 2 weeks
    records = get_attendance(request.user, start, today)

    context = {
        'section': section,
        'records': records,
        'period': 'Last 2 Weeks',
        'user': request.user,
    }

    return render(request, 'attendance/biweekly.html', context)

@login_required
def monthly_attendance(request):
    section.page_title = "Monthly Attendance"
    section.sidebar = True

    today = date.today()
    start = today.replace(day=1)
    records = get_attendance(request.user, start, today)

    context = {
        'section': section,
        'records': records,
        'period': 'This Month',
        'user': request.user,
    }

    return render(request, 'attendance/monthly.html', context)
