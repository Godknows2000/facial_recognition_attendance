from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from base.models import Department

from departments.forms import DepartmentForm
from base.section import Section
section = Section()
section.actionbar = True
section.breadcrumb = True

def index_view(request):
    
    section.page_title = "Departments"
    section.sidebar=False
    section.actionbar = True

    my_list = Department.objects.all().order_by('created_at')
    
    context = {
        'section': section,
        'query_string': "",
        'my_list': my_list,
        'user': request.user,
        
    }
    
    return render(request, 'departments/index.html', context)

def add_view(request):
    section.page_title = "Add new department"
    section.sidebar = False
    
    form = DepartmentForm
    
    if request.method == 'POST':
        
        form = DepartmentForm(request.POST)

        print("test")
        if form.is_valid():
            print('test')
            
            department = form.save(commit=False)
            department.save()
            
            return redirect(details_view, id=department.id)
        else:
            form = DepartmentForm()  # Instantiate the form here
    context = {
        'section': section,
        'query_string': "",
        'form': form,
        'user': request.user,
    }
    
    return render(request, 'departments/add.html', context)

def details_view(request, id):
    department = Department.objects.get(id = id)
    section.page_title = department.name
    section.sidebar = True
    section.actionbar = True
    
    # Count the total number of vehicles associated with the ministry
    # total_students = Vehicle.objects.filter(ministry_name=id).count()
    
    # # Retrieve the list of vehicles associated with the ministry
    # student_list = Vehicle.objects.filter(ministry_name=id)

    context = {
        'section': section,
        'query_string': "",
        'department': department,
        # 'total_vehicles': total_vehicles, 
        # 'vehicle_list': vehicle_list,    
        'user': request.user,
        
    }
    return render(request, 'departments/details.html', context)