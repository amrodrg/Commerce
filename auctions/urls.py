from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listings/<int:ID>", views.listing_page, name="listing"),
    path("bid/<int:ID>", views.bid, name = "bid"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("categories", views.categories_list, name="categories"),
    path("category/<int:ID>", views.category_view, name="category"),
    path("close/<int:ID>", views.close, name="close"),
    path("comment/<int:ID>", views.comment, name="comment"),
]
