from audioop import add
from django.urls import path
from . import views

urlpatterns = [
    path("",views.say_hello),
    path("add", views.add),
    path("login", views.login),
    path('login_user',views.login_user),
    path('reg',views.reg),
    path('register',views.register)
]