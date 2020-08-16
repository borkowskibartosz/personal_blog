import django
from .models import Category
from django.db.models import Count


def top_categories(request):
    top_categories = Category.objects.all().annotate(post_count=Count('category_posts')).order_by('post_count').reverse().values('id', 'name', 'post_count')

    ctx = {
    "top_categories": top_categories
    }
    return ctx