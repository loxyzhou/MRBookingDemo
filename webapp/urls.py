from django.urls import path
from django.contrib import admin
from webapp import views

urlpatterns = [
    path("admin/", admin.site.urls,name="admin"),
    path("", views.login, name="login"),
    path("login/", views.login, name="login"),
    path("index/", views.index, name="index"),
    path("book/", views.book,name="book"),
    path("mybooking/", views.mybooking, name="mybooking"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout,name="logout"),
]