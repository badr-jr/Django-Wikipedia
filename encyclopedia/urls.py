from django.urls import path

from . import views
app_name="wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>",views.topic,name="topic"),
    path("search/",views.search_topic,name="search_topic"),
    path("create/",views.create_page,name="create_page"),
    path("random/",views.random_page,name="random_page"),
    path("edit/<str:word>",views.edit_page,name="edit_page")
]
