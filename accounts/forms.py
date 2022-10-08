from django import forms
from .models import Profile


class UserUpdateForm(forms.Form):
    name = forms.CharField(label='На что влияет?', max_length=100)
    email = forms.CharField(label='Your имейл', max_length=100)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'email']
