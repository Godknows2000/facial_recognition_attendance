from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models
import uuid
import datetime
from django.contrib.postgres.fields import JSONField
from django.utils import timezone

# Create your models here.

# Departments table
class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'departments'

    def __str__(self):
        return self.name
    
# Students table (linked to User and Department)
class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    reg_number = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.reg_number}"
    
class Staff(models.Model):
    ROLE_CHOICES = [
        ('lecturer', 'Lecturer'),
        ('admin', 'Admin'),
        ('support', 'Support'),
    ]
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')
    staff_id = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'staff'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.staff_id}"
    
# Location table (for tracking attendance device locations)
class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    is_out_of_bound = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'locations'

    def __str__(self):
        return self.name
    
class Camera(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Camera'
        
# Attendance table (logs when students/staff check in/out)
class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')])
    
    # Web-based tracking fields
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # Store user's IP address
    browser_info = models.TextField(null=True, blank=True)  # Store browser details
    
    class Meta:
        db_table = 'attendance'
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.date} - {self.status}"
    
# Attendance Logs table (for raw attendance recognition logs)
class AttendanceLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    detected_at = models.DateTimeField(auto_now_add=True)
    confidence = models.FloatField()  # Face recognition confidence score
    image_path = models.TextField()  # Path to captured image
    
    # Web-based tracking fields
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    browser_info = models.TextField(null=True, blank=True)
    metadata = JSONField(null=True, blank=True)
    
    class Meta:
        db_table = 'attendance_logs'

    def __str__(self):
        return f"{self.user} - {self.detected_at} - {self.confidence}"


# Notifications table (to alert students/staff about attendance issues)
class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('sent', 'Sent'), ('read', 'Read')], default='sent')
    attachment_url = models.TextField(null=True, blank=True, default="")  # Default to empty string
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=None)
    creation_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'notifications'

    def __str__(self):
        return f"Notification to {self.user.first_name} {self.user.last_name}"

class Present(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attendance = models.ForeignKey('Attendance', on_delete=models.CASCADE, related_name='present_entries')
    date = models.DateField(default=datetime.date.today)
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {'Present' if self.present else 'Absent'}"
	
class Time(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attendance = models.ForeignKey('Attendance', on_delete=models.CASCADE, related_name='time_entries', null=True, blank=True)
    date = models.DateField(default=now)
    time = models.DateTimeField(default=now, null=True, blank=True)
    out = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {'OUT' if self.out else 'IN'} at {self.time}"

    