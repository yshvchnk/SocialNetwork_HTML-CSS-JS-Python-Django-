from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse

import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, NewPost, Like, Follow


def liked_items(posts, user):
    liked_post = []
    for post in posts:
        for pst in post.post_like_like.all():
            for usr in pst.users_like.all():
                if usr == user:
                    liked_post.append(post.id)
    return liked_post

def get_page(page_id):
    posts = NewPost.objects.all().order_by('-date_post')
    return Paginator(posts, 10).page(page_id)

def index(request):
    posts = get_page(1)
    users = liked_items(posts, request.user)
    return render(request, "network/index.html", {
        "posts": posts,
        "users": users,
        "pages": "page"
    })
    
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def new_post(request):
    if request.method == "POST":
        new_post = NewPost(user_post = request.user, content_post = request.POST["content"])
        new_post.save()
        return HttpResponseRedirect(reverse('index'))

@csrf_exempt
def post_like(request, post_id):
    if request.method == "POST":
        try:
            post = NewPost.objects.get(pk=post_id)
        except:
            return JsonResponse({"result": "error"}, status=404)
        try:
            likes = Like.objects.filter(post_like = post).first()
            likes = likes.users_like
        except:
            Like(post_like = post).save()
            likes = Like.objects.filter(post_like = post).first()
            likes = likes.users_like
        for user_in_likes in likes.all():
            if request.user == user_in_likes:
                likes.remove(request.user)
                post.likes_post = likes.count()
                post.save()
                return JsonResponse({"result": "Success", "likes": likes.count(), "action": "rem"}, status=200)
        likes.add(request.user)
        post.likes_post = likes.count()
        post.save()
        return JsonResponse({"result": "Success", "likes": likes.count(), "action": "add"}, status=200)
    return HttpResponse("Error")

# @csrf_exempt
def profile_page(request, user_id, page_no):
    user_posts = User.objects.get(pk=user_id)
    posts = NewPost.objects.filter(user_post=user_posts).order_by("-date_post")
    posts = Paginator(posts, 10).page(page_no)
    liked_users = liked_items(posts, request.user)
    followings = Follow.objects.filter(user_follow=user_posts)
    followers = Follow.objects.filter(followed_follow=user_posts)
    try:
        follow_check = followers.filter(user_follow=User.objects.get(pk=request.user.id))
        if len(follow_check) != 0:
            is_following = True
        else:
            is_following = False
    except:
        is_following = False
    return render(request, "network/profile.html", {
        "user_name": user_posts.username,
        "followers": followers.count(),
        "followings": followings.count(),
        "is_following": is_following,
        "posts": posts,
        "profile": user_posts,
        "pages": "pages",
        "page": "page",
        "users": liked_users,
    })
    
def follow(request):
    user_follows = request.POST['user_follow']
    print(user_follows)
    curr_user = User.objects.get(pk=request.user.id)
    print(curr_user)
    user_follows_info = User.objects.get(username=user_follows)
    follow = Follow(user_follow=curr_user, followed_follow=user_follows_info)
    follow.save()
    user_id = user_follows_info.id
    page_no = 1
    return HttpResponseRedirect(reverse(profile_page, kwargs={'user_id': user_id, 'page_no': page_no}))

def unfollow(request):
    user_follows = request.POST['user_follow']
    curr_user = User.objects.get(pk=request.user.id)
    user_follows_info = User.objects.get(username=user_follows)
    follow = Follow.objects.get(user_follow=curr_user, followed_follow=user_follows_info)
    follow.delete()
    user_id = user_follows_info.id
    page_no = 1
    return HttpResponseRedirect(reverse(profile_page, kwargs={"user_id": user_id, 'page_no': page_no}))

def view_following(request, page_id):
    curr_user = User.objects.get(pk=request.user.id)
    user_follows = Follow.objects.filter(user_follow = curr_user)
    posts_all = NewPost.objects.all().order_by('-date_post')
    posts_following = []
    for post in posts_all:
        for item in user_follows:
            if item.followed_follow == post.user_post:
                posts_following.append(post)
    posts_following = Paginator(posts_following, 10).page(page_id)
    liked_posts = liked_items(posts_following, request.user)
    return render(request, "network/following.html", {
        "posts": posts_following,
        "liked_items": liked_posts,
        "pages": "following"
    })

@csrf_exempt
def edit_post(request, post_id):
    if request.method == "POST":
        post = NewPost.objects.get(pk=post_id)
        if post.user_post == request.user:
            data = json.loads(request.body).get("edit")
            post.content_post = data
            post.save()
            return JsonResponse({"result": "Success", "content": data}, status=200)
        else:
            return JsonResponse({"result": "Error"}, status=404)
    else:
        return HttpResponse("Someting went wrong")

def page_next(request, page_no):
    posts = get_page(page_no)
    posts_liked = liked_items(posts, request.user)
    return render(request, "network/index.html", {
        "posts": posts,
        "liked_items": posts_liked,
        "pages": "page"
    })