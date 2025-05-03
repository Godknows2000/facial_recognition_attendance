from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from base.models import Notification
from base.section import Section

section = Section()
section.actionbar = True
section.breadcrumb = True

@login_required(login_url='/identity/login')
def index_view(request):
    section.page_title = "Notifications"
    section.sidebar = False

    query_string = request.GET.get('query_string', '').strip()
    notifications = Notification.objects.all().order_by('-creation_date')

    if query_string:
        notifications = notifications.filter(message__icontains=query_string)

    context = {
        'section': section,
        'query_string': query_string,
        'mylist': notifications,
    }
    return render(request, 'notifications/index.html', context)


@login_required(login_url='/identity/login')
def detail_view(request, pk):
    section.page_title = "Notification Details"
    section.title = "Notification Details"
    section.sidebar = False

    item = get_object_or_404(Notification, pk=pk)

    context = {
        'section': section,
        'item': item,
    }
    return render(request, 'notifications/detail.html', context)
