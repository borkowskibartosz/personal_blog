from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Post

# Create your views here.
class MainPage(TemplateView):
    template_name = 'main_t.html'
    def get_context_data(self):
        return {'posts': Post.objects.filter(status=0)}