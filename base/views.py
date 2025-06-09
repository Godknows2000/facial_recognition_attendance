from django.shortcuts import render
from base.models import AttendanceLog, Attendance, Student, Staff, Department
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Count

def index_view(request):
    today = timezone.now().date()

    # Summary Cards
    total_faces = AttendanceLog.objects.count()
    total_students = Student.objects.count()
    total_staff = Staff.objects.count()
    total_attendance_today = AttendanceLog.objects.filter(detected_at__date=today).count()

    # Weekly attendance counts (Mon-Fri)
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    weekly_logs = AttendanceLog.objects.filter(detected_at__date__range=(start_of_week, today))

    days = {'mon': 0, 'tue': 0, 'wed': 0, 'thu': 0, 'fri': 0}
    day_map = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    for log in weekly_logs:
        weekday = log.detected_at.weekday()
        if weekday <= 4:  # Monday to Friday
            days[day_map[weekday]] += 1

    # Department distribution
    department_data = {}
    for dept in Department.objects.all():
        student_ids = Student.objects.filter(department=dept).values_list('user_id', flat=True)
        staff_ids = Staff.objects.filter(department=dept).values_list('user_id', flat=True)
        user_ids = list(student_ids) + list(staff_ids)
        count = Attendance.objects.filter(user_id__in=user_ids).count()
        department_data[dept.name] = count

    # Recent logs
    recent_logs = AttendanceLog.objects.select_related('user').order_by('-detected_at')[:10]

    context = {
        'total_faces': total_faces,
        'total_students': total_students,
        'total_staff': total_staff,
        'total_attendance_today': total_attendance_today,
        'days': days,
        'department_data': {
            "keys": list(department_data.keys()),
            "values": list(department_data.values()),
        },
        'recent_logs': recent_logs,
    }

    return render(request, 'index.html', context)
