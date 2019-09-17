from django.db import models
from django.contrib.auth.admin import User


# Create your models here.

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(max_length=30)
    context = models.TextField()
    author = models.ForeignKey(User, on_delete=False)
    is_delete = models.BooleanField(default=True)
    blog_type = models.ForeignKey(BlogType, on_delete=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Blog: %s>' % self.title
