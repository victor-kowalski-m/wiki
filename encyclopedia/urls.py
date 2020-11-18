from django.urls import path

from . import views

#app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:TITLE>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random/", views.random_page, name="random")
]
