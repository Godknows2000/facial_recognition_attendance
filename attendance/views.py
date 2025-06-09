from collections import defaultdict
from django.shortcuts import render
from datetime import timedelta, date
from django.contrib.auth.decorators import login_required
from base.models import Attendance
from base.section import Section
import random
from base.models import Attendance, Student, Staff, Department
from django.db.models import Count
from datetime import timedelta, date

# Section object to manage layout and navigation
section = Section()
section.actionbar = True
section.breadcrumb = True

def get_real_attendance_data():
    today = date.today()
    start_date = today - timedelta(days=29)
    dates = [start_date + timedelta(days=i) for i in range(30)]

    # Create date string keys for charts
    line_dates = [d.strftime('%Y-%m-%d') for d in dates]

    # Line Chart: Department-wise attendance by date
    dept_line_data = {}
    departments = Department.objects.all()

    for dept in departments:
        dept_name = dept.name
        student_ids = Student.objects.filter(department=dept).values_list('user_id', flat=True)
        staff_ids = Staff.objects.filter(department=dept).values_list('user_id', flat=True)
        user_ids = list(student_ids) + list(staff_ids)

        counts_per_day = []
        for d in dates:
            count = Attendance.objects.filter(user_id__in=user_ids, date=d, status='present').count()
            counts_per_day.append(count)
        dept_line_data[dept_name] = counts_per_day

    # Pie Chart: Total attendance per department
    pie_data = {}
    for dept in departments:
        student_ids = Student.objects.filter(department=dept).values_list('user_id', flat=True)
        staff_ids = Staff.objects.filter(department=dept).values_list('user_id', flat=True)
        user_ids = list(student_ids) + list(staff_ids)

        count = Attendance.objects.filter(user_id__in=user_ids, status='present').count()
        pie_data[dept.name] = count

    # Calendar Heatmap: Daily total attendance
    calendar_data = {}
    for d in dates:
        count = Attendance.objects.filter(date=d, status='present').count()
        calendar_data[d.strftime('%Y-%m-%d')] = count

    return {
        'line_dates': line_dates,
        'dept_line_data': dept_line_data,
        'pie_data': pie_data,
        'calendar_data': calendar_data,
        'pie_labels': list(pie_data.keys()),
        'pie_values': list(pie_data.values()),
    }


def get_attendance(user, start_date, end_date):
    return Attendance.objects.filter(user=user, date__range=(start_date, end_date)).order_by('-date')

# Dummy departments
# DEPARTMENTS = ['Computer Science', 'Mathematics', 'Biology', 'Physics']

# def get_dummy_data():
#     today = date.today()
#     dates = [today - timedelta(days=i) for i in range(30)][::-1]  # Last 30 days

#     dept_line_data = {dept: [random.randint(10, 50) for _ in dates] for dept in DEPARTMENTS}
#     pie_data = {dept: random.randint(100, 300) for dept in DEPARTMENTS}
#     calendar_data = {d.strftime('%Y-%m-%d'): random.randint(20, 80) for d in dates}

#     return {
#         'line_dates': [d.strftime('%Y-%m-%d') for d in dates],
#         'dept_line_data': dept_line_data,
#         'pie_data': pie_data,
#         'calendar_data': calendar_data,
#         'pie_labels': list(pie_data.keys()),
#         'pie_values': list(pie_data.values()),
#     }

@login_required
def index_view(request):
    section.page_title = "Attendance Overview"

    real_data = get_real_attendance_data()

    context = {
        'section': section,
        'user': request.user,
        **real_data,
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
