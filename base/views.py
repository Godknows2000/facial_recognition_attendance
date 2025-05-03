from django.shortcuts import render
from base.models import AttendanceLog, User
from django.utils import timezone
 
def index_view(request):
    total_faces = AttendanceLog.objects.count()
    total_students = User.objects.filter(groups__name='Students').count()
    total_staff = User.objects.filter(groups__name='Staff').count()
    total_attendance_today = AttendanceLog.objects.filter(detected_at__date=timezone.now().date()).count()

    # Dummy weekly attendance
    days = {
        'mon': 35,
        'tue': 45,
        'wed': 25,
        'thu': 50,
        'fri': 40,
    }

    # Dummy department distribution
    department_data = {
        "Computer Science": 50,
        "Business": 30,
        "Engineering": 20
    }

    context = {
        'total_faces': total_faces,
        'total_students': total_students,
        'total_staff': total_staff,
        'total_attendance_today': total_attendance_today,
        'days': days,
        'department_data': {
            "keys": list(department_data.keys()),
            "values": list(department_data.values()),
        }
    }
    return render(request, 'index.html', context)