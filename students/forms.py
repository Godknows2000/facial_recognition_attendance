from django import forms
from base.models import Student
from base.models import Department

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'reg_number', 'department']  # Exclude face_encoding
