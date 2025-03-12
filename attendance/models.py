from django.contrib.auth.models import AbstractUser
from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=50, unique=True)
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='students_photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    USER_TYPE = (
        ('staff', 'Staff'),
        ('student', 'Student'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE, default='student')

    def __str__(self):
        return self.username
