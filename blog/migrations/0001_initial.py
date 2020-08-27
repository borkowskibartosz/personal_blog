# Generated by Django 3.1 on 2020-08-27 11:47

import blog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d', verbose_name='Photo to upload')),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Photo Uploader')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, upload_to='profile/')),
                ('email_confirmed', models.BooleanField(default=False)),
                ('reset_password', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('edited_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField(verbose_name='Post content')),
                ('status', models.IntegerField(choices=[(0, 'Published'), (1, 'Draft')], default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_posts', to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(blank=True, related_name='category_posts', to='blog.Category')),
                ('photos', models.ManyToManyField(blank=True, related_name='posts', to='blog.Photo')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, default=0, null=True)),
                ('content', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=models.SET(blog.models.get_deleted_user_instance), related_name='author_comments', to=settings.AUTH_USER_MODEL)),
                ('source_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='blog.post')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
