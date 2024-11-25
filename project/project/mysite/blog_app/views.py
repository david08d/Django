from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from taggit.models import Tag
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import BlogPost
from .forms import CommentForm
from .forms import CommentForm
from .models import BlogPost
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.utils.text import slugify


class BlogListView(ListView):
    paginate_by = 2
    model = BlogPost

    def get_queryset(self):
        return BlogPost.published_objects.all()
#
#
# class BlogDetailView(DetailView):
#     model = BlogPost
#     template_name = 'blog_app/blogpost_detail.html'
#
#     def get_object(self, queryset=None):
#         # Retrieve the blog post based on year, month, day, and slug
#         year = self.kwargs.get("year")
#         month = self.kwargs.get("month")
#         day = self.kwargs.get("day")
#         slug_id = self.kwargs.get("slug_id")
#         return get_object_or_404(self.model, created_at__year=year, created_at__month=month, created_at__day=day,
#                                  slug=slug_id)
#
#     def get_context_data(self, **kwargs):
#         # Fetch context data for the blog post detail page
#         context = super().get_context_data(**kwargs)
#         blogpost = self.get_object()  # Get the current BlogPost
#
#         # Add additional context variables
#         context['form'] = CommentForm()  # Comment form
#         context['comments'] = blogpost.comments.filter(is_active=True)  # Active comments
#         context['tags'] = blogpost.tags.all()  # Tags associated with the post
#
#         # Fetch similar posts based on shared tags
#         tag_ids = blogpost.tags.values_list('id', flat=True)  # Get the tag IDs of the current post
#         similar_posts = BlogPost.objects.filter(tags__in=tag_ids).exclude(id=blogpost.id).distinct()
#
#         context['similar_posts'] = similar_posts  # Pass similar posts to the template
#
#         return context
#
#     def post(self, request, *args, **kwargs):
#         blogpost = self.get_object()  # Get the current BlogPost
#         form = CommentForm(request.POST)  # Initialize the comment form with POST data
#
#         if form.is_valid():  # If the form is valid
#             comment = form.save(commit=False)  # Do not save immediately
#             comment.blogpost = blogpost  # Attach the comment to the BlogPost
#             comment.save()  # Save the comment
#
#             # Reload the page with the new comment
#             return self.get(request, *args, **kwargs)
#
#         # If the form is invalid, re-render the page with form errors
#         return self.render_to_response({'form': form, 'blogpost': blogpost, 'comments': blogpost.comments.filter(is_active=True)})


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_app/blogpost_detail.html'

    def get_object(self, queryset=None):
        # Retrieve the blog post based on year, month, day, and slug
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        slug_id = self.kwargs.get("slug_id")
        return get_object_or_404(
            self.model,
            created_at__year=year,
            created_at__month=month,
            created_at__day=day,
            slug=slug_id
        )

    def get_context_data(self, **kwargs):
        # Fetch context data for the blog post detail page
        context = super().get_context_data(**kwargs)
        blogpost = self.get_object()  # Get the current BlogPost

        # Add additional context variables
        context['form'] = CommentForm()  # Comment form
        context['comments'] = blogpost.comments.filter(is_active=True)  # Active comments
        context['tags'] = blogpost.tags.all()  # Tags associated with the post
        context['likes'] = blogpost.likes  # Current number of likes

        # Calculate total likes for all blog posts
        total_likes = BlogPost.objects.aggregate(total=Sum('likes'))['total'] or 0
        context['total_likes'] = total_likes  # Add total likes to the context

        # Fetch similar posts based on shared tags
        tag_ids = blogpost.tags.values_list('id', flat=True)  # Get the tag IDs of the current post
        similar_posts = BlogPost.objects.filter(tags__in=tag_ids).exclude(id=blogpost.id).distinct()
        context['similar_posts'] = similar_posts  # Pass similar posts to the template

        return context

    def post(self, request, *args, **kwargs):
        blogpost = self.get_object()  # Get the current BlogPost

        if 'like' in request.POST:  # Check if the "like" button was clicked
            blogpost.likes += 1  # Increment the likes count
            blogpost.save()  # Save the updated like count
            return redirect(blogpost.get_absolute_url())  # Redirect to the detail page

        form = CommentForm(request.POST)  # Initialize the comment form with POST data
        if form.is_valid():  # If the form is valid
            comment = form.save(commit=False)  # Do not save immediately
            comment.blogpost = blogpost  # Attach the comment to the BlogPost
            comment.save()  # Save the comment
            return redirect(blogpost.get_absolute_url())  # Redirect to the detail page

        # If the form is invalid, re-render the page with form errors
        context = self.get_context_data(form=form)
        context['comments'] = blogpost.comments.filter(is_active=True)  # Active comments
        return self.render_to_response(context)


class BlogUpdateView(UpdateView):
    model = BlogPost
    fields = ["title", "text", "status"]

    def get_queryset(self, **kwargs):
        qset = super().get_queryset(**kwargs)
        qset = qset.filter(owner=self.request.user)
        return qset
    def get_success_url(self):
        return reverse_lazy('blog_app:posts')


class BlogDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy("blog_app:posts")

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'text', 'status']
    template_name = 'blog_app/blogpost_create_post.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog_app:posts')




class MyPostsView(ListView):
    model = BlogPost
    template_name = 'blog_app/my_posts.html'
    context_object_name = 'blogpost_list'


    def get_queryset(self):
        return BlogPost.objects.filter(owner=self.request.user)



class DraftPostsView(ListView):
    model = BlogPost
    template_name = 'blog_app/draft_posts.html'
    context_object_name = 'draft_posts'

    def get_queryset(self):
        # Use the custom manager to get only draft posts
        return BlogPost.objects.filter(status=BlogPost.PublicationStatus.DRAFT)


def post_detail(request, year, month, day, slug):
    blogpost = get_object_or_404(BlogPost, created_at__year=year, created_at__month=month, created_at__day=day, slug=slug)
    comments = blogpost.comments.filter(is_active=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blogpost = blogpost
            comment.save()
            return redirect(blogpost.get_absolute_url())
    else:
        form = CommentForm()

    return render(request, 'blog/blogpost_detail.html', {'blogpost': blogpost, 'form': form, 'comments': comments})

class TaggedPostsView(ListView):
    model = BlogPost
    template_name = 'blog_app/tagged_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs.get('slug')
        tag = Tag.objects.get(slug=tag_slug)
        return BlogPost.objects.filter(tags=tag)