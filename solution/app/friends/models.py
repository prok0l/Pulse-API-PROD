from django.db import models

from user.models import UserModel


class Friends(models.Model):
    from_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserModel, on_delete=models.CASCADE,
                                related_name="to")
    addedAt = models.DateTimeField(auto_now_add=True)
