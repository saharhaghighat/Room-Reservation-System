from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from account.models import UserProfile, Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            "name",
            "manager",
            "members",
        ]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "team",
            "is_team_manager",
            "is_admin",
            "profile_image",
        ]


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone_number', 'team', 'email', 'profile_image']


class SignUpForm(forms.Form):
    email = forms.EmailField(label='Email')
    username = forms.CharField(max_length=30, label='Username')
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = UserProfile.objects.filter(email=email).exists()
        if user:
            raise ValidationError("This email is already used")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        if UserProfile.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("This phone number is already in use")
        if not phone_number.isdigit() or len(phone_number) != 11:
            raise ValidationError("Please enter a valid phone number with 11 digits")
        return phone_number


class CustomLoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Enter password'}))


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(label="Verification Code", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter verification code'}))

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code is None or code <= 0:
            raise forms.ValidationError("Invalid verification code.")
        return code
