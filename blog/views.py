from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Post

# Create your views here.
class MainPage(TemplateView):
    template_name = 'main.html'
    def get_context_data(self):
        return {'posts': Post.objects.all()}