from django import forms
from django.contrib.auth.models import User
from base.models import Student, Department

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'password', 'reg_number', 'department']
        exclude = ['id', 'created_at', 'face_encoding']

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
