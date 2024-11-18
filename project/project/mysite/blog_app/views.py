from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from .models import BlogPost
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.utils.text import slugify


class BlogListView(ListView):
    paginate_by = 2
    model = BlogPost

    def get_queryset(self):
        return BlogPost.published_objects.all()



class BlogDetailView(DetailView):
    model = BlogPost
    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")

        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        slug_id = self.kwargs.get("slug_id")

        if pk:
            return get_object_or_404(self.model, pk=pk)
        elif slug_id:
            return get_object_or_404(self.model, created_at__year=year, created_at__month=month, created_at__day=day, slug=slug_id)
        else:
            raise Http404("No object found matching the provided criteria.")
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

