from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views import View
from django.db.models import Count
from .models import Post, Comment, Category
from django.contrib.auth.models import User


class MainView(TemplateView):
    template_name = 'main.html'
    def get_context_data(self):
        return {'posts': Post.objects.filter(status=0)}

class PostView(DetailView):
    model = Post
    template_name = 'post_details.html'
    slug_url_kwarg = 'post_slug'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(source_post__pk=context['post'].pk)
        context['comments'] = comments
        return context

class AuthorView(TemplateView):
    template_name = 'author_posts.html'
    
    def get_context_data(self, post_author):
        posts = Post.objects.filter(author__username=str(post_author))
        ctx = {'posts': posts,
                'author': post_author}
        return ctx

class CategoriesView(TemplateView):
    model = Category
    template_name = 'categories.html'
    def get_context_data(self):
        categories_by_post_no = Category.objects.all().annotate(post_count=Count('category_posts')).values('name', 'post_count')
        print(categories_by_post_no)
        ctx = {'categories_by_post_no': categories_by_post_no}
        return ctx
     

# class StudentSearch(TemplateView):
#     template_name = 'student_search.html'
#     def get_context_data(self, **kwargs):
#         if self.request.GET:
#             form = StudentSearchForm(self.request.GET)
#             if form.is_valid():
#                 students = Student.objects.filter(last_name__icontains=form.cleaned_data['name'])
#             else:
#                 students = []
#         else:
#             form = StudentSearchForm()
#             students = None
#         ctx = {"form": form,
#                "students": students}
#         return ctx