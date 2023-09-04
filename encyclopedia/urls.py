from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:TITLE>/",views.title,name ="title"),
    path("search",views.search,name = "search"),
    path("newpage",views.newpage ,name = "newpage"),
    path("editpage/<str:TITLE>/",views.editpage,name ="editpage"),
    path("random",views.random,name= "random")

]
