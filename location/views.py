from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from base.models import Location
from base.section import Section

section = Section()
section.breadcrumb = True
section.actionbar = True

@login_required
def index_view(request):
    section.title = "Locations"
    section.page_title = "Location List"
    section.sidebar = False

    locations = Location.objects.all().order_by('-created_at')

    context = {
        'section': section,
        'mylist': locations,
    }
    return render(request, 'locations/index.html', context)

@login_required
def detail_view(request, id):
    section.title = "Location Details"
    section.page_title = "Location Info"
    section.sidebar = False

    location = get_object_or_404(Location, pk=id)

    context = {
        'section': section,
        'item': location,
    }
    return render(request, 'locations/detail.html', context)
