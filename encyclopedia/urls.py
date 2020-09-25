from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("newEntry", views.newEntry, name="newEntry"),
    path("randomEntry", views.randomEntry, name="randomEntry"),
    path("editEntry/<str:title>", views.editEntry, name="editEntry"),
    path("saveEntry", views.saveEntry, name="saveEntry")
]
