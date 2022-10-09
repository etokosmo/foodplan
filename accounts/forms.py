from django import forms
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    name = forms.CharField(label='На что влияет?', max_length=100)
    email = forms.CharField(label='Your имейл', max_length=100)

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'email']

def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg
