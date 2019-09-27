from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    nickname = models.CharField(max_length=20)

    def __str__(self):
        return "<Profile:%s %s>" %(self.user.username, self.nickname)

