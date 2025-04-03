from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Staff
from .forms import StaffForm

# 🔹 List all staff members
def staff_index(request):
    staff_list = Staff.objects.select_related('user', 'department').all()
    query_string = request.GET.get('query_string', '')

    if query_string:
        staff_list = staff_list.filter(
            user__first_name__icontains=query_string
        ) | staff_list.filter(
            user__last_name__icontains=query_string
        ) | staff_list.filter(
            staff_id__icontains=query_string
        )

    return render(request, 'staff/index.html', {'staff_list': staff_list, 'query_string': query_string})


# 🔹 Add a new staff member
def add_staff(request):
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff member added successfully!")
            return redirect('staff_index')  # Redirect to staff list
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StaffForm()

    return render(request, 'staff/add.html', {'form': form})


# 🔹 View staff details
def staff_details(request, staff_id):
    staff = get_object_or_404(Staff, staff_id=staff_id)
    return render(request, 'staff/details.html', {'staff': staff})
