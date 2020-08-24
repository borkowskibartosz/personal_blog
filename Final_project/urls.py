"""Final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.contrib import admin
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from blog.views import (
    AboutView,
    PostSearch,
    ContactView,
    ContactCompleteView,
    DeletePhoto,
    DeleteUser,
    AddPhotoView,
    CreatePost,
    UpdatePost,
    DeletePost,
    UpdateProfile,
    UpdateAvatar,
    ProfileView,
    SignupView,
    SignupViewComplete,
    PostView,
    MainView,
    AuthorView,
    CategoriesView,
    CategoryView,
    CommentUpdate,
    CommentsView,
    DeleteComment,
)
from django.views.decorators.http import require_POST

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    # path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path("", MainView.as_view(), name="main"),
    path("post/<slug:post_slug>/", PostView.as_view(), name="post_details"),
    path("create_post/", CreatePost.as_view(), name="create-post"),
    path("post/edit/<slug:slug>/", UpdatePost.as_view(), name="update-post"),
    path("post/delete/<slug:slug>/", DeletePost.as_view(), name="delete-post"),
    path("post/search", PostSearch.as_view(), name="post-search"),
    path("author/<str:post_author>/", AuthorView.as_view(), name="author_posts"),
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("category/<int:category_id>", CategoryView.as_view(), name="category_details"),
    path("comments/", CommentsView.as_view(), name="comments"),
    path("comment/edit/<int:pk>/", CommentUpdate.as_view(), name="update_comment"),
    path("comments/delete/<int:pk>/", DeleteComment.as_view(), name="delete_comment"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("signup/done/", SignupViewComplete.as_view(), 'signup-complete'),
    path("update_avatar/<int:pk>/", UpdateAvatar.as_view(), name="update-avatar"),
    path("update_profile/<int:pk>/", UpdateProfile.as_view(), name="update-profile"),
    path("add_photo/", AddPhotoView.as_view(), name="add-photo"),
    path("delete_photo/<int:pk>", DeletePhoto.as_view(), name="delete-photo"),
    path("about", AboutView.as_view(), name="about"),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/done/', ContactCompleteView.as_view(), name='contact-success'),

    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page="main"),
        name="logout",
    ),
    path("accounts/delete/<int:pk>", DeleteUser.as_view(), name='delete-user'),
    path("", include("social_django.urls", namespace="social")),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path("accounts/", include("django.contrib.auth.urls")),

    url(
        r"^password_reset/$",
        auth_views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    url(
        r"^password_reset/done/$",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    url(
        r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    url(
        r"^reset/done/$",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
