from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .forms import UserUpdateForm

# Create your views here.
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'index.html'

class LkPageView(FormView):
    template_name = 'lk.html'
    form_class = UserUpdateForm

def profile(request):
    print(request.POST)
    print(request.FILES)
    return HttpResponse("Hello")
