from django.urls import path

from . import views

app_name = "quotes"
urlpatterns = [
    path("", views.main, name="index"),
    path("page/<int:page>/", views.main, name="index_paginate"),
    path("add_author/", views.add_author, name="add_author"),
    path("add_quote/", views.add_quote, name="add_quote"),
    path("author/<str:author_fullname>", views.about_author, name="about_author"),
    path("tag/<str:tag_name>/", views.show_quotes, name="show_quotes"),
    path("tag/<str:tag_name>/page/<int:page>/", views.show_quotes, name="show_quotes_paginate"),
]