# from django.contrib import admin
# from .models import BlogPost
#
# admin.site.register(BlogPost)

from django.contrib import admin
from .models import BlogPost
from django.utils.text import slugify

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'slug', 'created_at']
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if not obj.slug:  # Якщо поле `slug` не заповнене
            base_slug = slugify(obj.title)
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            obj.slug = slug
        obj.save()

admin.site.register(BlogPost, BlogPostAdmin)

