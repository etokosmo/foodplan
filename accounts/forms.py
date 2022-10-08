import email
from django import forms

class UserUpdateForm(forms.Form):
    name = forms.CharField(label='На что влияет?', max_length=100)
    email = forms.CharField(label='Your имейл', max_length=100)
