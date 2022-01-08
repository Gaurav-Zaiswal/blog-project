from django import forms
from django.contrib import admin
from django.forms import fields

from .models import Category, Post

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget  # CKEditorWidget


class PostForm(forms.ModelForm):
    """ form class for news post """
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ['category', 'title', 'thumbnail_img', 'status', 'content']


class CategoryForm(forms.ModelForm):
    "form class to add new category"

    class Meta:
        model= Category
        fields = ['name']
