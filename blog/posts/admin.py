from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['author','title', 'slug']}),
        ('Body',                {'fields': ['thumbnail_img', 'content',]}),
        ('Date information',    {'fields': ['created_on'], 'classes': ['collapse']}),
        (None,                  {'fields': ['status']})
    ]

    list_display = ('title', 'author', 'status', 'created_on')
    list_filter = ['status', 'created_on']
    # list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator',)


admin.site.register(Post)
admin.site.register(Category, CategoryAdmin)
