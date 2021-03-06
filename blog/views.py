from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, CreateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, UpdateView, DeleteView
from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Count, Q
from django.utils.text import slugify
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator

from .models import Post, Comment, Category, UserProfile, Photo
from .forms import (
    PostSearchForm,
    CommentForm,
    UserSignUpForm,
    AddPhotoForm,
    UpdatePostForm,
    CreatePostForm,
    UpdateUserForm,
    ContactForm,
    CreateCategoryForm,
)
from django.views import View
from django.urls import reverse_lazy


class MainView(ListView):
    template_name = "main.html"
    paginate_by = 5
    queryset = Post.objects.filter(status=0)
    context_object_name = "posts"


class CreatePost(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("login")

    model = Post
    form_class = CreatePostForm
    success_url = reverse_lazy("main")

    def post(self, request, *args, **kwargs):
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title, allow_unicode=False)
            post.author = request.user
            post.save()
            return redirect('main')
        else:
            return render(request, 'blog/post_form.html', {'form': form})            


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy("login")

    model = Post
    form_class = UpdatePostForm
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("main")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = reverse_lazy("login")

    model = Post

    def get_success_url(self):
        return self.request.GET.get("next", reverse_lazy("main"))

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostView(FormMixin, DetailView):
    template_name = "post_details.html"
    slug_url_kwarg = "post_slug"
    slug_field = "slug"
    model = Post
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy("post_details", kwargs={"post_slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(source_post__pk=context["post"].pk)
        current_post = Post.objects.get(slug=self.object.slug)
        attached_photos = current_post.photos.all()

        context["comments"] = comments
        context["form"] = CommentForm(
            initial={"source_post": self.object, "author": self.request.user}
        )
        context["attached_photos"] = attached_photos
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
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
    template_name = "author_posts.html"

    def get_context_data(self, post_author):
        posts = Post.objects.filter(author__username=str(post_author))
        ctx = {"posts": posts, "author": post_author}
        return ctx


class CategoriesView(TemplateView):
    template_name = "categories.html"

    def get_context_data(self):
        categories_by_post_no = (
            Category.objects.all()
            .annotate(post_count=Count("category_posts"))
            .order_by("post_count")
            .reverse()
            .values("id", "name", "post_count")
        )
        ctx = {"categories_by_post_no": categories_by_post_no}
        return ctx


class CommentsView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")
    template_name = "comments.html"

    def get_context_data(self, **kwargs):
        comments_by_logged_user = Comment.objects.filter(author=self.request.user)
        ctx = {"comments_by_logged_user": comments_by_logged_user}
        return ctx


class CategoryView(TemplateView):
    template_name = "category.html"

    def get_context_data(self, category_id):
        category_id = int(str(category_id))
        cat = get_object_or_404(Category, id=category_id)
        posts = Post.objects.filter(categories__id=category_id)
        return {"cat": cat, "posts": posts}


class CommentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ["content"]
    template_name_suffix = "_update_form"
    success_url = "main"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class DeleteComment(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = reverse_lazy("login")
    model = Comment

    def get_success_url(self):
        return self.request.GET.get("next", reverse_lazy("main"))

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class SignupView(CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy("signup-complete")
    template_name = "signup.html"

class SignupViewComplete(TemplateView):
    template_name = "signup_complete.html"
    success_url = reverse_lazy("main")

class CreatePostComplete(TemplateView):
    template_name = "post_complete.html"
    success_url = reverse_lazy("main")

class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")
    template_name = "profile.html"

    def get_context_data(self):
        u = self.request.user  # .get_profile()
        users = User.objects.all()
        posts = Post.objects.filter(author__id=u.pk)
        comments = Comment.objects.filter(author__pk=u.pk)
        photos = Photo.objects.filter(uploaded_by__id=u.pk)
        return {"posts": posts, "comments": comments, "photos": photos, "users": users}


class UpdateAvatar(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy("login")
    model = UserProfile
    fields = ("avatar",)
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("main")

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class UpdateProfile(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy("login")
    form_class = UpdateUserForm
    model = User
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("main")

    def test_func(self):
        obj = self.get_object()
        return obj.pk == self.request.user.pk


class AddPhotoView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("login")

    model = Photo
    form_class = AddPhotoForm
    template_name = "add_photo.html"
    success_url = reverse_lazy("profile")

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        form = AddPhotoForm(request.POST, request.FILES)
        # form = self.get_form()
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploaded_by = request.user
            photo.save()
            return redirect('main')
        else:
            return render(request, 'blog/add_photo.html', {'form': form})   


class DeletePhoto(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy("login")

    model = Photo

    def get_success_url(self):
        return self.request.GET.get("next", reverse_lazy("main"))


class PostSearch(TemplateView):
    template_name = "post_search.html"

    def get_context_data(self, **kwargs):
        if self.request.GET:
            form = PostSearchForm(self.request.GET)
            if form.is_valid():
                posts = Post.objects.filter(
                    Q(title__icontains=form.cleaned_data["content"])
                    | Q(content__icontains=form.cleaned_data["content"])
                )

            else:
                posts = []
        else:
            form = PostSearchForm()
            posts = None
        ctx = {"form": form, "posts": posts}
        return ctx


class AboutView(TemplateView):
    template_name = "about.html"


class DeleteUser(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Delete user if owner or staff member logged in"""

    login_url = reverse_lazy("main")
    model = User

    def get_success_url(self):
        return self.request.GET.get("next", reverse_lazy("main"))

    def test_func(self):
        obj = self.get_object()
        if obj == self.request.user or self.request.user.is_staff:
            return True
        else:
            return False


class ContactView(FormView):
    form_class = ContactForm 
    template_name = "contact.html"
    success_url = reverse_lazy("contact-success")

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['borkowski.bartosz@gmail.com'])
            except BadHeaderError:
                return 'Invalid header found.'
            return redirect('contact-success')
        return render(request, "contact.html", {'form': form})            

class ContactCompleteView(TemplateView):
    template_name = 'contact_success.html'

class DeleteCategoryView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = reverse_lazy("login")

    model = Category

    def get_success_url(self):
        return self.request.GET.get("next", reverse_lazy("main"))

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False

class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ["name"]
    template_name_suffix = "_update_form"
    success_url = "main"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False

class CreateCategoryView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy("login")
    form_class = CreateCategoryForm

    model = Category
    success_url = reverse_lazy("main")

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False