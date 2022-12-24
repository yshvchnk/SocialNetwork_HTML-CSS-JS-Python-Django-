
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("follow", views.follow, name="follow"),
    path("like/<int:post_id>", views.post_like, name="post_like"), 
    path("edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("page/<int:page_no>", views.page_next, name="page"),
    path("profile/<int:user_id>/page/<int:page_no>", views.profile_page, name="profile"),   
    path("following/<int:page_id>", views.view_following, name="following"),

]
