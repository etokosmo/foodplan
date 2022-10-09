from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import UserUpdateForm, form_validation_error
from django.views import View
from .models import Profile
from django.contrib import messages
from datetime import date
from order.models import Order


# Create your views here.
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'index.html'

class LkPageView(FormView):
    template_name = 'lk.html'
    form_class = UserUpdateForm

class ProfileView(View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(ProfileView, self).dispatch(request, *args, **kwargs)    

    def get(self, request):
        context = {'profile': self.profile, 'segment': 'profile'}
        order = Order.objects.filter(user=request.user, is_paid=True).first()
        if order:
            context['order'] = order.get_description_with_day_menu(date.today())
        return render(request, 'lk.html', context)

    def post(self, request):
        form = UserUpdateForm(request.POST, request.FILES, instance=self.profile)

        if form.is_valid():
            profile = form.save()
            profile.user.name = form.cleaned_data.get('name')
            profile.user.email = form.cleaned_data.get('email')
            print(form.cleaned_data.get('email'))
            profile.user.save()

            messages.success(request, 'Profile saved successfully')
        else:
            messages.error(request, form_validation_error(form))
        return redirect('profile')

