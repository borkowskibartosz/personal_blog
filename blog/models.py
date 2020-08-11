from django.db import models
from django.contrib.auth.models import User
# Create your models here.

STATUS = ((0, 'Published'),
            (1, 'Draft'))

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True),
    slug = models.SlugField(max_length=150, unique=True),
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    edited_on = models.DateTimeField(auto_now= True)
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField(verbose_name=Post content),
    status = models.IntegerField(choices=STATUS, default=1)
    def __str__(self):
        return self.title

class Comment(models.Model):
    pass