from django import forms
from django.contrib.auth.models import User
from .models import Member, Book

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")



class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'phone', 'address']  # Exclude 'membership_date'

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["isbn", "title", "author", "genre", "published_year", "total_copies"]


class BookSearchForm(forms.Form):
    search_query = forms.CharField(max_length=255, required=False, label="Search by Title or ISBN")

