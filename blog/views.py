from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views import View
from django.db.models import Count
from .models import Post, Comment, Category
from .forms import CommentForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class MainView(TemplateView):
    template_name = 'main.html'
    def get_context_data(self):
        return {'posts': Post.objects.filter(status=0)}


class PostView(FormMixin, DetailView):
    template_name = 'post_details.html'
    slug_url_kwarg = 'post_slug'
    slug_field = 'slug'
    model = Post
    form_class = CommentForm
    
    def get_success_url(self):
        return reverse_lazy('post_details', kwargs={'post_slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(source_post__pk=context['post'].pk)
        context['comments'] = comments
        context['form'] = CommentForm(initial={'source_post': self.object, 'author': self.request.user})        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        # form = self.get_form()
        print('####')
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.source_post = self.object
            comment.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(PostView, self).form_valid(form)            

class AuthorView(TemplateView):
    template_name = 'author_posts.html'
    def get_context_data(self, post_author):
        posts = Post.objects.filter(author__username=str(post_author))
        ctx = {'posts': posts,
                'author': post_author}
        return ctx

class CategoriesView(TemplateView):
    template_name = 'categories.html'
    
    def get_context_data(self):
        categories_by_post_no = Category.objects.all().annotate(post_count=Count('category_posts')).order_by('post_count').reverse().values('id', 'name', 'post_count')
        ctx = {'categories_by_post_no': categories_by_post_no}
        return ctx
     
class CategoryView(TemplateView):
    template_name = 'category.html'
    def get_context_data(self, category_id):
        category_id = int(str(category_id))
        cat = get_object_or_404(Category, id=category_id)
        posts = Post.objects.filter(categories__id=category_id)
        return {'cat': cat,
                'posts': posts}
