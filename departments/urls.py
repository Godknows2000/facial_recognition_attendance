from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('', views.DepartmentListView.as_view(), name='index'),
    path('add/', views.DepartmentCreateView.as_view(), name='add'),
    path('<uuid:pk>/', views.DepartmentDetailView.as_view(), name='details'),
    path('<uuid:pk>/edit/', views.DepartmentUpdateView.as_view(), name='edit')
]
