# from django.contrib import admin
#
# # Register your models here.
# from django.contrib import admin
# from .models import *
# from django.contrib import admin
# from .models import BlogPost, Comment
# from django.contrib.auth.models import User
#
# admin.site.site_header = "📚 Blog Admin Panel"
# admin.site.site_title = "Blog Admin"
# admin.site.index_title = "Welcome to Blog Administration"
#
#
#
# class BlogPostAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'author', 'status', 'timestamp')  # 👀 दिखाने वाले fields
#     list_filter = ('status', 'timestamp')  # ⏳ Filter by
#     search_fields = ('title', 'content', 'author__username')  # 🔍 Search
#     ordering = ('-timestamp',)  # 🕒 Recent posts first
#
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'blog', 'user', 'content', 'created')
#     search_fields = ('content', 'user__username', 'blog__title')
#     list_filter = ('created',)
#
# admin.site.register(BlogPost, BlogPostAdmin)
# admin.site.register(Comment, CommentAdmin)
from django.contrib import admin
from .models import BlogPost, Comment
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'status', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-timestamp',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog', 'user', 'content', 'created')
    list_filter = ('created',)
    search_fields = ('content', 'user__username')

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.site_header = " Blog Admin Panel"
admin.site.site_title = "Blog Admin"
admin.site.index_title = "Welcome to Blog Management"

