from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Department
from .forms import DepartmentForm

# ✅ List all departments
class DepartmentListView(ListView):
    model = Department
    template_name = 'departments/index.html'
    context_object_name = 'my_list'

    def get_queryset(self):
        query_string = self.request.GET.get('query_string', '')
        if query_string:
            return Department.objects.filter(name__icontains=query_string)
        return Department.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query_string'] = self.request.GET.get('query_string', '')
        return context


# ✅ Department details page
class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'departments/details.html'
    context_object_name = 'department'


# ✅ Create a new department
class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/add.html'
    success_url = reverse_lazy('departments:index')


# ✅ Update department details
class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/add.html'  # Reuse the add.html for editing
    success_url = reverse_lazy('departments:index')