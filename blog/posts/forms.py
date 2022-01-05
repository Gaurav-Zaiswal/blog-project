from django import forms
from django.contrib import admin

from .models import Post

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget  # CKEditorWidget


class PostForm(forms.ModelForm):
    """ form class for news post """
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ['category', 'title', 'thumbnail_img', 'status', 'content']
