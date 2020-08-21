from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150, blank=True)
    def __str__(self):
        return self.name

class Photo(models.Model):
    description = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(User, verbose_name=('Photo Uploader'), on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, verbose_name="Photo to upload")
    def __str__(self):
        return f'Photo: {str(self.id)} Title: {self.description}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile/', blank=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    post_save.connect(create_user_profile, sender=User)


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
    photos = models.ManyToManyField(Photo, related_name='posts', blank=True)
    categories = models.ManyToManyField(Category, related_name='category_posts')

    class Meta:
        ordering = ['-created_on']

    def pub_date(self):
        return self.created_on.strftime('%b %e, %Y')

    def summary(self):
        return self.content[:100]

    def __str__(self):
        return self.title

def get_deleted_user_instance():
    return User.objects.get(username='deleted')

class Comment(models.Model):
    rating = models.IntegerField(default=0, null=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET(get_deleted_user_instance), related_name='author_comments')
    source_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def summary(self):
        return self.content[:30]

    def __str__(self):
        return f'{self.content[:10]} by {self.author.username}'

