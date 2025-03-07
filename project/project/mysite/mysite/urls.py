from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path("", include("helloapp.urls")),
    path("multipage_app/", include("multipage_app.urls")),
    path("sport_club/", include("Sport_Club.urls")),
    path("", include("blog_app.urls")),
]
