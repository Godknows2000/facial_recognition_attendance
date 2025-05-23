from django import forms
from base.models import *

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        exclude = ['id', 'creation_date']
        
    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['code'].widget.attrs['class'] = 'form-control'