import django
from .models import Category#, ProfilePicture
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404


def top_categories(request):
    top_categories = Category.objects.all().annotate(post_count=Count('category_posts')).order_by('post_count').reverse().values('id', 'name', 'post_count')

    ctx = {
    "top_categories": top_categories
    }
    return ctx

# def profile_picture_url(request):
#     print(request.user.username)
#     profile_picture_url = ProfilePicture.objects.get(user__username=request.user.username)
#     ctx = {'profile_picture_url': profile_picture_url}
#     return ctx