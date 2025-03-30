from django.contrib import admin
from django.urls import path
from mylibrary import views

urlpatterns = [
    path("", views.entry, name="entry"),
    path("register_member", views.register_member, name="register_member"),
    path("search", views.search_member, name='search_member'),
    

]
