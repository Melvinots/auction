from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listings/<int:listing_id>", views.listings, name="listings"),
    path("watchlists/<int:listing_id>", views.watchlists, name="watchlist_item"),
    path("watchlists", views.watchlists, name="watchlists"),
    path("categories/<str:category>", views.index, name="active_listing"),
    path("categories", views.category_view, name="category_list"),
    path("comments/<int:listing_id>", views.comment_view, name="comment"),
    path("bid/<int:listing_id>", views.bid_view, name="bid")
]
