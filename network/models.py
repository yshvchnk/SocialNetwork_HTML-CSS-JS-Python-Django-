from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class NewPost(models.Model):
    content_post = models.CharField(max_length = 1000)
    user_post = models.ForeignKey(User, on_delete = models.CASCADE, related_name="user_post_post")
    date_post = models.DateTimeField(auto_now_add = True)
    likes_post = models.IntegerField(default = '0')
    def __str__ (self):
        return f"{self.user_post}: {self.content_post} posts on {self.date_post}; {self.likes_post} likes"
    
class Like(models.Model):
    post_like = models.ForeignKey(NewPost, on_delete = models.CASCADE, related_name="post_like_like")
    users_like = models.ManyToManyField(User, blank=True, related_name="users_like_like")

class Follow(models.Model):
    user_follow = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="user_who_follow")
    followed_follow = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="who_followed")

    def __str__(self):
        return f"{self.user_follow} follows {self.followed_follow}"