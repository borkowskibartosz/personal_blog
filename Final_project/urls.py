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
from django.contrib import admin
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from blog.views import PostView, MainView, AuthorView, CategoriesView, CategoryView
from django.views.decorators.http import require_POST

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('post/<slug:post_slug>/', PostView.as_view(), name='post_details'),
    path('author/<str:post_author>/', AuthorView.as_view(), name = 'author_posts'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('category/<int:category_id>', CategoryView.as_view(), name='category_details'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('comment_form/', require_POST(CommentFormView.as_view()), name='comment_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
