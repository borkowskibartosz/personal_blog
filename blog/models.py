from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150, blank=True)
    def __str__(self):
        return self.name

class Photo(models.Model):
    imagename = models.TextField()
    postphoto = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)

STATUS = ((0, 'Published'),
            (1, 'Draft'))

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_posts')
    edited_on = models.DateTimeField(auto_now= True)
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField(verbose_name='Post content')
    status = models.IntegerField(choices=STATUS, default=1)
    photo = models.ManyToManyField(Photo, related_name='photos', blank=True)
    categories = models.ManyToManyField(Category, related_name='category_posts')

    class Meta:
        ordering = ['-created_on']

    @staticmethod
    def pub_date(self):
        return self.pub_date.strftime('%b %e, %Y')

    def __str__(self):
        return self.title

class Comment(models.Model):
    rating = models.IntegerField(default=0)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comments')
    created_on = models.DateTimeField(auto_now_add=True)  
    def __str__(self):
        return f'{self.content[:10]} by {self.author.username}'

