# base/forms.py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'reg_number', 'department', 'face_encoding']
        exclude = ['id', 'created_at']

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['reg_number'].widget.attrs['class'] = 'form-control'
        self.fields['department'].widget.attrs['class'] = 'form-control'
