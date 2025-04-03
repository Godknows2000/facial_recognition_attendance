from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import Staff
from staff.forms import StaffForm
from base.section import Section

section = Section()
section.actionbar = True
section.breadcrumb = True

# 🔹 List all staff members
@login_required
def index_view(request):
    section.page_title = "Staff Members"
    section.sidebar = False
    section.actionbar = True

    my_list = Staff.objects.all().order_by('created_at')

    context = {
        'section': section,
        'query_string': "",
        'my_list': my_list,
        'user': request.user,
    }
    
    return render(request, 'staff/index.html', context)

# 🔹 Add a new staff member
@login_required
def add_view(request):
    section.page_title = "Add New Staff Member"
    section.sidebar = False

    form = StaffForm()

    if request.method == 'POST':
        form = StaffForm(request.POST)

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
    
    return render(request, 'staff/add.html', context)


# 🔹 View staff details
@login_required
def details_view(request, id):
    staff = get_object_or_404(Staff, id=id)
    section.page_title = f"{staff.user.first_name} {staff.user.last_name}"
    section.sidebar = True
    section.actionbar = True

    context = {
        'section': section,
        'query_string': "",
        'staff': staff,
        'user': request.user,
    }
    
    return render(request, 'staff/details.html', context)
