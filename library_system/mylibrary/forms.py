from django import forms
from .models import Member

class MemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'phone', 'address', 'membership_date']
        widgets = {
            'membership_date': forms.DateInput(attrs={'type': 'date'}),  # Date picker for date input
        }
