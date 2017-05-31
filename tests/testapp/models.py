from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    username = models.CharField(max_length=128)
