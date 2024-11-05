from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from .models import BlogPost
from django.views.generic import DetailView,UpdateView,DeleteView
class BlogListView(ListView):
    model = BlogPost

class BlogDetailView(DetailView):
    model = BlogPost

class BlogUpdateView(UpdateView):
    model = BlogPost
    fields = ["title","text"]

    def get_queryset(self, **kwargs):
        qset = super().get_queryset(**kwargs)
        qset = qset.filter(owner = self.request.user)
        return qset

class BlogDeleteView(DeleteView,BlogUpdateView):
    model = BlogPost
    success_url = reverse_lazy("blog_app:posts")
    def get_queryset(self, **kwargs):
        qset = super().get_queryset(**kwargs)
        qset = qset.filter(owner = self.request.user)
        return qset


class BlogPostCreateView:
    pass

    def form_valid(self,form):
        print('form_valid called')
        object = form.save(commit=False)
        object.owner =  self.request.user
        object.save()
        return super(BlogPostCreateView,self).form_valid(form)





