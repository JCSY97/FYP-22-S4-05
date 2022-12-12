from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="Employee ID", max_length=128)
    password = forms.CharField(label="Password", max_length=256, widget=forms.PasswordInput)