from django.core.exceptions import ValidationError
from django import forms

from User.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Enter Username"
        }),
        required=True,
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Enter Email"
        }),
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter Password"
        }),
        required=True,
        label="Password"
    )
    re_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter Password Again"
        }),
        required=True,
        label="Repeat Password"
    )

    def clean_re_password(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")

        if len(password) < 8:
            raise ValidationError("Password Must be 8 Characters or More !")
        if password != re_password:
            raise ValidationError(
                "Password and Repeat Password must be the Same !")
        return password, re_password

    def clean_username(self):
        username = self.cleaned_data.get("username")
        filtered_user = User.objects.filter(username__iexact=username).exists()
        if filtered_user:
            raise ValidationError("this Username has been Taken !")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        filtered_user = User.objects.filter(email__iexact=email).exists()
        if filtered_user:
            raise ValidationError("this email has been Taken !")
        return email
