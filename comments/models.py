from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models


class Comments(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-create_time']
