from django import forms
from base.models import Staff
from django.contrib.auth.models import User

class StaffForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = Staff
        fields = '__all__'
        exclude = ['id', 'user', 'created_at']

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        
        # Set Bootstrap form-control class for each field
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['role'].widget.attrs['class'] = 'form-select'  # Dropdown styling
