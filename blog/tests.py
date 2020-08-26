import unittest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.test.client import Client

from blog.models import UserProfile, Category, Post

class UserCreationTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="Toady", first_name="John", last_name="Green",email='jg@thekingdom.com')

    def test_user_created(self):
        toady = User.objects.get(email='jg@thekingdom.com')
        self.assertEqual(toady.username, 'Toady')

    def test_userprofile_created(self):
        toady = User.objects.get(email='jg@thekingdom.com')
        up = UserProfile.objects.get(user=toady)
        self.assertEqual(up.email_confirmed, False)


class BasicViewsTest(TestCase):
    def test_create_post(self):
        response = self.client.get('/create_post/')
        self.assertEqual(response.status_code, 302)

    def test_categories(self):
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)

    def test_comments(self):
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, 302)

    def test_signup(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_done(self):
        response = self.client.get('/signup/done/')
        self.assertEqual(response.status_code, 200)

    def test_add_photo(self):
        response = self.client.get('/add_photo/')
        self.assertEqual(response.status_code, 302)

    def test_about(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_contact(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def test_contact_done(self):
        response = self.client.get('/contact/done/')
        self.assertEqual(response.status_code, 200)       

class LoggedInTest(TestCase):
    def setUp(self):
        Category.objects.create(name='test_category')
        User.objects.get_or_create(username='testuser')[0]
        self.client.force_login(User.objects.get(id=1))

    def test_profile_view(self):
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)    

    def test_comments_view(self):
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, 200)
    def test_create_category_view(self):
        response = self.client.get('/create_category/')
        self.assertEqual(response.status_code, 403)                  
    def test_add_category(self):
        response = self.client.post('/create_category/', {'name':'test_category'})
        self.assertEqual(response.status_code, 403)  
    def test_create_post(self):
        test_category = Category.objects.get(id=1)
        response = self.client.post('/create_post/', {'title':'test_title', 'status': 1, 'content': 'test content'})
        self.assertEqual(response.status_code, 200)

