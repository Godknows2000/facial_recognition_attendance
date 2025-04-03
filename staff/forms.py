from django import forms
from django.contrib.auth.models import User
from base.models import Staff, Department

class StaffForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    role = forms.ChoiceField(choices=Staff.ROLE_CHOICES, required=True)

    class Meta:
        model = Staff
        fields = ['staff_id', 'department', 'role']

    def save(self, commit=True):
        # Create User object
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )

        # Create Staff object linked to the User
        staff = super().save(commit=False)
        staff.user = user
        staff.department = self.cleaned_data['department']
        staff.role = self.cleaned_data['role']

        if commit:
            staff.save()
        
        return staff
