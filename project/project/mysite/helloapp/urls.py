from django.urls import path
from . import views

urlpatterns = [
    path('hello/<name>', views.hello),
    path('<number>', views.id),
    path('og/<name>', views.req),
    path('calc/<int:a>/<int:b>',views.calc),

];