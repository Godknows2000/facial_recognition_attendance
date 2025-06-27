from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserForm 

from base.section import Section

section = Section()
section.actionbar = True
section.breadcrumb = True

@login_required(login_url='/identity/login')
def index_view(request):
    section.page_title = ""
    section.title = "Users"
    section.sidebar=False

    mylist = User.objects.all().order_by('username')

    context = {
        'section': section,
        'query_string': "",
        'mylist': mylist,
        
    }
    return render(request, 'users/index.html', context)

def add_view(request):
    section.page_title = "Add user"
    section.sidebar = False
    
    form = UserForm

    if request.method == 'POST':
        
        form = UserForm(request.POST)
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = User.objects.create_user(username=cleaned_data['username'],date_joined= cleaned_data['date_joined'],password=cleaned_data['password'], email=cleaned_data['email'])
            user.is_student = cleaned_data['is_staff']
            user.save()
            
            return redirect(details_view, id=user.id)

        else:
            print(form.errors)
    context = {
        'section': section,
        'query_string': "",
        'form': form,
        'user': request.user,
    }
    
    return render(request, 'users/add.html', context)

def details_view(request, id):
    # user = User.objects.get(id = id)
    selected_user = User.objects.get(id=id)

    section.page_title = selected_user.username
    section.sidebar = True
    section.actionbar = True

    context = {
        'section': section,
        'query_string': "",     
        'user': request.user,
        'selected_user': selected_user,
    }
    return render(request, 'users/details.html', context)