# students/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from base.models import Student

from students.forms import StudentForm

from base.section import Section
section = Section()
section.actionbar = True
section.breadcrumb = True

# Index View - List all students
def index_view(request):
    section.page_title = "Students"
    section.sidebar = False
    section.actionbar = True

    # Filter based on search query if provided
    query_string = request.GET.get('query_string', '')
    if query_string:
        my_list = Student.objects.filter(user__first_name__icontains=query_string)
    else:
        my_list = Student.objects.all().order_by('created_at')

    context = {
        'section': section,
        'query_string': query_string,
        'my_list': my_list,
        'user': request.user,
    }
    
    return render(request, 'students/index.html', context)

# Add View - Add a new student
@login_required
def add_view(request):
    section.page_title = "Add New Student"
    section.sidebar = False

    form = StudentForm()

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            
            staff = form.save(commit=False)
            staff.user = user
            staff.save()

            messages.success(request, "Staff member added successfully!")
            return redirect(details_view, id=staff.id)
        else:
            messages.error(request, "Please correct the errors below.")

    context = {
        'section': section,
        'query_string': "",
        'form': form,
        'user': request.user,
    }
    
    return render(request, 'students/add.html', context)

# Details View - Show student details
def details_view(request, id):
    student = Student.objects.get(id=id)
    section.page_title = f"{student.user.first_name} {student.user.last_name}"
    section.sidebar = True
    section.actionbar = True
    
    context = {
        'section': section,
        'student': student,
        'user': request.user,
    }
    
    return render(request, 'students/details.html', context)
