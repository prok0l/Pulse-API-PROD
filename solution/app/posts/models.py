import uuid

from django.db import models

from user.models import UserModel


class Post(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=1000)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    tags = models.JSONField()


class Reactions(models.Model):
    from_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    positive = models.BooleanField()
