from django.urls import path
from . import views
app_name = "hello_app"
urlpatterns = [
    path('hello/<name>', views.hello),
    path('<number>', views.id),
    path('og/<name>', views.req),
    path('calc/<int:a>/<int:b>',views.calc),
    path('register/', views.register, name='register'),
    path('account/edit', views.edit_account, name='edit_account'),

];