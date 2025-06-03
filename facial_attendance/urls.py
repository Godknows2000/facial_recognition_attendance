from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from recognition import views as recog_views
from users import views as users_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    # Core app modules
    path('departments/', include('departments.urls')),
    path('students/', include('students.urls')),
    path('staff/', include('staff.urls')),
    path('locations/', include('location.urls')),
    path('attendance/', include('attendance.urls')),
    path('attendance_logs/', include('attendance_logs.urls')),
    path('notifications/', include('notifications.urls')),
    path('users/', include('users.urls')),
    path('identity/', include('identity.urls')),

    # Recognition features
    path('add_photos/', recog_views.add_photos, name='add-photos'),
    path('train/', recog_views.train, name='train'),
    path('mark_your_attendance', recog_views.mark_your_attendance, name='mark-your-attendance'),
    path('mark_your_attendance_out', recog_views.mark_your_attendance_out, name='mark-your-attendance-out'),

    # Attendance reports
    path('view_attendance_home', recog_views.view_attendance_home, name='view-attendance-home'),
    path('view_attendance_date', recog_views.view_attendance_date, name='view-attendance-date'),
    path('view_attendance_employee', recog_views.view_attendance_employee, name='view-attendance-employee'),
    path('view_my_attendance', recog_views.view_my_attendance_employee_login, name='view-my-attendance-employee-login'),

    # Auth and access
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='recognition/home.html'), name='logout'),
    path('register/', users_views.add_view, name='register'),
    path('not_authorised/', recog_views.not_authorised, name='not-authorised'),
]
