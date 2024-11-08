from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from .models import BlogPost
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView


class BlogListView(ListView):
    paginate_by = 2
    model = BlogPost



class BlogDetailView(DetailView):
    model = BlogPost


class BlogUpdateView(UpdateView):
    model = BlogPost
    fields = ["title", "text"]

    def get_queryset(self, **kwargs):
        qset = super().get_queryset(**kwargs)
        qset = qset.filter(owner=self.request.user)
        return qset


class BlogDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy("blog_app:posts")

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ["title", "text",]
    template_name = 'blog_app/blogpost_create_post.html'

    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(BlogPostCreateView, self).form_valid(form)

    def get_queryset(self, **kwargs):
        qset = super().get_queryset(**kwargs)
        qset = qset.filter(owner=self.request.user)
        return qset

    def get_success_url(self):
        return reverse_lazy('blog_app:posts')
