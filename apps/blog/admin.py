from django.contrib import admin
from .models import BlogPost, Category, Tag, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "created_at", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "email", "content")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(is_active=True)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "created_at")
    list_filter = ("is_published", "created_at", "category")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
