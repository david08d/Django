
from django.contrib import admin
from .models import BlogPost, Comment
from django.utils.text import slugify

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published_at', 'tags_display')
    list_filter = ('status', 'created_at', 'author', 'tags')
    search_fields = ('title', 'text', 'tags__name')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_at'
    ordering = ('status', 'published_at')

    def tags_display(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    tags_display.short_description = 'Tags'


    def save_model(self, request, obj, form, change):
        if not obj.slug:  # If slug is empty, generate it
            base_slug = slugify(obj.title)
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            obj.slug = slug
        obj.save()

# Comment Admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'blogpost', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments', 'block_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected comments were approved.")

    def block_comments(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected comments were blocked.")

    approve_comments.short_description = "Approve selected comments"
    block_comments.short_description = "Block selected comments"
