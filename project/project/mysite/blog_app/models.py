# from datetime import time
#
# from django.contrib.auth.models import User
# from django.db import models
# from django.conf import settings
# from django.core.validators import *
# from django.urls import reverse
# from django.utils import timezone
# from django.utils.text import slugify
#
#
# class BlogPost(models.Model):
#    class PublishedPostsManager(models.Manager):
#       def get_queryset(self):
#          return super().get_queryset().filter(status=BlogPost.PublicationStatus.PUBLISHED)
#    class Meta:
#       ordering = ['-published_at']
#
#    def get_default_author():
#       # Ensure that the username 'admin' exists in the database
#       user = User.objects.get(username='admin')
#       return user.id
#
#    class PublicationStatus(models.TextChoices):
#       DRAFT = "D", ("Draft")
#       PUBLISHED = "P", ("Published")
#
#    status = models.CharField(
#       max_length=1,
#       choices=PublicationStatus,
#       default=PublicationStatus.DRAFT,
#    )
#    author = models.ForeignKey(
#       User,
#       on_delete=models.CASCADE,
#       related_name='blog_posts',
#       default=get_default_author  # Use the function to get the default author
#    )
#
#
#
#    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', default=get_default_author)
#    title = models.CharField(max_length=100)
#    text = models.TextField()
#    owner = models.ForeignKey(User, on_delete=models.CASCADE)
#    slug = models.SlugField(unique_for_date='created_at', blank=False)
#    published_at = models.DateTimeField(default=timezone.now)
#    created_at = models.DateTimeField(auto_now_add=True)
#    updated_at = models.DateTimeField(auto_now=True)
#
#    objects = models.Manager()
#    published_objects = PublishedPostsManager()
#
#    def __str__(self):
#       return self.title + " | by " + self.author.username
#
#    def get_absolute_url(self):
#       # return reverse("post/<int:pk>", kwargs={"pk": self.pk})
#       return reverse(
#          'blog_app:post',
#          args=[
#             self.created_at.year,
#             self.created_at.month,
#             self.created_at.day,
#             self.slug
#          ]
#       )
#
#    def save(self, *args, **kwargs):
#       if self.pk:
#          previous = BlogPost.objects.get(pk=self.pk)
#          if previous.status == BlogPost.PublicationStatus.DRAFT and \
#                  self.status == BlogPost.PublicationStatus.PUBLISHED:
#             self.published_at = timezone.now()
#       self.slug = slugify(self.title)
#       super().save(*args, **kwargs)
#
#    def __str__(self):
#        return self.title

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse


class BlogPost(models.Model):
    class PublishedPostsManager(models.Manager):
        # Custom manager to filter only published posts
        def get_queryset(self):
            return super().get_queryset().filter(status=BlogPost.PublicationStatus.PUBLISHED)

    class Meta:
        ordering = ['-published_at']

    @staticmethod
    def get_default_author():
        # Function to get the default author (admin user)
        try:
            user = User.objects.get(username='admin')
            return user.id
        except User.DoesNotExist:
            return None  # Handle case where 'admin' user doesn't exist

    class PublicationStatus(models.TextChoices):
        DRAFT = "D", ("Draft")
        PUBLISHED = "P", ("Published")

    status = models.CharField(
        max_length=1,
        choices=PublicationStatus,
        default=PublicationStatus.DRAFT,
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        default=get_default_author  # Use the function to set default author as 'admin'
    )

    title = models.CharField(max_length=100)
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique_for_date='created_at', blank=False)
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Managers
    objects = models.Manager()  # Default manager
    published_objects = PublishedPostsManager()  # Manager for published posts

    def __str__(self):
        return self.title + " | by " + self.author.username

    def get_absolute_url(self):
        # Return the absolute URL for this post
        return reverse(
            'blog_app:post',
            args=[
                self.created_at.year,
                self.created_at.month,
                self.created_at.day,
                self.slug
            ]
        )

    def save(self, *args, **kwargs):
        # If status changes from DRAFT to PUBLISHED, set published_at date
        if self.pk:
            previous = BlogPost.objects.get(pk=self.pk)
            if previous.status == BlogPost.PublicationStatus.DRAFT and \
                    self.status == BlogPost.PublicationStatus.PUBLISHED:
                self.published_at = timezone.now()

        # Generate the slug from the title
        if not self.slug:  # Only generate a slug if it doesn't already exist
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)