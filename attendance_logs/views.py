from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from base.models import AttendanceLog
from base.section import Section

section = Section()
section.actionbar = True
section.breadcrumb = True

@login_required
def logs_index(request):
    section.page_title = "Attendance Logs"
    section.sidebar=False
    logs = AttendanceLog.objects.select_related('user').order_by('-detected_at')[:100]  # limit to latest 100
    context = {
        'section': section,
        'logs': logs,
    }
    return render(request, 'attendance_logs/index.html', context)

@login_required
def log_detail(request, pk):
    section.page_title = "Attendance Log Detail"
    section.sidebar = False
    
    log = get_object_or_404(AttendanceLog, pk=pk)
    context = {
        'section': section,
        'log': log,
    }
    return render(request, 'attendance_logs/detail.html', context)
