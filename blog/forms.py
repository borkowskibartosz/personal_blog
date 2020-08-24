from django import forms
from .models import Comment, Photo, Post
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, UserChangeForm
from django.core.exceptions import ValidationError

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        widgets = {
          'content': forms.Textarea(attrs={'rows':2, 'cols':60}),
        }
        exclude = ['created_on', 'rating', 'source_post', 'author']

User = get_user_model()

class UserPasswordResetForm(SetPasswordForm):
    """Change password form."""
    new_password1 = forms.CharField(label='Password',
        help_text="<ul class='errorlist text-muted'><li>Your password can 't be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can 't be a commonly used password.</li> <li>Your password can 't be entirely numeric.<li></ul>",
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'password',
            'type': 'password',
            'id': 'user_password',
        }))

    new_password2 = forms.CharField(label='Confirm password',
        help_text=False,
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'confirm password',
            'type': 'password',
            'id': 'user_password',
        }))


class UserForgotPasswordForm(PasswordResetForm):
    """User forgot password, check via email form."""
    email = forms.EmailField(label='Email address',
        max_length=254,
        required=True,
        widget=forms.TextInput(
         attrs={'class': 'form-control',
                'placeholder': 'email address',
                'type': 'text',
                'id': 'email_address'
                }
        ))


class UserSignUpForm(UserCreationForm):
    """User registration form."""
    username = forms.CharField(label='Username',
        max_length=100,
        required=True,
        widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'username',
               'type': 'text',
               'id': 'user_name'
               }
        ))

    first_name = forms.CharField(label='First name',
        max_length=100,
        required=True,
        widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'first name',
               'type': 'text',
               'id': 'first_name'
               }
        ))

    last_name = forms.CharField(label='Last name',
        max_length=100,
        required=True,
        widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'last name',
               'type': 'text',
               'id': 'last_name'
               }
        ))

    email = forms.EmailField(label='Email address',
        max_length=254,
        required=True,
        widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'email address',
               'type': 'text',
               'id': 'email_address'
               }
        ))

    password1 = forms.CharField(label='Password',
        help_text="<ul class='errorlist text-muted'><li>Your password can 't be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can 't be a commonly used password.</li> <li>Your password can 't be entirely numeric.</ul>",
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'password',
            'type': 'password',
            'id': 'user_password',
        }))

    password2 = forms.CharField(label='Confirm password',
        help_text=False,
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'confirm password',
            'type': 'password',
            'id': 'user_password',
        }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class AddPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        widgets = {
          'description': forms.TextInput(attrs={'input_type': 'text'}),
          'image': forms.FileInput()
        }
        exclude = ['uploaded_by']

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ['title', 'content', 'status', 'photos', 'categories']
        
        widgets = {
          'title': forms.TextInput(attrs={'label': 'title', 'input_type': 'text', 'class': 'form-control', 'placeholder': 'Post Title','id': 'title'}),
          'content': forms.Textarea(attrs={'rows':50, 'cols':60, 'class': 'form-control'}),
          'status': forms.RadioSelect(attrs={'class': 'radio-inline'}),
          'photos': forms.CheckboxSelectMultiple(attrs={'label': 'Attached photos','class': 'checkbox'}),
          'categories': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox'}),
        }

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ['title', 'status', 'photos', 'categories', 'content']
        
        widgets = {
          'title': forms.TextInput(attrs={'label': 'title', 'input_type': 'text', 'class': 'form-control', 'placeholder': 'Post title','id': 'title'}),
          'content': forms.Textarea(attrs={'rows':50, 'cols':60, 'class': 'form-control'}),
          'status': forms.RadioSelect(attrs={'class': 'radio-inline'}),
          'photos': forms.CheckboxSelectMultiple(attrs={'label': 'Attached photos','class': 'checkbox'}),
          'categories': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox'}),

        }

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ['username','first_name', 'last_name']

        widgets = {
          'username': forms.TextInput(attrs={'input_type': 'text', 'help_text': "<ul class='errorlist text-muted'><li>150 characters or fewer.</li>Letters, digits and @/./+/-/_ only.</ul>", 'class': 'form-control','id': 'username'}),
          'first_name': forms.TextInput(attrs={'input_type': 'text', 'class': 'form-control','id': 'first_name'}),
          'last_name': forms.TextInput(attrs={'input_type': 'text', 'class': 'form-control','id': 'last_name'}),
        }

class PostSearchForm(forms.Form):
    content = forms.CharField(max_length=50)

class ContactForm(forms.Form):
    from_email = forms.EmailField(
        label='Email from:',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email address',
                'type': 'email',
                'id': 'from_email',
            }))

    subject = forms.CharField(
        required=True,
        widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email subject',
            'type': 'text',
            'id': 'subject',            
        }))       

    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
            'class': 'form-control',
            'placeholder': 'Message',
            'type': 'text',
            'id': 'message',                   
        }))