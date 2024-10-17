from django.urls import path
from . import views
urlpatterns = [
    path('about/', views.about),
    path('main/', views.main),
    path('base/', views.base),
]